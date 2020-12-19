import scispacy
import spacy

nlp = spacy.load("en_core_sci_md")


def get_symptoms(text):
    return [phrase.text for phrase in nlp(text).noun_chunks]
