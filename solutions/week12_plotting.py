"""Week 12 reference solutions - matplotlib figures."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

WAIT_BANDS = [
    "up_to_18_weeks",
    "over_18_and_up_to_26_weeks",
    "over_26_and_up_to_40_weeks",
    "over_40_and_up_to_52_weeks",
    "over_52_and_up_to_65_weeks",
    "over_65_and_up_to_78_weeks",
    "over_78_and_up_to_104_weeks",
    "over_104_weeks",
]


def _axes(ax):
    """Return the Axes to draw on, creating a figure when none is given."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))
    return ax


def scatter_waiting_vs_target(df, ax=None):
    ax = _axes(ax)
    ax.scatter(
        df["total_waiting_list"],
        df["prop_within_18_weeks"],
        alpha=0.6,
        edgecolor="none",
    )
    ax.set_xlabel("Total waiting list (patients)")
    ax.set_ylabel("Proportion seen within 18 weeks")
    ax.set_title("Waiting-list size against 18-week performance")
    return ax


def histogram_of_waiting_lists(df, column="total_waiting_list", bins=20, ax=None):
    ax = _axes(ax)
    ax.hist(df[column].dropna(), bins=bins, edgecolor="white")
    ax.set_xlabel(column.replace("_", " ").capitalize())
    ax.set_ylabel("Number of organisations")
    ax.set_title(f"Distribution of {column.replace('_', ' ')}")
    return ax


def bar_mean_by_group(df, group_column, value_column, ax=None):
    ax = _axes(ax)
    means = df.groupby(group_column)[value_column].mean().sort_values()
    ax.bar(means.index.astype(str), means.values)
    ax.set_xlabel(group_column.replace("_", " ").capitalize())
    ax.set_ylabel(f"Mean {value_column.replace('_', ' ')}")
    ax.set_title(f"Mean {value_column.replace('_', ' ')} by {group_column.replace('_', ' ')}")
    ax.tick_params(axis="x", rotation=45)
    return ax


def stacked_wait_bands(df, org_codes, ax=None):
    ax = _axes(ax)
    subset = df[df["organisation_code"].isin(org_codes)].set_index(
        "organisation_code"
    ).reindex(org_codes)
    bottom = [0.0] * len(subset)
    for band in WAIT_BANDS:
        values = subset[band].fillna(0).tolist()
        ax.bar(subset.index.astype(str), values, bottom=bottom,
               label=band.replace("_", " "))
        bottom = [base + value for base, value in zip(bottom, values)]
    ax.set_xlabel("Organisation code")
    ax.set_ylabel("Patients waiting")
    ax.set_title("Waiting-list composition by band")
    ax.legend(fontsize="x-small")
    return ax
