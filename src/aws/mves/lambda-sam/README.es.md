# [Título del Proyecto]

Ejemplo mínimo viable para trabajar con **[Nombre del Servicio]** usando **[Tecnologías]**. Este ejemplo demuestra [propósito del MVE].

## Arquitectura

```mermaid
architecture-beta
    group api(cloud)[Cloud]
    
    service app(server)[Aplicación] in api
    service db(database)[Nombre del Servicio] in api
    
    db:L -- R:app
```

[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Índice

- [Prerrequisitos](#prerrequisitos)
- [Quickstart](#quickstart)
- [Configurar el Entorno](#configurar-el-entorno)
- [Iniciar Infraestructura](#iniciar-infraestructura)
- [Cómo ejecutar](#cómo-ejecutar)
- [Cómo depurar](#cómo-depurar)
- [Cómo probar](#cómo-probar)
- [Validar resultados](#validar-resultados)
- [Limpieza](#limpieza)

## Prerrequisitos

- [Docker](https://www.docker.com/get-started) instalado y en ejecución.
- Extensión [Dev Containers](vscode:extension/ms-vscode-remote.remote-containers) instalada.

## Quickstart

1. **Abrir en Contenedor**: Abre VS Code en la carpeta del proyecto y selecciona **Dev Containers: Reopen in Container** desde la Paleta de Comandos (`F1`).
2. **Ejecutar el Ejemplo**:
   ```bash
   python main.py
   ```

💡 **Próximos Pasos**: Consulta las secciones de [Cómo depurar](#cómo-depurar), [Cómo probar](#cómo-probar), [Validar resultados](#validar-resultados) y [Limpieza](#limpieza) a continuación.

## Configurar el Entorno

Instala las dependencias y herramientas del sistema usando mise:
```bash
scripts/setup.sh
```

## Iniciar Infraestructura

Lanza los contenedores necesarios:
```bash
docker compose up -d
```

## Cómo ejecutar

### Usando python

Ejecuta el script de demostración:
```bash
python main.py
```

## Cómo depurar

### El cliente main.py

1. Abre `main.py`.
2. Establece puntos de interrupción en el código.
3. Presiona `F5` para iniciar la depuración.

## Cómo probar

### Todas las pruebas

Ejecuta la suite de pruebas automatizadas:
```bash
scripts/run_tests.sh
```

## Validar resultados

Explica cómo verificar que el ejemplo funciona correctamente.

1. **[Paso de Validación 1]**: Instrucciones.
2. **[Paso de Validación 2]**: Instrucciones.

### Detalles de Conexión
- **Servidor**: `localhost`
- **Puerto**: `[puerto]`
- **Usuario**: `[usuario]`
- **Contraseña**: `[contraseña]`

## Limpieza

Para detener todos los servicios y eliminar el estado:
```bash
docker compose down -v
```
