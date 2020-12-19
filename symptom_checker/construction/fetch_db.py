from symptom_checker.includes.utils import download_from_url
from symptom_checker.config import DATA_DIR

# diseases
download_from_url(
    "http://www.orphadata.org/data/xml/en_product1.xml",
    DATA_DIR / "raw" / "en_product1.xml",
)

# diseases and symptoms
download_from_url(
    "http://www.orphadata.org/data/xml/en_product4.xml",
    DATA_DIR / "raw" / "en_product4.xml",
)

# diseases and genes
download_from_url(
    "http://www.orphadata.org/data/xml/en_product6.xml",
    DATA_DIR / "raw" / "en_product6.xml",
)
