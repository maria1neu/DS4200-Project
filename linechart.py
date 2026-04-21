import pandas as pd
import plotly.graph_objects as go
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

def plot_finals_vs_nonfinals(df):
    finals_months = ["May", "Dec"]
    df["is_finals"] = df["month"].isin(finals_months)
    agg = (
        df.groupby(["year", "is_finals", "month"])
        .size()
        .reset_index(name="plays")
    )
    avg_agg = (
        agg.groupby(["year", "is_finals"])["plays"]
        .mean()
        .reset_index(name="avg_monthly_plays")
    )
    finals = avg_agg[avg_agg["is_finals"] == True]
    non_finals = avg_agg[avg_agg["is_finals"] == False]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=finals["year"],
        y=finals["avg_monthly_plays"],
        mode="lines+markers",
        name="Finals Months (May & Dec)",
        line=dict(color="rgba(255, 80, 80, 0.9)", width=2),
        marker=dict(size=7)
    ))
    fig.add_trace(go.Scatter(
        x=non_finals["year"],
        y=non_finals["avg_monthly_plays"],
        mode="lines+markers",
        name="Non-Finals Months",
        line=dict(color="rgba(29, 185, 84, 0.9)", width=2),
        marker=dict(size=7)
    ))
    fig.update_layout(
    title="Average Monthly Listening: Finals vs. Non-Finals Months Over Time",
    xaxis_title="Year",
    yaxis_title="Average Plays per Month",
    legend_title="Period",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(color="#000000"),
    xaxis=dict(gridcolor="#dddddd"),
    yaxis=dict(gridcolor="#dddddd"),
)
    fig.write_html("linechart.html")

if __name__ == "__main__":
    df = load_data()
    plot_finals_vs_nonfinals(df)
