import pandas as pd
import zipfile


def list_zip_contents(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        contents = {
            name: zip_ref.getinfo(name).file_size for name in zip_ref.namelist()
        }
    return contents


def read_zip_files(zip_path, zip_contents):
    file_data = {}
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_contents.keys():
            # with zip_ref.open(file_name) as file:
            #     file_data[file_name] = file.read().decode("utf-8")

            # Read a pipe-delimited file
            df = pd.read_csv(file_name, delimiter="|")
            print(df.head())
            file_data[file_name] = df
    return file_data


### Split dataframe / JSON by task
# This is essentially the format that the API would return - a bucket of JSON data per task.
def parse_json_to_dfs(df, activity_name_col="activity_name"):
    """
    Parse the JSON data into a list of dataframes, one for each participant.
    """
    # Group the DataFrame by the 'activity_name' column
    grouped = df.groupby(activity_name_col)

    # Split into separate DataFrames for each group
    grouped_dataframes = {name: group.reset_index(drop=True) for name, group in grouped}
    return grouped_dataframes


def unnest_trial_level_data(
    df,
    drop_duplicates=True,
    column_order=[
        "participant_id",
        "session_id",
        "group",
        "wave",
        "activity_id",
        "study_id",
        "document_uuid",
    ],
):
    """
    Unnest trial level data from a DataFrame containing a column 'content' with a list of dictionaries.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a column 'content' with a list of dictionaries.

    Returns
    -------
    pd.DataFrame
        DataFrame with trial level data unnested.
    """

    # iterate over the dataset to get all trials ----
    all_trials = []
    for index, row in df.iterrows():
        json_data = row["content"].get("trials", [])
        all_trials.extend(json_data)

    # convert to DataFrame
    df = pd.DataFrame(all_trials)

    # Reorder columns
    other_columns = [col for col in df.columns if col not in column_order]
    new_column_order = column_order + other_columns

    # Apply the new column order
    df = df[new_column_order]

    # drop duplicates
    if drop_duplicates:
        df = df.drop_duplicates(
            subset=["activity_uuid", "session_uuid", "trial_begin_iso8601_timestamp"]
        )

    return df
