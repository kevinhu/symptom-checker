import ujson

from symptom_checker.config import DATA_DIR
from symptom_checker.includes.utils import invert_dict_of_lists

with open(DATA_DIR / "intermediate" / "disease_to_symptoms.json", "r") as f:
    disease_to_symptoms = ujson.load(f)

disease_to_symptoms_ids = {
    disease["disease_code"]: [
        symptom["symptom_hpo_id"] for symptom in disease["symptoms"]
    ]
    for disease in disease_to_symptoms
}

symptoms_to_disease_ids = invert_dict_of_lists(disease_to_symptoms_ids)

with open(DATA_DIR / "processed" / "symptoms_to_disease_ids.json", "w") as f:
    ujson.dump(symptoms_to_disease_ids, f)
