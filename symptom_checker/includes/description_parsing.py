import scispacy
import spacy

from symptom_checker.config import DATA_DIR

nlp = spacy.load("en_core_sci_md")

with open(DATA_DIR / "processed" / "disease_to_info_ids.json", "r") as f:
    disease_to_info_ids = ujson.load(f)

with open(DATA_DIR / "processed" / "symptoms_to_disease_ids.json", "r") as f:
    symptoms_to_disease_ids = ujson.load(f)

with open(DATA_DIR / "processed" / "disease_to_symptoms_complete.json", "r") as f:
    disease_to_symptoms_complete = ujson.load(f)

with open(DATA_DIR / "processed" / "symptom_text_to_ids.json", "r") as f:
    symptom_text_to_ids = ujson.load(f)

with open(DATA_DIR / "processed" / "disease_to_genes_ids.json", "r") as f:
    disease_to_genes_ids = ujson.load(f)


def get_symptoms(text):
    return [phrase.text for phrase in nlp(text).noun_chunks]


# def get_diseases(symptoms):
