from flask import Flask, request, jsonify
import spacy
import re
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

# Function to check and download the SpaCy model if not available
def load_spacy_model(model_name):
    try:
        nlp = spacy.load(model_name)
    except OSError:
        # If the model is not available, download it
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        nlp = spacy.load(model_name)
    return nlp

# Load SpaCy model
nlp = load_spacy_model("en_core_web_sm")

# Helper function to mask PII with entity labels
def mask_pii(text):
    doc = nlp(text)
    masked_text = text

    # Replace named entities with their labels
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "DATE", "MONEY"]:  # Including more entity labels
            masked_text = masked_text.replace(ent.text, f'[{ent.label_}]')

    # Custom patterns for financial and identification numbers
    patterns = {
        'SSN': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        'PHONE': re.compile(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b'),
        'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        'CREDIT_CARD': re.compile(r'\b(?:\d[ -]*?){13,16}\b')
    }

    for label, pattern in patterns.items():
        masked_text = pattern.sub(f'[{label}]', masked_text)

    return masked_text

# Define API endpoint to mask PII
@app.route('/mask', methods=['POST'])
def mask():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    masked_text = mask_pii(text)
    
    return jsonify({"masked_text": masked_text})

if __name__ == '__main__':
    app.run(debug=True)
