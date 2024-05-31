# End to end Text-Summarizer-Project

# Project Description

This project focuses on fine-tuning a pre-trained PEGASUS model to create a text summarization tool using the SAMSUM dataset. The SAMSUM dataset, which includes dialogues and their summaries, is ideal for training and evaluating models that summarize conversations. The parameters used in the project are for demonstration purposes, and you can adjust them as needed.

## Machine Learning Pipeline Components

1. **Data Ingestion:** We begin by loading the SAMSUM dataset, which contains dialogues and their corresponding summaries.

2. **Data Validation:** We ensure the quality and consistency of the data by performing several checks:

    - **Validate All Files Exist - DataDict:** Confirm that all required dataset dictionary files are present.
    - **Validate All Files Exist - CSV:** Verify that all necessary CSV files are available.
    - **Validate Schema - CSV:** Check that all required columns are present in the CSV files.
    - **Validate Data Types:** Ensure that the data types in the CSV files match the expected types.
    - **Check Missing Values:** Identify any missing values in critical columns.
    - **Check Data Consistency:** Detect duplicate entries in the data.
    - **Check Data Quantity:** Verify that the amount of data meets the minimum requirements.

3. **Data Transformation:** We preprocess the dataset, which includes tokenizing the text and formatting it correctly for training the summarization model.

4. **Model Training:** We fine-tune the pre-trained PEGASUS model using our prepared dataset. This step adapts the model specifically for summarizing dialogues.

5. **Model Evaluation:** After training, we evaluate the model's performance using the ROUGE metric. ROUGE measures how well the model-generated summaries match the human-written ones.

6. **Prediction Service:** To make our model accessible, we set up an API using FastAPI. This API includes a `/train` endpoint to start the training process and a `/predict` endpoint for generating summaries. This setup allows us to easily integrate the summarization functionality into various applications and services.

7. **Model Saving and Loading:** Finally, we save the fine-tuned model and its tokenizer for future use. This ensures that the model can be reloaded and used without needing to retrain it.

## Technologies Used

- **Programming Language:** Python
- **Frameworks/Libraries:** PyTorch, FastAPI, Hugging Face Transformers, Pandas, NLTK, tqdm
- **Base model**: google/pegasus-cnn_dailymail
- **Version Control:** Git
- **Continuous Integration:** GitHub Actions
- **Deployment:** Docker, AWS EC2, AWS ECR
- **Data Handling:** Hugging Face Datasets
- **Model Evaluation:** ROUGE Score
- **API Development:** FastAPI


## Workflows

1. Update config.yaml
2. Update params.yaml
3. Update entity
4. Update the configuration manager in src config
5. update the conponents
6. update the pipeline
7. update the main.py
8. update the app.py


# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/entbappy/End-to-end-Text-Summarization
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n summary python=3.8 -y
```

```bash
conda activate summary
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up you local host and port
```


```bash
Author: Krish Naik
Data Scientist
Email: krishnaik06@gmail.com

```



# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URI: 566373416292.dkr.ecr.us-east-1.amazonaws.com/text-s

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = us-east-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app
