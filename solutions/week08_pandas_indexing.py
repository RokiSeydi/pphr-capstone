"""Week 8 reference solutions - selecting data out of a DataFrame."""
import pandas as pd

CVD_RISK_TABLE = {
    "Vegan": {"Women": 0.74, "Men": 0.81},
    "Vegetarian": {"Women": 0.82, "Men": 0.88},
    "Omnivore": {"Women": 1.00, "Men": 1.00},
}


def referral_source():
    return pd.DataFrame({
        "org_code": ["RCF", "RBS", "RTK", "RF4", "RFF", "R1H"],
        "Total": [1103, 821, 2898, 4272, 931, 6154],
        "GP": [865, 394, 2538, 2981, 629, 4121],
    })


def cell_by_label(df, row_index, column):
    return df.loc[row_index, column]


def cell_by_position(df, row_position, column_position):
    return df.iloc[row_position, column_position]


def cell_by_mask(df, key_column, key_value, value_column):
    mask = df[key_column] == key_value
    # .squeeze() would also work; .iloc[0] is clearer about taking one value.
    return df.loc[mask, value_column].iloc[0]


def gp_share(df):
    out = df.copy()
    out["gp_share"] = out["GP"] / out["Total"]
    return out


def busiest_organisations(df, n):
    return df.sort_values("Total", ascending=False)["org_code"].head(n).tolist()


def cvd_risk_frame(table=CVD_RISK_TABLE):
    # from_dict with orient="index" keeps the diets as rows in insertion order.
    frame = pd.DataFrame.from_dict(table, orient="index")[["Women", "Men"]]
    frame.index.name = "diet"
    return frame


def risk_for(df, diet, sex):
    return df.loc[diet, sex]
