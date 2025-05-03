# Planificación del Proyecto: whisper-query-parser

## Visión General
Este proyecto tiene como objetivo crear una aplicación que convierta voz en texto utilizando el modelo Whisper de OpenAI y, en su segunda versión, procese ese texto mediante un modelo de lenguaje como Gemini para generar consultas estructuradas. La aplicación se desarrollará en dos fases principales:

1. **Fase 1:** Transcripción básica de voz a texto usando Whisper
2. **Fase 2:** Procesamiento del texto transcrito mediante un LM (Gemini) para generar consultas estructuradas

## Arquitectura

### Componentes Principales
1. **Interfaz de Usuario**: Interfaz basada en Gradio para subir/grabar archivos de audio.
2. **Motor de Transcripción**: Implementación de Whisper para convertir voz a texto.
3. **Preprocesamiento de Audio**: Módulos para manipular y preparar los archivos de audio.
4. **Procesador de Lenguaje** (Fase 2): Integración con Gemini u otro LM para interpretar el texto y generar consultas estructuradas.
5. **Exportación de Resultados**: Métodos para guardar y exportar tanto las transcripciones como las consultas generadas.

### Flujo de Datos
**Fase 1:**
```
Entrada de Audio → Preprocesamiento → Transcripción con Whisper → Texto Transcrito → Exportación
```

**Fase 2:**
```
Entrada de Audio → Preprocesamiento → Transcripción con Whisper → Texto Transcrito → Procesamiento con LM (Gemini) → Consulta Estructurada → Exportación
```

## Restricciones y Consideraciones
- **Fase 1:** La aplicación se enfocará exclusivamente en la transcripción de voz a texto con Whisper.
- **Fase 2:** Se integrará Gemini u otro LM para procesar el texto transcrito y generar consultas estructuradas.
- La integración con la base de datos será implementada en un proyecto separado.
- Se debe priorizar una interfaz fácil de usar y una configuración sencilla.
- El rendimiento es importante para transcripciones en tiempo real o con archivos grandes.
- La interfaz debe permitir visualizar tanto el texto transcrito como la consulta estructurada generada (en la Fase 2).

## Stack Tecnológico

### Lenguajes y Frameworks
- **Python**: Lenguaje principal para el desarrollo.
- **Gradio**: Para la interfaz de usuario interactiva.

### Librerías y Herramientas
- **OpenAI Whisper**: Motor principal para la transcripción de voz a texto.
- **PyTorch**: Como dependencia de Whisper.
- **FFmpeg**: Para el procesamiento de audio.
- **Librosa/PyDub**: Para manipulación y análisis de audio.
- **NumPy**: Para operaciones con arrays y procesamiento numérico.
- **Google Generative AI** (Fase 2): Cliente de Python para Gemini.
- **Langchain** (Opcional, Fase 2): Para estructurar prompts e interacciones con Gemini.
- **JSON/YAML**: Para estructurar y exportar las consultas generadas.

### Entorno de Desarrollo
- **Virtualenv/Conda**: Para gestionar el entorno virtual y dependencias.
- **Git**: Para control de versiones.
- **VSCode/PyCharm**: IDE recomendado.

## Modelos de Whisper a Considerar
- **whisper-tiny**: Para pruebas rápidas y desarrollo.
- **whisper-base**: Balance entre rendimiento y precisión.
- **whisper-small/medium**: Para mayor precisión en producción.
- **whisper-large**: Para máxima precisión (requiere más recursos).

## Estructura del Proyecto
```
whisper-query-parser/
├── app.py              # Punto de entrada de la aplicación
├── requirements.txt    # Dependencias del proyecto
├── README.md           # Documentación
├── PLANNING.md         # Este archivo
├── TASK.md             # Seguimiento de tareas
├── models/             # Modelos pre-entrenados o configuraciones
├── utils/              # Funciones auxiliares
│   ├── audio_processing.py  # Procesamiento de audio
│   ├── transcription.py     # Funciones de transcripción
│   └── query_generation.py  # Procesamiento LM para generar consultas (Fase 2)
├── configs/            # Archivos de configuración
│   └── prompt_templates/    # Templates para Gemini (Fase 2)
├── tests/              # Pruebas unitarias
└── examples/           # Ejemplos de consultas y resultados
```

## Referencias
- [Repositorio de ejemplo 1](https://github.com/EnkrateiaLucca/audio_transcription_app_version_2)
- [Repositorio de ejemplo 2](https://github.com/xAlpharax/whisper-stt-gradio)
- [Documentación de Whisper OpenAI](https://github.com/openai/whisper)
- [Documentación de Gradio](https://www.gradio.app/docs/)

## Plan de Desarrollo por Fases

### Fase 1: Transcripción de Voz a Texto
- Implementar la funcionalidad básica de transcripción con Whisper
- Desarrollar la interfaz de usuario con Gradio
- Implementar la carga de archivos y grabación de audio
- Optimizar el rendimiento de la transcripción

### Fase 2: Generación de Consultas Estructuradas
- Integrar el cliente de Gemini
- Desarrollar los prompts y templates para procesar las transcripciones
- Añadir funcionalidad para extraer entidades y relaciones del texto
- Implementar la generación de consultas estructuradas
- Expandir la interfaz para mostrar tanto la transcripción como la consulta generada

## Próximos Pasos
Consultar TASK.md para ver las tareas actuales y el progreso del proyecto.