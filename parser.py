from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, OWL

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

# Step 3: Print the extracted information (optional)
for class_uri, info in entities.items():
    print(f"Class URI: {class_uri}")
    print(f"Label: {info['label']}")
    print(f"CUI: {info['cui']}")
    print("-" * 20)

# Step 4: Train the entity linking model (if required)
# In this simplified example, we won't train a model as it requires more complex techniques.

# Step 5: Save the extracted information to a file (optional)
# Replace 'path_to_output_file.txt' with the path where you want to save the extracted information.
with open("path_to_output_file.txt", "w") as f:
    for class_uri, info in entities.items():
        f.write(f"Class URI: {class_uri}\n")
        f.write(f"Label: {info['label']}\n")
        f.write(f"CUI: {info['cui']}\n")
        f.write("-" * 20 + "\n")
