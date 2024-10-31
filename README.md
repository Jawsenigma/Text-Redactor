# Redactor Project

**Author**: Tanmay Saxena

## Project Description

This project is a Python package designed to redact sensitive information from text. The package includes functions to remove or obfuscate identifiable details like emails, dates, phone numbers, specific concepts, gendered pronouns, names, and addresses. Each function can be applied individually to process text for enhanced privacy and data protection.

## How to Install

1. Clone the repository:
    ```bash
    git clone https://github.com/username/redactor.git
    cd redactor
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

To redact information from a text file, use the individual redactor functions in `redactor.py`, such as `email_redactor`, `date_redactor`, etc., depending on the information you want to conceal.

Example usage:
```python
from redactor import email_redactor, date_redactor, phone_redactor

text = "Contact me at example@example.com on January 1, 2022. My phone is 123-456-7890."
redacted_text = phone_redactor(date_redactor(email_redactor(text)))
print(redacted_text)  # Outputs text with email, date, and phone number redacted
```

## Functions

### `email_redactor`
   - Identifies and redacts email addresses in the provided text.
   - Example: Converts `example@example.com` to `█`.

### `date_redactor`
   - Identifies and redacts dates in formats like "January 1, 2022".
   - Example: Converts `January 1, 2022` to `█`.

### `phone_redactor`
   - Identifies and redacts phone numbers in various formats.
   - Example: Converts `123-456-7890` to `█`.

### `concept_redactor`
   - Redacts specific words or concepts defined by the user.
   - Example: Converts `kids` in `The kids are playing.` to `█`.

### `gender_redactor`
   - Identifies and redacts gendered pronouns such as "he" and "she".
   - Example: Converts `He said she would come.` to `█ said █ would come.`

### `name_redactor`
   - Identifies and redacts personal names based on a list of common names or context.
   - Example: Converts `John Doe went to the store.` to `█ went to the store.`

### `address_redactor` *(optional)*
   - (Commented out in test file) Identifies and redacts addresses.
   - Example: Converts `123 Main Street` to `█`.

## Testing

Unit tests are available in `test_redactor.py`, providing automated testing for each redaction function. To run tests:
```bash
python -m unittest test_redactor.py
```

### Example Tests

1. **Email Redaction**: Verifies that email addresses are replaced with `█`.
2. **Date Redaction**: Confirms that dates are redacted.
3. **Phone Redaction**: Ensures phone numbers are removed from the text.
4. **Concept Redaction**: Tests custom word/phrase redaction.
5. **Gender Redaction**: Checks that gendered pronouns are obfuscated.
6. **Name Redaction**: Ensures personal names are redacted.
7. **Address Redaction**: (Optional) Redacts specific address information.

## Considerations and Assumptions

- **Text Formatting**: The functions assume specific formats for emails, dates, and phone numbers.
- **User-Defined Concepts**: `concept_redactor` relies on user input to define which words to redact.
- **Sensitive Information**: This package focuses on common personally identifiable information and may need adjustments for other types of sensitive data.

--- 