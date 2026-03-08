# Ejemplos Mínimos Viables (MVE)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raulcastillabravo/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green.svg)](https://github.com/raulcastillabravo/mve-collection/blob/main/LICENSE)

Este repositorio enseña cómo desarrollar para el Cloud gratis, sin cuenta y sin tarjeta de crédito, emulando AWS, Azure y Google Cloud en local:

* ✅ **Gratis y sin cuenta**: Todas las tecnologías son gratis y no requieren de crear una cuenta en ningún sitio.
* **💯% compatible**: El código que desarrollas en local es 100% compatible con el Cloud real.
* 📦 **Autocontenido**: Cada ejemplo es independiente e incluye todo lo necesario para ejecutarlo.
* 🚀 **Listo para ejecutar**: Los ejemplos están listos para ejecutar sin hacer cambios en el código.
* 🐳 **Dockerizado**: Todos cuentan con entornos de desarrollo dockerizados.
* 🖥️ **Interfaces gráficas**: Uso de herramientas gráficas para gestionar el entorno Cloud local.
* 📖 **Bien documentado**: Todos los ejemplos están documentados en inglés y español.

> ⭐ **Si encuentras este repositorio útil, ¡por favor considera darle una estrella!** Ayuda a otros desarrolladores a encontrar estos ejemplos y apoya el desarrollo continuo.

## 🚀 Inicio Rápido

1. **Requisitos previos:**
    1. [Docker](https://www.docker.com/get-started) instalado y ejecutándose.
    2. [Extensión Dev Containers](vscode:extension/ms-vscode-remote.remote-containers) instalada.

2. **Abrir un ejemplo:** Abre una carpeta de ejemplo (ej. `src/aws-dynamo-db`) en VS Code.
3. **Reabrir en Contenedor:** Abre la **Paleta de Comandos** (`F1` o `Ctrl/Cmd+Shift+P`) y selecciona **Dev Containers: Reopen in Container**.
4. **Sigue las instrucciones:** Una vez que el contenedor esté listo, sigue las instrucciones en el `README.md` del ejemplo. Normalmente es solo:
   ```bash
   python main.py
   ```

## 📚 Ejemplos Disponibles

Algunos ejemplos aparecen varias veces porque integran varios servicios cloud.

### 🟠 AWS (Amazon Web Services)

| Servicio | MVE | Descripción |
| :--- | :--- | :--- |
| **S3** | [aws-lambda](./src/aws-lambda/) | Despliega una función Lambda que sube objetos a S3, emulado con LocalStack, Terraform, CloudFormation y Boto3. |
| **S3** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demuestra un pipeline de procesamiento de archivos donde las subidas a S3 disparan una Lambda para registrar metadatos en una tabla DynamoDB, todo emulado con LocalStack, Terraform y CloudFormation. |
| **Dynamo DB** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demuestra un pipeline de procesamiento de archivos donde las subidas a S3 disparan una Lambda para registrar metadatos en una tabla DynamoDB, todo emulado con LocalStack, Terraform y CloudFormation. |
| **Dynamo DB** | [aws-step-functions](./src/aws-step-functions/) | Orquesta un flujo de registro de usuarios con AWS Step Functions que ejecuta Lambdas en paralelo y registra los resultados en DynamoDB, usando LocalStack y el AWS Toolkit. |
| **RDS (Postgres)** | [localstack-hybrid-cloud](./src/localstack-hybrid-cloud/) | Demuestra un escenario de nube híbrida donde una Lambda de AWS (simulada en LocalStack) recupera credenciales de Secrets Manager vía Terraform para interactuar con una base de datos PostgreSQL externa. |
| **Lambda** | [aws-lambda](./src/aws-lambda/) | Despliega una función Lambda que sube objetos a S3, emulado con LocalStack, Terraform, CloudFormation y Boto3. |
| **Lambda** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demuestra un pipeline de procesamiento de archivos donde las subidas a S3 disparan una Lambda para registrar metadatos en una tabla DynamoDB, todo emulado con LocalStack, Terraform y CloudFormation. |
| **Lambda** | [aws-step-functions](./src/aws-step-functions/) | Orquesta un flujo de registro de usuarios con AWS Step Functions que ejecuta Lambdas en paralelo y registra los resultados en DynamoDB, usando LocalStack y el AWS Toolkit. |
| **Step Functions** | [aws-step-functions](./src/aws-step-functions/) | Orquesta un flujo de registro de usuarios con AWS Step Functions que ejecuta Lambdas en paralelo y registra los resultados en DynamoDB, usando LocalStack y el AWS Toolkit. |

### 🔵 Microsoft Azure

| Servicio | MVE | Descripción |
| :--- | :--- | :--- |
| **Blob Storage** | [azurite-docker](./src/azurite-docker/) | Implementa operaciones locales de Azure Blob Storage como creación de contenedores y subida/descarga de blobs usando Azurite y Python. |
| **Blob Storage** | [azure-functions](./src/azure-functions/) | Crea una Azure Function disparada por HTTP que sube archivos a un almacenamiento de blobs local emulado por Azurite, usando Python y Docker Compose. |
| **Cosmos DB** | [azure-cosmos-db](./src/azure-cosmos-db/) | Integra una aplicación Python con el Emulador de Azure Cosmos DB ejecutándose en Docker para realizar operaciones de base de datos básicas localmente. |
| **Azure SQL** | [azure-sql-database](./src/azure-sql-database/) | Procesa archivos CSV subidos a Azurite (Blob Storage) mediante una aplicación FastAPI impulsada por Dapr que inserta datos en Azure SQL Edge. |
| **Azure Functions** | [azure-functions](./src/azure-functions/) | Crea una Azure Function disparada por HTTP que sube archivos a un almacenamiento de blobs local emulado por Azurite, usando Python y Docker Compose. |
| **Databricks** | [databricks-docker](./src/databricks-docker/) | Simula un entorno Databricks de alta fidelidad (Runtime 15.4 LTS) usando Docker, MinIO para almacenamiento S3 y PostgreSQL para el Metastore de Hive para probar ETLs con Spark y Delta Lake. |

### 🔴 GCP (Google Cloud Platform)

| Servicio | MVE | Descripción |
| :--- | :--- | :--- |
| **Cloud Storage** | [gcp-functions](./src/gcp-functions/) | Implementa una Google Cloud Function disparada por HTTP que sube archivos a Cloud Storage usando Firebase Emulator Suite para desarrollo local. |
| **Cloud Storage** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Procesa archivos CSV subidos a Cloud Storage usando una Cloud Function disparada que inserta los datos en una base de datos PostgreSQL local. |
| **Firestore** | [gcp-cloud-run](./src/gcp-cloud-run/) | Despliega un servicio de Google Cloud Run contenedorizado que registra datos de pacientes en Firestore usando Firebase Emulator Suite y Python. |
| **Cloud Functions** | [gcp-functions](./src/gcp-functions/) | Implementa una Google Cloud Function disparada por HTTP que sube archivos a Cloud Storage usando Firebase Emulator Suite para desarrollo local. |
| **Cloud Functions** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Procesa archivos CSV subidos a Cloud Storage usando una Cloud Function disparada que inserta los datos en una base de datos PostgreSQL local. |
| **Cloud Run** | [gcp-cloud-run](./src/gcp-cloud-run/) | Despliega un servicio de Google Cloud Run contenedorizado que registra datos de pacientes en Firestore usando Firebase Emulator Suite y Python. |
| **Cloud SQL (Postgres)** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Procesa archivos CSV subidos a Cloud Storage usando una Cloud Function disparada que inserta los datos en una base de datos PostgreSQL local. |

### 🟢 Nube Híbrida y Otros

| Servicio | MVE | Descripción |
| :--- | :--- | :--- |
| **MinIO** | [minio-docker-boto3](./src/minio-docker-boto3/) | Demuestra operaciones de almacenamiento de objetos compatibles con S3 usando MinIO, el SDK Boto3 y pandas para gestionar archivos CSV localmente. |
| **MinIO** | [minio-docker-delta](./src/minio-docker-delta/) | Implementa transacciones ACID y capacidades de "time travel" en MinIO usando Delta Lake (delta-rs) y Python para un almacenamiento de datos local fiable. |
| **Mongo** | [mongo-docker-mongoengine](./src/mongo-docker-mongoengine/) | Integra Python con MongoDB usando el ODM MongoEngine y Docker Compose para el desarrollo local de bases de datos NoSQL. |
| **Postgres** | [postgres-docker-sqlalchemy](./src/postgres-docker-sqlalchemy/) | Configura una base de datos PostgreSQL con el ORM SQLAlchemy y Docker Compose para el desarrollo y prueba de bases de datos relacionales estándar. |
| **Postgres** | [localstack-hybrid-cloud](./src/localstack-hybrid-cloud/) | Demuestra la interacción con una base de datos PostgreSQL externa desde un entorno AWS simulado en LocalStack. |
| **Redis** | [redis-docker](./src/redis-docker/) | Implementa operaciones básicas de Redis usando el cliente de Python redis y Docker para caché local y almacenamiento de estructuras de datos. |
| **Redis** | [redis-docker-mutex](./src/redis-docker-mutex/) | Implementa un mutex (bloqueo) distribuido usando Redis para coordinar el acceso a recursos compartidos entre múltiples procesos o hilos. |
| **Metabase** | [metabase-docker](./src/metabase-docker/) | Configura Metabase para visualización de datos y BI, conectado a una base de datos PostgreSQL local con datos de ejemplo generados vía SQLAlchemy. |
| **RabbitMQ** | [rabbitmq-docker-pika](./src/rabbitmq-docker-pika/) | Implementa un patrón de mensajería de publicación-suscripción usando RabbitMQ, el cliente pika y Python para el procesamiento de eventos asíncronos. |
| **Airflow** | [airflow-docker](./src/airflow-docker/) | Despliega un entorno completo de Apache Airflow con Docker para ejecutar y monitorizar un pipeline ETL basado en Python usando pandas. |
| **Dev Containers** | [devcontainers-docker](./src/devcontainers-docker/) | Explica los conceptos básicos de VS Code Dev Containers a través de una aplicación pandas sencilla, mostrando el aislamiento del entorno y las herramientas preconfiguradas. |

_Más ejemplos próximamente..._

## 📝 Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
