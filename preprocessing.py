import spacy
import re
import json

nlp = spacy.load("en_core_sci_md")

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s.,!?;()"\']', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_and_extract_entities(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_
        })
    return entities

def process_json(input_json_path, output_json_path):
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    
    for item in data:
        if 'text' in item:
            item['preprocessed_text'] = clean_text(item['text'])
            item['entities'] = preprocess_and_extract_entities(item['text'])
    
    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=4)
