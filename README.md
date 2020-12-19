# symptom-checker

Given a natural language query, extract symptom terms and match them to possible diseases.



## How it works

1. Make the database:
   1. Sources of data:
      1. We need to match phenotypes (e.g. symptoms) to diseases, so we use the "Rare diseases with associated phenotypes" dataset from http://www.orphadata.org/cgi-bin/index.php
      2. We'd also like to find genes associated with rare diseases, so we use the "Genes associated with rare diseases" dataset from Orphanet
      3. We'd also like to have a comprehensive set of disease info in general, so we use the "Cross-referencing of rare diseases" dataset from Orphanet
   2. Preprocessing:
      1. Extract a list of all symptom terms from the disease-phenotypes dataset to use for filtering
      2. Convert all datasets to JSON for ease of use
      3. Do any additional key-mapping for final use
2. Build the server:
   1. Take an input sentence, segment with NLTK/SpaCy, extract nouns, and search for conditions as a Django endpoint
   2. Allow for basic sorting/filtering on conditions



## Getting started

First, clone the repo:

```bash
git clone git@github.com:kevinhu/symptom-checker.git
```

Next, install dependencies.

```bash
# if using Poetry:
poetry install 

# if using Pip:
pip3 install -r requirements.txt
```

Installing via Poetry will automatically create a virtual environment. If using Pip, you may want to manually create one before installing, for instance with `python3 -m venv symptom-checker`.

The final JSON dictionaries with disease information and symptom+gene associations are included within the repository. If you would like to regenerate them on your own, run

```bash
# fetch files (originally XMLs)
python ./symptom_checker/construction/fetch_db.py
# convert to intermediate JSONs
python ./symptom_checker/construction/db_to_json.py
# make final database files
python ./symptom_checker/construction/finalize_db.py
```

Finally, to start the server, run

```bash
cd symptom_checker/server && gunicorn server.wsgi
```

This will start the server on `http://localhost:8000` by default with the endpoint of interest at `http://localhost:8000/check_symptoms`, accessible via POST.

The parameters for the endpoint are as follows:

- `description` (required): the plaintext query to analyze.
- `min_frequency`: the minimum frequency of a symptom in a disease to consider. Case-sensitive options include "Very rare", "Occasional", "Frequent", "Very frequent", and "Obligate", in order of exclusivity. If not specified, defaults to "Very rare".
- `sort_method` (required): how to sort returned diseases. Options are "first_matched_symptom" (show diseases in order of position of first matched symptom in text) and "num_matched_symptoms" (number of supplied symptoms matching the disease).

The endpoint is accessible via methods such as `curl`. For instance, use

```
curl \
		-X POST \
    --data-urlencode "description=microencephaly, cataracts, and autophagic vacuoles" \
    --data-urlencode "min_frequency=Occasional" \
    --data-urlencode "sort_method=num_matched_symptoms" \
    localhost:8000/check_symptoms/
```



## Test cases

```
""
"."
" "
"The patient had a seizure"
"The patient has seizures and autism"
"The patient has seizures and seizures and autism"
"The patient has seizures, autism, and corneal dystrophy"
"The patient has seizures but no autism"
"The patient has seizures but not autism"
"Seizures, autism, microcephaly"
"Seizures, seizures, seizures"
```

