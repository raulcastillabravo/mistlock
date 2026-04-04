# Redis Mutex Distribuido + Python + Docker Ejemplo

Ejemplo mínimo viable para implementar un mutex distribuido (bloqueo) usando Redis con Docker Compose y Python. Este ejemplo demuestra cómo coordinar de forma segura el acceso a recursos compartidos entre múltiples hilos o procesos.

## Estructura del Proyecto

```
redis-docker-mutex/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── redis_client.py
├── mutex.py
├── main.py
├── main_acquire.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para usar dev container)
- Python 3.12+ (si se ejecuta localmente sin dev container)

## ¿Qué es un Mutex Distribuido?

Un **mutex** (exclusión mutua) es un mecanismo de sincronización que evita que múltiples hilos o procesos accedan simultáneamente a un recurso compartido. Un **mutex distribuido** extiende este concepto a través de múltiples máquinas o procesos, usando un servicio externo (como Redis) como punto de coordinación.

### Casos de Uso:

- **Prevenir condiciones de carrera**: Cuando múltiples procesos escriben en el mismo archivo o base de datos
- **Garantizar consistencia de datos**: Al actualizar estructuras de datos compartidas
- **Programación de trabajos**: Prevenir la ejecución duplicada de tareas programadas
- **Asignación de recursos**: Coordinar el acceso a recursos limitados

## Cómo Funciona Este Ejemplo

El ejemplo crea 5 hilos que todos intentan escribir en el mismo archivo (`shared_file.txt`). Los hilos se inician simultáneamente y compiten por el bloqueo del mutex. El mutex de Redis asegura que solo un hilo pueda escribir a la vez, demostrando un comportamiento verdaderamente concurrente donde el orden de adquisición es no determinista.

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

### Paso 3: Ejecutar los Ejemplos de Mutex

Ejecuta los scripts de Python:

**Ejemplo 1: Usando lock/unlock explícito**
```bash
python main.py
```

**Ejemplo 2: Usando el context manager acquire**
```bash
python main_acquire.py
```

Deberías ver una salida como:

```
[Thread 1] ✓ Done
[Thread 3] ✓ Done
[Thread 2] ✓ Done
[Thread 5] ✓ Done
[Thread 4] ✓ Done
```

El archivo `shared_file.txt` contendrá:

```
Thread 1 wrote this line
Thread 3 wrote this line
Thread 2 wrote this line
Thread 5 wrote this line
Thread 4 wrote this line
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

### Paso 3: Ejecutar los Ejemplos de Mutex

```bash
python main.py
# o
python main_acquire.py
```

## Entendiendo la Implementación del Mutex

### Características Clave

La clase `RedisMutex` hereda de `RedisClient` y proporciona:

#### 1. `lock(resource, wait_sec, retry_sec)` - Adquirir un bloqueo

```python
if mutex.lock("my_resource", wait_sec=10.0, retry_sec=0.5):
    # Bloqueo adquirido, hacer trabajo
    mutex.unlock("my_resource")
else:
    # No se pudo adquirir el bloqueo dentro del timeout
    print("Timeout adquiriendo bloqueo")
```

- **resource**: Nombre del recurso a bloquear (string)
- **wait_sec**: Tiempo máximo de espera para el bloqueo (por defecto: 10.0 segundos)
- **retry_sec**: Tiempo entre intentos de reintento (por defecto: 0.1 segundos)
- **Devuelve**: `True` si se adquiere el bloqueo, `False` si timeout

#### 2. `unlock(resource)` - Liberar el bloqueo

```python
mutex.unlock("my_resource")
```

Libera el bloqueo especificado. Debe proporcionar el nombre del recurso a desbloquear.

#### 3. `acquire(resource, wait_sec, retry_sec)` - Context Manager (Recomendado)

```python
try:
    with mutex.acquire("my_resource", wait_sec=5.0, retry_sec=0.5):
        # Sección crítica - solo un hilo puede estar aquí a la vez
        write_to_file("shared_file.txt", "data")
        # El bloqueo se libera automáticamente aquí
except LockAcquisitionError as e:
    print(f"No se pudo adquirir el bloqueo: {e}")
```

Este es el **enfoque recomendado** para el patrón lock/unlock porque asegura que el bloqueo siempre se libere, incluso si ocurre una excepción.

#### 4. Context Manager para Gestión de Conexión

```python
with RedisMutex() as mutex:
    # Usar mutex aquí
    # La conexión se cierra automáticamente al salir
```

### Cómo Funciona Internamente

1. **Herencia**: `RedisMutex` hereda de `RedisClient` y gestiona su propia conexión
2. **Adquisición de Bloqueo**: Usa el comando `SET` de Redis con la opción `NX` (set if Not eXists) - operación atómica
3. **Expiración**: Los bloqueos expiran automáticamente después de 30 segundos para prevenir deadlocks
4. **Lógica de Reintento**: Si no se puede adquirir el bloqueo, espera `retry_sec` y lo intenta de nuevo
5. **Timeout**: Si se excede `wait_sec`, devuelve `False` (para `lock()`) o lanza `LockAcquisitionError` (para `acquire()`)
6. **Limpieza de Recursos**: La conexión se cierra mediante el método `close()` o context manager

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
docker exec -it redis_mutex redis-cli -a redis123

# Ver bloqueos activos
KEYS lock:*

# Verificar si existe un bloqueo específico
GET lock:my_resource

# Eliminar manualmente un bloqueo (¡usar con precaución!)
DEL lock:my_resource

# Salir de Redis CLI
exit
```

## Ejemplos de Código

### Ejemplo 1: Usando lock/unlock explícito (main.py)

```python
import threading
import time
import random
from mutex import RedisMutex

def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"
    lock_acquired = False

    try:
        if not mutex.lock(resource, wait_sec=15.0, retry_sec=0.5):
            print(f"[Thread {thread_id}] X Unable to lock")
            return
        
        lock_acquired = True
        time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
        with open(filename, 'a') as f:
            f.write(f"Thread {thread_id} wrote this line\n")
        print(f"[Thread {thread_id}] ✓ Done")
    finally:
        if lock_acquired:
            mutex.unlock(resource)
        mutex.close()

def main():
    threads = []
    
    for i in range(5):
        thread = threading.Thread(target=write_to_file, args=[i + 1])
        threads.append(thread)
        thread.start() 
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

### Ejemplo 2: Usando context manager acquire (main_acquire.py)

```python
import threading
import time
import random
from mutex import RedisMutex, LockAcquisitionError

def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"

    try:
        with mutex.acquire(resource, wait_sec=15.0, retry_sec=0.5):
            time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
            with open(filename, 'a') as f:
                f.write(f"Thread {thread_id} wrote this line\n")
            print(f"[Thread {thread_id}] ✓ Done")
    except LockAcquisitionError:
        print(f"[Thread {thread_id}] X Unable to lock")
    finally:
        mutex.close()

def main():
    threads = []
    
    for i in range(5):
        thread = threading.Thread(target=write_to_file, args=[i + 1])
        threads.append(thread)
        thread.start() 
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

### Ejemplo 3: Usando RedisMutex como context manager

```python
from mutex import RedisMutex, LockAcquisitionError

def write_to_file(thread_id: int, filename: str):
    # Gestión de conexión con context manager
    with RedisMutex() as mutex:
        try:
            with mutex.acquire("file_write_lock", wait_sec=15.0):
                with open(filename, 'a') as f:
                    f.write(f"Thread {thread_id} writing\n")
        except LockAcquisitionError as e:
            print(f"Error: {e}")
    # La conexión se cierra automáticamente
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

### El Bloqueo Expira Inmediatamente

- Verifica que Redis está funcionando: `docker ps`
- Comprueba la conexión a Redis: `docker exec -it redis_mutex redis-cli -a redis123 PING`
- Asegúrate de que el archivo `.env` existe y tiene las credenciales correctas

### El Bloqueo Nunca se Libera

Si un bloqueo está atascado (ej. el proceso se bloqueó), puedes eliminarlo manualmente:

```bash
docker exec -it redis_mutex redis-cli -a redis123 DEL lock:nombre_recurso
```

## Limpieza

Para eliminar todo completamente:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de Redis (opcional)
docker rmi redis:7-alpine

# Eliminar el archivo compartido creado por el ejemplo
rm shared_file.txt
```

## Mejores Prácticas

1. **Usa context managers**: 
   - Usa `with RedisMutex() as mutex:` para gestión de conexión
   - Usa `with mutex.acquire():` para gestión de bloqueo
2. **Establece timeouts apropiados**: Equilibra entre demasiado corto (fallos falsos) y demasiado largo (mala experiencia de usuario)
3. **Maneja excepciones**: Siempre captura y maneja `LockAcquisitionError` graciosamente
4. **Mantén las secciones críticas cortas**: Minimiza el tiempo que mantienes un bloqueo
5. **Usa nombres de recursos descriptivos**: Deja claro qué protege cada bloqueo
6. **Cierra las conexiones explícitamente**: Llama a `mutex.close()` o usa context manager
7. **Monitorea la expiración de bloqueos**: La expiración por defecto de 30 segundos previene deadlocks pero puede ser demasiado corta para operaciones largas

## Decisiones de Diseño

### ¿Por qué `SET` con `NX` en lugar de `HSET`?

- **Operación atómica**: `SET` con `nx=True` solo crea la clave si no existe
- **Expiración automática**: `ex=30` previene bloqueos huérfanos si un proceso muere
- **Patrón oficial de Redis**: Recomendado por Redis para bloqueos distribuidos
- **Simple y eficiente**: Una sola operación, sin complejidad adicional

### ¿Por qué `lock()` devuelve `False` en lugar de lanzar una excepción?

- **Flexibilidad**: Permite diferentes estrategias de manejo de errores
- **Control de flujo explícito**: `if not mutex.lock()` es claro y legible
- **El context manager sí lanza excepción**: `acquire()` lanza `LockAcquisitionError` para un manejo de excepciones más limpio

### ¿Por qué `RedisMutex` hereda de `RedisClient`?

- **Encapsulación**: Cada mutex gestiona su propio ciclo de vida de conexión
- **Simplicidad**: No necesita pasar instancias de `RedisClient`
- **Thread-safe**: Cada hilo puede crear su propio mutex con conexión aislada

## Limitaciones y Consideraciones

- **Instancia única de Redis**: Este ejemplo usa una instancia única de Redis. Para producción, considera Redis Cluster o Redis Sentinel para alta disponibilidad
- **Expiración de bloqueos**: Los bloqueos expiran después de 30 segundos para prevenir deadlocks. Ajusta esto según tus necesidades
- **No adecuado para muy alto rendimiento**: Si necesitas miles de operaciones de bloqueo por segundo, considera otras soluciones
- **Dependencia de red**: La fiabilidad del mutex depende de la estabilidad de la red
- **Múltiples conexiones**: Cada instancia de `RedisMutex` crea su propia conexión (usa connection pooling de Redis internamente)

## Próximos Pasos

- Implementar renovación de bloqueos para operaciones de larga duración
- Añadir semáforos distribuidos (permitir N accesos concurrentes)
- Implementar bloqueos de lectura/escritura
- Añadir verificación de propiedad de bloqueos con identificadores únicos
- Explorar el algoritmo RedLock de Redis para configuraciones multi-nodo
- Añadir métricas y monitoreo para contención de bloqueos
- Implementar pool de conexiones compartido para escenarios de alto rendimiento

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
