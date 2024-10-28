import unittest
from redactor import email_redactor, date_redactor, phone_redactor, concept_redactor, gender_redactor, name_redactor, address_redactor

class TestRedactor(unittest.TestCase):

    def test_email_redactor(self):
        text = "Contact me at example@example.com for more information."
        self.assertIn('█', email_redactor(text))

    def test_date_redactor(self):
        text = "The event is scheduled for January 1, 2022."
        self.assertIn('█', date_redactor(text))

    def test_phone_redactor(self):
        text = "Call me at 123-456-7890."
        redacted_text = phone_redactor(text)
        self.assertIn('█', redacted_text)
        self.assertNotIn('123-456-7890', redacted_text)

    def test_concept_redactor(self):
        text = "The kids are playing in the park."
        concepts = ["kids"]
        redacted_text = concept_redactor(text, concepts)
        self.assertIn('█', redacted_text)

    def test_gender_redactor(self):
        text = "He said she would arrive soon."
        redacted_text = gender_redactor(text)
        self.assertIn('█', redacted_text)

    def test_name_redactor(self):
        text = "John Doe went to the store."
        redacted_text = name_redactor(text)
        self.assertIn('█', redacted_text)

    # def test_address_redactor(self):
    #     text = "123 Main Street is where I live."
    #     redacted_text = address_redactor(text)
    #     self.assertIn('█', redacted_text)
    #     self.assertNotIn('123 Main Street', redacted_text)

if __name__ == '__main__':
    unittest.main()