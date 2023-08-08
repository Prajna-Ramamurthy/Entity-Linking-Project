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

# Step 3: Prepare a gold standard/reference set of CUIs
# Replace these with actual CUIs from your gold standard/reference set
gold_standard_cuis = [
    "C3842145", "C3174435", "C3476283", "C0943547", "C5168892",
    "C4698115", "C5148274", "C5427135", "C4266342", "C3483252",
    "C0803245", "C1525337", "C4285199", "C3846324", "C1829630",
    "C4072699", "C3172504", "C4319297", "C5161017", "C4255024",
    "C4255020", "C4255364", "C0802129", "C4263525", "C4255045",
    "C4263526", "C5214826", "C4255028", "C4255027", "C5152109",
    "C5452283", "C1543786", "C5181614", "C0459471", "C0364386",
    "C1641518", "C1291910", "C2718181", "C4483471", "C0369927",
    "C4297809", "C4483540", "C4482619", "C4319142", "C1544486",
    "C4034375", "C5178954", "C0883026", "C5211767", "C4068722",
    "C5213399", "C3845648", "C0941326", "C0484586", "C5166032",
    "C0802248", "C3176493", "C0944457", "C5177847", "C3541867",
    "C3846931", "C1415825", "C0019728", "C0019759", "C2738089",
    "C1440752", "C0019751", "C1440751", "C1440750", "C0019765",
    "C0019761", "C5162314", "C4532599", "C0944961", "C0944409"
]
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

print("Performance Metrics:")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1_score:.2f}")

'''# Step 5: Print the extracted information (optional)
for class_uri, info in entities.items():
    print(f"Class URI: {class_uri}")
    print(f"Label: {info['label']}")
    print(f"CUI: {info['cui']}")
    print("-" * 20)'''

# Step 6: Save the extracted information to a file (optional)
# Replace 'path_to_output_file.txt' with the path where you want to save the extracted information.
with open("path_to_output_file.txt", "w") as f:
    for class_uri, info in entities.items():
        f.write(f"Class URI: {class_uri}\n")
        f.write(f"Label: {info['label']}\n")
        f.write(f"CUI: {info['cui']}\n")
        f.write("-" * 20 + "\n")

# Step 7: Save the performance metrics to a file (optional)
# Replace 'path_to_metrics_file.txt' with the path where you want to save the metrics.
with open("path_to_metrics_file.txt", "w") as f:
    f.write("Performance Metrics:\n")
    f.write(f"Precision: {precision:.2f}\n")
    f.write(f"Recall: {recall:.2f}\n")
    f.write(f"F1-Score: {f1_score:.2f}\n")

