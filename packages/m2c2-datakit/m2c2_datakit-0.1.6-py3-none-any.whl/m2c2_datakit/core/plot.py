import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


from .config import default_plot_color, default_plot_dpi

DEFAULT_DPI = default_plot_dpi


def plot_pairplot(df: pd.DataFrame):
    """
    Plot a pairplot for all numeric variables in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to plot.
    """
    # Set the global aesthetic style and high-quality font
    sns.set(style="whitegrid", rc={"axes.facecolor": "#F5F5F5"})
    mpl.rcParams["font.family"] = "Arial"
    mpl.rcParams["figure.dpi"] = DEFAULT_DPI  # High DPI for clarity

    # Create pairplot with clean styling
    pairplot = sns.pairplot(
        df,
        diag_kind="kde",
        plot_kws={"alpha": 0.7, "color": default_plot_color},
        diag_kws={"color": default_plot_color},
    )
    pairplot.fig.suptitle(
        "Pairplot of Variables", fontsize=16, fontweight="bold", y=1.02
    )
    plt.show()


def plot_distribution(df: pd.DataFrame):
    """
    Plot the distribution of each variable in the DataFrame as separate plots.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to plot.
    """
    # Set the global aesthetic style and high-quality font
    sns.set(style="whitegrid", rc={"axes.facecolor": "#F5F5F5"})
    mpl.rcParams["font.family"] = "Arial"  # Use Arial or Helvetica
    mpl.rcParams["figure.dpi"] = DEFAULT_DPI  # High DPI for clarity

    # Iterate through each column and plot
    for column in df.columns:
        plt.figure(figsize=(8, 4))  # Create a new figure for each plot
        sns.histplot(
            df[column], kde=True, label=column, alpha=0.7, color=default_plot_color
        )

        # Style the plot titles and labels
        plt.title(f"Distribution of {column}", fontsize=14, fontweight="bold", pad=10)
        plt.xlabel("Value", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.legend(fontsize=10)

        # Remove unnecessary spines for a clean look
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        plt.show()
