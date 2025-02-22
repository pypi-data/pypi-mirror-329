import pandas as pd


def calculate_accuracy_symbol_search(row):
    try:
        # Return total error distance
        return row["user_response_index"] == row["correct_response_index"]
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def calculate_accuracy_symbol_search_legacy(row):
    try:
        # Return total error distance
        return row["user_response"] == row["correct_response"]
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def summary_symbol_search_simple(
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
    d["trials_match_expected"] = d["n_trials_total"] == trials_expected

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


def summary_symbol_search_simple_legacy(
    x, trials_expected=20, rt_outlier_low=100, rt_outlier_high=10000
):
    d = {}

    # trial counts and validation checks
    d["number_of_trials"] = x["trial_num"].nunique()

    # trial counts (for various denominators)
    d["n_trials_total"] = x["trial_num"].nunique()
    d["n_trials_lure"] = (x["trial_type"] == "LURE").sum()
    d["n_trials_normal"] = (x["trial_type"] == "NORMAL").sum()

    # Check if trials match expectations
    d["trials_match_expected"] = d["n_trials_total"] == trials_expected

    # tabulate accuracy
    d["n_trials_correct"] = (x["user_response"] == x["correct_response"]).sum()

    d["n_trials_incorrect"] = (x["user_response"] != x["correct_response"]).sum()

    # Filter out outliers: RT < 100 ms or RT > 10,000 ms
    rt_filtered = x.loc[
        (x["response_time"] >= rt_outlier_low)
        & (x["response_time"] <= rt_outlier_high),
        "response_time",
    ]
    d["median_response_time_filtered"] = rt_filtered.median()

    # get RTs for correct and incorrect trials
    d["median_response_time_overall"] = x["response_time"].median()
    d["median_response_time_correct"] = x.loc[
        (x["user_response"] == x["correct_response"]),
        "response_time",
    ].median()
    d["median_response_time_incorrect"] = x.loc[
        (x["user_response"] != x["correct_response"]),
        "response_time",
    ].median()

    # return as series
    indices = list(d.keys())
    return pd.Series(
        d,
        index=indices,
    )


def summary_symbol_search(x, trials_expected=20):
    d = {}
    d["flag_is_invalid_n_trials"] = x["session_uuid"].count() != trials_expected
    d["n_trials"] = x["session_uuid"].count()
    d["n_trials_lure"] = (x["trial_type"] == "lure").sum()
    d["n_trials_responsetime_lt250ms"] = (x["response_time_duration_ms"] < 250).sum()
    d["n_trials_responsetime_gt10000ms"] = (
        x["response_time_duration_ms"] > 10000
    ).sum()
    d["n_correct_trials"] = (
        x["user_response_index"] == x["correct_response_index"]
    ).sum()
    d["n_incorrect_trials"] = (
        x["user_response_index"] != x["correct_response_index"]
    ).sum()
    d["mean_response_time_overall"] = x["response_time_duration_ms"].mean()
    d["mean_response_time_correct"] = x.loc[
        (x["user_response_index"] == x["correct_response_index"]),
        "response_time_duration_ms",
    ].mean()
    d["mean_response_time_incorrect"] = x.loc[
        (x["user_response_index"] != x["correct_response_index"]),
        "response_time_duration_ms",
    ].mean()
    d["median_response_time_overall"] = x["response_time_duration_ms"].median()
    d["median_response_time_correct"] = x.loc[
        (x["user_response_index"] == x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()
    d["median_response_time_incorrect"] = x.loc[
        (x["user_response_index"] != x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()
    d["sd_response_time_overall"] = x["response_time_duration_ms"].std()
    d["sd_response_time_correct"] = x.loc[
        (x["user_response_index"] == x["correct_response_index"]),
        "response_time_duration_ms",
    ].std()
    d["sd_response_time_incorrect"] = x.loc[
        (x["user_response_index"] != x["correct_response_index"]),
        "response_time_duration_ms",
    ].std()
    return pd.Series(
        d,
        index=[
            "flag_is_invalid_n_trials",
            # 'flag_is_potentially_invalid_rt',
            "n_trials",
            "n_trials_lure",
            "n_correct_trials",
            "n_incorrect_trials",
            "n_trials_responsetime_lt250ms",
            "n_trials_responsetime_gt10000ms",
            "mean_response_time_overall",
            "mean_response_time_correct",
            "mean_response_time_incorrect",
            "median_response_time_overall",
            "median_response_time_correct",
            "median_response_time_incorrect",
            "sd_response_time_overall",
            "sd_response_time_correct",
            "sd_response_time_incorrect",
        ],
    )
