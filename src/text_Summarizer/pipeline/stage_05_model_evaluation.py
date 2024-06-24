from text_Summarizer.components.model_evaluation import ModelEvaluation
from text_Summarizer.config.configuration import ConfigurationManager
import dagshub


class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        dagshub.init(repo_owner='iheb.aamrii', repo_name='Mlops-Text-Summarizer', mlflow=True)
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
        metrics = model_evaluation_config.evaluate()
        model_evaluation_config.log_into_mlflow(metrics)
