from text_Summarizer.components.model_trainer import ModelTrainer
from text_Summarizer.logging import logger
from text_Summarizer.pipeline.stage_01_data_ingestion import \
    DataIngestionTrainingPipeline
from text_Summarizer.pipeline.stage_02_data_validation import \
    DataValidationTrainingPipeline
from text_Summarizer.pipeline.stage_03_data_transformation import \
    DataTransformationTrainingPipeline
from text_Summarizer.pipeline.stage_04_model_trainer import \
    ModelTrainerTrainingPipline
from text_Summarizer.pipeline.stage_05_model_evaluation import \
    ModelEvaluationTrainingPipeline

# Data Ingestion Stage
STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# Data Validation Stage
STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationTrainingPipeline()
    status = data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# Check status file before starting Data Transformation stage
if status:
    # Data Transformation Stage
    STAGE_NAME = "Data Transformation stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_transformation = DataTransformationTrainingPipeline()
        data_transformation.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
else:
    logger.error(
        f">>>>>> stage Data Transformation stage Skipped due to failed data validation. <<<<<<\n\nx==========x"
    )

# Model trainer stage
STAGE_NAME = "Model trainer stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrainerTrainingPipline()
    model_trainer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Evaluation stage"
try:
    logger.info(f"*******************")
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationTrainingPipeline()
    model_evaluation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
