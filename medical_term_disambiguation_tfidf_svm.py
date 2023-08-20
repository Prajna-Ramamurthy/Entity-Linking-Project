import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Pre-processing
def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    return text

# Synthetic texts and corresponding CUIs
synthetic_texts = [
    "For how long in total have you used oral contraceptives:Time:Pt:^Patient:Qn:PhenX",
    "Ocular alignment and motility",
    "Lutropin^7th specimen post XXX challenge:ACnc:Pt:Ser/Plas:Qn",
    "IgG.monoclonal | Serum | Chemistry - non-challenge",
    "Influenza A virus not detected, Influenza B virus inconclusive",
    "Norepinephrine^pre 300 ug clonidine PO",
    "Glycine receptor Ab | Cerebral spinal fluid | Serology - non-micro",
    "Desflurane:VFr/PPres:Pt:Gas delivery system:Qn"
]

synthetic_cuis = [
    "C3174435",
    "C3476283",
    "C0943547",
    "C5168892",
    "C4698115",
    "C5148274",
    "C5427135",
    "C4266342"
]

# Preprocess the texts
preprocessed_texts = [preprocess_text(text) for text in synthetic_texts]

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(preprocessed_texts)
test_vectors = vectorizer.transform(preprocessed_texts)

# Create a Support Vector Machine classifier
classifier = SVC()
classifier.fit(train_vectors, synthetic_cuis)

# Predict CUIs for test texts
predicted_cuis = classifier.predict(test_vectors)

# Evaluate the performance of the classifier
report = classification_report(synthetic_cuis, predicted_cuis, zero_division=1)
print("Classification Report:")
print(report)

