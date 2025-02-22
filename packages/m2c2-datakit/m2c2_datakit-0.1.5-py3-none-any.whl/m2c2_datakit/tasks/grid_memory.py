import pandas as pd
import json
import numpy as np


def summary_grid_memory_simple(x, trials_expected=4):
    d = {}

    # trial counts and validation checks
    d["n_trials"] = x["trial_index"].nunique()

    d["n_trials_total"] = x["trial_index"].nunique()

    # Check if trials match expectations
    d["trials_match_expected"] = d["n_trials_total"] == trials_expected
    d["trials_lt_expected"] = d["n_trials_total"] < trials_expected
    d["trials_gt_expected"] = d["n_trials_total"] > trials_expected

    d["sum_correct_dots"] = (x["number_of_correct_dots"]).sum()

    # return as series
    indices = list(d.keys())
    return pd.Series(
        d,
        index=indices,
    )


def summary_grid_memory(x, trials_expected=4):
    d = {}
    d["flag_is_invalid_n_trials"] = x["session_uuid"].count() != trials_expected
    d["n_trials"] = x["session_uuid"].count()
    d["n_perfect_trials"] = (x["number_of_correct_dots"] == 3.0).sum()
    d["mean_correct_dots"] = (x["number_of_correct_dots"]).mean()
    d["min_correct_dots"] = (x["number_of_correct_dots"]).min()
    d["sum_correct_dots"] = (x["number_of_correct_dots"]).sum()
    # TODO: error distance, hausdorff distance
    return pd.Series(
        d,
        index=[
            "flag_is_invalid_n_trials",
            "n_trials",
            "n_perfect_trials",
            "mean_correct_dots",
            "min_correct_dots",
            "sum_correct_dots",
        ],
    )


def calculate_total_user_dot_actions(row):
    import json

    import numpy as np

    try:
        # Parse the JSON strings into lists of dictionaries
        presented_cells = row["presented_cells"]
        selected_cells = row["selected_cells"]

        # Ensure both lists have the same length
        if len(presented_cells) != len(selected_cells):
            return None  # Mismatch in length

        # Calculate Euclidean distances
        distances = []
        for p_cell, s_cell in zip(presented_cells, selected_cells):
            dist = np.sqrt(
                (p_cell["row"] - s_cell["row"]) ** 2
                + (p_cell["column"] - s_cell["column"]) ** 2
            )
            distances.append(dist)

        # Return average error distance
        return np.mean(distances)
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def calculate_mean_error_distance(row):

    try:
        # Parse the JSON strings into lists of dictionaries
        presented_cells = row["presented_cells"]
        selected_cells = row["selected_cells"]

        # Ensure both lists have the same length
        if len(presented_cells) != len(selected_cells):
            return None  # Mismatch in length

        # Calculate Euclidean distances
        distances = []
        for p_cell, s_cell in zip(presented_cells, selected_cells):
            dist = np.sqrt(
                (p_cell["row"] - s_cell["row"]) ** 2
                + (p_cell["column"] - s_cell["column"]) ** 2
            )
            distances.append(dist)

        # Return average error distance
        return np.mean(distances)
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def calculate_sum_error_distance(row):
    import json

    import numpy as np

    try:
        # Parse the JSON strings into lists of dictionaries
        presented_cells = row["presented_cells"]
        selected_cells = row["selected_cells"]

        # Ensure both lists have the same length
        if len(presented_cells) != len(selected_cells):
            return None  # Mismatch in length

        # Calculate Euclidean distances
        distances = []
        for p_cell, s_cell in zip(presented_cells, selected_cells):
            dist = np.sqrt(
                (p_cell["row"] - s_cell["row"]) ** 2
                + (p_cell["column"] - s_cell["column"]) ** 2
            )
            distances.append(dist)

        # Return total error distance
        return np.sum(distances)
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def calculate_hausdorff_distance(row):
    import json

    import numpy as np
    from scipy.spatial.distance import directed_hausdorff

    try:
        # Parse the JSON strings into lists of dictionaries
        presented_cells = row["presented_cells"]
        selected_cells = row["selected_cells"]

        # Convert to numpy arrays of coordinates
        presented_coords = np.array(
            [[cell["row"], cell["column"]] for cell in presented_cells]
        )
        selected_coords = np.array(
            [[cell["row"], cell["column"]] for cell in selected_cells]
        )

        # Calculate directed Hausdorff distances
        d1 = directed_hausdorff(presented_coords, selected_coords)[0]
        d2 = directed_hausdorff(selected_coords, presented_coords)[0]

        # Return the Hausdorff distance
        return max(d1, d2)
    except Exception as e:
        print(f"Error processing row: {e}")
        return None
