from pathlib import Path

from text_Summarizer.components.data_transformation import DataTransformation
from text_Summarizer.config.configuration import ConfigurationManager


class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().strip()
                if status == "True":
                    config = ConfigurationManager()
                    data_transformation_config = config.get_data_transformation_config()
                    data_transformation = DataTransformation(config=data_transformation_config)
                    data_transformation.convert()
                else:
                    raise Exception("Your Data Validation Steps did not passed successfully")


        except Exception as e:
            print(e)
