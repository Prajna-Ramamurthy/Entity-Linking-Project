from rdflib import Graph, Namespace
from rdflib.namespace import RDF, OWL
import spacy
from spacy.matcher import Matcher

# Load the LOINC TTL file
g = Graph()
g.parse("/home/prajna/Downloads/LOINC.ttl", format="turtle")

# Define namespaces
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
umls = Namespace("http://bioportal.bioontology.org/ontologies/umls/")

# Extract information from the RDF graph
entities = {}
for class_uri in g.subjects(predicate=RDF.type, object=OWL.Class):
    label = g.value(subject=class_uri, predicate=skos.prefLabel)
    cui = g.value(subject=class_uri, predicate=umls.cui)

    if label and cui:
        entities[class_uri] = {"label": label, "cui": cui}

# Initialize spaCy with a blank English model
nlp = spacy.blank("en")
matcher = Matcher(nlp.vocab)

# Add patterns for LOINC concepts
for class_uri, info in entities.items():
    label = info["label"]
    pattern = [{"LOWER": token.lower()} for token in label.split()]
    matcher.add(info["cui"], [pattern])

# Sample texts
texts = [
    "None noted",
    "For how long in total have you used oral contraceptives:Time:Pt:^Patient:Qn:PhenX",
    "Ocular alignment and motility",
    "Lutropin^7th specimen post XXX challenge:ACnc:Pt:Ser/Plas:Qn"
]

# Annotations with correct CUI values
annotations = {
    "None noted": "C3842145",
    "For how long in total have you used oral contraceptives:Time:Pt:^Patient:Qn:PhenX": "C3174435",
    "Ocular alignment and motility": "C3476283",
    "Lutropin^7th specimen post XXX challenge:ACnc:Pt:Ser/Plas:Qn": "C0943547"
}

# Initialize variables for evaluation
true_positives = 0
false_positives = 0
false_negatives = 0

# Process the texts and match with LOINC concepts
for text in texts:
    doc = nlp(text)
    matches = matcher(doc)
    expected_cui = annotations.get(text, None)

    if expected_cui:
        if any(nlp.vocab.strings[match_id] == expected_cui for match_id, _, _ in matches):
            true_positives += 1
        else:
            false_negatives += 1
    else:
        if len(matches) > 0:
            false_positives += 1

# Calculate precision, recall, and F1-score
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Display the metrics
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")
