import pandas as pd

from ..core.parse import parse_json_to_dfs
from ..core.validate import verify_dataframe_parsing


def load_mongodb_export(fn):
    df = pd.read_json(fn)

    # preview dataframe
    df.head()

    # group dataframe by activity_name
    grouped_dataframes = parse_json_to_dfs(df)

    validation, activity_names = verify_dataframe_parsing(df, grouped_dataframes)

    return df, grouped_dataframes, validation, activity_names
