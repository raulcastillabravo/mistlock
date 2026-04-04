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

*   **MVE (Minimal Viable Example)**: Define todo lo necesario para emular un servicio Cloud específico y las herramientas necesarias para desarrollar con él localmente.
*   **Project**: Muestra cómo combinar diferentes servicios Cloud (MVEs) para desarrollar un caso de uso específico. Puedes ver los servicios utilizados en cada proyecto entre paréntesis en la tabla de abajo.

## 📚 Ejemplos Disponibles

Algunos ejemplos aparecen varias veces porque integran varios servicios cloud.

### 🟠 AWS (Amazon Web Services)

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **S3** | • [s3-garage](./src/aws/mves/s3-garage/)<br>• [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **Dynamo DB** | • *(próximamente)* | • [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **Lambda** | • *(próximamente)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Step Functions** | • [step-functions-localstack](./src/aws/mves/step-functions-localstack/) | • *(próximamente)* |
| **RDS (Postgres)** | • [rds-postgres (Postgres)](./src/hybrid/mves/postgres/) | • [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **ElastiCache (Redis)** | • [elasti-cache (Redis)](./src/hybrid/mves/redis/) | • *(próximamente)* |


### 🔵 Microsoft Azure

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Blob Storage** | • [blob-storage](./src/azure/mves/blob-storage/) | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage) |
| **Cosmos DB** | • *(próximamente)* | • [no-sql-writer](./src/azure/projects/no-sql-writer/) (Python → Cosmos DB) |
| **Azure SQL** | • *(próximamente)* | • [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Azure Functions** | • *(próximamente)* | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage)<br>• [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Databricks** | • [databricks](./src/azure/mves/databricks/) | • *(próximamente)* |
| **Cache for Redis** | • [cache-for-redis (Redis)](./src/hybrid/mves/redis/) | • *(próximamente)* |


### 🔴 GCP (Google Cloud Platform)

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Cloud Storage** | • *(próximamente)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Firestore** | • *(próximamente)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Cloud Functions** | • *(próximamente)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud Run** | • *(próximamente)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Cloud SQL** | • [cloud-sql (Postgres)](./src/hybrid/mves/postgres/) | • [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Memorystore (Redis)** | • [memorystore (Redis)](./src/hybrid/mves/redis/) | • *(próximamente)* |


### 🟢 Nube Híbrida y Otros

| Servicio | MVE | Projects |
| :--- | :--- | :--- |
| **Airflow** | • [airflow](./src/hybrid/mves/airflow/) | • *(próximamente)* |
| **Dev Containers** | • [devcontainers](./src/hybrid/mves/devcontainers/) | • *(próximamente)* |
| **Metabase** | • [metabase](./src/hybrid/mves/metabase/) | • *(próximamente)* |
| **Mongo** | • [mongo](./src/hybrid/mves/mongo/) | • *(próximamente)* |
| **Postgres** | • [postgres](./src/hybrid/mves/postgres/) | • *(próximamente)* |
| **RabbitMQ** | • [rabbitmq](./src/hybrid/mves/rabbitmq/) | • *(próximamente)* |
| **Redis** | • [redis](./src/hybrid/mves/redis/) | • [redis-mutex](./src/hybrid/projects/redis-mutex/) (Python → Redis) |


_Más ejemplos próximamente..._

## 📝 Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
