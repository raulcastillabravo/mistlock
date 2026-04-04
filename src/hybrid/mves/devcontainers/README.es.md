# Ejemplo de DevContainers con Docker

Ejemplo mínimo viable para entender cómo funcionan los DevContainers con Docker, Python y VS Code. Este ejemplo demuestra los conceptos clave y componentes de DevContainers a través de una aplicación simple con pandas DataFrame.

## ¿Qué son los DevContainers?

**DevContainers** (Contenedores de Desarrollo) son una característica de VS Code que te permite usar un contenedor Docker como un entorno de desarrollo completo. En lugar de instalar dependencias, herramientas y extensiones en tu máquina local, todo se ejecuta dentro de un entorno contenedorizado.

### Beneficios Clave

- **Consistencia**: Todo el equipo usa exactamente el mismo entorno de desarrollo
- **Aislamiento**: Las dependencias del proyecto no entran en conflicto con tu sistema local
- **Reproducibilidad**: Los nuevos miembros del equipo pueden empezar a programar en minutos
- **Portabilidad**: Tu entorno de desarrollo viaja con tu código

## Estructura del Proyecto

```
devcontainers-docker/
├── .devcontainer/
│   └── devcontainer.json       # Configuración del DevContainer
├── .vscode/
│   └── settings.json           # Configuración de VS Code
├── .env                        # Variables de entorno
├── main.py                     # Script principal de Python
├── pyproject.toml              # Dependencias de Python
├── uv.lock                     # Archivo de bloqueo de dependencias (auto-generado)
├── README.md                   # Versión en inglés
└── README.es.md                # Este archivo
```

## Requisitos Previos

- **Docker** instalado y en ejecución
- **VS Code** con la extensión **Dev Containers** instalada

## Cómo Usar Este Ejemplo

### Paso 1: Abrir el Proyecto en Dev Container

1. Abre VS Code en la carpeta de este proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

**Qué sucede detrás de escena:**
- Docker descarga la imagen base de Python
- Se instala la feature de AWS CLI
- Se instala la extensión Git History en el contenedor
- El `postCreateCommand` se ejecuta para instalar dependencias con `uv`

### Paso 2: Ejecutar el Ejemplo

Una vez dentro del contenedor, abre una terminal y ejecuta:

```bash
python main.py
```

Deberías ver una salida como:

```
Environment variable EXAMPLE_VAR: devcontainer-example

Creating a pandas DataFrame...

DataFrame created successfully!

DataFrame contents:
      Name  Age           City
0    Alice   25       New York
1      Bob   30  San Francisco
2  Charlie   35   Los Angeles
3    Diana   28        Chicago

DataFrame info:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   Name    4 non-null      object
 1   Age     4 non-null      int64 
 2   City    4 non-null      object
dtypes: int64(1), object(2)
memory usage: 224.0+ bytes
None

DataFrame statistics:
             Age
count   4.000000
mean   29.500000
std     4.203173
min    25.000000
25%    27.250000
50%    29.000000
75%    31.250000
max    35.000000
```

### Paso 3: Verificar la Instalación de AWS CLI

El DevContainer incluye la feature de AWS CLI. Verifica que esté instalado:

```bash
aws --version
```

Deberías ver una salida como:

```
aws-cli/2.x.x Python/3.x.x Linux/x.x.x
```

### Paso 4: Explorar la Extensión Git History

La extensión **Git History** se instala automáticamente en el contenedor. Puedes:

1. Hacer clic derecho en cualquier archivo en VS Code
2. Seleccionar **Git: View File History**
3. Navegar visualmente por el historial de commits

## Configuración del DevContainer Explicada

### El Archivo `devcontainer.json`

Este es el corazón de los DevContainers. Analicemos cada sección:

```json
{
  "name": "DevContainers Python Example",
  "image": "mcr.microsoft.com/devcontainers/python:3.12-bookworm",
  "features": {
    "ghcr.io/devcontainers/features/aws-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "donjayamanne.githistory"
      ]
    }
  },
  "postCreateCommand": "pip3 install uv && uv sync"
}
```

#### 1. **`name`** - Nombre del Contenedor

```json
"name": "DevContainers Python Example"
```

El nombre de visualización para tu DevContainer. Aparece en la barra de estado de VS Code cuando estás conectado al contenedor.

#### 2. **`image`** - Imagen Base del Contenedor

```json
"image": "mcr.microsoft.com/devcontainers/python:3.12-bookworm"
```

**Qué hace**: Especifica la imagen de Docker a usar como base para tu entorno de desarrollo.

**En este ejemplo**: Usamos la imagen oficial de DevContainer de Python 3.12 de Microsoft basada en Debian Bullseye.

**Alternativas**:
- Usar un `Dockerfile` en su lugar: `"dockerFile": "Dockerfile"`
- Usar `docker-compose.yml`: `"dockerComposeFile": "docker-compose.yml"`

#### 3. **`features`** - Herramientas y Capacidades Adicionales

```json
"features": {
  "ghcr.io/devcontainers/features/aws-cli:1": {}
}
```

**¿Qué son las features?**: Las features son unidades autocontenidas y compartibles de código de instalación que agregan herramientas, runtimes o librerías a tu DevContainer.

**En este ejemplo**: Instalamos la feature de AWS CLI, que agrega la interfaz de línea de comandos de AWS a nuestro contenedor.

**Features populares**:
- `ghcr.io/devcontainers/features/docker-outside-of-docker:1` - Docker CLI
- `ghcr.io/devcontainers/features/node:1` - Node.js
- `ghcr.io/devcontainers/features/git:1` - Git
- `ghcr.io/devcontainers/features/terraform:1` - Terraform

**Dónde encontrar features**: [https://containers.dev/features](https://containers.dev/features)

#### 4. **`customizations`** - Extensiones de VS Code

```json
"customizations": {
  "vscode": {
    "extensions": [
      "donjayamanne.githistory"
    ]
  }
}
```

**Qué hace**: Instala automáticamente extensiones de VS Code dentro del DevContainer.

**En este ejemplo**: Instalamos la extensión **Git History** (`donjayamanne.githistory`), que proporciona una interfaz visual para ver el historial de commits de Git.

**Por qué es importante**: Las extensiones instaladas en el contenedor están aisladas de tu instalación local de VS Code. Esto asegura que todos en el equipo tengan las mismas herramientas de desarrollo.

**Cómo encontrar IDs de extensiones**:
1. Abre el panel de Extensiones de VS Code
2. Haz clic en una extensión
3. Busca el ID (ej., `donjayamanne.githistory`)

#### 5. **`postCreateCommand`** - Script Post-Instalación

```json
"postCreateCommand": "pip3 install uv && uv sync"
```

**Qué hace**: Ejecuta un comando después de que el contenedor se crea pero antes de que comiences a trabajar.

**En este ejemplo**: 
1. `pip3 install uv` - Instala `uv`, un instalador rápido de paquetes Python
2. `uv sync` - Instala todas las dependencias desde `pyproject.toml`

**Otros casos de uso**:
- Instalar paquetes del sistema: `"apt-get update && apt-get install -y git"`
- Ejecutar migraciones de base de datos: `"python manage.py migrate"`
- Construir el proyecto: `"npm install && npm run build"`

**Alternativas**:
- `postStartCommand` - Se ejecuta cada vez que el contenedor inicia
- `postAttachCommand` - Se ejecuta cuando te conectas al contenedor
- `initializeCommand` - Se ejecuta en la máquina host antes de crear el contenedor

## Dependencias de Python con `uv`

### ¿Qué es `uv`?

`uv` es un instalador y resolvedor de paquetes Python moderno y rápido escrito en Rust. Es significativamente más rápido que `pip` y proporciona mejor resolución de dependencias.

### El Archivo `pyproject.toml`

```toml
[project]
name = "devcontainers-docker"
version = "0.1.0"
description = "Minimal viable example to understand DevContainers with Python and pandas"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pandas",
    "python-dotenv",
]
```

**Secciones clave**:
- **`name`**: Nombre del proyecto
- **`dependencies`**: Paquetes Python requeridos para el proyecto
- **`requires-python`**: Versión mínima de Python

### Gestión de Dependencias

```bash
# Instalar todas las dependencias
uv sync

# Agregar una nueva dependencia
uv add numpy

# Actualizar dependencias
uv lock --upgrade
```

## Script Principal Explicado

El archivo `main.py` demuestra una operación simple con pandas y carga de variables de entorno:

```python
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Load environment variable
EXAMPLE_VAR = os.getenv("EXAMPLE_VAR", "default-value")

def main():
    print(f"Environment variable EXAMPLE_VAR: {EXAMPLE_VAR}\n")
    print("Creating a pandas DataFrame...")
    
    # Create a simple DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
    }
    
    df = pd.DataFrame(data)
    
    print("\nDataFrame created successfully!")
    print("\nDataFrame contents:")
    print(df)
```

**Propósito**: Este script simple verifica que:
1. Python está funcionando correctamente
2. Las dependencias (pandas, python-dotenv) están instaladas
3. Las variables de entorno se cargan desde `.env`
4. El entorno de desarrollo está completamente funcional

## Variables de Entorno

El archivo `.env` contiene variables de entorno:

```
EXAMPLE_VAR=devcontainer-example
```

**Uso**: El script `main.py` carga esta variable usando `python-dotenv` y la muestra al inicio de la ejecución. Esto demuestra cómo gestionar la configuración a través de variables de entorno en tus proyectos DevContainer.

## Comandos Útiles

### Comandos de DevContainer

```bash
# Reconstruir contenedor (si cambias devcontainer.json)
# Presiona F1 → "Dev Containers: Rebuild Container"

# Cerrar contenedor y volver a local
# Presiona F1 → "Dev Containers: Reopen Folder Locally"

# Ver logs del contenedor
# Presiona F1 → "Dev Containers: Show Container Log"
```

### Comandos de Python

```bash
# Ejecutar el script principal
python main.py

# Instalar dependencias
uv sync

# Agregar un nuevo paquete
uv add requests

# Verificar versión de Python
python --version
```

### Comandos de AWS CLI

```bash
# Verificar versión de AWS CLI
aws --version

# Configurar credenciales de AWS (ejemplo)
aws configure

# Listar buckets de S3 (si está configurado)
aws s3 ls
```

## Cómo Funcionan los DevContainers: Bajo el Capó

1. **Creación del Contenedor**: Cuando abres el proyecto en un DevContainer, VS Code:
   - Lee `.devcontainer/devcontainer.json`
   - Descarga la imagen de Docker especificada
   - Crea un contenedor Docker desde esa imagen

2. **Instalación de Features**: VS Code instala cualquier feature especificada (como AWS CLI) en el contenedor

3. **Instalación de Extensiones**: VS Code instala las extensiones especificadas dentro del contenedor

4. **Comando Post-Creación**: VS Code ejecuta el `postCreateCommand` para configurar dependencias

5. **Conexión**: VS Code se conecta al contenedor y abre una sesión remota

6. **Desarrollo**: Programas dentro del contenedor, pero VS Code se ejecuta en tu máquina local

## Solución de Problemas

### El Contenedor No Inicia

**Problema**: El DevContainer falla al construirse o iniciar.

**Solución**:
1. Verifica que Docker esté ejecutándose: `docker ps`
2. Ver logs del contenedor: Presiona `F1` → "Dev Containers: Show Container Log"
3. Reconstruir contenedor: Presiona `F1` → "Dev Containers: Rebuild Container"

### Las Dependencias No Se Instalan

**Problema**: `postCreateCommand` falla o faltan paquetes.

**Solución**:
1. Ejecuta manualmente dentro del contenedor:
   ```bash
   pip3 install uv && uv sync
   ```
2. Verifica errores de sintaxis en `pyproject.toml`

### La Extensión No Funciona

**Problema**: Git History u otras extensiones no aparecen.

**Solución**:
1. Verifica que el ID de la extensión sea correcto en `devcontainer.json`
2. Reconstruye el contenedor: Presiona `F1` → "Dev Containers: Rebuild Container"

### Puerto Ya En Uso

**Problema**: Si necesitas exponer puertos y ya están en uso.

**Solución**: Agrega `forwardPorts` a `devcontainer.json`:
```json
"forwardPorts": [8000, 3000]
```

## Características Avanzadas de DevContainer

### Ejecutar Docker Dentro del DevContainer

Si necesitas Docker dentro de tu DevContainer, agrega la feature Docker-in-Docker:

```json
"features": {
  "ghcr.io/devcontainers/features/docker-in-docker:1": {}
}
```

### Montar Carpetas Locales

Para montar carpetas adicionales desde tu máquina host:

```json
"mounts": [
  "source=/ruta/en/host,target=/ruta/en/contenedor,type=bind"
]
```

### Variables de Entorno en DevContainer

Establecer variables de entorno directamente en `devcontainer.json`:

```json
"containerEnv": {
  "MI_VARIABLE": "valor"
}
```

### Usar Docker Compose

Para configuraciones complejas con múltiples servicios:

```json
"dockerComposeFile": "docker-compose.yml",
"service": "app",
"workspaceFolder": "/workspace"
```

## Mejores Prácticas

1. **Mantenlo Simple**: Comienza con una configuración básica y agrega complejidad según sea necesario
2. **Documenta Features**: Explica por qué se necesita cada feature o extensión
3. **Usa Imágenes Oficiales**: Prefiere las imágenes DevContainer de Microsoft para mayor confiabilidad
4. **Control de Versiones**: Haz commit de `.devcontainer/` en Git para que todos usen la misma configuración
5. **Prueba Regularmente**: Reconstruye contenedores periódicamente para detectar problemas temprano

## Próximos Pasos

- Agregar más features (Node.js, Terraform, etc.)
- Crear un Dockerfile personalizado para más control
- Usar Docker Compose para configuraciones multi-contenedor
- Agregar servicios de base de datos (PostgreSQL, MongoDB, etc.)
- Implementar pruebas automatizadas en el DevContainer

## Recursos

- **Documentación de DevContainers**: [https://containers.dev/](https://containers.dev/)
- **VS Code DevContainers**: [https://code.visualstudio.com/docs/devcontainers/containers](https://code.visualstudio.com/docs/devcontainers/containers)
- **Features de DevContainer**: [https://containers.dev/features](https://containers.dev/features)
- **Imágenes de DevContainer**: [https://github.com/devcontainers/images](https://github.com/devcontainers/images)

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
