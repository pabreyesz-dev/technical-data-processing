import logging

from ingest import run_ingestion
from transform import run_transformation
from quality_checks import run_quality_checks


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    logger.info("===== INICIO PIPELINE ETL =====")

    # 1. Ingesta
    df_raw = run_ingestion()

    # 2. Validaciones de calidad
    run_quality_checks(df_raw)

    # 3. Transformación y carga final
    run_transformation(df_raw)

    logger.info("===== PIPELINE FINALIZADO CORRECTAMENTE =====")


if __name__ == "__main__":
    main()
