# Processing Protocol

## 1. Objetivo

Este documento define el protocolo del procesamiento de los datos utilizados en el proyecto, estableciendo las etapas obligatorias para garantizar la integridad, trazabilidad y calidad de la información procesada.

El protocolo está diseñado para entornos de procesamiento técnico de datos y es aplicable a flujos batch que manejan información estructurada de complejidad media y alta.

---

## 2. Alcance del Protocolo

El protocolo aplica desde la recepción de datos en estado *raw* hasta la generación de datos procesados listos para análisis técnico o generación de reportes.

Incluye:

* Ingesta de datos
* Validaciones iniciales
* Transformaciones controladas
* Control de calidad
* Generación de outputs

---

## 3. Estructura de Almacenamiento

Los datos se organizan en capas lógicas dentro de Azure Blob Storage:

* **raw/**

  * Contiene los datos originales sin modificaciones.
  * Los archivos en esta capa no deben alterarse manualmente.

* **processed/**

  * Contiene los datos transformados y validados.
  * Es la capa utilizada para análisis y generación de resultados.

Esta separación permite trazabilidad y repetibilidad del procesamiento.

---

## 4. Etapas del Protocolo

### 4.1 Ingesta de Datos

* Recepción de archivos CSV en la capa `raw`.
* Verificación de que el archivo contiene encabezados y estructura tabular válida.
* Registro de fecha y origen del archivo.

---

### 4.2 Validación Inicial

Se realizan validaciones básicas antes de cualquier transformación:

* Verificación de columnas obligatorias.
* Validación de tipos de datos (numéricos, categóricos).
* Detección de valores nulos críticos.

Los archivos que no cumplan estas validaciones no continúan el procesamiento.

---

### 4.3 Transformación de Datos

Incluye, cuando corresponde:

* Normalización de valores categóricos.
* Conversión de tipos de datos.
* Estandarización de nombres y formatos.

Las transformaciones deben ser reproducibles y documentadas.

---

### 4.4 Control de Calidad

Se aplican reglas de control de calidad para asegurar la consistencia de los datos:

* Validación de rangos aceptables.
* Detección de valores atípicos.
* Evaluación de métricas de calidad definidas.

Los resultados de estas validaciones pueden ser utilizados para análisis técnico posterior.

---

### 4.5 Generación de Datos Procesados

* Los datos que cumplen los criterios definidos se almacenan en la capa `processed`.
* Se conserva la estructura tabular y se documentan los cambios realizados.

---

## 5. Manejo de Errores

* Los errores de validación se registran y se documenta la causa.
* No se modifican los datos originales en la capa `raw`.
* El procesamiento puede ser repetido una vez corregida la fuente de datos.

---

## 6. Principios del Protocolo

* **Integridad:** los datos originales no se alteran.
* **Trazabilidad:** cada etapa del procesamiento es identificable.
* **Repetibilidad:** el flujo puede ejecutarse múltiples veces con resultados consistentes.
* **Rigurosidad técnica:** se prioriza la calidad sobre la velocidad de procesamiento.

---

## 7. Observaciones Finales

Este protocolo está diseñado como base demostrativa y puede extenderse a otros tipos de datos técnicos, incluyendo información geoespacial o datasets de mayor volumen, manteniendo la misma lógica de procesamiento.
