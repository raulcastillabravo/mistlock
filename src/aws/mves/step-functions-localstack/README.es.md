# Ejemplo de AWS Step Functions + LocalStack

Ejemplo mínimo viable para trabajar con **AWS Step Functions** de forma local utilizando **LocalStack**, **Python** y el **AWS Toolkit de VS Code**. Este ejemplo demuestra un flujo de alta de usuario con ejecución paralela de Lambdas y creación de un usuario de IAM.

## Estructura del Proyecto

```
aws-step-functions/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── lambdas/
│   ├── log_user.py          # Escribe en DynamoDB
│   └── validate_email.py    # Valida el formato del email
├── deploy.py                # Script de despliegue de infraestructura
├── docker-compose.yml       # Servicios de LocalStack
├── main.py                  # Script de ejecución del flujo
├── pyproject.toml
├── step_function.asl.json   # Definición de la Step Function (ASL)
├── utils.py                 # Utilidades para ZIP y configuración
└── README.md
```

## Prerrequisitos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración de contenedores)
- [AWS Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-aws-us.aws-toolkit-vscode) (Incluido en el Dev Container)
- [AWS CLI](https://aws.amazon.com/cli/) (Incluido en el Dev Container)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en el Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Configurar Perfil de LocalStack

Antes de ejecutar el ejemplo, configura un perfil de AWS dedicado para LocalStack:

```bash
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack
aws configure set endpoint_url http://localhost:4566 --profile localstack
```

### Paso 3: Ejecutar el Ejemplo

1. Levantar LocalStack:
   ```bash
   docker compose up -d
   ```
2. Desplegar la infraestructura:
   ```bash
   python deploy.py
   ```
3. Ejecutar el flujo de trabajo:
   ```bash
   python main.py
   ```

> **Nota**: Espera **5-10 segundos** después de `deploy.py` para que LocalStack termine de inicializar el entorno de las Lambdas antes de ejecutar `main.py`.

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 2: Configurar Perfil de LocalStack

Configura el perfil `localstack` como se describe en la Opción 1.

### Paso 3: Ejecutar el Ejemplo

Sigue los mismos pasos que en la configuración del Dev Container:
1. `docker compose up -d`
2. `python deploy.py`
3. `python main.py`

> **Nota**: Espera **5-10 segundos** después de `deploy.py` para que LocalStack termine de inicializar el entorno de las Lambdas.

## Componentes del Proyecto

### Script de Infraestructura (`deploy.py`)

Gestiona la creación de todos los recursos de AWS:
- Crea la tabla de DynamoDB para logs.
- Despliega las funciones Lambda usando la utilidad `deploy_lambda`.
- Crea/Actualiza la máquina de estados de Step Functions.

### Utilidades (`utils.py`)

Funciones auxiliares compartidas:
- **`create_lambda_zip(path)`**: Genera un ZIP en memoria para el despliegue de Lambdas.
- **`get_boto_config()`**: Devuelve la configuración estándar de Boto3 para LocalStack.
- **`deploy_lambda(client, name, ...)`**: Lógica centralizada para crear/actualizar Lambdas e inyectar variables de entorno.

### Script Principal (`main.py`)

Demuestra cómo lanzar y monitorizar el flujo de trabajo:
1. Se conecta a Step Functions usando el endpoint de `localstack`.
2. Genera datos de usuario aleatorios.
3. Inicia la ejecución y consulta el estado hasta que finaliza.
4. Imprime el estado final y la salida.

### Step Function (`step_function.asl.json`)

La definición de la máquina de estados usando Amazon States Language (ASL):
- **ProcessUserOnboarding**: Un estado `Parallel` que ejecuta ambas Lambdas simultáneamente.
- **CreateIAMUser**: Un `Task` que usa la integración con el SDK de AWS para crear un usuario IAM local si los pasos anteriores tienen éxito.

## Pasos de Validación

Después de ejecutar `main.py`, puedes verificar los resultados:

### 1. Verificar Creación de Usuario IAM
```bash
aws iam list-users --profile localstack
```

### 2. Verificar Logs de DynamoDB
```bash
aws dynamodb scan --table-name UserLogs --profile localstack
```

### 3. Verificar Funciones Lambda
```bash
aws lambda list-functions --profile localstack
```

## Trabajando con AWS Toolkit

Este MVE está diseñado para mostrar el editor ASL proporcionado por AWS Toolkit:

1. **Abrir Paleta de Comandos**: Presiona `F1` o `Ctrl+Shift+P`.
2. **Conectar a AWS**: Escribe y selecciona **AWS: Connect to AWS**.
3. **Seleccionar Perfil**: Selecciona el perfil `localstack`.
4. **Renderizar Grafo**: Abre `step_function.asl.json` y haz clic en el icono de **Visual Graph** (arriba a la derecha).
5. **Ejecutar**: En el **AWS Explorer**, haz clic derecho en `UserOnboardingWorkflow` y selecciona **Start Execution**.

## Variables de Entorno

El archivo `.env` contiene:

```
AWS_REGION=us-east-1
LOCALSTACK_ENDPOINT=http://localhost:4566
DYNAMODB_TABLE=UserLogs
STEP_FUNCTION_NAME=UserOnboardingWorkflow
```

## Comandos Útiles

### Comandos de Docker

```bash
# Levantar LocalStack
docker compose up -d

# Detener LocalStack
docker compose down

# Ver logs
docker compose logs -f localstack
```

### Invocación Manual de Lambdas (Pruebas)

Puedes invocar las Lambdas de forma independiente para probarlas:

**Probar Validación de Email:**
```bash
aws lambda invoke \
  --function-name ValidateEmailLambda \
  --payload '{"email": "valid@example.com"}' \
  --cli-binary-format raw-in-base64-out \
  --profile localstack \
  response.json
```

**Probar Registro de Usuario:**
```bash
aws lambda invoke \
  --function-name LogUserLambda \
  --payload '{"username": "debug_user", "email": "debug@example.com"}' \
  --cli-binary-format raw-in-base64-out \
  --profile localstack \
  response.json
```

## Resolución de Problemas

### La función Lambda está en estado 'Pending'

Si ejecutas `main.py` inmediatamente después de `deploy.py`, es posible que LocalStack aún esté inicializando el entorno.

**Solución**: Espera de 5 a 10 segundos y vuelve a intentarlo.

### Conexión Rechazada (Connection Refused)

Asegúrate de que LocalStack esté funcionando:

```bash
docker ps
```

## Limpieza

Para eliminar todo completamente:

```bash
docker compose down -v
```

## Siguientes Pasos

- Añadir manejo de errores a la Step Function (Catch/Retry).
- Implementar un estado `Choice` para ramificar la lógica según la validación del email.
- Añadir pruebas unitarias para las funciones Lambda.

## Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según necesites.
