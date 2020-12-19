from typing import Dict, Union, List, Any
import xml.etree.ElementTree as ET


def process_disease(disease_elem: ET.XML) -> Dict[str, Union[str, List[Any]]]:

    """
    Process a disease element in the <DisorderList> group for en_product1.
    Args:
        disease_elem:
            ElementTree object corresponding to the disease.
    Returns:
        dictionary of disease attributes
    """

    disease_code = disease_elem.find("OrphaCode").text
    disease_link = disease_elem.find("ExpertLink").text
    disease_name = disease_elem.find("Name").text

    disease_synonyms = [elem.text for elem in disease_elem.find("SynonymList")]

    disease_type = disease_elem.find("DisorderType/Name").text
    disease_group = disease_elem.find("DisorderGroup/Name").text

    def process_reference(reference_elem):

        reference_source = reference_elem.find("Source").text
        reference_reference = reference_elem.find("Reference").text

        # get nested relation and validation info
        relation_elem, icd_relation_elem, validation_elem = (
            reference_elem.find("DisorderMappingRelation/Name"),
            reference_elem.find("DisorderMappingICDRelation/Name"),
            reference_elem.find("DisorderMappingValidationStatus/Name"),
        )

        reference_relation = ""
        reference_icd_relation = ""
        reference_validation = ""

        # overwrite values if exists
        if relation_elem is not None:
            reference_relation = relation_elem.text

        if icd_relation_elem is not None:
            reference_icd_relation = icd_relation_elem.text

        if validation_elem is not None:
            reference_validation = validation_elem.text

        return {
            "reference_source": reference_source,
            "reference_reference": reference_reference,
            "reference_relation": reference_relation,
            "reference_icd_relation": reference_icd_relation,
            "reference_validation": reference_validation,
        }

    references_elem = disease_elem.find("ExternalReferenceList")
    disease_references = [process_reference(elem) for elem in references_elem]

    disease_summary_elem = disease_elem.find(
        "SummaryInformationList/SummaryInformation/TextSectionList/TextSection/Contents"
    )

    disease_summary = ""

    # overwrite if exists
    if disease_summary_elem is not None:

        disease_summary = disease_summary_elem.text

    return {
        "disease_code": disease_code,
        "disease_link": disease_link,
        "disease_name": disease_name,
        "disease_synonyms": disease_synonyms,
        "disease_type": disease_type,
        "disease_group": disease_group,
        "disease_references": disease_references,
        "disease_summary": disease_summary,
    }
