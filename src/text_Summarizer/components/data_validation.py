import os

import pandas as pd

from text_Summarizer.entity import DataValidationConfig
from text_Summarizer.logging import logger


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def read_status(self) -> bool:
        try:
            with open(self.config.STATUS_FILE, "r") as f:
                status = f.read().strip()
                return status == "True"
        except FileNotFoundError:
            return False

    def write_status(self, status: bool):
        with open(self.config.STATUS_FILE, "w") as f:
            f.write(str(status))

    def validate_all_files_exist_DataDict(self) -> bool:
        try:
            validation_status = True
            all_files = os.listdir(
                os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            )
            logger.info(f"All files in the dataset directory: {all_files}")
            for required_file in self.config.ALL_REQUIRED_ARROW_FILES:
                if required_file not in all_files:
                    validation_status = False
                    logger.error(
                        f"Validation status: {validation_status}. Missing file for the required Dataset Dictionary: {required_file}"
                    )
                    break

            if validation_status:
                logger.info(
                    "Validation status: True. All required files are present for the required Dataset Dictionary."
                )

            self.write_status(validation_status)
            return validation_status

        except Exception as e:
            logger.error(
                f"Error occurred while validating all files for Dataset Dictionary: {str(e)}"
            )
            self.write_status(False)
            return False

    def validate_all_files_exist_csv(self) -> bool:
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Validation of the presence all required CSV files."
            )
            return False

        try:
            validation_status = True
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)
                if not os.path.exists(csv_file_path):
                    validation_status = False
                    logger.error(
                        f"Validation status: {validation_status}. Missing file for the required CSV files: {csv_file}"
                    )
                    break

            if validation_status:
                logger.info(
                    "Validation status: True. All required CSV files are present."
                )

            self.write_status(validation_status)
            return validation_status

        except Exception as e:
            logger.error(
                f"Error occurred while validating all CSV files: {str(e)}")
            self.write_status(False)
            return False

    def validate_schema_csv(self) -> bool:
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Schema Validation.")
            return False

        try:
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)

                df = pd.read_csv(csv_file_path)
                missing_columns = [
                    col for col in self.config.REQUIRED_COLUMNS if col not in df.columns
                ]
                if missing_columns:
                    logger.error(
                        f"Schema validation failed for {csv_file}. Missing columns: {missing_columns}"
                    )
                    self.write_status(False)
                    return False
                logger.info(f"Schema validation passed for {csv_file}.")

            self.write_status(True)
            return True
        except Exception as e:
            logger.error(f"Error occurred while validating schema: {str(e)}")
            self.write_status(False)
            return False

    def validate_data_types(self) -> bool:
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Data types Validation."
            )
            return False

        try:
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)

                df = pd.read_csv(csv_file_path)
                expected_data_types = self.config.EXPECTED_DATA_TYPES
                for col, dtype in expected_data_types.items():
                    if df[col].dtype != dtype:
                        logger.error(
                            f"Data type validation failed for {csv_file}. Column '{col}' is of type {df[col].dtype}, not of type {dtype}."
                        )
                        self.write_status(False)
                        return False
                logger.info(f"Data type validation passed for {csv_file}.")

            self.write_status(True)
            return True
        except Exception as e:
            logger.error(
                f"Error occurred while validating data types: {str(e)}")
            self.write_status(False)
            return False

    def check_missing_values(self) -> bool:
        """
        Checks for missing values in critical columns of the DataFrame.

        Returns:
            bool: True if no missing values found, False otherwise.
        """
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Missing Values Validation."
            )
            return False
        try:
            validation_status = True
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)
                df = pd.read_csv(csv_file_path)
                missing_values_mask = (
                    df[self.config.REQUIRED_COLUMNS].isnull().any(axis=1)
                )
                if missing_values_mask.any():
                    missing_ids = df.loc[missing_values_mask, "id"].tolist()
                    logger.error(
                        f"Missing values found in critical columns of {csv_file}. IDs of affected rows: {missing_ids}"
                    )
                    validation_status = (
                        False  # Update status to False if missing values are found
                    )
            if validation_status:
                logger.info(
                    "No missing values found in critical columns of all CSV files."
                )
            else:
                self.write_status(
                    False
                )  # Write False status if missing values are found
            return validation_status
        except Exception as e:
            logger.error(
                f"Error occurred while checking missing values: {str(e)}")
            return False

    def check_data_consistency(self) -> bool:
        """
        Checks data consistency within the DataFrame.

        Returns:
            bool: True if data is consistent, False otherwise.
        """
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Data consistency Validation."
            )
            return False
        try:
            validation_status = True
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)
                df = pd.read_csv(csv_file_path)
                duplicates_mask = df.duplicated(
                    subset=self.config.REQUIRED_COLUMNS, keep=False
                )
                if duplicates_mask.any():
                    duplicate_ids = df.loc[duplicates_mask, "id"].tolist()
                    logger.error(
                        f"Duplicate entries found in {csv_file}. IDs of affected rows: {duplicate_ids}"
                    )
                    validation_status = (
                        False  # Update status to False if duplicates are found
                    )
            if validation_status:
                logger.info("No duplicate entries found in any CSV file.")
            else:
                # Write False status if duplicates are found
                self.write_status(False)
            return validation_status
        except Exception as e:
            logger.error(
                f"Error occurred while checking data consistency: {str(e)}")
            return False

    def check_data_quantity(self) -> bool:
        """
        Checks if the quantity of data meets the requirements.

        Returns:
            bool: True if data quantity meets the requirements, False otherwise.
        """
        if not self.read_status():
            logger.info(
                "Due Previous Validation Status: Skipping Data Quantity Validation."
            )
            return False
        try:
            validation_status = True
            for csv_file in self.config.ALL_REQUIRED_CSV_FILES:
                csv_file_path = os.path.join(
                    "artifacts", "data_ingestion", csv_file)
                df = pd.read_csv(csv_file_path)
                dataset_type = csv_file.split("-")[1].split(".")[0]
                min_data_quantity_key = f"MINIMUM_DATA_QUANTITY.{dataset_type}"
                min_data_quantity = getattr(
                    self.config, min_data_quantity_key, 0)
                if len(df) < min_data_quantity:
                    logger.error(
                        f"Insufficient data in {csv_file}. Expected at least {min_data_quantity} examples, but found {len(df)} examples."
                    )
                    validation_status = (
                        False  # Update status to False if data quantity is insufficient
                    )
                else:
                    logger.info(
                        f"Sufficient data quantity found in {csv_file}. Number of examples: {len(df)}"
                    )
            if not validation_status:
                self.write_status(
                    False
                )  # Write False status if data quantity is insufficient
            return validation_status
        except Exception as e:
            logger.error(
                f"Error occurred while checking data quantity: {str(e)}")
            return False
