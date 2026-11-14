# AWS Emulator has no prebuilt image: this follows the official Dockerfile
# (https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html)
# with a pinned version and automatic x86_64 / aarch64 selection.
FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal

ARG EMULATOR_VERSION
ARG TARGETARCH

RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo aarch64 || echo x86_64) \
    && curl -fsSLo /tmp/aws-emulator.rpm "https://downloads.aws.com/aws-emulator/packages/aws-emulator/LTS/aws-emulator-${EMULATOR_VERSION}-1-${ARCH}.rpm" \
    && rpm -i /tmp/aws-emulator.rpm && rm /tmp/aws-emulator.rpm \
    && mkdir -p /home/emulator && chown 1000 /home/emulator

USER 1000
ENV HOME=/home/emulator
EXPOSE 9297
ENTRYPOINT ["aws-emulator", "-b", "0.0.0.0"]
