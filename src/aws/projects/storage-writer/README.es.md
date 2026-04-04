# AWS Lambda

Ejemplo mínimo viable de una función **AWS Lambda** que sube archivos a **S3**. Diseñado para ejecutarse 100% localmente usando **LocalStack**.

## Arquitectura

```mermaid
architecture-beta
    group localstack(cloud)[AWS LocalStack]

    service lambda(server)[Lambda Function] in localstack
    service s3(disk)[S3 Bucket] in localstack

    lambda:R -- L:s3
```

[![Ver Diagrama](https://img.shields.io/badge/Ver_Diagrama-Instalar-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Índice

- [Inicio Rápido (Dev Container)](#inicio-rápido-dev-container)
- [Paso a Paso (sin Dev Container)](#paso-a-paso-sin-dev-container)
    - [1. Iniciar infraestructura](#1-iniciar-infraestructura)
    - [2. Configurar el entorno](#2-configurar-el-entorno)
    - [3. Instalar AWS Toolkit](#3-instalar-aws-toolkit)
    - [4. Desplegar recursos](#4-desplegar-recursos)
    - [5. Ejecutar el ejemplo](#6-ejecutar-el-ejemplo)
    - [6. Validación](#7-validación)
    - [7. Limpieza](#8-limpieza)
- [Solución de problemas](#solución-de-problemas)
- [Licencia](#licencia)

---

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
4. **Verificar subida:**
   ```bash
   aws s3 ls s3://test-bucket/
   ```
5. **Limpieza:**
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

### 2. Configurar el entorno

En lugar de configurarlo manualmente, utiliza nuestro script de configuración estandarizado. Este script automáticamente:
1. Instala **mise** y **uv** (gestores de herramientas).
2. Instala las versiones requeridas de **Python**, **AWS CLI** y **Terraform**.
3. Configura el perfil de AWS `localstack`.
4. Sincroniza las dependencias de Python usando **uv**.

```bash
scripts/setup-mve.sh
```

### 3. Instalar AWS Toolkit

Instala la extensión [AWS Toolkit](vscode:extension/amazonwebservices.aws-toolkit-vscode). Para usarla con LocalStack:

1. Abre el explorador de **AWS Toolkit** en VS Code.
2. Haz clic en la configuración de **Profiles** o **Connections**.
3. Selecciona el perfil `localstack` configurado en el paso 2.

### 4. Desplegar recursos

Elige tu opción de despliegue preferida usando nuestros scripts estandarizados:

💡 **Nota:** Si cambias entre diferentes métodos de despliegue (**Terraform**, **CloudFormation** o **Boto3**), asegúrate de realizar una **Limpieza** primero para evitar conflictos de nombres de recursos.

* **Opción A**: Terraform

   ```bash
   scripts/terraform/deploy.sh
   ```

* **Opción B**: CloudFormation

   ```bash
   scripts/cloudformation/deploy.sh
   ```

   > 🎨 **Consejo:** Puedes visualizar esta plantilla usando **AWS Infrastructure Composer** desde **AWS Toolkit** abriendo `deploy/cloudformation/template.yaml` y haciendo clic en el botón "Infrastructure composer" en la esquina superior derecha del editor.

* **Opción C**: Boto3 (Python)

   ```bash
   scripts/boto3/deploy.sh
   ```

* <details><summary><b>Opción D</b>: AWS CLI (Manual) - Haz clic para expandir</summary>

   ```bash
   # 1. Empaquetar Lambda
   python deploy/utils/package_lambda.py

   # 2. Crear Rol de IAM
   aws iam create-role --profile localstack \
     --role-name lambda-s3-role \
     --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

   # 3. Crear Función Lambda
   aws lambda create-function --profile localstack \
     --function-name upload-to-s3 \
     --runtime python3.12 \
     --role arn:aws:iam::000000000000:role/lambda-s3-role \
     --handler lambda.lambda_handler \
     --zip-file fileb://deploy/dist/function.zip \
     --environment Variables={ENDPOINT_URL=http://localhost:4566}

   # 4. Crear Bucket de S3
   aws s3 mb s3://test-bucket --profile localstack
   ```
</details>

### 5. Ejecutar el ejemplo

* **Opción A**: Script de Python. Ejecuta el script de demostración para invocar la Lambda y verificar la subida:

   ```bash
   python main.py
   ```

* **Opción B**: AWS Toolkit. Puedes explorar los recursos y activar la Lambda directamente desde el IDE:
    1. Selecciona el perfil `localstack` en el AWS Toolkit.
    2. Para activar el ejemplo, haz clic derecho en la función `upload-to-s3` y selecciona **Invoke Lambda...**.

---

### 7. Validación

Elige tu forma preferida de verificar los resultados:

* **Opción A**: AWS CLI. Verifica que el archivo se ha subido correctamente:
    - **Check S3 Bucket**:
      ```bash
      aws s3 ls s3://test-bucket/ --profile localstack
      ```
    - **Ver Logs de Lambda**:
      ```bash
      aws logs tail /aws/lambda/upload-to-s3 --profile localstack
      ```

* **Opción B**: AWS Toolkit. Explora los recursos directamente desde la barra lateral de VS Code:
    1. **S3**: Expande la sección S3 para ver los archivos subidos.
    2. **CloudWatch**: Expande la sección de Logs para ver la salida de ejecución de la Lambda.

---

### 8. Limpieza

Para eliminar los recursos creados por un método de despliegue específico, puedes usar los scripts de destrucción correspondientes:

**Terraform**:
```bash
scripts/terraform/destroy.sh
```

**CloudFormation**:
```bash
scripts/cloudformation/destroy.sh
```

**Boto3**:
```bash
scripts/boto3/destroy.sh
```

Para eliminar completamente la infraestructura local (contenedores y volúmenes):

```bash
docker compose down -v
```

## Solución de problemas

| Problema | Solución |
| :--- | :--- |
| **Timeout de Lambda** | Asegúrate de que LocalStack tenga suficientes recursos de memoria/CPU. |
| **Conexión rechazada** | Asegúrate de que LocalStack esté ejecutándose y espera al mensaje `Ready.` en los logs. |

## Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
