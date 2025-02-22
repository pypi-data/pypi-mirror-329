# Standard Libraries
import datetime
import glob
import json

# 3rd Party Libraries
import pandas as pd

from ..core.parse import parse_json_to_dfs
from ..core.validate import verify_dataframe_parsing


def read_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def get_data_from_json_files(json_files):
    data = []
    for file in json_files:
        data.append(read_json_file(file))
    return data


def load_metricwire_export(filepath="metricwire/data/unzipped/*/*/*.json"):
    # locate json files in the unzipped folder
    json_files = glob.glob(filepath)
    print(f"Ready to process {len(json_files)} JSON files exported from Metricwire.")

    # specify filename from current run time for filenames
    ts_fn = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # load all data into list of dictionaries
    data = get_data_from_json_files(json_files)

    # Elevate the data
    datao = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            print(data[i][j])
            x = data[i][j]

            # Extract the identifiers
            identifiers = {k: v for k, v in x.items() if k != "data"}
            identifiers_keys = set(identifiers.keys())

            for entry in x["data"]:
                new_entry = {**identifiers, **entry}
                datao.append(new_entry)

    # # group dataframe by activity_name
    df = pd.DataFrame(datao)
    grouped_dataframes = parse_json_to_dfs(df, activity_name_col="activityName")

    validation, activity_names = verify_dataframe_parsing(
        df, grouped_dataframes, activity_name_col="activityName"
    )

    return df, grouped_dataframes, validation, activity_names
