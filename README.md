# Text-Redactor

**Author**: Tanmay Saxena

## Project Description

The **Text-Redactor** is a Python package designed to redact sensitive information from text. It provides functions to remove or obfuscate identifiable details such as emails, dates, phone numbers, names, addresses, gendered pronouns, and user-defined concepts. This tool is ideal for protecting personal data in documents and ensuring compliance with privacy standards.

## Features

- **Email Redaction**: Obfuscates email addresses.
- **Date Redaction**: Redacts dates in multiple formats.
- **Phone Number Redaction**: Redacts phone numbers in various formats.
- **Name Redaction**: Detects and redacts personal names.
- **Address Redaction**: Redacts physical addresses.
- **Gendered Pronoun Redaction**: Obfuscates gender-specific terms.
- **Concept Redaction**: Allows users to define custom words or phrases to redact.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Jawsenigma/cis6930fa24-project1.git
    cd cis6930fa24-project1
    ```

2. Install dependencies using `pipenv`:
    ```bash
    pipenv install
    ```

## Usage

You can use the individual redactor functions from `redactor.py` to redact specific types of information from text.

### Command-Line Usage:
Given below is an example command to redact information from a text file via the command line:
```bash
pipenv run python redactor.py --input '*.txt' --names --dates --phones --address --concept 'kids' --output 'files/' --stats stderr
```
You can specify flags for different types of sensitive data to redact (e.g., `--emails`, `--dates`).

### Available Flags:
- `--emails`: Redact email addresses.
- `--dates`: Redact dates.
- `--phones`: Redact phone numbers.
- `--genders`: Redact gender-specific terms.
- `--names`: Redact personal names.
- `--addresses`: Redact physical addresses.
- `--concepts`: Redacts any text related to the concept given eg: 'child', 'prison' etc.

## Functions Overview

| Function          | Description                                                                 | Example Input               | Example Output |
|-------------------|-----------------------------------------------------------------------------|-----------------------------|----------------|
| `email_redactor`   | Identifies and redacts email addresses.                                     | `example@example.com`        | `█`            |
| `date_redactor`    | Identifies and redacts dates in various formats.                            | `January 1, 2022`            | `█`            |
| `phone_redactor`   | Identifies and redacts phone numbers in common formats.                     | `123-456-7890`               | `█`            |
| `concept_redactor` | Redacts specific user-defined words or phrases.                             | `The kids are playing.`      | `The █ are playing.` |
| `gender_redactor`  | Identifies and redacts gendered pronouns like "he" and "she".               | `He said she would come.`    | `█ said █ would come.` |
| `name_redactor`    | Identifies and redacts personal names based on a list of common names.      | `John Doe went to the store.`| `█ went to the store.` |
| `address_redactor` | Identifies and redacts physical addresses.                                  | `123 Main Street`            | `█`            |

## Running Tests

Unit tests are available in the file `test_redactor.py`. To run all tests using pytest:

```bash
pipenv run python -m pytest
```

### Example Test Cases:
1. **Email Redaction**: Ensures that email addresses are obfuscated.
2. **Date Redaction**: Confirms that dates are properly redacted.
3. **Phone Number Redaction**: Verifies that phone numbers are removed.
4. **Concept Redaction**: Tests user-defined word/phrase redaction.
5. **Gender Pronoun Redaction**: Ensures gendered pronouns are obfuscated.
6. **Name Redaction**: Confirms that personal names are detected and redacted.
7. **Address Redaction** : Tests address obfuscation.

## Statistics Output

When using the tool with the `--stats` option, it generates a report with details about the redacted content:

1. **Files Processed**: Number of files processed.
2. **Files Redacted**: Number of files where sensitive information was found and redacted.
3. **Errors**: Number of files that encountered errors during processing.

For each type of sensitive information (emails, dates, etc.), it will also display:
- **Count**: Total number of occurrences redacted.
- **Details**: Starting and ending index positions of each redacted term.

Example usage with statistics output:
```bash
pipenv run python redactor.py --input <input_file> --output <output_file> --emails --stats
```

## Bugs and Assumptions

### 1. **spaCy Bugs and Limitations**
   - **Inconsistent NER Recognition**: spaCy may not always recognize entities like names or dates correctly, especially in domain-specific texts or non-standard formats. For example, names with unusual spellings or abbreviations might be missed.
   - **False Positives/Negatives**: spaCy can sometimes misclassify entities, leading to either over-redaction (redacting non-sensitive information) or under-redaction (missing sensitive data).
   - **Limited Customization**: Out-of-the-box spaCy models may not perform well for specialized domains without additional fine-tuning.

### 2. **NLTK Bugs and Limitations**
   - **Limited NER Accuracy**: NLTK's default NER tagger may not accurately detect certain entities like dates or names, especially in informal or complex text formats.
   - **No Built-in Support for Dates/Times**: NLTK does not natively support date/time recognition, requiring custom regex patterns or external libraries to handle such cases.

### 3. **Regex-Based Redaction Issues**
   - **Address Redaction**: Regex patterns used for redacting addresses may miss non-standard address formats (e.g., international addresses) or produce false positives by matching non-address text.
   - **Phone Number Redaction**: Regex patterns for phone numbers may fail to capture all variations, particularly international formats or numbers written in unconventional ways.

### 4. **Concept Redaction Challenges**
   - **Synonym Handling**: The `concept_redactor` function relies on WordNet (via NLTK) to identify synonyms, which may not cover all relevant terms in specialized domains, leading to incomplete redactions.
   - **Contextual Misinterpretation**: The function does not consider context, which can lead to over-redaction if a word has multiple meanings (e.g., "bank" referring to a riverbank vs. a financial institution).

### 5. **Gender Redaction Issues**
   - **Incomplete Pronoun Coverage**: The predefined list of gendered terms may miss newer or less common pronouns (e.g., "xe", "ze"), requiring manual updates to handle evolving language use.

### 6. **General Assumptions**
   - **Standard Text Formats**: The tool assumes that text follows conventional formats for emails, dates, phone numbers, etc. Non-standard formats may result in missed redactions.
   - **Pre-trained Model Limitations**: Both spaCy and NLTK models are trained on general-purpose data and may not perform well on domain-specific texts without additional training.


## Considerations

- The package assumes specific formats for emails, dates, and phone numbers based on common patterns.
- Custom concept redactions rely on user input to define which terms should be censored.
- The tool focuses on common personally identifiable information (PII) but can be extended for other types of sensitive data.
