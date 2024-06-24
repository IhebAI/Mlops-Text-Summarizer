import pandas as pd
import torch
import transformers
from datasets import load_dataset, load_from_disk, load_metric
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import mlflow
from urllib.parse import urlparse
from text_Summarizer.entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        self.model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """split the dataset into smaller batches that we can process simultaneously
        Yield successive batch-sized chunks from list_of_elements."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i: i + batch_size]

    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer,
                                    batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
                                    column_text="article",
                                    column_summary="highlights"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
                zip(article_batches, target_batches), total=len(article_batches)):
            inputs = tokenizer(article_batch, max_length=1024, truncation=True,
                               padding="max_length", return_tensors="pt")

            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                                       attention_mask=inputs["attention_mask"].to(device),
                                       length_penalty=0.8, num_beams=8, max_length=128)
            ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''

            # Finally, we decode the generated texts,
            # replace the  token, and add the decoded texts with the references to the metric.
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                                  clean_up_tokenization_spaces=True)
                                 for s in summaries]

            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]

            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        #  Finally compute and return the ROUGE scores.
        score = metric.compute()
        return score

    def evaluate(self):
        # loading data
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        rouge_metric = load_metric('rouge')

        score = self.calculate_metric_on_test_ds(
            dataset_samsum_pt['test'][0:10], rouge_metric, self.model_pegasus, self.tokenizer, batch_size=2,
            column_text='dialogue', column_summary='summary'
        )

        rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)

        df = pd.DataFrame(rouge_dict, index=['pegasus'])
        # Saving metrics as local
        df.to_csv(self.config.metric_file_name, index=False)
        return rouge_dict

    def log_into_mlflow(self, metrics: dict):

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        summarization_pipeline = transformers.pipeline("summarization", model=self.model_pegasus,
                                                       tokenizer=self.tokenizer,
                                                       device=0 if torch.cuda.is_available() else -1)
        with mlflow.start_run():
            mlflow.set_experiment("Fine tuning Pegasus model")

            # Log the metrics
            for metric in metrics:
                mlflow.log_metric(metric, metrics[metric])

            mlflow.log_params(self.config.all_params)

            #mlflow.transformers.log_model(summarization_pipeline, "model_pegasus_fine_tuned", registered_model_name="PegasusSamsumModel")

            # Register the model if the tracking URI is not a file store
            if tracking_url_type_store != "file":
                mlflow.register_model("runs:/{}/model_pegasus_fine_tuned".format(mlflow.active_run().info.run_id),
                                      "PegasusSamsumModel")
