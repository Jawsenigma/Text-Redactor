 
import os
import re
import argparse
import nltk
from nltk.corpus import names
from datetime import datetime
from collections import defaultdict

# Ensure necessary nltk resources are downloaded
nltk.download('names', quiet=True)
nltk.download('punkt', quiet=True)

# Utility function for reading common names from nltk's names corpus
def load_names():
    return set(names.words())

def email_redactor(text):
    # Regex pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, lambda match: '█' * len(match.group()), text)  # Replace with length-matched redaction

def date_redactor(text):
    date_patterns = [
        r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',
        r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,\s+\d{4})?\b',
        r'\b(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:\s+\d{4})?)\b'
    ]
    
    for pattern in date_patterns:
        text = re.sub(pattern, lambda match: '█' * len(match.group()), text)  # Replace with length-matched redaction
    return text

def phone_redactor(text):
    phone_patterns = [
        r'\b(?:\+?\d{1,2}[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b',  
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', 
        r'\b\d{3}[-.\s]?\d{4}\b', 
        r'\b\d{10}\b'  
    ]
    
    for pattern in phone_patterns:
        text = re.sub(pattern, lambda match: '█' * len(match.group()), text)  # Replace with length-matched redaction
    return text

def concept_redactor(text, concepts):
    sentences = nltk.sent_tokenize(text)
    redacted_text = []
    for sentence in sentences:
        if any(concept.lower() in sentence.lower() for concept in concepts):
            redacted_text.append('█' * len(sentence))  # Use length-matched redaction for entire sentence
        else:
            redacted_text.append(sentence)
    return ' '.join(redacted_text)

def gender_redactor(text):
    gender_terms = r'\b(he|she|him|her|his|hers)\b'
    return re.sub(gender_terms, lambda match: '█' * len(match.group()), text, flags=re.IGNORECASE)

def name_redactor(text, common_names):
    name_pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, common_names)))
    return re.sub(name_pattern, lambda match: '█' * len(match.group()), text, flags=re.IGNORECASE)

def address_redactor(text):
    address_patterns = [
        r'\b\d{1,5}\s(?:[A-Za-z]+\s){1,4}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Court|Ct|Square|Sq|Lane|Ln|Way|Wy|Highway|Hwy)\b'
    ]
    
    for pattern in address_patterns:
        text = re.sub(pattern, lambda match: '█' * len(match.group()), text)  # Use Unicode blocks
    return text


def redact_text(text, flags, concepts, common_names):
    if flags['dates']:
        text = date_redactor(text)
    if flags['phones']:
        text = phone_redactor(text)
    if flags['genders']:
        text = gender_redactor(text)
    if flags['names'] and common_names:
        text = name_redactor(text, common_names)
    if flags['concepts'] and concepts:
        text = concept_redactor(text, concepts)
    if flags['addresses']:
        text = address_redactor(text)
    if flags['emails']:  # Add this line
        text = email_redactor(text)  # Add this line
    return text

def write_output(redacted_text, output_path, stats_type, original_text):
    # Ensure the directory for output_path exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the redacted output with UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(redacted_text)
    print(f"Redacted file saved to: {output_path}")
    
    # If stats are needed, add them to the output file or print to console
    if stats_type:
        stats_output = f"\nRedaction statistics for the input file:\n"
        stats_output += f"Original Text Length: {len(original_text)}\n"
        stats_output += f"Redacted Text Length: {len(redacted_text)}\n"
        
        if stats_type == "stdout":
            print(stats_output)
        elif stats_type == "stderr":
            print(stats_output, file=sys.stderr)
        else:
            # Ensure the directory for stats file exists
            os.makedirs(os.path.dirname(stats_type), exist_ok=True)
            with open(stats_type, 'a', encoding='utf-8') as s:
                s.write(stats_output)
                s.write('\n')

def calculate_statistics(original_text, redacted_text):
    original_words = set(re.findall(r'\b\w+\b', original_text))
    redacted_words = set(re.findall(r'\b\w+\b', redacted_text))
    redacted_count = len(original_words - redacted_words)
    return {
        "Total Words": len(original_words),
        "Redacted Words": redacted_count,
        "Redacted Percentage": f"{(redacted_count / len(original_words) * 100):.2f}%"
    }

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Text Redaction Tool")
    parser.add_argument('input_path', type=str, help="Path to input text file or directory")
    parser.add_argument('--output', type=str, required=True, help="Directory to save redacted files")
    parser.add_argument('--stats', type=str, default="stdout", help="Output stats to file, stderr, or stdout")
    parser.add_argument('--dates', action='store_true', help="Redact dates")
    parser.add_argument('--phones', action='store_true', help="Redact phone numbers")
    parser.add_argument('--genders', action='store_true', help="Redact gender-specific terms")
    parser.add_argument('--names', action='store_true', help="Redact common names")
    parser.add_argument('--concepts', nargs='+', help="List of concepts to redact")
    parser.add_argument('--addresses', action='store_true', help="Redact addresses")
    parser.add_argument('--emails', action='store_true', help='Redact email addresses')

    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Load resources and common names if required
    common_names = load_names() if args.names else None
    flags = {
        'dates': args.dates,
        'phones': args.phones,
        'genders': args.genders,
        'names': args.names,
        'concepts': bool(args.concepts),
        'addresses': args.addresses,
        'emails': args.emails,
    }
    
    # Process files
    if os.path.isdir(args.input_path):
        files = [os.path.join(args.input_path, f) for f in os.listdir(args.input_path) if f.endswith('.txt')]
    else:
        files = [args.input_path]
    
    for file_path in files:
        with open(file_path, 'r') as f:
            original_text = f.read()
        
        redacted_text = redact_text(original_text, flags, args.concepts, common_names)
        output_path = os.path.join(args.output, os.path.basename(file_path).replace('.txt', '.redacted.txt'))
        
        write_output(redacted_text, output_path, args.stats, original_text)
        print(f"Redacted file saved to: {output_path}")

if __name__ == "__main__":
    main()
