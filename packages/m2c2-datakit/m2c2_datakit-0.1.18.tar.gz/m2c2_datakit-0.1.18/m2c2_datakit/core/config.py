from importlib.metadata import version

package_version = version("m2c2_datakit")

# Approach #1: Simple Constants
package_version = package_version
standard_grouping_for_aggregation = ["participant_id", "session_uuid", "session_id"]
standard_grouping_for_aggregation_metricwire = [
    "userId",
    "submissionSessionId",
    "activityId",
]
default_plot_color = "steelblue"
default_plot_dpi = 150
