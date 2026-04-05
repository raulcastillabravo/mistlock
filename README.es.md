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
    2. (Opcional, pero recomendado) [VS Code](https://code.visualstudio.com/) con [Extensión Dev Containers](vscode:extension/ms-vscode-remote.remote-containers) instalada.

2. **Abrir un ejemplo:** Abre una carpeta de ejemplo (ej. `src/aws/mves/s3-garage/`) en VS Code.
3. **Reabrir en Contenedor:** Abre la **Paleta de Comandos** (`F1` o `Ctrl/Cmd+Shift+P`) y selecciona **Dev Containers: Reopen in Container**.
4. **Sigue las instrucciones:** Una vez que el contenedor esté listo, sigue las instrucciones en el `README.md` del ejemplo. Normalmente es solo:
   ```bash
   python main.py
   ```

Hay dos tipos de ejemplos:

*   **MVE (Minimal Viable Example)**: Se centra en un servicio Cloud específico, cómo emularlo y qué herramientas son necesarias para desarrollar con él localmente. Puede haber más de un MVE por servicio si hay varias herramientas para emularlo.
*   **Project**: Combina diferentes servicios Cloud en el mismo entorno de desarrollo local. Puedes ver los servicios utilizados en cada proyecto entre paréntesis en la tabla de abajo.

## 📚 Ejemplos Disponibles

Algunos ejemplos aparecen varias veces porque integran varios servicios cloud.

### 🟠 AWS (Amazon Web Services)

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Lambda** | • *(próximamente)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **ECS / EKS** | • *(próximamente)* | |
| **Glue** | • *(próximamente)* | |
| **S3** | • [s3-garage](./src/aws/mves/s3-garage/)<br>• [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **RDS (Postgres)** | • [rds-postgres (Postgres)](./src/hybrid/mves/postgres/) | • [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Dynamo DB** | • *(próximamente)* | • [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **ElastiCache (Redis)** | • [elasti-cache (Redis)](./src/hybrid/mves/redis/) | |
| **Step Functions** | • [step-functions-localstack](./src/aws/mves/step-functions-localstack/) | |
| **SQS / SNS** | • *(próximamente)* | |
| **EventBridge** | • *(próximamente)* | |
| **CloudFormation** | • *(próximamente)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |


### 🔵 Microsoft Azure

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Azure Functions** | • *(próximamente)* | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage)<br>• [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Container Apps** | • *(próximamente)* | |
| **Databricks** | • [databricks](./src/azure/mves/databricks/) | |
| **Blob Storage** | • [blob-storage](./src/azure/mves/blob-storage/) | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage) |
| **Azure SQL** | • *(próximamente)* | • [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Cosmos DB** | • *(próximamente)* | • [no-sql-writer](./src/azure/projects/no-sql-writer/) (Python → Cosmos DB) |
| **Cache for Redis** | • [cache-for-redis (Redis)](./src/hybrid/mves/redis/) | |
| **Service Bus** | • *(próximamente)* | |
| **Event Grid** | • *(próximamente)* | |


### 🔴 GCP (Google Cloud Platform)

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Cloud Functions** | • *(próximamente)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud Run** | • *(próximamente)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Dataflow** | • *(próximamente)* | |
| **Cloud Storage** | • *(próximamente)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud SQL** | • [cloud-sql (Postgres)](./src/hybrid/mves/postgres/) | • [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Firestore** | • *(próximamente)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Memorystore** | • [memorystore (Redis)](./src/hybrid/mves/redis/) | |
| **Pub/Sub** | • *(próximamente)* | |


### 🟢 Nube Híbrida y Otros

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **MinIO** | • [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | |
| **Postgres** | • [postgres](./src/hybrid/mves/postgres/) | |
| **MongoDB** | • [mongo](./src/hybrid/mves/mongo/) | |
| **Redis** | • [redis](./src/hybrid/mves/redis/) | • [redis-mutex](./src/hybrid/projects/redis-mutex/) (Python → Redis) |
| **Airflow** | • [airflow](./src/hybrid/mves/airflow/) | |
| **RabbitMQ** | • [rabbitmq](./src/hybrid/mves/rabbitmq/) | |
| **Terraform** | • *(próximamente)* | • [storage-writer (AWS)](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl (AWS)](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer (AWS)](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Metabase** | • [metabase](./src/hybrid/mves/metabase/) | |
| **Dev Containers** | • [devcontainers](./src/hybrid/mves/devcontainers/) | |


## 🚀 Roadmap
- [ ] Añadir un MVE por cada servicio en la tabla superior.
  <details>
  <summary>Ver siguientes pasos</summary>

  - 2026-04-20
    - [ ] MVE Google Functions.
    - [ ] MVE Azure Functions.
    - [ ] MVE AWS Lambda con SAM Framework.
  - Próximo lote:
    - [ ] MVE Google Dataflow.
    - [ ] MVE Azure Cosmos DB.
    - [ ] MVE AWS Glue.
  - Backlog:
    - [ ] MVE AWS Lambda con MiniStack.
    - [ ] MVE AWS ECS / EKS.
    - [ ] MVE AWS S3 con RustFS.
    - [ ] MVE AWS DynamoDB Official Image.
    - [ ] MVE AWS Step Functions Official Image.
    - [ ] MVE AWS SQS / SNS.
    - [ ] MVE AWS Eventbridge.
    - [ ] MVE AWS CloudFormation.
    - [ ] Unificar los MVEs de MinIO en uno solo.
    - [ ] MVE Azure Container Apps (ACA).
    - [ ] MVE Azure SQL Edge.
    - [ ] MVE Azure Service Bus.
    - [ ] MVE Azure Event Grid.
    - [ ] MVE Google Cloud Run.
    - [ ] MVE Google Firebase Storage.
    - [ ] MVE Google Firebase Firestore.
    - [ ] MVE Google Firebase Pub/Sub.
    - [ ] MVE Terraform.
  </details>
- [ ] Añadir tests y unificar la estructura de todos los MVEs y proyectos para seguir el mismo patrón.
- [ ] Crear una GitHub Pages con documentación del repositorio.
- [ ] Grabar vídeos con explicaciones y demostraciones para cada MVE.

## 📝 Nota del autor

Este proyecto es la base del **contenido educativo** que genero en redes sociales (y mi mayor proyecto Open Source hasta la fecha 😄). 

Es completamente gratuito y abierto para la comunidad, úsalo para **aprender y practicar con total libertad**. 

Solo espero que te sea de gran utilidad y que lo apoyes para que otros desarrolladores también lo conozcan. Es el motor que me permite seguir creando **contenido y formación para la comunidad**.