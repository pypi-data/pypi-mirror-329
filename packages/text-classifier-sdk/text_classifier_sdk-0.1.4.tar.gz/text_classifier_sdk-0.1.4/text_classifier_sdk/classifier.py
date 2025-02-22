import os
import requests
from .train import train_text_classifier
from .model_utils import load_trained_model

API_BASE = "http://classify.ngmkt.site/api"
# API_BASE = "http://localhost:8000/api"

class TextClassifier:
    def __init__(self, labels, api_key, model_name="facebook/bart-large-mnli"):
        """
        Initialize the TextClassifier.

        Args:
        - labels (list): A list of labels for classification.
        - api_key (str): API key for authentication.
        - model_name (str): Pretrained model name.
        """
        self.labels = labels
        self.api_key = api_key
        self.model_name = model_name
        self.model, self.tokenizer = load_trained_model(model_name, len(labels))

        # Verify API Key
        if not self._validate_api_key():
            raise ValueError("Invalid API Key. Please check your subscription. login to your account at https://dokwick.com/login")

    def _validate_api_key(self):
        """Check if the API key is valid."""
        print(f"Validating API Key... {API_BASE}/validate-key")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
            response = requests.post(f"{API_BASE}/validate-key", headers=headers, json={"api_key": self.api_key}, verify=False)
            return response.json().get("valid", False)
        except Exception as e:
            print("API Response:", response.status_code, response.text)  # <-- Log this!

    def _log_usage(self, text, prediction):
        try:
            """Log usage data to the API."""
            data = {
                "api_key": self.api_key,
                "text": text,
                "prediction": prediction
            }
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
            requests.post(f"{API_BASE}/log", headers=headers, verify=False, json=data)
        except:
            print("Server Error")  # <-- Log this!

    def train(self, train_file, test_file, output_dir="./model_output"):
        try:
            """Train the model locally."""
            train_text_classifier(self.labels, train_file, test_file, self.model_name, output_dir)
            data = {
                "api_key": self.api_key,
                "text": "training",
                "prediction": "training"
            }
            
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
            requests.post(f"{API_BASE}/log", headers=headers, verify=False, json=data)
        except Exception as e:
            print("Server Error")  # <-- Log this!


    def predict(self, text):
        try:
            """Predict the label for a given text."""
            # Check if user exceeded their quota
            response = requests.post(f"{API_BASE}/check-usage", json={"api_key": self.api_key})
            if not response.json().get("allowed", True):
                raise ValueError("API call limit reached. Upgrade your plan.")

            # Run Prediction
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = self.model(**inputs)
            prediction = outputs.logits.argmax(dim=-1).item()
            label = self.labels[prediction]

            # Log this request
            self._log_usage(text, label)
            return label
        except Exception as e:
            print("Server Error")  # <-- Log this!

