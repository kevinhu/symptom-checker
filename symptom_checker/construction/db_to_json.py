import xml.etree.ElementTree as ET
import ujson

from symptom_checker.config import DATA_DIR
from symptom_checker.includes.db_processing import process_disease

# parse in XML
with open(DATA_DIR / "raw" / "en_product1.xml", "r", encoding="ISO-8859-1") as file:
    diseases_xml = file.read()

# list of diseases
diseases_xml = ET.XML(diseases_xml).find("DisorderList")

# parse diseases XML
diseases = [process_disease(elem) for elem in diseases_xml]

with open(DATA_DIR / "intermediate" / "diseases.json", "w") as f:
    ujson.dump(diseases, f)
