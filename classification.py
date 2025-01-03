import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model_and_vectorizer(model_path="misinformation_classifier.pkl", vectorizer_path="tfidf_vectorizer.pkl"):
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        logger.info("Model and vectorizer loaded successfully.")
        return model, vectorizer
    except Exception as e:
        logger.error(f"Error loading model or vectorizer: {e}")
        raise

def preprocess_text(text):
    text = text.strip()
    text = text.lower()
    logger.info("Text preprocessing complete.")
    return text

def classify_misinformation(text, model, vectorizer):
    try:
        preprocessed_text = preprocess_text(text)
        features = vectorizer.transform([preprocessed_text])
        prediction = model.predict(features)
        if prediction == 1:
            return "Misleading"
        else:
            return "Accurate"
    except Exception as e:
        logger.error(f"Error classifying text: {e}")
        return "Error in classification"

def classify_bulk_text(text_list, model, vectorizer):
    results = []
    for text in text_list:
        result = classify_misinformation(text, model, vectorizer)
        results.append(result)
    return results

def save_classification_results(results, output_file="classification_results.json"):
    try:
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)
        logger.info(f"Classification results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving classification results: {e}")
        raise

if __name__ == "__main__":
    model, vectorizer = load_model_and_vectorizer()

    sample_text = "This is a misleading claim about health."
    result = classify_misinformation(sample_text, model, vectorizer)
    print(f"Classification result for single text: {result}")

    sample_texts = [
        "This is a misleading claim about health.",
        "This is an accurate statement based on scientific research."
    ]
    results = classify_bulk_text(sample_texts, model, vectorizer)
    print("Bulk classification results:", results)

    save_classification_results(results)
