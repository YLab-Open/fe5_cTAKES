import os
import glob
import pandas as pd
import multiprocessing
import json

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

config = load_config()

NUM_PROCESSES = config["num_processes"]

def aggregate_csv_files(folders, output_csv):
    """
    Given a list of folder paths, find all CSV files within these folders,
    read them into DataFrames, concatenate them, print the total row count,
    and save the result to output_csv.
    """
    # List to hold DataFrames read from CSV files.
    df_list = []
    
    # Iterate over each folder.
    for folder in folders:
        # Use glob to find all CSV files in the folder.
        csv_files = glob.glob(os.path.join(folder, "*_aggregated.csv"))
        if len(csv_files) == 0:
            print(f"No CSV files found in folder: {folder}")
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                df_list.append(df)
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
    
    # Concatenate all DataFrames if any were found.
    if df_list:
        aggregated_df = pd.concat(df_list, ignore_index=True)
        total_rows = len(aggregated_df)
        print(f"Total number of rows in {output_csv}: {total_rows}")
        try:
            aggregated_df.to_csv(output_csv, index=False)
            print(f"Aggregated CSV saved to {output_csv}")
        except Exception as e:
            print(f"Error saving {output_csv}: {e}")
    else:
        print(f"No CSV files found in folders: {folders}")

def process_obesity():
    """
    Process all obesity CSV files from: 
      ./Result/Result_{folder_index}/obesity
    and save the aggregated CSV to:
      ./fe_feature_detail_table_obesity.csv
    """
    folders = [
        f"./Result/Result_{folder_index}/obesity" for folder_index in range(1, NUM_PROCESSES + 1)
    ]
    output_csv = "./fe_feature_detail_table_obesity.csv"
    aggregate_csv_files(folders, output_csv)

def process_substance_abuse():
    """
    Process all substance abuse CSV files from: 
      ./Result/Result_{folder_index}/substance_abuse
    and save the aggregated CSV to:
      ./fe_feature_detail_table_substance_abuse.csv
    """
    folders = [
        f"./Result/Result_{folder_index}/substance_abuse" for folder_index in range(1, NUM_PROCESSES + 1)
    ]
    output_csv = "./fe_feature_detail_table_substance_abuse.csv"
    aggregate_csv_files(folders, output_csv)

def main():
    # Create two processes: one for obesity and one for substance abuse.
    p_obesity = multiprocessing.Process(target=process_obesity)
    p_substance = multiprocessing.Process(target=process_substance_abuse)
    
    p_obesity.start()
    p_substance.start()
    
    p_obesity.join()
    p_substance.join()
    
    print("Aggregation completed for both obesity and substance abuse CSV files. Note level results saved as fe_feature_detail_table_obesity.csv and fe_feature_detail_table_substance_abuse.csv. Post Processing Step 2 complete.")

if __name__ == "__main__":
    main()
