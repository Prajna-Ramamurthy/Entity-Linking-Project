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

# Define a regex pattern for valid CUI format
cui_pattern = re.compile(r'^C\d{7}$')

# Step 3: Evaluate performance metrics
true_positives = 0
false_positives = 0

for info in entities.values():
    extracted_cui = info["cui"]
    if cui_pattern.match(extracted_cui):
        true_positives += 1
    else:
        false_positives += 1

# Calculate precision, recall, and F1-score
total_predicted = true_positives + false_positives
precision = true_positives / total_predicted if total_predicted > 0 else 0

# Since there is no gold standard, recall and F1-score will be based solely on the extracted CUIs
recall = precision
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Step 4: Print performance metrics
print("Performance Metrics:")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1_score:.2f}")

# Step 5: Save the extracted information to a file
output_file_path = "extracted_information.txt"
with open(output_file_path, "w") as f:
    for class_uri, info in entities.items():
        f.write(f"Class URI: {class_uri}\n")
        f.write(f"Label: {info['label']}\n")
        f.write(f"CUI: {info['cui']}\n")
        f.write("-" * 20 + "\n")

# Step 6: Save the performance metrics to a separate file
metrics_file_path = "performance_metrics.txt"
with open(metrics_file_path, "w") as f:
    f.write("Performance Metrics:\n")
    f.write(f"Precision: {precision:.2f}\n")
    f.write(f"Recall: {recall:.2f}\n")
    f.write(f"F1-Score: {f1_score:.2f}\n")


# Step 7: Print the head of the extracted information (optional)
print("The extracted information and performance metrics have been saved to file. The following is the first five sets of output.")
count = 1
for class_uri, info in entities.items():
    if count <= 5:
        print(f"Class URI: {class_uri}")
        print(f"Label: {info['label']}")
        print(f"CUI: {info['cui']}")
        count = count + 1
