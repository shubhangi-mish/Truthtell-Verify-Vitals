import json
from Extraction import extract_twitter_data, extract_instagram_data, save_data_as_json
from preprocessing import process_json

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

if __name__ == "__main__":
    main()
