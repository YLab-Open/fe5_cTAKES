## Overview

The obesity and the substance abuse pipeline use cTAKES to annotate the clinical notes. This pipeline consistes of the following 3 parts:
* `Step 1 - Prepare Input.py`: Process the `csv` files that contains the clinical notes. Save each piece of clinical note as a `txt` file, and evenly distribute the files into `num_folders` input folders at `./Input`.
* `Step 2 - Run cTAKES.sh`: Use cTAKES to process the clinical notes stored in each input folder, and save the processed file (in `xmi` format) into `num_folders` output folders at `./Output`.
* `Step 3 - Process Output.py`: Process the output `xmi` files and generate the FE feature table (`fe_feature_detail_table_obesity.csv`, `fe_feature_detail_table_substance_abuse.csv`, `fe_feature_table_obesity.csv`, and `fe_feature_table_substance_abuse.csv`).

You do not need to specify the keyword for which feature to run as the two features are annotated simutaneously in one run.

## Prerequisites
* `cTAKES 4.0.0.1`: Install at [here](https://dlcdn.apache.org//ctakes/ctakes-4.0.0.1/apache-ctakes-4.0.0.1-bin.tar.gz).
* `Java JDK 1.8+`
* `numpy`
* `pandas`
* `regex`
* `json`
* `tqdm`

## Setup

The setup process is completed in the following 3 steps.

### Step 1: Clone the repository

`git clone https://github.com/YLab-Open/fe5_cTAKES.git`

### Step 2: Place the cTAKES folder

Unzip `apache-ctakes-4.0.0.1-bin.tar.gz` and put the `apache-ctakes-4.0.0.1` folder (it is inside the unzipped `apache-ctakes-4.0.0.1-bin` folder) under the **same directory** as `run_all.sh`. **IMPORTANT: Please make sure that you put the `apache-ctakes-4.0.0.1` folder within `apache-ctakes-4.0.0.1-bin` instead of `apache-ctakes-4.0.0.1-bin` itself under the same directory as `run_all.sh`**

### Step 3: Setup `config.json`

To run the obesity and the substance abuse pipeline. You need to specify your variables in [config.json](./config.json). Some fields are already pre-filled to serve as an example. Below is a detailed explanation about what each variable refers to.

`clinical_notes_directory`: The **directory** that stores the clinical notes that need to be processed. The clinical notes must be stored in `csv` format, but there can be multiple `csv` files.
`num_folders`: The **number of input and output folders** to create. The input folders will be used to store the `txt` files for cTAKES to process, and the output folders will be used to store the output `xmi` files. The reason for creating multiple input and output folders is to make it easier to use multiple cTAKES to process the notes, which greatly improve the processing speed.
`patient_id_column_name`: The name of the column in the `csv` file that contains the **patient ID**.
`encounter_id_column_name`: The name of the column in the `csv` file that contains the **encounter ID**.
`note_id_column_name`: The name of the column in the `csv` file that contains the **note ID**.
`note_date_column_name`: The name of the column in the `csv` file that contains the **note date**.
`provider_id_column_name`: The name of the column in the `csv` file that contains the **provider ID**.
`note_text_column_name`: The name of the column in the `csv` file that contains the **note text**.
`preprocess_process`: The **number of preprocess processes** to create to process the clinical notes in the `csv` files and save them as `txt` files.
`UMLS_username`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) username.
`UMLS_assword`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) password.
`UMLS_API_key`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) API key, which can be found at your [UMLS profile](https://uts.nlm.nih.gov/uts/profile) after you log in.
`cTAKES_process`: The **number of cTAKES processes** to create to annotate the clinical notes.

## Execution

After setting up `config.json`, simply execute `nohup ./run_all.sh > output.log 2>&1 &`, and you will find your results (the FE feature tables) under the same directory of `run_all.sh` after the pipeline finishes.

## Example

Suppose that you have 1,000,000 clinical notes stored in 1,000 `csv` files, with each of them contains 1,000 clinical notes, and your `csv` files are stored at `/PHShome/bg615/FE5/EHR Notes`. Then you can setup your `config.json` as follows (which are the pre-filled values you see at [config.json](./config.json)):

```yaml
"clinical_notes_directory": "/PHShome/bg615/FE5/EHR Notes",
"num_folders": 40,
"patient_id_column_name": "PATIENT_NUM",
"encounter_id_column_name": "ENCOUNTER_NUM",
"note_id_column_name": "COLUMN_1",
"note_date_column_name": "UPDATE_DATE",
"provider_id_column_name": "PROVIDER_ID",
"note_text_column_name": "OBSERVATION_BLOB",
"preprocess_process": 40,
"UMLS_username": "",
"UMLS_password": "",
"UMLS_API_key": "",
"cTAKES_process": 40
```

The config above will use **40** processes to process each of your `csv` files, converting each of the 1,000,000 clinical notes into 1,000,000 separate `txt` files, and evenly distributing them into **40** input folders (named from `./Input/Input_1` to `./Input/Input_40`). Then it will create **40** cTAKES processes, with each cTAKES process processing all clinical notes within one input folder. Specifically, there will be **40** folders under `./cTAKES` (named from `./cTAKES/apache-ctakes-4.0.0.1_1` to `./cTAKES/apache-ctakes-4.0.0.1_40`), where `./cTAKES/apache-ctakes-4.0.0.1_{X}` will annotate `./Input/Input_{X}` and save the annotated clinical notes into the `xmi` format under `./Output/Output_{X}`.

Finally, the annotated `xmi` files will be processed and used to generate the FE feature table (`fe_feature_detail_table_obesity.csv`, `fe_feature_detail_table_substance_abuse.csv`, `fe_feature_table_obesity.csv`, and `fe_feature_table_substance_abuse.csv`).

## Output

For the 4 output files:
* `fe_feature_detail_table_obesity.csv` is the **note-level** result of the FE feature table for the **obesity** feature.
* `fe_feature_detail_table_substance_abuse.csv` is the **note-level** result of the FE feature table for the **substance abuse** feature.
* `fe_feature_table_obesity.csv` is the **encounter-level** result of the FE feature table for the **obesity** feature.
* `fe_feature_table_substance_abuse.csv` is the **encounter-level** result of the FE feature table for the **substance abuse** feature.

The `fe_feature_detail_table_obesity.csv` and `fe_feature_detail_table_substance_abuse.csv` will contain the following columns:
*	`PatID` – individual patient ID
*	`EncounterID` – linked EncounterID with note
*   `NoteID` - note ID (This is the only column that will NOT appear in the **encounter-level** results)
*	`FeatureID` – linked to the FE metadata table storing pipeline details (This field is always `C0028754` for `obesity` and `C0740858` for `substance abuse`)
*	`Feature_dt` – date of note
*	`Feature` - obesity or substance abuse (This field is always `Obesity` for `obesity` and `Substance Abuse` for `substance abuse`)
*	`FE_CodeType` – UMLS CUI (This field is always `UC` for both features)
*	`ProviderID` – linked ProviderID with note  
*	`Confidence` – confidence label (This field is always `N` for both features)
*	`Feature_Status` – A = Active H = Historical N = Negated X = Non-patient (e.g. Family History) U = Unknown

The `fe_feature_table_obesity.csv` and `fe_feature_table_substance_abuse.csv` will contain the following columns:
*	`PatID` – individual patient ID
*	`EncounterID` – linked EncounterID with note
*	`FeatureID` – linked to the FE metadata table storing pipeline details (This field is always `C0028754` for `obesity` and `C0740858` for `substance abuse`)
*	`Feature_dt` – date of note (This field will be aggregated to be the **earliest** date of all notes associated with the same `PatID` and `EncounterID`)
*	`Feature` - obesity or substance abuse (This field is always `Obesity` for `obesity` and `Substance Abuse` for `substance abuse`)
*	`FE_CodeType` – UMLS CUI (This field is always `UC` for both features)
*	`ProviderID` – linked ProviderID with note (This field will be aggregated to be the ProviderID of the **earliest** date of all notes associated with the same `PatID` and `EncounterID`)
*	`Confidence` – confidence label (This field is always `N` for both features)
*	`Feature_Status` – A = Active H = Historical N = Negated X = Non-patient (e.g. Family History) U = Unknown (This field will be aggregated in the following order: A > H > N > X > U of all notes associated with the same `PatID` and `EncounterID`)

## Logs

The following log files will be generated during the execution of the pipeline, which helps you track the processes of each step:
*   `Step 1 - Prepare Input.log`: This is the log of Step 1, which uses tqdm progress bar to track the progress. The progress unit is `file`, so it will update once a `csv` file has finished processing.
*   `Step 2 - Run cTAKES.log`: This is the log of Step 2, which shows the output of the cTAKES pipeline.
*   `Step 3 - Process Output.log`: This is the log of Step 3, which uses tqdm progress bar to track the progress. The progress unit is `file`, so it will update once an `xmi` file has finished processing.

## Auxiliary Tools

There are two auxiliary shell scripts that help you check the correctness of the pipeline.
*   `./count_txt.sh`: Helps count the number of `txt` files within `./Input`. You may run this script during or after Step 1 to check the progress and see if the total number of `txt` files generated equals the total number of clinical notes that you want to process.
*   `./count_xmi.sh`: Helps count the number of `xmi` files within `./Output`. You may run this script during or after Step 2 to check the progress and see if the total number of `xmi` files generated equals the total number of clinical notes that you want to process.