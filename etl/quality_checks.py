import logging
import pandas as pd

logger = logging.getLogger(__name__)


EXPECTED_COLUMNS = [
    "project_id",
    "client_type",
    "project_category",
    "estimated_hh",
    "team_size",
    "technology_stack",
    "data_volume_gb",
    "data_complexity",
    "risk_level",
    "deadline_days",
    "quality_score",
]


def check_not_empty(df: pd.DataFrame) -> None:
    """Valida que el DataFrame no esté vacío."""
    if df.empty:
        raise ValueError("El DataFrame está vacío")
    logger.info("Check OK: DataFrame no vacío")


def check_expected_columns(df: pd.DataFrame) -> None:
    """Valida que existan las columnas esperadas."""
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas esperadas: {missing}")
    logger.info("Check OK: Columnas esperadas presentes")


def check_nulls(df: pd.DataFrame) -> None:
    """Valida que no existan nulos en columnas críticas."""
    critical_cols = ["project_id", "estimated_hh", "deadline_days"]
    nulls = df[critical_cols].isnull().any()
    if nulls.any():
        raise ValueError("Existen valores nulos en columnas críticas")
    logger.info("Check OK: Sin nulos en columnas críticas")


def run_quality_checks(df: pd.DataFrame) -> None:
    """Ejecuta todos los controles de calidad."""
    logger.info("Iniciando controles de calidad")
    check_not_empty(df)
    check_expected_columns(df)
    check_nulls(df)
    logger.info("Todos los controles de calidad fueron superados")
