# RabbitMQ + Python + Docker Example

Ejemplo mínimo viable para trabajar con RabbitMQ usando Docker Compose, cliente pika de Python y la interfaz de gestión de RabbitMQ.

## Estructura del Proyecto

```
rabbitmq-docker-python/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── rabbitmq_client.py
├── publish.py
├── listen.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para usar dev container)
- Navegador web para acceder a la interfaz de gestión de RabbitMQ

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Iniciar Contenedor de RabbitMQ

Dentro del terminal del dev container:

```bash
docker compose up -d
```

Verifica que está funcionando:

```bash
docker ps
```

### Paso 3: Publicar Eventos

Abre una terminal y ejecuta el publicador:

```bash
python publish.py
```

Deberías ver una salida como:

```
--- Publishing event to RabbitMQ ---
✓ Published: User logged in: jane@example.com

✓ Done! Event published to queue 'user_events'
✓ You can run listen.py to consume this event
```

Cada vez que ejecutes `publish.py`, publicará un evento aleatorio de las opciones disponibles.

### Paso 4: Escuchar Eventos

Abre una **nueva terminal** (mantén la primera abierta) y ejecuta el listener:

```bash
python listen.py
```

Deberías ver:

```
--- Listening for events on queue 'user_events' ---
✓ Waiting for messages. Press CTRL+C to exit

✓ Received: User logged in: jane@example.com
```

El listener seguirá ejecutándose y esperando nuevos eventos. Presiona `CTRL+C` para detenerlo.

### Paso 5: Probar Procesamiento de Eventos en Tiempo Real

Con `listen.py` aún ejecutándose, abre otra terminal y publica más eventos:

```bash
python publish.py
```

Verás que el listener recibe y procesa inmediatamente el nuevo evento. Cada ejecución de `publish.py` envía un evento aleatorio a la cola.

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias con uv

```bash
pip install uv && uv sync
```

### Paso 2: Iniciar Contenedor de RabbitMQ

```bash
docker compose up -d
```

### Paso 3: Publicar y Escuchar Eventos

Sigue los pasos 3-5 de la Opción 1.

## Acceder a la Interfaz de Gestión de RabbitMQ

RabbitMQ incluye una interfaz de gestión basada en web que te permite monitorizar colas, exchanges, conexiones y más.

### Paso 1: Abrir la Interfaz de Gestión

Abre tu navegador web y navega a:

```
http://localhost:15672
```

### Paso 2: Iniciar Sesión

Usa las credenciales de tu archivo `.env`:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Paso 3: Ver Colas

1. Haz clic en la pestaña **Queues** en la parte superior
2. Deberías ver la cola `user_events`
3. Haz clic en el nombre de la cola para ver estadísticas detalladas:
   - Número de mensajes listos
   - Número de mensajes siendo entregados
   - Tasas de mensajes
   - Detalles de consumidores

### Paso 4: Ver Mensajes

Mientras visualizas una cola, desplázate hacia abajo hasta la sección **Get messages** para inspeccionar mensajes sin eliminarlos de la cola.

## Conceptos de RabbitMQ

### Cola (Queue)
Un buffer que almacena mensajes. Los productores envían mensajes a las colas, y los consumidores reciben mensajes de las colas.

### Productor (Publisher)
Una aplicación que envía mensajes a una cola. En este ejemplo, `publish.py` es el productor.

### Consumidor (Listener)
Una aplicación que recibe mensajes de una cola. En este ejemplo, `listen.py` es el consumidor.

### Confirmación de Mensaje (Acknowledgment)
Cuando un consumidor procesa un mensaje, envía una confirmación (ack) a RabbitMQ. Esto asegura que los mensajes no se pierdan si un consumidor falla.

### Cola Durable
Una cola que sobrevive a reinicios de RabbitMQ. Los mensajes en colas durables se persisten en disco.

## Variables de Entorno

El archivo `.env` contiene:

```
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin123
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672
```

- **Puerto 5672**: Protocolo AMQP (para aplicaciones)
- **Puerto 15672**: Interfaz de Gestión (para navegador web)

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

# Ver solo logs de RabbitMQ
docker compose logs -f rabbitmq
```

### Comandos CLI de RabbitMQ

```bash
# Listar todas las colas
docker exec rabbitmq_local rabbitmqctl list_queues

# Listar todos los exchanges
docker exec rabbitmq_local rabbitmqctl list_exchanges

# Purgar una cola (eliminar todos los mensajes)
docker exec rabbitmq_local rabbitmqctl purge_queue user_events
```

## Solución de Problemas

### Puerto Ya en Uso

Si los puertos 5672 o 15672 ya están en uso, cambia los puertos en `.env`:

```
RABBITMQ_PORT=5673
RABBITMQ_MANAGEMENT_PORT=15673
```

Luego reinicia:

```bash
docker compose down
docker compose up -d
```

### Conexión Rechazada

Asegúrate de que el contenedor de RabbitMQ está funcionando:

```bash
docker ps
```

Revisa los logs en busca de errores:

```bash
docker compose logs rabbitmq
```

Espera unos segundos después de iniciar el contenedor para que RabbitMQ se inicialice completamente.

### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

### Autenticación Fallida

Asegúrate de usar las credenciales correctas del archivo `.env`.

## Limpieza

Para eliminar todo completamente:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de RabbitMQ (opcional)
docker rmi rabbitmq:3-management-alpine
```

## Próximos Pasos

- Implementar múltiples consumidores para balanceo de carga
- Usar exchanges y routing keys para enrutamiento de mensajes
- Implementar colas de mensajes muertos (dead letter queues) para mensajes fallidos
- Añadir prioridades de mensajes
- Explorar clustering de RabbitMQ para alta disponibilidad
- Implementar patrones RPC (Remote Procedure Call)

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.