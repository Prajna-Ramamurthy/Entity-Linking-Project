from rdflib import Graph, Namespace
from rdflib.namespace import RDF, OWL
import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

# Define the namespaces for skos and umls
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
UMLS = Namespace("http://bioportal.bioontology.org/ontologies/umls/")

# Step 1: Create an RDF graph and parse the Turtle file
g = Graph()
file_path = "/home/prajna/Documents/summer23/IEEE_CS/final/LOINC.ttl"
g.parse(file_path, format="turtle")

# Step 2: Extract information from the RDF graph
# In this example, we will extract the labels and CUIs for each class in the ontology.
entities = []
for class_uri in g.subjects(predicate=RDF.type, object=OWL.Class):
    label = g.value(subject=class_uri, predicate=SKOS.prefLabel)
    cui = g.value(subject=class_uri, predicate=UMLS.cui)
    if label and cui:
        entities.append({"label": label, "cui": cui})

# Convert the extracted data to a DataFrame for ML
import pandas as pd
df = pd.DataFrame(entities)

# Extract the string values from the RDF literals
df['cui'] = df['cui'].apply(lambda x: str(x))

# Define a regex pattern for valid CUI format
cui_pattern = re.compile(r'^C\d{7}$')

# Add a new column indicating whether the CUI is valid based on the pattern
df['valid_cui'] = df['cui'].apply(lambda x: cui_pattern.match(x) is not None)

# Encode the CUIs using label encoding
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
df['cui_encoded'] = encoder.fit_transform(df['cui'])

# Step 3: Split the data into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Step 4: Train a Decision Tree classifier
X_train = train_df[['cui_encoded']]
y_train = train_df['valid_cui']

classifier = DecisionTreeClassifier(random_state=42)
classifier.fit(X_train, y_train)

# Step 5: Evaluate the classifier on the test set
X_test = test_df[['cui_encoded']]
y_test = test_df['valid_cui']
y_pred = classifier.predict(X_test)

# Calculate precision, recall, and F1-score
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Step 6: Save the performance metrics to a separate file
metrics_file_path = "performance_metrics.txt"
with open(metrics_file_path, "w") as f:
    f.write("Performance Metrics:\n")
    f.write(f"Precision: {precision:.2f}\n")
    f.write(f"Recall: {recall:.2f}\n")
    f.write(f"F1-Score: {f1:.2f}\n")

# Step 7: Print the head of the extracted information (optional)
print("The extracted information and performance metrics have been saved to file.")
count = 1
print("The following is the first five sets of output.")
for entity in entities:
    if count <= 5:
        print(f"Label: {entity['label']}")
        print(f"CUI: {entity['cui']}")
        count += 1
