"""Week 9 - Matplotlib figures that would earn full marks.

Exam archetype: Q9 (10 marks) - "visualise the relationship between X and Y
using a suitable plot, and describe your findings". Half those marks are for
the axis labels, title and written interpretation, not the plot call.

Each function takes an `ax` so the figure can be inspected by the tests.
Always return the `ax`.
"""
import matplotlib

matplotlib.use("Agg")  # no display needed; safe in tests and on a server
import matplotlib.pyplot as plt


def scatter_waiting_vs_target(df, ax=None):
    """Scatter total_waiting_list against prop_within_18_weeks.

    Requirements (each one is worth marks):
        - x = total_waiting_list, y = prop_within_18_weeks
        - both axes labelled, with units or a clear description
        - a title
        - return the Axes

    :param df: DataFrame with total_waiting_list and prop_within_18_weeks
    :param ax: existing Axes to draw on; create a new figure if None
    :return: the matplotlib Axes
    """
    raise NotImplementedError


def histogram_of_waiting_lists(df, column="total_waiting_list", bins=20, ax=None):
    """Plot the distribution of one column as a histogram.

    Label both axes and set a title that names the column.

    :param df: DataFrame
    :param column: column to plot
    :param bins: number of bins
    :param ax: existing Axes, or None
    :return: the matplotlib Axes
    """
    raise NotImplementedError


def bar_mean_by_group(df, group_column, value_column, ax=None):
    """Plot the mean of `value_column` for each level of `group_column`.

    Group, take the mean, then draw a bar chart. Label both axes.

    :param df: DataFrame
    :param group_column: categorical column to group by
    :param value_column: numeric column to average
    :param ax: existing Axes, or None
    :return: the matplotlib Axes
    """
    raise NotImplementedError


def stacked_wait_bands(df, org_codes, ax=None):
    """Stacked bar of the wait-band columns for the given organisations.

    One bar per organisation, segmented by waiting band (up_to_18_weeks,
    over_18_and_up_to_26_weeks, and so on). Include a legend.

    :param df: waiting-list DataFrame, indexed or filterable by org code
    :param org_codes: list of organisation_code values to include
    :param ax: existing Axes, or None
    :return: the matplotlib Axes
    """
    raise NotImplementedError
