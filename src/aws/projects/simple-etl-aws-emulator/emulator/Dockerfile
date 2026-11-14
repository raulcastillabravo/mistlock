# AWS Emulator has no prebuilt image: this follows the official Dockerfile
# (https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html)
# with a pinned version, automatic x86_64 / aarch64 selection and an
# entrypoint that runs the emulator as the host user (see entrypoint.sh).
FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal

ARG EMULATOR_VERSION
ARG TARGETARCH

# util-linux provides setpriv, used by the entrypoint to drop root
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo aarch64 || echo x86_64) \
    && curl -fsSLo /tmp/aws-emulator.rpm "https://downloads.aws.com/aws-emulator/packages/aws-emulator/LTS/aws-emulator-${EMULATOR_VERSION}-1-${ARCH}.rpm" \
    && rpm -i /tmp/aws-emulator.rpm && rm /tmp/aws-emulator.rpm \
    && microdnf install -y util-linux && microdnf clean all \
    && mkdir -p /home/emulator && chmod 755 /home/emulator

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

ENV HOME=/home/emulator
EXPOSE 9297
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
