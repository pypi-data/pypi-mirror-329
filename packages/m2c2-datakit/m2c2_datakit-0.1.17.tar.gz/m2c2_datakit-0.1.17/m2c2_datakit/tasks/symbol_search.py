import pandas as pd

def score(row, legacy=False):
    try:
        if legacy:
            return row["user_response"] == row["correct_response"]
        else:
            return row["user_response_index"] == row["correct_response_index"]
    except Exception as e:
        print(f"Error processing row: {e}")
        return None

def summarize(
    x, trials_expected=20, rt_outlier_low=100, rt_outlier_high=10000
):
    d = {}

    # trial counts and validation checks
    d["number_of_trials"] = x["trial_index"].nunique()

    # trial counts (for various denominators)
    d["n_trials_total"] = x["trial_index"].nunique()
    d["n_trials_lure"] = (x["trial_type"] == "lure").sum()
    d["n_trials_normal"] = (x["trial_type"] == "normal").sum()

    # Check if trials match expectations
    d["flag_trials_match_expected"] = d["n_trials_total"] == trials_expected

    # tabulate accuracy
    d["n_trials_correct"] = (
        x["user_response_index"] == x["correct_response_index"]
    ).sum()

    d["n_trials_incorrect"] = (
        x["user_response_index"] != x["correct_response_index"]
    ).sum()

    # Filter out outliers: RT < 100 ms or RT > 10,000 ms
    rt_filtered = x.loc[
        (x["response_time_duration_ms"] >= rt_outlier_low)
        & (x["response_time_duration_ms"] <= rt_outlier_high),
        "response_time_duration_ms",
    ]
    d["median_response_time_filtered"] = rt_filtered.median()

    # get RTs for correct and incorrect trials
    d["median_response_time_overall"] = x["response_time_duration_ms"].median()
    d["median_response_time_correct"] = x.loc[
        (x["user_response_index"] == x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()
    d["median_response_time_incorrect"] = x.loc[
        (x["user_response_index"] != x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()

    # return as series
    indices = list(d.keys())
    return pd.Series(
        d,
        index=indices,
    )

