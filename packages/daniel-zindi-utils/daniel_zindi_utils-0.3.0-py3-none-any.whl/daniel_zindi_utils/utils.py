import pandas as pd
import numpy as np
import csv
from daniel_zindi_utils.chrf import calculate_f1, chrF
from datasets import Dataset

def create_submission(test_flag):
  if test_flag:
    df1 = pd.read_csv("swahili_sentiment.csv")
    df2 = pd.read_csv("hausa_sentiment.csv")
    df3 = pd.read_csv("swahili_xnli.csv")
    df4 = pd.read_csv("hausa_xnli.csv")
    df5 = pd.read_csv("swahili_translation.csv")
    df6 = pd.read_csv("hausa_translation.csv")
  else:
    df1 = pd.read_csv("swahili_sentiment_test.csv")
    df2 = pd.read_csv("hausa_sentiment_test.csv")
    df3 = pd.read_csv("swahili_xnli_test.csv")
    df4 = pd.read_csv("hausa_xnli_test.csv")
    df5 = pd.read_csv("swahili_translation_test.csv")
    df6 = pd.read_csv("hausa_translation_test.csv")

  result = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)
  if test_flag:
    result = result[["ID", "Response", "Targets"]]
    result.to_csv("submission_train.csv", index=False)
  else:
    result = result[["ID", "Response"]]
    result.to_csv("submission.csv", index=False)

def evaluate_zindi(csv_file_path):
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        scores = []
        y_pred_sent = []
        y_true_sent = []
        y_pred_xnli = []
        y_true_xnli = []
        chrfs_scores = []

        for row in reader:
            if "sent" in row["ID"] or "xnli" in row["ID"]:
                if "xnli" in row["ID"]:
                    y_pred_xnli.append(row["Response"])
                    y_true_xnli.append(row["Targets"])
                if "sent" in row["ID"]:
                    y_pred_sent.append(row["Response"])
                    y_true_sent.append(row["Targets"])

            elif "mt" in row["ID"]:
                chrf_pred = row["Response"]
                chrf_true = row["Targets"]
                chrfs = chrF(reference=chrf_true, hypothesis=chrf_pred)
                chrfs_scores.append(chrfs)

        # F1 score for sentiment
        f1_sent = calculate_f1(np.array(y_true_sent), np.array(y_pred_sent), 3)
        scores.append(f1_sent)
        # F1 score for xnli
        f1_xnli = calculate_f1(np.array(y_true_xnli), np.array(y_pred_xnli), 3)
        scores.append(f1_xnli)
        # chrF score for mt
        chrfs_score = np.mean(chrfs_scores)
        scores.append(chrfs_score)
        # Zindi score: Average of all performances
        zindi_score = np.mean(scores)

    # Round to 4 decimal places and multiply by 100
    zindi_score = round(zindi_score, 4)
    zindi_score *= 100

    return zindi_score

def classification_main(csv_file_path, model, dataset, task):
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "Input Text",
                "Response",
                "Targets",
                "Task",
                "Langs",
            ]
        )

        len_dataset = len(dataset)
        correct = 0
        y_pred_sent = []
        y_true_sent = []
        for item in dataset:
            input_text = item["inputs"]
            output = model(input_text)
            label = int(output[0]['label'].split('_')[1])
            target = item["targets"]

            labels = []
            lang = item["langs"]

            if task == "sentiment":
                if "swahili" in item["ID"]:
                    lang = "swahili"
                    labels = ["Chanya", "Wastani", "Hasi"]
                elif "hausa" in item["ID"]:
                    lang = "hausa"
                    labels = ["Kyakkyawa", "Tsaka-tsaki", "Korau"]

                if labels:  # Ensure labels is not empty
                    label_to_id = {label: i for i, label in enumerate(labels)}
                    target = label_to_id.get(target, -1)  # Default to -1 if not found
            y_pred_sent.append(label)
            y_true_sent.append(target)
            if label == target:
                correct += 1

            writer.writerow(
                [
                    item["ID"],
                    input_text,
                    label,
                    target,
                    task,
                    lang,
                ]
            )
        f1_sent = calculate_f1(np.array(y_true_sent), np.array(y_pred_sent), 3)
        accuracy = correct / len_dataset
        return {"f1": f1_sent, "accuracy": accuracy}
    
def translation_main(csv_file_path, model, dataset, test_flag:bool):
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "Input Text",
                "Response",
                "Targets",
                "Task",
                "Langs",
            ]
        )
        scores = []
        for item in dataset:
            input_text = item["inputs"]
            output = model(input_text)
            target = item["targets"]
            lang = item["langs"]
            chrf_pred = output[0]['translation_text']
            chrf_true = target if test_flag else ""
            chrfs = chrF(reference=chrf_true, hypothesis=chrf_pred)
            scores.append(chrfs)
            writer.writerow(
                [
                    item["ID"],
                    input_text,
                    output[0]['translation_text'],
                    target,
                    "translation",
                    lang,
                ]
            )

        return np.mean(scores)


sentiment_train_df =  pd.read_parquet("hf://datasets/lelapa/SentimentTrain/data/train-00000-of-00001.parquet")

hau_dataset_sent = Dataset.from_pandas(
    sentiment_train_df[sentiment_train_df['langs']=='hausa']
)
swa_dataset_sent = Dataset.from_pandas(
    sentiment_train_df[sentiment_train_df['langs']=='swahili']
)

xnli_train_df = pd.read_parquet("hf://datasets/lelapa/XNLITrain/data/train-00000-of-00001.parquet")

hau_dataset_xnli = Dataset.from_pandas(
    xnli_train_df[xnli_train_df['langs']=='hau']
)
swa_dataset_xnli = Dataset.from_pandas(
    xnli_train_df[xnli_train_df['langs']=='swa']
)

mtt_train_df = pd.read_parquet("hf://datasets/lelapa/MTTrain/data/train-00000-of-00001.parquet")

hau_dataset_mtt = Dataset.from_pandas(
    mtt_train_df[mtt_train_df['langs']=='eng-hau']
)

swa_dataset_mtt = Dataset.from_pandas(
    mtt_train_df[mtt_train_df['langs']=='eng-swa']
)

sentiment_test_df = pd.read_parquet("hf://datasets/lelapa/SentimentTest/data/train-00000-of-00001.parquet")

hau_dataset_sent_test = Dataset.from_pandas(
    sentiment_test_df[sentiment_test_df['langs']=='hausa']
)
swa_dataset_sent_test = Dataset.from_pandas(
    sentiment_test_df[sentiment_test_df['langs']=='swahili']
)

xnli_test_df = pd.read_parquet("hf://datasets/lelapa/XNLITest/data/train-00000-of-00001.parquet")

hau_dataset_xnli_test = Dataset.from_pandas(
    xnli_test_df[xnli_test_df['langs']=='hau']
)
swa_dataset_xnli_test = Dataset.from_pandas(
    xnli_test_df[xnli_test_df['langs']=='swa']
)

mtt_test_df = pd.read_parquet("hf://datasets/lelapa/MTTest/data/train-00000-of-00001.parquet")

hau_dataset_mtt_test = Dataset.from_pandas(
    mtt_test_df[mtt_test_df['langs']=='eng-hau']
)
swa_dataset_mtt_test = Dataset.from_pandas(
    mtt_test_df[mtt_test_df['langs']=='eng-swa']
)
