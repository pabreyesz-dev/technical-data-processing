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
RAW_FILE_NAME = os.getenv("RAW_FILE_NAME")

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
def get_blob_client():
    """Inicializa el cliente de Azure Blob Storage"""
    if not AZURE_CONNECTION_STRING:
        raise ValueError("Connection string no encontrada en variables de entorno")

    service_client = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )
    return service_client


def read_csv_from_blob(service_client):
    """Lee un archivo CSV desde Blob Storage y lo retorna como DataFrame"""
    logger.info("Conectando a Blob Storage...")

    blob_client = service_client.get_blob_client(
        container=RAW_CONTAINER,
        blob=RAW_FILE_NAME
    )

    logger.info(f"Leyendo archivo CSV: {RAW_FILE_NAME}")
    blob_data = blob_client.download_blob().readall()

    csv_data = StringIO(blob_data.decode("utf-8"))
    df = pd.read_csv(csv_data)

    return df


def basic_validation(df: pd.DataFrame):
    """Validaciones básicas de la data"""
    logger.info("Ejecutando validaciones básicas")

    if df.empty:
        raise ValueError("El archivo CSV está vacío")

    logger.info(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    logger.info(f"Columnas detectadas: {list(df.columns)}")


# ------------------------
# Main
# ------------------------
def main():
    logger.info("Inicio del proceso de ingesta")

    service_client = get_blob_client()
    df = read_csv_from_blob(service_client)
    basic_validation(df)

    logger.info("Vista previa de la data:")
    logger.info(df.head(3))

    logger.info("Ingesta finalizada correctamente")


if __name__ == "__main__":
    main()
