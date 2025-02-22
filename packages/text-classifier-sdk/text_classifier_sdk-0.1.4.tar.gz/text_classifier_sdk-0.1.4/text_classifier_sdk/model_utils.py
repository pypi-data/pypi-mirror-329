from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_label_mappings(labels):
    """
    Generate label mappings dynamically.

    Args:
    - labels (list): List of user-defined labels.

    Returns:
    - (dict, dict): label2id and id2label mappings.
    """
    label2id = {label: i for i, label in enumerate(labels)}
    id2label = {i: label for i, label in enumerate(labels)}
    return label2id, id2label

def load_trained_model(model_path, num_labels):
    """
    Load a trained model and tokenizer.

    Args:
    - model_path (str): Path to the saved model.
    - num_labels (int): Number of labels.

    Returns:
    - (transformers model, tokenizer): Loaded model and tokenizer.
    """
    # model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=num_labels)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=num_labels, ignore_mismatched_sizes=True)

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer
