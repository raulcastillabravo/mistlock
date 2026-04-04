# Redis + Python + Docker Example

Ejemplo mínimo viable para trabajar con Redis usando Docker Compose, cliente redis de Python y Redis Insight.

## Estructura del Proyecto

```
redis-docker-python/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── redis_client.py
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para usar dev container)
- Redis Insight o cualquier cliente de Redis

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Iniciar Contenedor de Redis

Dentro del terminal del dev container:

```bash
docker compose up -d
```

Verifica que está funcionando:

```bash
docker ps
```

### Paso 3: Ejecutar Operaciones de Redis

Ejecuta el script de Python:

```bash
python main.py
```

Deberías ver una salida como:

```

--- Setting user data with HSET ---

--- Retrieving specific fields with HGET ---

User 1001 details:
  Name: John Doe
  Email: john@example.com

✓ Done! You can now see the data in Redis Insight.
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias con uv

```bash
pip install uv && uv sync
```

### Paso 2: Iniciar Contenedor de Redis

```bash
docker compose up -d
```

### Paso 3: Ejecutar Operaciones de Redis

```bash
python main.py
```

## Conectar con Redis Insight

### Paso 1: Instalar Redis Insight

1. Descarga e instala [Redis Insight](https://redis.io/insight/) si aún no lo tienes
2. Abre Redis Insight

### Paso 2: Añadir Conexión de Base de Datos

1. Haz clic en **Add Redis Database**
2. Selecciona **Add Database Manually**
3. Configura la conexión:
   - **Host:** `localhost`
   - **Puerto:** `6379`
   - **Database Alias:** `Local Redis` (o cualquier nombre que prefieras)
   - **Username:** dejar vacío
   - **Password:** `redis123`
4. Haz clic en **Add Redis Database**

### Paso 3: Ver Datos

1. Haz clic en tu conexión de base de datos
2. Ve a la pestaña **Browser**
3. Deberías ver las claves hash: `user:1001`, `user:1002`, `user:1003`
4. Haz clic en cualquier clave para ver sus campos y valores

## Estructura de Datos de Redis

Este ejemplo usa el tipo de datos **Hash** de Redis para almacenar información de usuarios:

| Clave      | Campo | Valor              |
| ---------- | ----- | ------------------ |
| user:1001  | name  | John Doe           |
| user:1001  | email | john@example.com   |
| user:1001  | age   | 30                 |

## Variables de Entorno

El archivo `.env` contiene:

```
REDIS_PASSWORD=redis123
REDIS_PORT=6379
REDIS_HOST=localhost
```

Puedes modificar estos valores según tus necesidades. Recuerda recrear los contenedores si cambias la contraseña de Redis.

## Comandos Útiles

### Comandos de Docker

```bash
# Iniciar contenedores
docker compose up -d

# Detener contenedores
docker compose down

# Detener y eliminar volúmenes (borrar todos los datos)
docker compose down -v

# Ver logs
docker compose logs -f

# Ver solo logs de Redis
docker compose logs -f redis
```

### Comandos de Redis CLI

```bash
# Conectar a Redis CLI desde el contenedor
docker exec -it redis_local redis-cli -a redis123

# Obtener todas las claves
KEYS *

# Obtener todos los campos de un hash
HGETALL user:1001

# Obtener campo específico
HGET user:1001 name

# Eliminar una clave
DEL user:1001

# Salir de Redis CLI
exit
```

## Operaciones de Redis Explicadas

### HSET (Hash Set)
Establece un campo en un hash a un valor. Si el hash no existe, se crea.

```python
redis.client.hset("user:1001", "name", "John Doe")
```

Equivalente en Redis:
```
HSET user:1001 name "John Doe"
```

### HGET (Hash Get)
Obtiene el valor de un campo específico en un hash.

```python
name = redis.client.hget("user:1001", "name")
```

Equivalente en Redis:
```
HGET user:1001 name
```

### HGETALL (Hash Get All)
Obtiene todos los campos y valores en un hash.

```python
user_data = redis.client.hgetall("user:1001")
```

Equivalente en Redis:
```
HGETALL user:1001
```

## Solución de Problemas

### Puerto Ya en Uso

Si el puerto 6379 ya está en uso, cambia `REDIS_PORT` en `.env` a otro puerto (ej. 6380) y reinicia:

```bash
docker compose down
docker compose up -d
```

### Conexión Rechazada

Asegúrate de que el contenedor de Redis está funcionando:

```bash
docker ps
```

Revisa los logs en busca de errores:

```bash
docker compose logs redis
```

### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

### Autenticación Fallida

Asegúrate de usar la contraseña correcta del archivo `.env` al conectar.

## Limpieza

Para eliminar todo completamente:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de Redis (opcional)
docker rmi redis:7-alpine
```

## Próximos Pasos

- Explorar otros tipos de datos de Redis (Listas, Sets, Sorted Sets, Streams)
- Implementar patrones de caché
- Añadir tiempos de expiración con TTL
- Usar pub/sub de Redis para mensajería
- Implementar bloqueo distribuido
- Añadir transacciones de Redis

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.