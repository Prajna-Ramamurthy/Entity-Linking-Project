from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, OWL
import re

# Define the namespaces for skos and umls
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
UMLS = Namespace("http://bioportal.bioontology.org/ontologies/umls/")

# Step 1: Create an RDF graph and parse the Turtle file
g = Graph()
file_path = "/home/prajna/Downloads/LOINC.ttl"
g.parse(file_path, format="turtle")

# Step 2: Extract information from the RDF graph
# In this example, we will extract the labels and CUIs for each class in the ontology.
entities = {}
for class_uri in g.subjects(predicate=RDF.type, object=OWL.Class):
    label = g.value(subject=class_uri, predicate=SKOS.prefLabel)
    cui = g.value(subject=class_uri, predicate=UMLS.cui)

    if label and cui:
        entities[class_uri] = {"label": label, "cui": cui}

# Step 3: Define the gold standard/reference set of CUIs
gold_standard_cuis = [
    "C3842145", "C3174435", "C3476283",  # ... add more gold standard CUIs
]

# Define a regex pattern for valid CUI format
cui_pattern = re.compile(r'^C\d{7}$')

# Step 4: Evaluate performance metrics
true_positives = 0
false_positives = 0
false_negatives = len(gold_standard_cuis)

for info in entities.values():
    extracted_cui = info["cui"]
    if cui_pattern.match(extracted_cui) and extracted_cui in gold_standard_cuis:
        true_positives += 1
        false_negatives -= 1
    else:
        false_positives += 1

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Step 5: Print performance metrics
print("Performance Metrics:")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1_score:.2f}")

# Step 6: Print the extracted information along with gold standard info (optional)
for class_uri, info in entities.items():
    print(f"Class URI: {class_uri}")
    print(f"Label: {info['label']}")
    print(f"Extracted CUI: {info['cui']}")

    if cui_pattern.match(info['cui']):
        if info['cui'] in gold_standard_cuis:
            print("Gold Standard: Yes")
        else:
            print("Gold Standard: No (False Positive)")
    else:
        print("Gold Standard: No (Invalid Format)")

    print("-" * 20)
