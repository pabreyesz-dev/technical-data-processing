import os
import logging
from io import StringIO

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
RAW_CONTAINER = os.getenv("RAW_CONTAINER_NAME")
RAW_FILE_NAME = os.getenv("RAW_FILE_NAME")

logger = logging.getLogger(__name__)


def get_blob_service_client():
    if not AZURE_CONNECTION_STRING:
        raise ValueError("Connection string no encontrada en variables de entorno")

    return BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )


def run_ingestion() -> pd.DataFrame:
    logger.info("Inicio del proceso de ingesta")
    logger.info("Conectando a Blob Storage...")

    service_client = get_blob_service_client()
    blob_client = service_client.get_blob_client(
        container=RAW_CONTAINER,
        blob=RAW_FILE_NAME
    )

    logger.info(f"Leyendo archivo CSV: {RAW_FILE_NAME}")
    blob_data = blob_client.download_blob().readall()
    csv_data = StringIO(blob_data.decode("utf-8"))

    df = pd.read_csv(csv_data, sep=";")

    logger.info(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    logger.info(f"Columnas detectadas: {list(df.columns)}")

    return df
