import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import os
from typing import Dict, Any
import logging



logger = logging.getLogger(__name__)


class TaskPriorityPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_path = "/data/task_priority_model.joblib"
        self.training_in_progress = False

    def train_model(self, csv_path: str = "src/tasks.csv"):

        if self.training_in_progress:
            return {"error": "Training already in progress"}

        self.training_in_progress = True
        try:

            df = pd.read_csv(csv_path)

            df['priority_numeric'] = df['priority'].map({'low': 0, 'high': 1})

            X = df['task_description']
            y = df['priority_numeric']

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2)
                )),
                ('classifier', LogisticRegression(
                    random_state=42,
                    max_iter=1000
                ))
            ])


            self.model.fit(X_train, y_train)

            self.save_model()

            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)

            logger.info(f"Model trained successfully!")
            logger.info(f"Train accuracy: {train_score:.2f}")
            logger.info(f"Test accuracy: {test_score:.2f}")

            self.training_in_progress = False
            return True

        except Exception as e:
            logger.error(f"Error training model: {e}")
            self.training_in_progress = False
            return False

    def predict_priority(self, task_description: str) -> Dict[str, Any]:
        if self.model is None:
            self.load_model()
            if self.model is None:
                return {"error": "Model not trained"}

        try:
            prediction = self.model.predict([task_description])[0]
            probability = self.model.predict_proba([task_description])[0]

            priority = "high" if prediction == 1 else "low"
            confidence = float(probability[prediction])

            return {
                "priority": priority,
                "confidence": confidence,
                "task_description": task_description
            }

        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}

    def save_model(self):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
                return True
            else:
                logger.error("No trained model found")
                return False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False


predictor = TaskPriorityPredictor()


def initialize_model():
    if not predictor.load_model():
        logger.info("Training model from scratch...")
        predictor.train_model()
