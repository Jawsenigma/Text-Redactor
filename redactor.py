import os
import argparse
import spacy
from spacy.matcher import Matcher

# Load the spaCy model
# nlp = spacy.load("en_core_web_sm")
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm") 
    nlp = spacy.load("en_core_web_sm")  

def email_redactor(text):
    doc = nlp(text)
    redacted_text = []
    for token in doc:
        if token.like_email:
            redacted_text.append('█' * len(token.text))
        else:
            redacted_text.append(token.text)
    return ' '.join(redacted_text)


import spacy

# Load SpaCy's pre-trained NER model
nlp = spacy.load("en_core_web_sm")

def date_redactor(text):
    doc = nlp(text)  # Process the text with SpaCy
    redacted_text = text  # Start with the original text

    # Collect all dates for redaction
    dates_to_redact = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    # Replace each date in the text with the redaction placeholder
    for date in dates_to_redact:
        redacted_text = redacted_text.replace(date, "██████")

    return redacted_text





def phone_redactor(text):
    # Use a Matcher to identify phone number patterns
    matcher = Matcher(nlp.vocab)
    phone_patterns = [
        [{"SHAPE": "ddd"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "ddd"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "dddd"}],
        [{"SHAPE": "ddd"}, {"SHAPE": "dddd"}],  # Matches like 1234567
        [{"SHAPE": "dd"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "ddd"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "dddd"}],  # Matches like 12-3456-7890
    ]

    for pattern in phone_patterns:
        matcher.add("PHONE_NUMBER", [pattern])

    doc = nlp(text)
    matches = matcher(doc)
    redacted_text = text

    for match_id, start, end in matches:
        span = doc[start:end]
        redacted_text = redacted_text.replace(span.text, '█' * len(span.text))

    return redacted_text

def concept_redactor(text, concepts):
    doc = nlp(text)
    redacted_text = []
    for sentence in doc.sents:
        if any(concept.lower() in sentence.text.lower() for concept in concepts):
            redacted_text.append('█' * len(sentence.text))
        else:
            redacted_text.append(sentence.text)
    return ' '.join(redacted_text)

def gender_redactor(text):
    gender_terms = ['he', 'she', 'him', 'her', 'his', 'hers']
    doc = nlp(text)
    redacted_text = []
    for token in doc:
        if token.text.lower() in gender_terms:
            redacted_text.append('█' * len(token.text))
        else:
            redacted_text.append(token.text)
    return ' '.join(redacted_text)

def name_redactor(text):
    doc = nlp(text)
    redacted_text = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_text.append('█' * len(ent.text))
        else:
            redacted_text.append(ent.text)
    return ' '.join(redacted_text)

def address_redactor(text):
    # Create a simple Matcher for addresses
    matcher = Matcher(nlp.vocab)
    address_patterns = [
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["street", "st", "avenue", "ave", "road", "rd", "boulevard", "blvd", "drive", "dr", "court", "ct", "lane", "ln", "way", "wy"]}}],
        [{"LOWER": {"IN": ["street", "st", "avenue", "ave", "road", "rd", "boulevard", "blvd"]}}, {"LIKE_NUM": True}],  # Matches like Street 123
    ]

    for pattern in address_patterns:
        matcher.add("ADDRESS", [pattern])

    doc = nlp(text)
    matches = matcher(doc)
    redacted_text = text

    for match_id, start, end in matches:
        span = doc[start:end]
        redacted_text = redacted_text.replace(span.text, '█' * len(span.text))

    return redacted_text

def redact_text(text, flags, concepts):
    if flags['dates']:
        text = date_redactor(text)
    if flags['phones']:
        text = phone_redactor(text)
    if flags['genders']:
        text = gender_redactor(text)
    if flags['names']:
        text = name_redactor(text)
    if flags['concepts'] and concepts:
        text = concept_redactor(text, concepts)
    if flags['addresses']:
        text = address_redactor(text)
    if flags['emails']:
        text = email_redactor(text)
    return text

def write_output(redacted_text, output_path, stats_type, original_text):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(redacted_text)
    print(f"Redacted file saved to: {output_path}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Text Redaction Tool")
    parser.add_argument('input_path', type=str, help="Path to input text file or directory")
    parser.add_argument('--output', type=str, required=True, help="Directory to save redacted files")
    parser.add_argument('--stats', type=str, default="stdout", help="Output stats to file, stderr, or stdout")
    parser.add_argument('--dates', action='store_true', help="Redact dates")
    parser.add_argument('--phones', action='store_true', help="Redact phone numbers")
    parser.add_argument('--genders', action='store_true', help="Redact gender-specific terms")
    parser.add_argument('--names', action='store_true', help="Redact names")
    parser.add_argument('--concepts', nargs='+', help="List of concepts to redact")
    parser.add_argument('--addresses', action='store_true', help="Redact addresses")
    parser.add_argument('--emails', action='store_true', help='Redact email addresses')

    return parser.parse_args()

def main():
    args = parse_arguments()
    flags = {
        'dates': args.dates,
        'phones': args.phones,
        'genders': args.genders,
        'names': args.names,
        'concepts': bool(args.concepts),
        'addresses': args.addresses,
        'emails': args.emails,
    }
    
    if os.path.isdir(args.input_path):
        files = [os.path.join(args.input_path, f) for f in os.listdir(args.input_path) if f.endswith('.txt')]
    else:
        files = [args.input_path]
    
    for file_path in files:
        with open(file_path, 'r') as f:
            original_text = f.read()
        
        redacted_text = redact_text(original_text, flags, args.concepts)
        output_path = os.path.join(args.output, os.path.basename(file_path).replace('.txt', '.redacted.txt'))
        
        write_output(redacted_text, output_path, args.stats, original_text)

if __name__ == "__main__":
    main()
