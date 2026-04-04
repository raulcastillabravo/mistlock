# Ejemplo de Google Cloud Functions + Firebase Emulator

Ejemplo mínimo viable para trabajar con Google Cloud Functions localmente usando Firebase Emulator Suite y Python. Este ejemplo demuestra cómo crear una función activada por HTTP que sube archivos a Cloud Storage.

## Estructura del Proyecto

```
gcp-functions/
├── functions/
│   ├── main.py
│   └── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── firebase.json
├── .firebaserc
├── storage.rules
├── .env
├── test_function.py
├── pyproject.toml
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración con dev container)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

El dev container incluye:
- **Python 3.12** para scripts de prueba
- **Node.js 18** para Firebase CLI
- **Java 17** requerido por Firebase Emulator Suite
- **Firebase Tools** (instalado automáticamente)
- **Extensión VSFire** para integración con Firebase

### Paso 2: Configurar el Entorno Virtual de Functions

Firebase requiere un entorno virtual llamado `venv` dentro del directorio `functions` para cargar tu código:

```bash
python3.12 -m venv functions/venv && functions/venv/bin/pip install -r functions/requirements.txt
```

### Paso 3: Iniciar los Emuladores de Firebase

Dentro del terminal del dev container:

```bash
firebase emulators:start
```

Deberías ver una salida como:

```
┌─────────────────────────────────────────────────────────────┐
│ ✔  All emulators ready! It is now safe to connect your app. │
│ i  View Emulator UI at http://localhost:4000                │
└─────────────────────────────────────────────────────────────┘

┌───────────┬────────────────┬─────────────────────────────────┐
│ Emulator  │ Host:Port      │ View in Emulator UI             │
├───────────┼────────────────┼─────────────────────────────────┤
│ Functions │ localhost:5001 │ http://localhost:4000/functions │
│ Storage   │ localhost:9199 │ http://localhost:4000/storage   │
└───────────┴────────────────┴─────────────────────────────────┘
```

### Paso 4: Ver la UI del Emulador

Abre tu navegador y navega a:

```
http://localhost:4000
```

La UI del Emulador de Firebase proporciona:
- **Pestaña Functions**: Ver funciones desplegadas y sus logs
- **Pestaña Storage**: Navegar archivos subidos
- **Pestaña Logs**: Logs de ejecución de funciones en tiempo real

### Paso 5: Probar la Función

Abre un nuevo terminal (mantén el emulador ejecutándose) y ejecuta:

```bash
python test_function.py
```

Deberías ver una salida como:

```
Testing Firebase Cloud Function...
Function URL: http://localhost:5001/demo-project/us-central1/upload_file

Uploading 'test.txt'...
Status: 200
Response: File 'test.txt' uploaded to 'demo-bucket'

Check the Firebase Emulator UI at http://localhost:4000
```

### Paso 6: Verificar la Subida en la UI del Emulador

1. Ve a `http://localhost:4000`
2. Haz clic en la pestaña **Storage**
3. Deberías ver `demo-bucket` con `test.txt` dentro
4. Haz clic en la pestaña **Functions** para ver los logs de ejecución

### Paso 7: Probar con curl

También puedes probar la función directamente con curl:

```bash
curl -X POST http://localhost:5001/demo-project/us-central1/upload_file \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "hola.txt",
    "content": "¡Hola desde curl!"
  }'
```

Respuesta esperada:

```
File 'hola.txt' uploaded to 'demo-bucket'
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Requisitos Previos

**Instalar Node.js 18+:**
- Descarga desde [nodejs.org](https://nodejs.org/)

**Instalar Java 17+:**
- Descarga desde [adoptium.net](https://adoptium.net/)

**Instalar Firebase CLI:**

```bash
npm install -g firebase-tools
```

**Instalar Dependencias de Python:**

```bash
pip3 install uv && uv sync
```

### Paso 2: Configurar el Entorno Virtual de Functions

Firebase requiere un entorno virtual llamado `venv` dentro del directorio `functions`:

```bash
python3.12 -m venv functions/venv && functions/venv/bin/pip install -r functions/requirements.txt
```

### Paso 3: Iniciar los Emuladores de Firebase

```bash
firebase emulators:start
```

Deberías ver una salida como:

```
┌─────────────────────────────────────────────────────────────┐
│ ✔  All emulators ready! It is now safe to connect your app. │
│ i  View Emulator UI at http://localhost:4000                │
└─────────────────────────────────────────────────────────────┘

┌───────────┬────────────────┬─────────────────────────────────┐
│ Emulator  │ Host:Port      │ View in Emulator UI             │
├───────────┼────────────────┼─────────────────────────────────┤
│ Functions │ localhost:5001 │ http://localhost:4000/functions │
│ Storage   │ localhost:9199 │ http://localhost:4000/storage   │
└───────────┴────────────────┴─────────────────────────────────┘
```

### Paso 4: Probar la Función

Abre un nuevo terminal y ejecuta:

```bash
python test_function.py
```

## Componentes del Proyecto

### Cloud Function (`functions/main.py`)

Función Cloud activada por HTTP que sube archivos a Cloud Storage:

- **`@https_fn.on_request()`**: Decorador que define una función activada por HTTP
- **`upload_file(req)`**: Función manejadora que:
  - Valida el método de la petición (solo POST)
  - Extrae `filename` y `content` del cuerpo JSON
  - Sube el contenido a Cloud Storage usando el cliente `google-cloud-storage`
  - Retorna una respuesta de éxito (los errores son gestionados por el framework)

### Dependencias de la Función (`functions/requirements.txt`)

Paquetes Python requeridos por la Cloud Function:

- **`firebase-functions`**: SDK de Firebase Functions para Python
- **`google-cloud-storage`**: Librería cliente de Google Cloud Storage

### Configuración de Firebase (`firebase.json`)

Configuración del emulador:

- **`functions.port`**: Puerto 5001 para Cloud Functions
- **`storage.port`**: Puerto 9199 para Cloud Storage
- **`ui.port`**: Puerto 4000 para la UI del Emulador
- **`functions.source`**: Apunta al directorio `functions/`
- **`storage.rules`**: Referencia al archivo de reglas de seguridad

### Configuración del Proyecto (`.firebaserc`)

Define el ID del proyecto Firebase para emulación local:

- **`projects.default`**: Establecido a `demo-project` para desarrollo local

### Reglas de Storage (`storage.rules`)

Reglas de seguridad para Cloud Storage:

- Permite todas las operaciones de lectura/escritura para desarrollo local
- En producción, estas deberían restringirse basándose en autenticación

### Script de Prueba (`test_function.py`)

Script de demostración que invoca la Cloud Function:

- Carga variables de entorno desde `.env`
- Construye la URL de la función usando el ID del proyecto y región
- Envía petición POST con payload JSON
- Muestra la respuesta y recuerda revisar la UI del Emulador

## Variables de Entorno

El archivo `.env` contiene:

```
FIREBASE_PROJECT_ID=demo-project
STORAGE_BUCKET=demo-bucket
REGION=us-central1

# Emulator Endpoints
FUNCTIONS_EMULATOR_HOST=localhost:5001
STORAGE_EMULATOR_HOST=localhost:9199
FIRESTORE_EMULATOR_HOST=localhost:8080
```

**Nota**: Estos son valores de desarrollo local. El emulador usa automáticamente estos endpoints.

## Comandos Útiles

### Comandos de Firebase CLI

```bash
# Iniciar todos los emuladores
firebase emulators:start

# Iniciar emuladores específicos
firebase emulators:start --only functions,storage

# Iniciar con importación/exportación de datos
firebase emulators:start --import=./emulator-data --export-on-exit

# Ver estado del emulador
firebase emulators:exec "echo 'Emuladores ejecutándose'"
```

### Comandos de Prueba

```bash
# Ejecutar script de prueba
python test_function.py

# Probar con curl
curl -X POST http://localhost:5001/demo-project/us-central1/upload_file \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.txt", "content": "¡Hola!"}'
```

## Solución de Problemas

### Puerto Ya en Uso

Si los puertos 4000, 5001 o 9199 ya están en uso, modifica `firebase.json`:

```json
{
  "emulators": {
    "functions": { "port": 5002 },
    "storage": { "port": 9200 },
    "ui": { "port": 4001 }
  }
}
```

Luego actualiza `.env` en consecuencia.

### Java No Encontrado

Firebase Emulator Suite requiere Java 17+. Instálalo:

**Ubuntu/Debian:**
```bash
sudo apt-get install openjdk-17-jdk
```

**macOS:**
```bash
brew install openjdk@17
```

**Windows:**
Descarga desde [adoptium.net](https://adoptium.net/)

### Función No Encontrada

Si la función no aparece:

1. Verifica que `functions/main.py` existe
2. Revisa que `firebase.json` tiene la ruta correcta en `functions.source`
3. Asegúrate de que `functions/requirements.txt` está presente
4. Reinicia el emulador

### Errores de Importación en la Función

Si obtienes errores de importación cuando la función se ejecuta:

1. Verifica que `functions/requirements.txt` incluye todas las dependencias
2. El emulador instala automáticamente las dependencias en la primera ejecución
3. Elimina `functions/__pycache__` y reinicia el emulador

### Conexión Rechazada

Asegúrate de que el emulador está ejecutándose:

```bash
firebase emulators:start
```

Revisa la salida para cualquier error durante el inicio.

## Limpieza

Para detener los emuladores:

```bash
# Presiona Ctrl+C en el terminal que ejecuta el emulador
```

Para limpiar los datos del emulador:

```bash
# Elimina el directorio de datos del emulador
rm -rf .firebase
```

## Próximos Pasos

- Agregar más tipos de triggers (Pub/Sub, Firestore, Storage triggers)
- Implementar autenticación y autorización
- Agregar pruebas unitarias para las funciones
- Desplegar a Google Cloud Functions
- Integrar con otros servicios de Firebase (Firestore, Auth)

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
