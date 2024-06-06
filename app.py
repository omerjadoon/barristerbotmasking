from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Helper function to mask PII with entity labels
def mask_pii(text):
    doc = nlp(text)
    masked_text = text

    # Replace named entities with their labels
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "DATE", "MONEY", "LOC"]:  # Including more entity labels
            masked_text = masked_text.replace(ent.text, f'[{ent.label_}]')

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
