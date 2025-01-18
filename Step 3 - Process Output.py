import numpy as np
import pandas as pd
import glob
import xml.etree.ElementTree as ET
import re
from collections import defaultdict
from tqdm import tqdm

def get_cui_list(feature):
    cui_list = []
    with open(f'./CUI/{feature}_umls_cui_clean.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            cui_list.append(line.split("|")[-1].strip())
    return cui_list

def assign_status(xmi_file, cui_list):
    status = "U"
    order = {"A": 5, "N": 4, "H": 3, "X": 2, "U": 1}
    # Load and parse the XMI file
    tree = ET.parse(xmi_file)
    root = tree.getroot()
    
    # Define namespace map
    namespaces = {
        'refsem': 'http:///org/apache/ctakes/typesystem/type/refsem.ecore',
        'textsem': 'http:///org/apache/ctakes/typesystem/type/textsem.ecore'
    }
    
    # Extract xmi:id
    target_ids = []
    for concept in root.findall(".//refsem:UmlsConcept", namespaces):
        cui = concept.get('cui')
        if cui in cui_list:
            target_ids.append(concept.get('{http://www.omg.org/XMI}id'))
    
    # Get polarity, conditional, subject, and historyOf from textsem:DiseaseDisorderMention fields
    for target_id in target_ids:
        for mention in root.findall(".//textsem:DiseaseDisorderMention", namespaces):
            ontology_concepts = mention.get('ontologyConceptArr')
            if ontology_concepts and target_id in ontology_concepts.split():
                confidence = mention.get('confidence')
                polarity = mention.get('polarity')
                conditional = mention.get('conditional')
                subject = mention.get('subject')
                historyOf = mention.get('historyOf')
                if polarity == '1' and conditional == 'false' and subject == 'patient' and historyOf == '0':
                    status = "A"
                    return status
                elif polarity == '-1' and conditional == 'false' and subject == 'patient' and historyOf == '0':
                    status = "N" if order[status] < order["N"] else status
                elif polarity == '1' and conditional == 'false' and subject == 'patient' and historyOf == '1':
                    status = "H" if order[status] < order["H"] else status
                elif polarity == '1' and conditional == 'false' and subject != 'patient' and historyOf == '0':
                    status = "X" if order[status] < order["X"] else status
                else:
                    status = "U" if order[status] < order["U"] else status

    return status

def main():
    feature_list = ["obesity", "substance_abuse"]
    # Get all XMI files
    xmi_files = glob.glob("./Output/**/*.xmi", recursive=True)
    print(f"Found {len(xmi_files)} XMI files.")
    
    for feature in feature_list:
        PatID_list = []
        EncounterID_list = []
        NoteID_list = []
        FeatureID_list = []
        Feature_dt_list = []
        Feature_list = []
        FE_CodeType_list = []
        ProviderID_list = []
        Confidence_list = []
        Feature_Status_list = []
        cui_list = get_cui_list(feature)
        
        # Use tqdm for a progress bar
        for xmi_file in tqdm(xmi_files, desc=f"Processing {feature} XMI files", unit="file"):
            PatID, EncounterID, NoteID, Feature_dt, ProviderID = xmi_file.split("/")[-1].split(".")[0].split("_")
            # Convert Feature_dt to datetime format
            Feature_dt = pd.to_datetime(Feature_dt)

            status = assign_status(xmi_file, cui_list)
            PatID_list.append(PatID)
            EncounterID_list.append(EncounterID)
            NoteID_list.append(NoteID)
            FeatureID_list.append("C0028754" if feature == "obesity" else "C0740858")
            Feature_dt_list.append(Feature_dt)
            Feature_list.append("Obesity" if feature == "obesity" else "Substance Abuse")
            FE_CodeType_list.append("UC")
            ProviderID_list.append(ProviderID)
            Confidence_list.append("N")
            Feature_Status_list.append(status)
        
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame()
        df["PatID"] = PatID_list
        df["EncounterID"] = EncounterID_list
        df["NoteID"] = NoteID_list
        df["FeatureID"] = FeatureID_list
        df["Feature_dt"] = Feature_dt_list
        df["Feature"] = Feature_list
        df["FE_CodeType"] = FE_CodeType_list
        df["ProviderID"] = ProviderID_list
        df["Confidence"] = Confidence_list
        df["Feature_Status"] = Feature_Status_list
        
        # Save the DataFrame to a CSV file
        df.to_csv(f"fe_feature_detail_table_{feature}.csv", index=False)
        print(f"Saved fe_feature_detail_table_{feature}.csv")

        # Group the rows and aggregate the Feature_Status values of different NoteIDs by the order
        order = {"A": 5, "N": 4, "H": 3, "X": 2, "U": 1}
        df_grouped_status = df.groupby(["PatID", "EncounterID", "FeatureID", "Feature", "FE_CodeType", "Confidence"]).agg({"Feature_Status": lambda x: max(x, key=lambda y: order[y])}).reset_index()

        # Group the rows and aggregate the Feature_dt and ProviderID of different NoteIDs by the earliest date
        df_grouped_date = df.groupby(["PatID", "EncounterID", "FeatureID", "Feature", "FE_CodeType", "Confidence"]).agg({"Feature_dt": "min", "ProviderID": "first"}).reset_index()

        # Merge the two DataFrames
        df = pd.merge(df_grouped_date, df_grouped_status, on=["PatID", "EncounterID", "FeatureID", "Feature", "FE_CodeType", "Confidence"], how="inner")

        # Ensure that the columns are in the order of the original table
        df = df[["PatID", "EncounterID", "FeatureID", "Feature_dt", "Feature", "FE_CodeType", "ProviderID", "Confidence", "Feature_Status"]]

        df.to_csv(f"fe_feature_table_{feature}.csv", index=False)
        print(f"Saved fe_feature_table_{feature}.csv")

if __name__ == "__main__":
    main()