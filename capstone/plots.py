"""Figures for the capstone report.

Every function takes an optional `ax` and returns it, so figures compose
into subplots and can be checked by tests. Labels and titles are set here,
not in the notebook - the marks follow the figure, not the cell.
"""
import matplotlib.pyplot as plt
import numpy as np

from capstone.analysis import BAND_ORDER, TRIAGE_ORDER


def _axes(ax, figsize=(8, 5)):
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
    return ax


def plot_icu_rate_by_news2_band(table, ax=None):
    """Bar chart of ICU admission rate across NEWS2 bands.

    :param table: output of analysis.outcomes_by_news2_band
    :param ax: existing Axes, or None
    :return: the Axes
    """
    ax = _axes(ax)
    bands = [b for b in BAND_ORDER if b in table.index]
    rates = table.loc[bands, "icu_rate"]
    bars = ax.bar(bands, rates, color="#4C72B0")
    for bar_, (band, rate) in zip(bars, rates.items()):
        ax.annotate(
            f"{rate:.1f}%\nn={int(table.loc[band, 'n'])}",
            (bar_.get_x() + bar_.get_width() / 2, rate),
            ha="center", va="bottom", fontsize=8,
        )
    ax.set_xlabel("NEWS2 risk band at triage")
    ax.set_ylabel("ICU admission rate (%)")
    ax.set_title("ICU admission rises with NEWS2 band")
    ax.set_ylim(0, max(rates) * 1.25 if len(rates) else 1)
    return ax


def plot_news2_distribution(df, ax=None):
    """Histogram of NEWS2 totals, split by whether ICU followed.

    :param df: analysis frame with news2_total and icu_admission
    :param ax: existing Axes, or None
    :return: the Axes
    """
    ax = _axes(ax)
    bins = np.arange(-0.5, df["news2_total"].max() + 1.5, 1)
    ax.hist(
        [df.loc[df["icu_admission"] == 0, "news2_total"],
         df.loc[df["icu_admission"] == 1, "news2_total"]],
        bins=bins, stacked=True, label=["No ICU", "ICU"],
        color=["#C7CFE0", "#C44E52"],
    )
    ax.set_xlabel("NEWS2 total at triage")
    ax.set_ylabel("Number of attendances")
    ax.set_title("NEWS2 at triage, by whether the patient went to ICU")
    ax.legend()
    return ax


def plot_time_to_antibiotics(df, ax=None):
    """Distribution of door-to-antibiotics time, with the 60-minute target.

    :param df: analysis frame with minutes_to_antibiotics
    :param ax: existing Axes, or None
    :return: the Axes
    """
    ax = _axes(ax)
    minutes = df["minutes_to_antibiotics"].dropna()
    ax.hist(minutes, bins=30, color="#55A868", edgecolor="white")
    ax.axvline(60, color="#C44E52", linestyle="--", linewidth=1.5,
               label="60-minute target")
    ax.set_xlabel("Minutes from arrival to antibiotics")
    ax.set_ylabel("Number of attendances")
    ax.set_title(
        f"Door-to-antibiotics time (n={len(minutes)} of {len(df)} treated)"
    )
    ax.legend()
    return ax


def plot_lactate_vs_news2(df, ax=None):
    """Lactate against NEWS2, coloured by ICU admission.

    Three variables on one figure - the shape the Sep 2025 paper asks for.

    :param df: analysis frame
    :param ax: existing Axes, or None
    :return: the Axes
    """
    ax = _axes(ax)
    subset = df.dropna(subset=["lactate", "news2_total"])
    for value, label, colour in [(0, "No ICU", "#8EA6C8"), (1, "ICU", "#C44E52")]:
        rows = subset[subset["icu_admission"] == value]
        # Jitter the integer NEWS2 totals so overlapping points stay visible.
        jitter = np.random.default_rng(0).normal(0, 0.12, len(rows))
        ax.scatter(rows["news2_total"] + jitter, rows["lactate"],
                   s=14, alpha=0.6, label=label, color=colour, edgecolor="none")
    ax.set_xlabel("NEWS2 total at triage")
    ax.set_ylabel("Serum lactate (mmol/L)")
    ax.set_title("Lactate against NEWS2, by ICU admission")
    ax.legend(title="Outcome")
    return ax


def plot_hospital_variation(table, ax=None):
    """ICU rate per hospital against median NEWS2, to separate case mix.

    :param table: output of analysis.hospital_variation
    :param ax: existing Axes, or None
    :return: the Axes
    """
    ax = _axes(ax)
    ax.scatter(table["median_news2"], table["icu_rate"],
               s=table["attendances"] / 3, alpha=0.7, color="#4C72B0")
    for _, row in table.iterrows():
        ax.annotate(row["hospital_id"],
                    (row["median_news2"], row["icu_rate"]),
                    textcoords="offset points", xytext=(6, 3), fontsize=8)
    ax.set_xlabel("Median NEWS2 at triage (case mix)")
    ax.set_ylabel("ICU admission rate (%)")
    ax.set_title("ICU rate against case mix, by hospital (point size = volume)")
    return ax
