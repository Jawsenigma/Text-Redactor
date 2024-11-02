import os
import argparse
import spacy
from spacy.matcher import Matcher
from spacy.cli import download
import sys
import re
import crim as CommonRegex
import nltk
from nltk.corpus import wordnet as wn

nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)

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


def date_redactor(text):
    date_list = CommonRegex.dates(text)
    
    for date in date_list:
        redaction = "█" * len(date)  
        text = text.replace(date, redaction)
    
    return text



def phone_redactor(text):
    phone_pattern = re.compile(r'''
        (\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}) |
        (\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{3,4}[-.\s]?\d{4})
    ''', re.VERBOSE)

    redacted_text = re.sub(phone_pattern, lambda x: '█' * len(x.group()), text)
    
    return redacted_text



def concept_redactor(data, concept):
    if not isinstance(concept, str) or len(concept.split()) > 1:
        raise ValueError("Concept must be a single word as a string.")
    
    concept_list = set()
    syns = wn.synsets(concept)
    for syn in syns:
        for lemma in syn.lemma_names():
            concept_list.add(lemma.lower())
    
    concept_list.add(concept.lower())

    sentences = [sentence.strip() for sentence in data.replace('\n', '. ').split('.') if sentence.strip()]
    block = '█' 

    redacted_data = data

    for sentence in sentences:
        if any(synonym in sentence.lower() for synonym in concept_list):
            redacted_sentence = block * len(sentence)
            redacted_data = redacted_data.replace(sentence, redacted_sentence)

    return redacted_data



def gender_redactor(text):
    gender_terms = [
        'he', 'she', 'him', 'her', 'his', 'hers', 'them', 'their', 'theirs',
        'man', 'woman', 'boy', 'girl', 'father', 'mother',
        'brother', 'sister', 'husband', 'wife', 
        'male', 'female', 'masculine', 'feminine',
        'non-binary', 'genderqueer', 'genderfluid',
        'ze', 'zir', 'xe', 'xem',
        'mr.', 'mrs.', 'ms.', 'miss'
    ]
    doc = nlp(text)
    redacted_text = []
    
    for token in doc:
        if token.text.lower() in gender_terms:
            redacted_text.append('█' * len(token.text))
        else:
            redacted_text.append(token.text)
    
    return ' '.join(redacted_text)



def name_redactor(text):
    email_pattern = r'(\S+)@(\S+\.\S+)'
    doc = nlp(text)
    redacted_text = []
    previous_end = 0

    for ent in doc.ents:
        start, end = ent.start_char, ent.end_char
        redacted_text.append(text[previous_end:start])

        if ent.label_ == 'PERSON':
            redacted_text.append('█' * (end - start))
        else:
            redacted_text.append(text[start:end])

        previous_end = end

    redacted_text.append(text[previous_end:])

    redacted_email_text = ''.join(redacted_text)
    redacted_email_text = re.sub(email_pattern, lambda x: '█' * len(x.group(1)) + '@' + x.group(2), redacted_email_text)

    return redacted_email_text




def address_redactor(data):
    pattern = re.compile(r'\b\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Wy|Parkway|Pkwy)\b', re.IGNORECASE)

    redacted_data = pattern.sub(lambda match: '█' * len(match.group()), data)

    return redacted_data



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
        for concept in concepts:
            text = concept_redactor(text, concept)  
    if flags['addresses']:
        text = address_redactor(text)
    if flags['emails']:
        text = email_redactor(text)
    return text


def write_output(redacted_text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(redacted_text)
    print(f"Redacted file saved to: {output_path}")

def write_stats(stats, stats_type):
    stats_output = []
    
    stats_output.append(f"Files Processed: {stats['files_processed']}")
    stats_output.append(f"Files Redacted: {stats['files_redacted']}")
    stats_output.append(f"Errors: {stats['errors']}\n")
    
    for category, details in stats.items():
        if category not in ['files_processed', 'files_redacted', 'errors']:
            stats_output.append(f"{category.capitalize()} - Count: {details['count']}")
            for position in details.get('positions', []):
                stats_output.append(f"  Position: Start {position[0]}, End {position[1]}")
    
    formatted_stats = "\n".join(stats_output)
    
    if stats_type == "stdout":
        print(formatted_stats)
    elif stats_type == "stderr":
        print(formatted_stats, file=sys.stderr)
    else:
        with open(stats_type, 'w') as f:
            f.write(formatted_stats)
        print(f"Statistics written to {stats_type}")

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
    
    stats = {"files_processed": 0, "files_redacted": 0, "errors": 0}

    if os.path.isdir(args.input_path):
        files = [os.path.join(args.input_path, f) for f in os.listdir(args.input_path) if f.endswith('.txt')]
    else:
        files = [args.input_path]
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                original_text = f.read()
            stats["files_processed"] += 1
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            stats["errors"] += 1
            continue
        
        redacted_text = redact_text(original_text, flags, args.concepts)
        output_path = os.path.join(args.output, os.path.basename(file_path).replace('.txt', '.censored'))
        write_output(redacted_text, output_path)
        stats["files_redacted"] += 1

    write_stats(stats, args.stats)

if __name__ == "__main__":
    main()
