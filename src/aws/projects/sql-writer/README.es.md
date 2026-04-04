# Ejemplo de Nube Híbrida con LocalStack

Ejemplo mínimo viable para demostrar un escenario de nube híbrida utilizando LocalStack y una instancia externa de PostgreSQL. Este ejemplo muestra cómo una Lambda de AWS (simulada en LocalStack) puede obtener secretos de Secrets Manager e interactuar con una base de datos fuera del entorno de AWS.

## Estructura del Proyecto

```
localstack-hybrid-cloud/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── add_user_lambda/          # Código de la función Lambda
│   ├── lambda_handler.py
│   └── models.py
├── docker-compose.yml        # LocalStack + Postgres
├── package_lambda.py         # Script para crear el ZIP
├── main.tf                   # Infraestructura (Secretos + Lambda)
├── terraform.tfvars          # Variables de Terraform
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- Terraform instalado
- AWS CLI instalado
- DBeaver o cualquier cliente SQL (para verificar resultados)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en el Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P`
3. Selecciona: **Dev Containers: Reopen in Container**

### Paso 2: Configurar AWS CLI

Si no has configurado el CLI aún, ejecuta:

```bash
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region us-east-1
```

### Paso 3: Preparar y Desplegar

```bash
docker compose up -d
python package_lambda.py
terraform init && terraform apply -auto-approve
```

### Paso 4: Invocar la Lambda vía CLI

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
    --function-name AddUserFunction \
    --payload '{}' \
    response.json
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Iniciar Infraestructura

```bash
docker compose up -d
```

### Paso 2: Construir y Desplegar

```bash
python package_lambda.py
terraform init && terraform apply -auto-approve
```

### Paso 3: Ejecutar Aplicación (Invocar Lambda)

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
    --function-name AddUserFunction \
    --payload '{}' \
    response.json

cat response.json
```

## Verificación de Resultados

Dado que la Lambda interactúa con una base de datos PostgreSQL local, puedes verificar los resultados usando **DBeaver** o cualquier otro cliente de base de datos:

1. **Host**: `localhost`
2. **Port**: `5432`
3. **Database**: `mydb`
4. **User**: `myuser`
5. **Password**: `mypassword`

Ejecuta la siguiente consulta:
```sql
SELECT * FROM users ORDER BY created_at DESC;
```

## Componentes del Proyecto

### `main.tf`

Define la infraestructura usando Terraform:
- **AWS Secrets Manager**: Almacena las credenciales de Postgres como un único objeto JSON.
- **AWS Lambda**: Despliega la función utilizando el archivo `lambda.zip`.
- **IAM**: Crea los roles necesarios para la Lambda.

### `add_user_lambda/`

Contiene la lógica de la función Lambda:
- `models.py`: Modelos ORM de SQLAlchemy y lógica de recuperación de secretos.
- `lambda_handler.py`: Manejador que recupera secretos, **inicializa la tabla** e inserta un usuario aleatorio.

### `package_lambda.py`

Un script de ayuda que utiliza **Docker** para construir un entorno Linux compatible y empaquetar la carpeta `add_user_lambda/` junto con sus dependencias (SQLAlchemy, psycopg2) en un archivo `lambda.zip`.

## Configuración

Toda la configuración, incluyendo las credenciales de la base de datos y los endpoints de LocalStack, se gestiona en `terraform.tfvars`. La configuración de los servicios para Docker se gestiona directamente en el archivo `docker-compose.yml`.

## Comandos Útiles

### Comandos Docker

```bash
# Iniciar contenedor
docker compose up -d

# Detener contenedor
docker compose down

# Ver logs
docker compose logs -f
```

### AWS CLI (LocalStack)

```bash
# Listar funciones Lambda
aws --endpoint-url=http://localhost:4566 lambda list-functions

# Consultar Secretos
aws --endpoint-url=http://localhost:4566 secretsmanager list-secrets
```

## Resolución de Problemas

### Conexión Rechazada (Connection Refused)

Si la Lambda no puede conectarse a Postgres, asegúrate de que `host.docker.internal` sea accesible desde dentro del contenedor de LocalStack.

### Puerto ya en uso

Si los puertos 4566 o 5432 ya están en uso, modifica los mapeos de puertos en `docker-compose.yml`.

## Limpieza

Para eliminar todo:

```bash
terraform destroy -auto-approve
docker compose down -v
rm lambda.zip response.json
```

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
