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
    "Desflurane:VFr/PPres:Pt:Gas delivery system:Qn",
    "3-Hydroxyglutarate:SCnc:Pt:Bld.dot:Qn",
    "Non-primary surgical procedure to other regional sites",
    "2-Methylglutaconate",
    "Oxygen.alveolar",
    "Bacterial heat-labile enterotoxin LT gene",
    "Views & Guidance for injection of non-vascular shunt:Find:Pt:XXX:Doc:RF",
    "Coumaphos | XXX | Drug toxicology",
    "pH:LsCnc:Pt:BldMV:Qn",
    "Supersaturation panel",
    "Referring physician phone number",
    "Tobacco smoking status.tobacco smoker",
    "Alternaria alternata Ab.IgE|ACnc|Pt|ANYBldSerPl",
    "Send document that conforms to CDP Set 1 R1.1 template",
    "Send document that conforms to CDP Set 1 R1.0 template",
    "Aldosterone and renin concentration panel | Plasma | Chemistry Panels",
    "Norfentanyl:PrThr:Pt:TissCo:Ord:Confirm",
    "Multisection perfusion^W stress+W radionuclide IV:Find:Pt:Chest>Heart:Doc:NM.SPECT",
    "Sporothrix schenckii Ab | Serum | Microbiology",
    "Interpretation",
    "Estriol:MCnc:Pt:Ser/Plas:Qn",
    "Glucose:MCnc:Pt:BldV:Qn",
    "Streptococcus pneumoniae 14 Ab",
    "Rh immune globulin screen",
    "Risk assessment and screening note",
    "Streptococcus pneumoniae 3 Ab",
    "HER2:PrThr:Pt:Breast cancer specimen:Ord:Immune stain",
    "Streptococcus pneumoniae Danish serotype 9N Ab.IgG^2nd specimen/1st specimen:Ratio:Pt:Ser:Qn",
    "Externally defined clinical data elements",
    "QRS terminal amplitude.lead V2 | Heart | EKG measurements",
    "Electrolytes 3 panel",
    "Deterrents of most severe suicidal ideation:Find:Lifetime:^Patient:Ord:C-SSRS",
    "NEI eyeGENE electrooculogram",
    "Evaluation and management of workers compensation note | {Setting} | Document ontology",
    "Limitation on one side",
    "Para nitrophenol/Creatinine:SRto:Pt:Urine:Qn",
    "Glucose^2H post meal:MCnc:Pt:Bld:Qn",
    "Goosefoot (Chenopodium album) IgG4 | Serum | Allergy",
    "Barbital cutoff:MCnc:Pt:Urine:Qn:Screen",
    "Dysphoria - irritable impatient:Find:Pt:^Patient:Ord:DI-PAD CGP V 1.4",
    "Producer code:Type:Pt:Contact lens.prescription.right:Nom",
    "Porcine circovirus type 2 IgG | XXX | Microbiology",
    "Adolescent depression screening assessment",
    "Transaldolase:CCnt:Pt:Fibroblasts:Qn",
    "HYAL1 gene",
    "HLA-A",
    "HLA-DP",
    "E wave/A wave",
    "HLA-A+B+C",
    "HLA-C",
    "HLA-A+B+Bw",
    "4-Hydroxyphenylpyruvate/Creatinine:SRto:Pt:Urine:Qn",
    "Correction text:Find:Pt:Contact lens.left:Nar",
    "Parasites | Gastric fluid | Microbiology",
    "HLA-A & B & DRB & DQB1 panel:Type:Pt:Bld/Tiss:-:Low resolution",
    "Amobarbital | Vitreous fluid | Drug toxicology",
    "Administrative note:Find:Pt:{Setting}:Doc:Physical medicine and rehab",
    "Cefepime:Susc:Pt:Isolate:OrdQn",
    "Ephedrine+Pseudoephedrine:PrThr:Pt:Ser/Plas:Ord",
    "Porcine circovirus type 2 RFLP pattern | Isolate | Microbiology",
    "Views for bone density:Zscore:Pt:Lower extremity.left>Hip:Qn:DXA",
    "Thyroxine.free^4th specimen post XXX challenge:SCnc:Pt:Ser/Plas:Qn",
    "Travelled to country 5 years ago",
    "Cognition Knowledge",
    "Multisection for pulmonary embolus^W contrast IV",
    "Source of follow-up information",
    "Bumetanide:MCnc:Pt:Urine:Qn"
]

synthetic_cuis = [
    "C3174435",
    "C3476283",
    "C0943547",
    "C5168892",
    "C4698115",
    "C5148274",
    "C5427135",
    "C4266342",
    "C4285199",
    "C3846324",
    "C1829630",
    "C4072699",
    "C3172504",
    "C4319297",
    "C5161017",
    "C0802129",
    "C4263525",
    "C4255045",
    "C4263526",
    "C5214826",
    "C4255028",
    "C4255027",
    "C5152109",
    "C5452283",
    "C1543786",
    "C5181614",
    "C0459471",
    "C0364386",
    "C0364386",
    "C4483471",
    "C0369927",
    "C4297809",
    "C4483540",
    "C4482619",
    "C4319142",
    "C4034375",
    "C5178954",
    "C0883026",
    "C5211767",
    "C4068722",
    "C5213399",
    "C3845648",
    "C0941326",
    "C0484586",
    "C5166032",
    "C0941326",
    "C3176493",
    "C0944457",
    "C5177847",
    "C3541867",
    "C3846931",
    "C1415825",
    "C0019728",
    "C0019759",
    "C2738089",
    "C1440752",
    "C0019751",
    "C1440751",
    "C0944961",
    "C0944409",
    "C5176237",
    "C4036495",
    "C5152750",
    "C4297971",
    "C0945074",
    "C0365823",
    "C5177850",
    "C4265815",
    "C0945264",
    "C3166474",
    "C0947293",
    "C5145049",
    "C0807975",
    "C0945264"
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
