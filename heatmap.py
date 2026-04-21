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
    df = df.dropna(subset=["Time Stamp"]).copy()

    df["month"] = df["Time Stamp"].dt.strftime("%b")
    df["year"] = df["Time Stamp"].dt.year

    return df


def plot_heatmap(df):
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Keep only recent years with more complete data
    df = df[df["year"] >= 2023].copy()

    agg = (
        df.groupby(["year", "month"])
        .agg(plays=("Track Name", "count"))
        .reset_index()
    )

    chart = (
        alt.Chart(agg)
        .mark_rect(stroke="white", strokeWidth=0.5)
        .encode(
            x=alt.X(
                "month:O",
                sort=month_order,
                title="Month",
                axis=alt.Axis(labelAngle=0, labelFontSize=12, titleFontSize=14)
            ),
            y=alt.Y(
                "year:O",
                title="Year",
                axis=alt.Axis(labelFontSize=12, titleFontSize=14)
            ),
            color=alt.Color(
                "plays:Q",
                title="Plays",
                scale=alt.Scale(scheme="greens")
            ),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("month:O", title="Month"),
                alt.Tooltip("plays:Q", title="Number of Plays", format=",")
            ]
        )
        .properties(
            title="Monthly Listening Volume by Year",
            width=700,
            height=300
        )
        .configure_title(
            fontSize=22,
            anchor="start"
        )
        .configure_axis(
            labelColor="black",
            titleColor="black"
        )
        .configure_view(
            stroke=None
        )
    )

    chart.save("heatmap.html")


if __name__ == "__main__":
    df = load_data()
    plot_heatmap(df)