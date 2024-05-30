from text_Summarizer.components.data_ingestion import DataIngestion
from text_Summarizer.components.model_trainer import ModelTrainer
from text_Summarizer.config.configuration import ConfigurationManager


class ModelTrainerTrainingPipline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()
