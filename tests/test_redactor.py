import pytest
from redactor import (
    email_redactor,
    date_redactor,
    phone_redactor,
    concept_redactor,
    gender_redactor,
    name_redactor,
    address_redactor,
    redact_text,
)
import warnings


def test_email_redactor():
    result = email_redactor("Contact us at example@example.com")
    assert "Contact us at" in result
    assert "████████████" in result  

def test_date_redactor():
    result = date_redactor("Today's date is 01/01/2024.")
    assert "Today's date is" in result
    assert "██████" in result  

def test_phone_redactor():
    result = phone_redactor("Call me at (123) 456-7890.")
    assert "Call me at" in result
    assert "███████████" in result  

def test_concept_redactor():
    result = concept_redactor("Artificial Intelligence is fascinating.", "Intelligence")
    assert "AI" not in result  
    assert "██████████████████████████████" in result  

def test_gender_redactor():
    result = gender_redactor("He is a good boy and she is a good girl.")
    assert "He is a good" not in result  
    assert "she is a good" not in result  
    assert "██" in result  

def test_name_redactor():
    result = name_redactor("Alice and Bob went to the market.")
    assert "Alice and" not in result 
    assert "Bob" not in result  
    assert "█████ and ███" in result  

def test_address_redactor():
    result = address_redactor("I live at 123 Main St.")
    assert "123 Main St." not in result  
    assert "I live at ███████████." in result  

def test_redact_text():
    flags = {
        'dates': True,
        'phones': True,
        'genders': True,
        'names': True,
        'concepts': False,
        'addresses': True,
        'emails': True
    }
    text = "Alice's email is alice@example.com and her phone is (123) 456-7890. The date is 01/01/2024."

    result = redact_text(text, flags, [])
    
    assert "Alice's email is" not in result  
    assert "her phone is" not in result  
    
    assert "██████'s email is" in result or "█ █ █ █ █ 's email is" in result  


if __name__ == "__main__":
    pytest.main()
