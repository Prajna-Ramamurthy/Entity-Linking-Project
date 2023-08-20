# Entity-Linking-Project
Summer Research Project for IEEE CS on Entity Linking for Ambiguity Removal

### Dataset has been downloaded from https://bioportal.bioontology.org/ontologies/LOINC

This project demonstrates two different approaches for medical entity disambiguation, focusing on mapping medical terms to their corresponding CUIs (Concept Unique Identifiers). The goal is to improve the accuracy of interpreting and classifying medical text data.

### File 1: Entity Linking with spaCy and RDFLib
File: `entity_linking_with_spacy_and_rdflib.py`

This file showcases how to use the spaCy NLP library and RDFLib to perform entity linking for medical terms. It leverages RDF knowledge graphs to link medical terms to their unique CUIs, allowing for more accurate and context-aware disambiguation.

### File 2: Medical Term Disambiguation with TF-IDF and SVM
File: `medical_term_disambiguation_tfidf_svm.py`

This file demonstrates a different approach using TF-IDF vectorization and Support Vector Machines (SVM) for medical term disambiguation. It uses machine learning techniques to classify medical texts and map them to appropriate CUIs, helping to mitigate ambiguity in medical terminology.

## Usage
1. **Entity Linking with spaCy and RDFLib:**
   - Ensure you have the required libraries (`rdflib` and `spacy`) installed.
   - Run the script `entity_linking_with_spacy_and_rdflib.py`.
   - The script will use spaCy for NLP processing and RDFLib to link medical terms to CUIs.

2. **Medical Term Disambiguation with TF-IDF and SVM:**
   - Install the necessary libraries (`scikit-learn` and `numpy`) if not already installed.
   - Run the script `medical_term_disambiguation_tfidf_svm.py`.
   - The script will demonstrate TF-IDF vectorization and SVM classification for medical entity disambiguation.

## Results
Both approaches aim to enhance the accuracy of medical term disambiguation. The first approach leverages semantic knowledge from RDF graphs, while the second approach employs machine learning techniques. Feel free to experiment with different texts and terms to observe the disambiguation results.

## Acknowledgements
The project was inspired by the need for accurate medical text processing and the concept of entity linking in natural language processing.
