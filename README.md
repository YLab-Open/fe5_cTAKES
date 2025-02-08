## Overview

The obesity and the substance abuse pipeline uses cTAKES to annotate the clinical notes.

**You do not need to specify the keyword for which feature to run as the two features are annotated simutaneously in one run.**

This pipeline consistes of the following 2 parts:

### Pipeline
The purpose of the pipeline is to process the `csv` files that contains the input clinical notes under a user-defined folder. Due to different system constrains (e.g. memory/storage limit), user may choose to chunk the input `csv` files into multiple folders so only process one at a time. The pipeline can be started by executing:

```yaml
chmod 777 *.sh
chmod 777 *.py
nohup bash Pipeline.sh > Pipeline.log 2>&1 &
```

The pipeline consists of the following 5 steps and executes them sequentially:
* `Pipeline Step 1 - Prepare Input.py`: Process the `csv` files that contains the clinical notes. Save each piece of clinical note as a `txt` file, and evenly distribute the files into `num_folders` folders (specified by the user) under `./Input/Input_{folder_index}`.
* `Pipeline Step 2 - Chunk Input.py`: Chunk all `txt` files generated by `Pipeline Step 1 - Prepare Input.py` into smaller pieces (chunk size defined by the user) to speed up processing. Save each chunk of clinical note as a `txt` file with the name `{original_name}_{chunk_id}.txt`, and save them into the same number of folders under `./Input_chunk/Input_{folder_index}`. For example, if note `a.txt` is saved at `./Input/Input_1`, then all chunks of `a.txt`, such as `a_1.txt`, `a_2.txt`, will be saved under `./Input_chunk/Input_1`. **The files under `./Input/Input_{folder_index}` will be removed after this step.** 
* `Pipeline Step 3 - Run cTAKES.sh`: Use cTAKES to process the chunked `txt` files stored in each `./Input_chunk/Input_{folder_index}` folder, and save the processed file (in `xmi` format) into `num_folders` output folders under `./Output/Output_{folder_index}`. For example, if note `a_1.txt` is saved at `./Input_chunk/Input_1`, then its corresponding output, named as `a_1.txt.xmi`, will be saved under `./Output/Output_{folder_index}`.
* `Pipeline Step 4 - Remove Processed Note Chunks.sh`: Use cTAKES to process the chunked `txt` files stored in each `./Input_chunk/Input_{folder_index}` folder, and save the processed file (in `xmi` format) into `num_folders` output folders under `./Output/Output_{folder_index}`. For example, if note `a_1.txt` is saved at `./Input_chunk/Input_1`, then its corresponding output, named as `a_1.txt.xmi`, will be saved under `./Output/Output_{folder_index}`. **The files under `./Input_chunk/Input_{folder_index}` will be removed after this step.**
* `Pipeline Step 5 - Process Output.py`: Process the output `xmi` files and generate the chunk-level FE feature tables for each chunk of the input clinical notes under `./Result/Result_{folder_index}/obesity/fe_feature_detail_table_obesity_{folder_index}.csv` and `./Result/Result_{folder_index}/substance_abuse/fe_feature_detail_table_substance_abuse_{folder_index}.csv` respectively, which will need to be aggregated in the post processing step to generate the final (encounter-level) FE feature tables. **The files under `./Output/Output_{folder_index}` will be removed after this step.**

### Post Processing
The porpose of post processing is to aggregate the chunk-level FE feature tables for all input processed by the pipeline and generate the final (encounter-level) FE feature tables. The post processing script can be started by executing:

```yaml
chmod 777 *.sh
chmod 777 *.py
nohup bash "Post Processing.sh" > "Post Processing.log" 2>&1 &
```

The post processing consists of the following 3 steps and executes them sequentially:
* `Post Processing Step 1 - Aggregate Output.py`: Aggregate the chunk-level FE feature tables generated by `Pipeline Step 5 - Process Output.py` so that each chunk of the same input clinical note will result in just one line in the aggregated FE feature tables. The result of this step will be saved under `./Result/Result_{folder_index}/obesity/fe_feature_detail_table_obesity_{folder_index}_aggregated.csv` and `./Result/Result_{folder_index}/substance_abuse/fe_feature_detail_table_substance_abuse_{folder_index}_aggregated.csv` respectively.
* `Post Processing Step 2 - Generate Note Level Results.py`: Concat all aggregated `csv` files generated by `Post Processing Step 1 - Aggregate Output.py` to generate the note-level FE feature tables. The result of this step will be saved under `fe_feature_detail_table_obesity.csv` and `./fe_feature_detail_table_substance_abuse.csv` respectively. 
* `Post Processing Step 3 - Generate Final Results.sh`: Aggregate the note-level FE feature tables generated by `Post Processing Step 2 - Generate Note Level Results.py` to generate the final (encounter-level) FE feature tables. The result of this step will be saved under `./fe_feature_table_obesity.csv` and `./fe_feature_table_substance_abuse.csv` respectively.

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

Unzip `apache-ctakes-4.0.0.1-bin.tar.gz` and put the `apache-ctakes-4.0.0.1` folder (it is inside the unzipped `apache-ctakes-4.0.0.1-bin` folder) under the **same directory** as `run_all.sh`. 

**IMPORTANT: Please make sure that you put the `apache-ctakes-4.0.0.1` folder within `apache-ctakes-4.0.0.1-bin` instead of `apache-ctakes-4.0.0.1-bin` itself under the same directory as `run_all.sh`**

### Step 3: Setup `config.json`

To run the obesity and the substance abuse pipeline. You need to specify your variables in [config.json](./config.json). Some fields are already pre-filled to serve as an example. Below is a detailed explanation about what each variable refers to.

* `clinical_notes_directory`: The **directory** that stores the clinical notes that need to be processed. The clinical notes must be stored in `csv` format, but there can be multiple `csv` files.
* `patient_id_column_name`: The name of the column in the `csv` file that contains the **patient ID**.
* `encounter_id_column_name`: The name of the column in the `csv` file that contains the **encounter ID**.
* `note_id_column_name`: The name of the column in the `csv` file that contains the **note ID**.
* `note_date_column_name`: The name of the column in the `csv` file that contains the **note date**.
* `provider_id_column_name`: The name of the column in the `csv` file that contains the **provider ID**.
* `note_text_column_name`: The name of the column in the `csv` file that contains the **note text**.
* `num_processes`: The **number of processes** to create to run the pipeline. **Note: This is also the number of subfolders to be created for the input and the output.** The **number of cTAKES processes** is also represented by this number.
* `note_chunk_size_bytes`: The size (in bytes) of each chunk of the input clinical notes. **Please make this number no larger than 10240 (10KB)** as we have found that the cTAKES annotation speed will drop significant or even completely stucked when your chunk size is too large.
* `UMLS_username`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) username.
* `UMLS_assword`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) password.
* `UMLS_API_key`: Your [UMLS](https://www.nlm.nih.gov/research/umls/index.html) API key, which can be found at your [UMLS profile](https://uts.nlm.nih.gov/uts/profile) after you log in.

## Execution

After setting up `config.json`, simply execute
```yaml
chmod 777 *.sh
chmod 777 *.py
nohup bash Pipeline.sh > Pipeline.log 2>&1 &
```

If you separate the input into multiple folders, then after the pipeline has finished executing the previous folder, **change the `clinical_notes_directory` field** of `config.json` and execute
```yaml
nohup bash Pipeline.sh > Pipeline.log 2>&1 &
```

You will see multiple folders being created during the execution of the pipeline, but **do not manually modify the files within these folders** (even if you start the pipeline on a different `clinical_notes_directory`) as they will be updated automatically and the later steps depend on them.

You will find your results (the final (encounter-level) FE feature tables) under the same directory of `run_all.sh` after the pipeline finishes.

## Example

Suppose that you have 1,000,000 clinical notes stored in 1,000 `csv` files, with each of them contains 1,000 clinical notes, and your `csv` files are stored at `./EHR Notes Test`. Then you can setup your `config.json` as follows (which are the pre-filled values you see at [config.json](./config.json)):

```yaml
"clinical_notes_directory": "./EHR Notes Test",
"patient_id_column_name": "PATIENT_NUM",
"encounter_id_column_name": "ENCOUNTER_NUM",
"note_id_column_name": "COLUMN_1",
"note_date_column_name": "UPDATE_DATE",
"provider_id_column_name": "PROVIDER_ID",
"note_text_column_name": "OBSERVATION_BLOB",
"num_processes": 40,
"note_chunk_size_bytes": 5120,
"UMLS_username": "",
"UMLS_password": "",
"UMLS_API_key": ""
```

The config above will use **40** processes to process each of your `csv` files, converting each of the 1,000,000 clinical notes into 1,000,000 separate `txt` files, and evenly distributing them into **40** input folders (named from `./Input/Input_1` to `./Input/Input_40`). Then it will chunk the input `txt` files into mutiple smaller `txt` files, with each of them no larger than 5KB, save them under `./Input_chunk/Input_1` to `./Input_chunk/Input_40`, and remove the `txt` files under `./Input/Input_1` to `./Input/Input_40`. Then it will create **40** cTAKES processes, with cTAKES process `X` annotate all clinical notes under `./Input_chunk/Input_X` and save the annotated clinical notes in `xmi` format under `./Output/Output_X`. After the cTAKES annotation has finished, it will removed all the `txt` files under `./Input_chunk/Input_1` to `./Input_chunk/Input_40`. Finally, it will use **40** processes to process the output `xmi` files of each output folder into the chunk-level `csv` file and save them under folders from `./Result/Result_1/obesity/fe_feature_detail_table_obesity_1.csv` and `./Result/Result_1/substance_abuse/fe_feature_detail_table_substance_abuse_1.csv` to `./Result/Result_40/obesity/fe_feature_detail_table_obesity_40.csv` and `./Result/Result_40/substance_abuse/fe_feature_detail_table_substance_abuse_40.csv`.

If you want to process a second folder of input `csv`, simply update the `clinical_notes_directory` field in `config.json` and start the pipeline again. The results will be accumulated automatically.

After all input `csv` files have been processed, execute the `Post Processing.sh` to generate the final (encounter-level) FE feature table.

Finally, the final (encounter-level) FE feature tables can be found under `./fe_feature_table_obesity.csv` and `./fe_feature_table_substance_abuse.csv` respectively.

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

Every pipeline and post processing script will have its own log files created, which contains progress information or error messages. Please refer to individual log files for details.

## Run cATKES in parallel

**The pipeline already implemented parallel execution of cTAKES, see [Pipeline Step 3 - Run cTAKES.sh](Pipeline%20Step%203%20-%20Run%20cTAKES.sh) for details.**

Specifically, the shell script does the following:

*	Copy the original cTAKES source folder `apache-ctakes-4.0.0.1` `$PROCESS` times using name `apache-ctakes-4.0.0.1_X`, where `$PROCESS` is the number of processes you want to execute in parallel and is defined in `config.json`. The reason that we need to copy the original cTAKES source folder many times is that if we only use a single cTAKES source folder, the first process will place a lock on the source folder, which prevent other process from using it. As a result, all processes need to use different cTAKES source folder.
*	The code will use cTAKES source folder `apache-ctakes-4.0.0.1_X` to annotate all text in `Input/Input_X`, and output in `Output/Output_X`, where `X` is an integer range from `1` to `$PROCESS` (inclusive)

If you just want to run cTAKES in parallel to annotate the notes instead of excuting the whole pipeline, use the following command:

```yaml
chmod 777 "Step 3 - Run cTAKES.sh"
nohup bash "Step 3 - Run cTAKES.sh" > "Step 3 - Run cTAKES.log" 2>&1 &
```

After executing the code above, you will see that `Output/Output_X` will have the annotation result of all text files in `Input_chunk/Input_X`, and `a_0.txt` in `Input/Input_X` will have the corresponding `a_0.txt.xmi` in `Output/Output_X`.


## Auxiliary Tools

There are two auxiliary shell scripts that help you check the correctness of the pipeline.

*   `./count_txt.sh`: Helps count the number of `txt` files within `./Input`. You may run this script during or after Step 1 to check the progress and see if the total number of `txt` files generated equals the total number of clinical notes that you want to process.
*   `./count_xmi.sh`: Helps count the number of `xmi` files within `./Output`. You may run this script during or after Step 2 to check the progress and see if the total number of `xmi` files generated equals the total number of clinical notes that you want to process.
