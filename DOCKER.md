# Usar whisper-query-parser con Docker

Este documento explica cómo ejecutar la API de whisper-query-parser usando Docker, lo que te permite ejecutarla fácilmente en cualquier sistema que soporte Docker.

## Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (opcional pero recomendado)

## Opciones de despliegue

### Opción 1: Usando Docker Compose (recomendado)

1. Clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd whisper-query-parser
   ```

2. (Opcional) Configura tu clave de API de Google para Gemini:
   - Edita el archivo `docker-compose.yml`
   - Descomenta y establece la variable `GOOGLE_API_KEY`

3. Inicia la aplicación:
   ```bash
   docker-compose up -d
   ```

4. Accede a la API:
   - La API estará disponible en `http://localhost:8000`
   - Documentación: `http://localhost:8000/docs`

5. Para detener la aplicación:
   ```bash
   docker-compose down
   ```

### Opción 2: Usando Docker directamente

1. Clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd whisper-query-parser
   ```

2. Construye la imagen Docker:
   ```bash
   docker build -t whisper-query-parser .
   ```

3. Ejecuta el contenedor:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/exports:/app/exports \
     --name whisper-query-parser-api \
     whisper-query-parser
   ```

4. (Opcional) Para habilitar la generación de consultas con Gemini, incluye tu clave de API:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/exports:/app/exports \
     -e GOOGLE_API_KEY=tu_clave_de_api_gemini \
     --name whisper-query-parser-api \
     whisper-query-parser
   ```

5. Accede a la API:
   - La API estará disponible en `http://localhost:8000`
   - Documentación: `http://localhost:8000/docs`

6. Para detener el contenedor:
   ```bash
   docker stop whisper-query-parser-api
   docker rm whisper-query-parser-api
   ```

## Personalización

Puedes personalizar el comportamiento de la API mediante variables de entorno:

- `WHISPER_MODEL`: Modelo de Whisper a utilizar (tiny, base, small, medium, large)
- `DEFAULT_LANGUAGE`: Idioma predeterminado para transcripciones (auto-detect, en, es, etc.)
- `EXPORT_DIR`: Directorio donde se guardan las exportaciones
- `GOOGLE_API_KEY`: Clave de API de Google para habilitar la generación de consultas con Gemini

Ejemplo con configuración personalizada:
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/exports:/app/exports \
  -e WHISPER_MODEL=medium \
  -e DEFAULT_LANGUAGE=es \
  -e GOOGLE_API_KEY=tu_clave_de_api_gemini \
  --name whisper-query-parser-api \
  whisper-query-parser
```

## Endpoints principales

- `GET /`: Información básica sobre la API
- `GET /health`: Verificación de estado
- `POST /transcribe`: Transcripción de audio
- `POST /generate-query`: Generación de consulta estructurada a partir de texto
- `POST /process`: Proceso completo (transcripción + generación de consulta)

Para más detalles, consulta la documentación completa en `http://localhost:8000/docs`

## Volúmenes

El contenedor utiliza un volumen para persistir las exportaciones en `./exports`. Puedes modificar la ruta de montaje según tus necesidades. 