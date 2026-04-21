import pandas as pd
import plotly.express as px
from data import load_final_data


def add_finals_flag(df):
    possible_time_cols = ["Time Stamp", "ts", "endTime", "timestamp", "date"]
    time_col = None

    for col in possible_time_cols:
        if col in df.columns:
            time_col = col
            break

    if time_col is None:
        raise ValueError(f"No timestamp column found. Columns are: {list(df.columns)}")

    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col]).copy()

    df["date"] = df[time_col].dt.date
    df["month"] = df[time_col].dt.month
    df["Period"] = df["month"].apply(lambda x: "Finals" if x in [5, 12] else "Non-Finals")

    return df


def plot_finals_vs_nonfinals(df):
    daily_counts = (
        df.groupby(["date", "Period"])
        .size()
        .reset_index(name="plays_per_day")
    )

    summary = (
        daily_counts.groupby("Period")["plays_per_day"]
        .mean()
        .reset_index()
    )

    summary["Period"] = pd.Categorical(
        summary["Period"],
        categories=["Finals", "Non-Finals"],
        ordered=True
    )
    summary = summary.sort_values("Period")

    fig = px.bar(
        summary,
        x="Period",
        y="plays_per_day",
        title="Average Daily Listening: Finals vs Non-Finals",
        text="plays_per_day",
        color="Period",
        plot_bgcolor="#080810",
        color_discrete_map={
        "Finals": "#ff6060",
        "Non-Finals": "#1db954"
        }
    )

    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Average Plays per Day",
        template="simple_white"
    )

    fig.write_image("viz3_finals_vs_nonfinals.png", width=800, height=500)

    return summary


def main():
    df = load_final_data()
    df = add_finals_flag(df)

    plot_data = plot_finals_vs_nonfinals(df)


if __name__ == "__main__":
    main()