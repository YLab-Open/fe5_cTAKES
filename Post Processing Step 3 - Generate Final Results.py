import numpy as np
import pandas as pd

def main():
    feature_list = ["obesity", "substance_abuse"]
    
    for feature in feature_list:
        # Read the CSV file
        df = pd.read_csv(f"fe_feature_detail_table_{feature}.csv")

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

    print("Final results generated for both obesity and substance abuse. Final results saved as fe_feature_table_obesity.csv and fe_feature_table_substance_abuse.csv. Post Processing Step 3 complete.")

if __name__ == "__main__":
    main()