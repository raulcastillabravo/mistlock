# AWS DynamoDB

Este proyecto demuestra un pipeline de procesamiento de archivos donde las subidas a S3 disparan una Lambda para registrar metadatos en una tabla de DynamoDB.

```mermaid
architecture-beta
   group localstack(cloud)[AWS LocalStack]
    service s3(disk)[S3 Bucket] in localstack
    service lambda(server)[Lambda] in localstack
    service db(database)[Dynamo DB] in localstack

    s3:R --> L:lambda
    lambda:R --> L:db
```
[![Ver Diagrama](https://img.shields.io/badge/Ver_Diagrama-Instalar-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Índice

- [Inicio Rápido (Dev Container)](#inicio-rápido-dev-container)
- [Paso a Paso (sin Dev Container)](#paso-a-paso-sin-dev-container)
    - [1. Iniciar infraestructura](#1-iniciar-infraestructura)
    - [2. Configurar AWS CLI](#2-configurar-aws-cli)
    - [3. Instalar AWS Toolkit](#3-instalar-aws-toolkit)
    - [4. Instalar Python](#4-instalar-python)
    - [5. Desplegar recursos](#5-desplegar-recursos)
    - [6. Ejecutar el ejemplo](#6-ejecutar-el-ejemplo)
    - [7. Validación](#7-validación)
    - [8. Limpieza](#8-limpieza)
- [Solución de problemas](#solución-de-problemas)
- [Licencia](#licencia)

## Inicio Rápido (Dev Container)

El Dev Container provisiona automáticamente la infraestructura de LocalStack y configura el entorno Python y AWS CLI para su uso inmediato.

1. **Prerrequisitos:**
    1. [Docker](https://www.docker.com/get-started) instalado y ejecutándose.
    2. [Extensión Dev Containers](vscode:extension/ms-vscode-remote.remote-containers) instalada.

2. **Abrir proyecto:** Abre la **Paleta de Comandos** (`F1` o `Ctrl/Cmd+Shift+P`), también accesible vía **Ver > Paleta de Comandos**, y selecciona **Dev Containers: Reopen in Container**.
3. **Ejecutar MVE:** 
   ```bash
   python main.py
   ```
4. **Listar buckets**:
    ```bash
    aws s3 ls
    ```
5. **Escanear tabla DynamoDB**:
   ```bash
   aws dynamodb scan --table-name file-logs
   ```
6. **Limpieza:**
   ```bash
   docker compose down -v
   ```

## Paso a Paso (sin Dev Container)

Esta sección detalla los pasos realizados automáticamente dentro del Dev Container, explorando variaciones adicionales y opciones de despliegue.

### 1. Iniciar infraestructura

Para iniciar solo el servicio de **LocalStack** (evitando el contenedor de desarrollo), ejecuta:

```bash
docker compose up -d localstack
```

### 2. Configurar AWS CLI

Instala el [AWS CLI](https://docs.aws.amazon.com/es_es/cli/latest/userguide/getting-started-install.html) y configura un perfil dedicado para apuntar a tu instancia de LocalStack:

```bash
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack
aws configure set endpoint_url http://localhost:4566 --profile localstack
aws configure set cli_pager "" --profile localstack
```

### 3. Instalar AWS Toolkit

Instala la extensión [AWS Toolkit](vscode:extension/amazonwebservices.aws-toolkit-vscode). Para usarla con LocalStack:

1. Abre el explorador de **AWS Toolkit** en VS Code.
2. Haz clic en la configuración de **Profiles** o **Connections**.
3. Selecciona el perfil `localstack` configurado en el paso 2.

### 4. Instalar Python

Instala [Python](https://www.python.org/downloads/) y verifica la instalación:

```bash
python --version
```

Luego, instala [uv](https://github.com/astral-sh/uv) y sincroniza las dependencias para crear el entorno virtual:

```bash
pip install uv
uv sync
```

### 5. Desplegar recursos

Antes de desplegar, debes empaquetar la función Lambda:

```bash
python deploy/utils/package_lambda.py
```

Elige tu opción de despliegue preferida:

💡 **Nota:** Si cambias entre diferentes métodos de despliegue (**Terraform**, **CloudFormation**, **Boto3** o **CLI**), asegúrate de realizar una **Limpieza** primero para evitar conflictos de nombres de recursos.

* **Opción A**: Terraform

   ```bash
   terraform -chdir=deploy init
   terraform -chdir=deploy apply -auto-approve
   ```

* **Opción B**: CloudFormation

   ```bash
   # 1. Crear un bucket temporal para el despliegue
   aws s3 mb s3://lambda-deploy-bucket --profile localstack

   # 2. Subir el paquete de la Lambda
   aws s3 cp tmp/lambda.zip s3://lambda-deploy-bucket/lambda.zip --profile localstack

   # 3. Desplegar el stack
   aws cloudformation deploy --profile localstack \
     --stack-name aws-dynamo-db-stack \
     --template-file deploy/cloud_formation_deploy.yaml \
     --capabilities CAPABILITY_NAMED_IAM
   ```

   > 🎨 **Tip:** Puedes visualizar esta plantilla usando **AWS Infrastructure Composer** desde **AWS Toolkit** abriendo `deploy/cloud_formation_deploy.yaml` y haciendo clic en el botón "Infrastructure composer" en la esquina superior derecha del editor.

* **Opción C**: Boto3 (Python)

   ```bash
   python deploy/boto3_deploy.py
   ```

* <details><summary><b>Opción D</b>: AWS CLI (Manual) - Haz clic para expandir</summary>

   ```bash
   # 1. Crear tabla DynamoDB
   aws dynamodb create-table --profile localstack \
     --table-name file-logs \
     --attribute-definitions AttributeName=file_id,AttributeType=S \
     --key-schema AttributeName=file_id,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST

   # 2. Crear Rol IAM
   aws iam create-role --profile localstack \
     --role-name lambda-s3-processor-role \
     --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

   # 3. Crear Función Lambda
   aws lambda create-function --profile localstack \
     --function-name s3-file-processor \
     --runtime python3.12 \
     --role arn:aws:iam::000000000000:role/lambda-s3-processor-role \
     --handler lambda.lambda_handler \
     --zip-file fileb://tmp/lambda.zip \
     --environment Variables={DYNAMODB_TABLE=file-logs}

   # 4. Crear Bucket S3
   aws s3 mb s3://file-uploads-bucket --profile localstack

   # 5. Añadir Permiso a Lambda y Configurar Notificación
   aws lambda add-permission --profile localstack \
     --function-name s3-file-processor \
     --statement-id s3-trigger \
     --action lambda:InvokeFunction \
     --principal s3.amazonaws.com \
     --source-arn arn:aws:s3:::file-uploads-bucket

   aws s3api put-bucket-notification-configuration --profile localstack \
     --bucket file-uploads-bucket \
     --notification-configuration '{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"arn:aws:lambda:us-east-1:000000000000:function:s3-file-processor","Events":["s3:ObjectCreated:*"]}]}'
   ```
</details>

### 6. Ejecutar el ejemplo

* **Opción A**: Script Python. Ejecuta el script de demostración para subir archivos de muestra y ver los logs:

   ```bash
   python main.py
   ```

* **Opción B**: Subida Manual (CURL). También puedes disparar la Lambda manualmente subiendo cualquier archivo vía `curl`:

   ```bash
   curl -X PUT -T src/lambda.py http://localhost:4566/file-uploads-bucket/manual-upload.py
   ```

* **Opción C**: AWS Toolkit. Puedes explorar recursos e incluso subir archivos directamente desde el IDE:
    1. Selecciona el perfil `localstack` en el AWS Toolkit.
    2. Para disparar el ejemplo, haz clic derecho en el `file-uploads-bucket` y selecciona **Upload Files...**.

### 7. Validación

Elige tu forma preferida de verificar los resultados:

* **Opción A**: AWS CLI. Verifica que los archivos se subieron y los registros se crearon:
    - **Check S3 Bucket**:
      ```bash
      aws s3 ls s3://file-uploads-bucket --profile localstack
      ```
    - **Scan DynamoDB Table**:
      ```bash
      aws dynamodb scan --table-name file-logs --profile localstack
      ```
    - **View Lambda Logs**:
      ```bash
      aws logs tail /aws/lambda/s3-file-processor --profile localstack
      ```

* **Opción B**: AWS Toolkit. Explora los recursos directamente desde la barra lateral de VS Code:
    1. **S3**: Expande la sección S3 para ver los archivos subidos.
    2. **CloudWatch**: Expande la sección de Logs para ver la salida de ejecución de la Lambda.
    3. **Visualizador**: Abre `deploy/cloud_formation_deploy.yaml` y haz clic en **Infrastructure composer** (botón superior derecho) para ver el diagrama de recursos.

* **Opción C**: NoSQL Workbench. Una aplicación de escritorio para diseñar y visualizar datos de DynamoDB.
    1. **Descarga**: [NoSQL Workbench para DynamoDB](https://docs.aws.amazon.com/es_es/amazondynamodb/latest/developerguide/workbench.settingup.html).
    2. **Configurar Conexión**: 
        - Haz clic en **Operation builder** > **Add connection**.
        - Selecciona **DynamoDB local**.
        - Introduce los siguientes valores:
            - **Connection Name**: `LocalStack`
            - **Hostname**: `localhost`
            - **Port**: `4566`
        - Haz clic en **Connect** para explorar y editar los documentos de la tabla `file-logs`.

### 8. Limpieza

Para eliminar completamente la infraestructura local:

```bash
docker compose down -v
```

## Solución de problemas

| Problema | Solución |
| :--- | :--- |
| **Conexión rechazada** | Asegúrate de que LocalStack esté ejecutándose y espera al mensaje `Ready.` en los logs. |
| **Lambda no se dispara** | Verifica los logs: `aws logs tail /aws/lambda/s3-file-processor --profile localstack` |

## Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
