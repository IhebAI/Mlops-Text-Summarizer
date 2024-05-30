
from text_Summarizer.config.configuration import ConfigurationManager
from text_Summarizer.components.data_validation import DataValidation


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_files_exist_DataDict()
        data_validation.validate_all_files_exist_csv()
        data_validation.validate_schema_csv()
        data_validation.validate_data_types()
        data_validation.check_missing_values()
        data_validation.check_data_consistency()
        data_validation.check_data_quantity()
        return data_validation.read_status()

