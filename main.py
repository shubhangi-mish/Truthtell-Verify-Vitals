import json
from Extraction import extract_twitter_data, extract_instagram_data, save_data_as_json
from preprocessing import process_json
from classification import load_model_and_vectorizer, classify_bulk_text, save_classification_results
from factchecking import fact_check_with_api

def main():
    twitter_query = "health OR medicine OR treatment OR disease OR symptom"
    instagram_tag = "health"

    print("Extracting data from Twitter...")
    twitter_data = extract_twitter_data(query=twitter_query, count=100)

    print("Extracting data from Instagram...")
    instagram_data = extract_instagram_data(tag=instagram_tag)

    all_data = twitter_data + instagram_data

    output_filename = "medical_data.json"
    save_data_as_json(data=all_data, filename=output_filename)

    print(f"Data extraction complete. Data saved to {output_filename}.")

    print("Starting preprocessing...")
    input_json_path = output_filename
    output_json_path = "preprocessed_medical_data.json"
    process_json(input_json_path, output_json_path)
    print(f"Preprocessing complete. Preprocessed data saved to {output_json_path}.")

    model, vectorizer = load_model_and_vectorizer()

    with open(output_json_path, 'r') as file:
        preprocessed_data = json.load(file)

    text_data = [entry['text'] for entry in preprocessed_data]

    print("Classifying texts as Accurate or Misleading...")
    classification_results = classify_bulk_text(text_data, model, vectorizer)

    for i, result in enumerate(classification_results):
        preprocessed_data[i]['classification'] = result

    print("Fact-checking classified texts...")
    for i, entry in enumerate(preprocessed_data):
        claim = entry['text']
        fact_check_result = fact_check_with_api(claim)
        preprocessed_data[i]['fact_check'] = fact_check_result

    classification_output_path = "classified_and_fact_checked_medical_data.json"
    save_classification_results(preprocessed_data, classification_output_path)

    print(f"Classification and fact-checking complete. Results saved to {classification_output_path}.")

if __name__ == "__main__":
    main()
