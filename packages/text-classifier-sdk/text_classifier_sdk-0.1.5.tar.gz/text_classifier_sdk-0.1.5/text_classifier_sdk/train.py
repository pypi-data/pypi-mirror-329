import pandas as pd
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from .model_utils import get_label_mappings

def train_text_classifier(labels, train_file, test_file, model_name, output_dir):
    print("Training the model...")
    """
    Train a text classifier using the user-defined labels.

    Args:
    - labels (list): List of user-defined labels.
    - train_file (str): Path to the training CSV file.
    - test_file (str): Path to the test CSV file.
    - model_name (str): Pretrained model name.
    - output_dir (str): Directory to save trained model.
    """
    # Convert label names to numerical IDs
    label2id, id2label = get_label_mappings(labels)
    print("Labels:", label2id) 
    print("Inverse Labels:", id2label)
    print(len(labels))

    # Load CSV data
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    # Convert text labels to numerical IDs
    train_df["label"] = train_df["label"].map(label2id)
    test_df["label"] = test_df["label"].map(label2id)
    # train_df["label"] = train_df["label"].astype(int)
    # test_df["label"] = test_df["label"].astype(int)

    print("Sample Labels:", train_df["label"].head())  # Should be integers like 0,1,2...
    print("Unique Labels:", train_df["label"].unique())  # Should match 0 to len(labels)-1
    
    # Debug: Print any rows with NaN labels
    nan_rows = train_df[train_df["label"].isna()]
    if not nan_rows.empty:
        print("Rows with NaN labels in train data:\n", nan_rows)
        
    nan_rows_test = test_df[test_df["label"].isna()]
    if not nan_rows_test.empty:
        print("Rows with NaN labels in test data:\n", nan_rows_test)

    # Handle NaN labels before converting to int
    train_df["label"] = train_df["label"].fillna(-1).astype(int)  # Assign -1 for unknown labels
    test_df["label"] = test_df["label"].fillna(-1).astype(int)

    # Ensure all labels are valid
    if -1 in train_df["label"].values or -1 in test_df["label"].values:
        raise ValueError("Some labels in the dataset are not recognized. Check label names in the CSV and label2id mapping.")
    # return
    # Save preprocessed CSVs (optional for debugging)
    train_df.to_csv("train_numeric.csv", index=False)
    test_df.to_csv("test_numeric.csv", index=False)

    # Load dataset into Hugging Face format
    dataset = load_dataset("csv", data_files={"train": "train_numeric.csv", "test": "test_numeric.csv"})

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=len(labels), ignore_mismatched_sizes=True
    )

    # Apply tokenization
    def preprocess(example):
        return tokenizer(example["text"], truncation=True, padding="max_length")

    dataset = dataset.map(preprocess, batched=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=5,  # Increase for better training
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"]
    )

    trainer.train()


    # Save model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
