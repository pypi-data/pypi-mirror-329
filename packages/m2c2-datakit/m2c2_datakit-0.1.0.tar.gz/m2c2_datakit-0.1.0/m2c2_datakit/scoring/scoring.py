import uuid

import pandas as pd

from ..core.config import package_version
from ..tasks.grid_memory import *
from ..tasks.symbol_search import *
from ..utils.utils import compute_md5_hash
from ..core.validate import validate_input


def score_data(df, scoring_func, **kwargs):
    """
    Scores a DataFrame using the provided scoring function.

    Parameters:
        df (pd.DataFrame): Input DataFrame to score.
        scoring_func (Callable): Function to apply to each row for scoring.
        **kwargs: Additional arguments passed to the scoring function.

    Returns:
        pd.DataFrame: A scored DataFrame with metadata columns.
    """
    batch_id = str(uuid.uuid4())

    # Validate and compute the pre-process hash
    validate_input(df)
    original_hash = compute_md5_hash(df)

    # Apply scoring function
    df_scored = df.apply(scoring_func, axis=1, **kwargs).reset_index()

    # Compute post-process hash and add metadata
    final_hash = compute_md5_hash(df_scored)
    df_scored["pkg_batch_id"] = batch_id
    df_scored["pkg_process_timestamp"] = pd.Timestamp.now()
    df_scored["pkg_process_prehash"] = original_hash
    df_scored["pkg_process_posthash"] = final_hash
    df_scored["pkg_version"] = package_version

    return df_scored


def summarize_data(df, grouping, summarization_func, **kwargs):
    """
    Summarizes a DataFrame based on grouping and summarization function.

    Parameters:
        df (pd.DataFrame): Input DataFrame to summarize.
        grouping (List[str]): Columns to group by.
        summarization_func (Callable): Function to summarize each group.
        **kwargs: Additional arguments passed to the summarization function.

    Returns:
        pd.DataFrame: A summarized DataFrame with metadata columns.
    """
    batch_id = str(uuid.uuid4())

    # Validate and compute the pre-process hash
    validate_input(df)
    original_hash = compute_md5_hash(df)

    # Apply summarization function
    df_summary = df.groupby(grouping).apply(summarization_func, **kwargs).reset_index()

    # Compute post-process hash and add metadata
    final_hash = compute_md5_hash(df_summary)
    df_summary["pkg_batch_id"] = batch_id
    df_summary["pkg_process_timestamp"] = pd.Timestamp.now()
    df_summary["pkg_process_prehash"] = original_hash
    df_summary["pkg_process_posthash"] = final_hash
    df_summary["pkg_version"] = package_version

    return df_summary
