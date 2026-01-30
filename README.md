Technical Data Processing Pipeline (Azure)

<ESPAÑOL>

Descripción General

Este repositorio presenta un proyecto demostrativo de procesamiento técnico de datos, desarrollado utilizando servicios de Microsoft Azure, inspirado en una solución cloud implementada durante mi práctica profesional.

El objetivo del proyecto es mostrar el diseño y ejecución de un flujo ETL completo (ingesta, validación, transformación y carga de datos), siguiendo principios utilizados en entornos productivos de procesamiento de datos de alta complejidad.

El proyecto está orientado a demostrar competencias en:

- Procesamiento estructurado de datos
- Diseño de flujos y protocolos de trabajo
- Control de calidad de información
- Uso práctico de servicios cloud


Arquitectura General

El flujo del proyecto sigue una arquitectura modular, inspirada en entornos cloud reales:

- Proveedor Cloud: Microsoft Azure
- Storage: Azure Blob Storage
- Lenguaje: Python 3.11
- Formato de datos: CSV
- Pipeline: ETL (Extract – Transform – Load)

Azure Blob Storage (raw)
        ↓
   ingest.py
        ↓
 quality_checks.py
        ↓
 transform.py
        ↓
Azure Blob Storage (processed)


Flujo de Procesamiento

Ingesta:
Lectura de archivos CSV desde contenedor raw en Azure Blob Storage.

Validación de Calidad:
Controles básicos de integridad, estructura y valores críticos antes de continuar el pipeline.

Transformación:
Normalización de columnas, conversión de tipos y preparación de la data para análisis.

Carga:
Escritura del dataset procesado en contenedor processed.

La ejecución del flujo se realiza desde un punto de entrada único:

python etl/main.py


Tecnologías Utilizadas

- Python 3.11
- Azure Blob Storage
- Pandas
- azure-storage-blob
- python-dotenv

Buenas Prácticas Aplicadas

Separación clara de responsabilidades (ETL desacoplado)

Uso de variables de entorno para credenciales

Logging del proceso

Control de calidad previo a la transformación

Entorno virtual para dependencias


Contexto Profesional

Este proyecto fue desarrollado como simulación técnica de un flujo cloud trabajado durante práctica profesional, con el objetivo de demostrar capacidades en procesamiento de datos, automatización de flujos y trabajo con servicios cloud.

Autor

Pablo Reyes
Data Analyst / BI / Data Processing
Portafolio: https://pablo-portfolio.vercel.app/