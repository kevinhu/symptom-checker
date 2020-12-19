from typing import List

import scispacy
import spacy
import ujson

from symptom_checker.config import DATA_DIR
from symptom_checker.includes.utils import (
    remove_duplicates_in_order,
    flatten_list_of_lists,
)

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


def get_symptoms(text: str) -> List[str]:

    noun_chunks = [phrase.text for phrase in nlp(text).noun_chunks]
    noun_chunks = remove_duplicates_in_order(noun_chunks)

    return [phrase.text for phrase in nlp(text).noun_chunks]


def get_diseases(symptoms: List[str]) -> List[str]:

    symptom_ids = [symptom_text_to_ids.get(symptom) for symptom in symptoms]

    # removed non-matched terms
    symptom_ids = [symptom_id for symptom_id in symptom_ids if symptom_id is not None]

    # flatten list of lists
    symptom_ids = flatten_list_of_lists(symptom_ids)

    # remove any duplicate symptom IDs (if two text terms point to the same ID)
    symptom_ids = remove_duplicates_in_order(symptom_ids)

    disease_ids = [
        symptoms_to_disease_ids.get(symptom_id) for symptom_id in symptom_ids
    ]

    return disease_ids
