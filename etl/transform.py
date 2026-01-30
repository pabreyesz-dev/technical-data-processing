import os
import logging
from io import StringIO
from datetime import datetime

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
PROCESSED_CONTAINER = os.getenv("PROCESSED_CONTAINER_NAME")

logger = logging.getLogger(__name__)


def get_service_client():
    if not AZURE_CONNECTION_STRING:
        raise ValueError("Connection string no encontrada")
    return BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


def run_transformation(df: pd.DataFrame) -> None:
    logger.info("Iniciando transformación de datos")

    # Normalización columnas (tu lógica, intacta)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

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

    df["processed_at"] = datetime.utcnow().isoformat()

    # Guardado
    service_client = get_service_client()
    blob_client = service_client.get_blob_client(
        container=PROCESSED_CONTAINER,
        blob=f"processed_data_{datetime.utcnow().strftime('%Y%m%d')}.csv"
    )

    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    blob_client.upload_blob(buffer.getvalue(), overwrite=True)

    logger.info("Data procesada guardada correctamente en Blob Storage")
