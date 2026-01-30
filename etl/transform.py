import os
import logging
from io import StringIO

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


# ------------------------
# Configuración inicial
# ------------------------
load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
RAW_CONTAINER = os.getenv("RAW_CONTAINER_NAME")
PROCESSED_CONTAINER = os.getenv("PROCESSED_CONTAINER_NAME")
RAW_FILE_NAME = os.getenv("RAW_FILE_NAME")
PROCESSED_FILE_NAME = "processed_data300126.csv"


# ------------------------
# Logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ------------------------
# Funciones
# ------------------------
def get_service_client():
    if not AZURE_CONNECTION_STRING:
        raise ValueError("Connection string no encontrada")
    return BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


def load_raw_data(service_client):
    logger.info("Cargando data RAW desde Blob Storage")

    blob_client = service_client.get_blob_client(
        container=RAW_CONTAINER,
        blob=RAW_FILE_NAME
    )

    blob_data = blob_client.download_blob().readall()
    csv_data = StringIO(blob_data.decode("utf-8"))

    # Importante: el CSV usa ';' como separador
    df = pd.read_csv(csv_data, sep=";")

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando transformación de datos")

    # Normalizar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Conversión de tipos
    numeric_columns = [
        "estimated_hh",
        "team_size",
        "data_volume_gb",
        "deadline_days",
        "quality_score"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info("Transformación completada")
    return df


def save_processed_data(service_client, df: pd.DataFrame):
    logger.info("Guardando data procesada en Blob Storage")

    output = df.to_csv(index=False)
    blob_client = service_client.get_blob_client(
        container=PROCESSED_CONTAINER,
        blob=PROCESSED_FILE_NAME
    )

    blob_client.upload_blob(output, overwrite=True)
    logger.info(f"Archivo procesado guardado: {PROCESSED_FILE_NAME}")


# ------------------------
# Main
# ------------------------
def main():
    logger.info("Inicio del proceso de transformación")

    service_client = get_service_client()
    df_raw = load_raw_data(service_client)

    logger.info(f"Dataset cargado: {df_raw.shape[0]} filas")

    df_processed = transform_data(df_raw)
    save_processed_data(service_client, df_processed)

    logger.info("Proceso de transformación finalizado correctamente")


if __name__ == "__main__":
    main()