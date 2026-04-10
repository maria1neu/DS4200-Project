import pandas as pd
import altair as alt

from data import data_frame, column_rename, combine_data, DATA_1, DATA_2, DATA_3, DATA_4


def load_data():
    df1 = column_rename(data_frame(DATA_1))
    df2 = column_rename(data_frame(DATA_2))
    df3 = column_rename(data_frame(DATA_3))
    df4 = column_rename(data_frame(DATA_4))
    df = combine_data(df1, df2, df3, df4)

    df["Time Stamp"] = pd.to_datetime(df["Time Stamp"], utc=True, errors="coerce")
    df["month"] = df["Time Stamp"].dt.strftime("%b")
    df["year"] = df["Time Stamp"].dt.year

    return df.dropna(subset=["Time Stamp"])


def plot_heatmap(df):
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    agg = df.groupby(["year", "month"]).agg(
        plays=("Track Name", "count"),
        skip_rate=("Skipped", lambda x: round(x.fillna(0).astype(float).mean() * 100, 1))
    ).reset_index()

    finals_months = ["May", "Dec"]
    agg["is_finals"] = agg["month"].isin(finals_months)

    base = (
        alt.Chart(agg)
        .mark_rect()
        .encode(
            x=alt.X("month:O", sort=month_order),
            y=alt.Y("year:O"),
            color=alt.Color("plays:Q", scale=alt.Scale(scheme="greens")),
            tooltip=["year:O", "month:O", "plays:Q", "skip_rate:Q", "is_finals:N"]
        )
        .properties(title="listening activity by month & year (skip rate % shown in cells)")
    )

    # overlay red border on finals months to highlight academic stress periods
    finals_overlay = (
        alt.Chart(agg[agg["is_finals"]])
        .mark_rect(filled=False, stroke="red", strokeWidth=2)
        .encode(
            x=alt.X("month:O", sort=month_order),
            y=alt.Y("year:O"),
        )
    )

    # show skip rate as text inside each cell so Spotify can see engagement level
    skip_text = (
        alt.Chart(agg)
        .mark_text(fontSize=8, color="white")
        .encode(
            x=alt.X("month:O", sort=month_order),
            y=alt.Y("year:O"),
            text=alt.Text("skip_rate:Q", format=".0f")
        )
    )

    chart = base + finals_overlay + skip_text
    chart.save("heatmap.html")


if __name__ == "__main__":
    df = load_data()
    plot_heatmap(df)
