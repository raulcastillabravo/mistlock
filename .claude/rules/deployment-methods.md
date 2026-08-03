# Deployment Methods (Cloud Emulator Labs)

Applies to every Lab whose infrastructure runs on a **cloud emulator** — a
container that reimplements a provider's APIs locally (LocalStack, Floci,
MiniStack, Robotocore… for AWS; the same idea applies to any provider-wide
emulator). Single-service emulators (MinIO, Azurite, Firebase Emulator Suite)
only need this when the Lab deploys real cloud resources on top of them.

Reference implementation: `src/aws/projects/storage-writer` (structure only —
the paths below supersede the ones it currently uses).

## Why

The emulator makes the same resource deployable through every tool the real
cloud supports. Each Lab must therefore expose **more than one deployment
method** so users can compare the SDK, the provider's IaC, and third-party IaC
against the exact same result.

## Structure

```
src/aws/[mves|projects]/[name]/
├── build/
│   └── package_lambda.py           # packaging code — Lab root
├── deploy/
│   ├── boto3/deploy.py             # SDK deployment (default method)
│   ├── cli/{deploy.sh,destroy.sh}  # raw AWS CLI commands
│   ├── cloudformation/template.yaml
│   └── terraform/main.tf
├── dist/                           # build artifacts (Lambda zips) — Lab root
├── scripts/
│   ├── build.sh
│   ├── deploy/
│   │   ├── boto3/{deploy.sh,destroy.sh}
│   │   ├── cli/{deploy.sh,destroy.sh}
│   │   ├── cloudformation/{deploy.sh,destroy.sh}
│   │   └── terraform/{deploy.sh,destroy.sh}
│   ├── setup.sh
│   ├── run_main.sh
│   └── run_tests.sh
├── main.py
└── mise.toml
```

Rules:

- **`build/` and `deploy/` are separate stages.** The flow is always
  **build → deploy**: `build/` produces the artifacts, `deploy/` consumes them.
  A deploy script never packages anything.
- **`build/`** lives at the **Lab root** and holds the packaging code
  (`package_lambda.py` and any other artifact builder). Its output goes to
  `dist/`. Its entry point is `scripts/build.sh`.
- **`dist/`** lives at the **Lab root**, never inside `deploy/`. It holds
  generated artifacts only and is **not** removed by `destroy.sh` — artifacts
  survive deploy/destroy cycles and are rebuilt only by the build stage.
- **`deploy/[method]/`** holds the *definition* of the infrastructure (SDK
  script, CLI commands, template, HCL). One directory per method, named exactly
  as the method: `boto3`, `cli`, `cloudformation`, `terraform`.
- **`scripts/deploy/[method]/`** holds the *execution* of that method:
  `deploy.sh` and `destroy.sh`, always both. These scripts are the single entry
  point — docs and tests never call `terraform`/`aws`/`python` directly.
- **`.gitignore`** (Lab root) must ignore `.terraform/` and `terraform.tfstate*`;
  `.terraform.lock.hcl` is committed. `dist/` is already ignored by the repo
  root `.gitignore`. Note that `build/` holds **versioned source code** — the
  repo root pattern is scoped to `/build/` on purpose, since the Python
  gitignore template ignores `build/` as a packaging output directory.
- **Resource names come from `.env`** — never hardcoded in scripts or templates.
  Pass them through: `-var` for Terraform, `--parameter-overrides` for
  CloudFormation, `os.getenv` for boto3, shell variables for the AWS CLI.

## Methods

| Method | Definition | Purpose |
|--------|------------|---------|
| `boto3` | `deploy/boto3/deploy.py` | Default method. Used by Step 1 of the docs and by the Lab's own setup. |
| `cli` | `deploy/cli/{deploy.sh,destroy.sh}` | Mirrors the AWS documentation command by command. |
| `cloudformation` | `deploy/cloudformation/template.yaml` | Provider-native IaC. |
| `terraform` | `deploy/terraform/main.tf` | Third-party IaC. |

A Lab implements the methods that make sense for its services; `boto3` is
mandatory as the default, and at least one IaC method should exist.

## Script templates

```bash
# scripts/build.sh
#!/bin/bash
set -e

.venv/bin/python build/package_lambda.py
```

```bash
# scripts/deploy/boto3/deploy.sh
#!/bin/bash
set -e

.venv/bin/python deploy/boto3/deploy.py
```

```bash
# scripts/deploy/terraform/deploy.sh
#!/bin/bash
set -e

terraform -chdir=deploy/terraform init
terraform -chdir=deploy/terraform apply -auto-approve -var "bucket_name=$BUCKET_NAME"
```

```bash
# scripts/deploy/terraform/destroy.sh
#!/bin/bash
set -e

terraform -chdir=deploy/terraform destroy -auto-approve -var "bucket_name=$BUCKET_NAME"
```

`destroy.sh` removes the deployed resources and nothing else — it never touches
`dist/`, so the next deploy reuses the artifacts already built.

Terraform references the artifacts through the Lab root, e.g.
`filename = "${path.module}/../../dist/function.zip"`.

## mise.toml

Install the tooling each implemented method needs, and expose build and deploy
as separate tasks. `setup` ends at `build`: deploying is a user choice between
methods, so the `deploy` task is the documented **exception** to the rule that
every task must be referenced from `setup`.

```toml
[tools]
python = "3.12"
uv = "latest"
awscli = "latest"
terraform = "latest"

[tasks.build]
description = "Package the Lambda artifacts into dist/"
run = "scripts/build.sh"

[tasks.deploy]
description = "Deploy resources with the default method (boto3)"
run = "scripts/deploy/boto3/deploy.sh"

[tasks.setup]
description = "Full environment setup"
run = [
  { task = "sync" },
  { task = "build" },
]
```

## Emulator readiness

Deploy scripts must never poll the emulator with a wait loop. The `dev` service
waits for it in `docker-compose.yml`, using the emulator image's own healthcheck:

```yaml
  dev:
    depends_on:
      localstack:
        condition: service_healthy
```

## Tests

The global integration test uses the `deploy` fixture in `tests/conftest.py`,
which resolves `scripts/deploy/[method]/deploy.sh` and the matching
`destroy.sh`. Parametrize it to cover every method:

```python
import pytest


@pytest.mark.parametrize(
    "deploy", ["boto3", "cli", "cloudformation", "terraform"], indirect=True
)
def test_[example_name](deploy, run_tests, run_main):
    pass
```

## Docs

Follow section 6 of `.claude/rules/docs-style-guide.md`:

- The **default method** (`boto3`) goes inside the "Manually" tab of Step 1 in
  "How to execute", as `scripts/deploy/boto3/deploy.sh`.
- The alternatives go in a "Deployment methods" H2 with
  `<Tabs syncKey="deploy-method">`, followed by the
  `:::note[Switching deployment methods]` callout.
- "Clean Up" repeats the same `<Tabs syncKey="deploy-method">` with each
  `destroy.sh`, then `docker compose down -v`.
