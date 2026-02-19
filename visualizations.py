
import pandas as pd
import altair as alt
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

def add_genres(df):
    track_df = pd.read_csv("track_data_final.csv")
    track_df["artist_name"] = track_df["artist_name"].str.strip().str.lower()
    df["artist_name_lower"] = df["Artist Name"].str.strip().str.lower()

    merged = df.merge(
        track_df[["artist_name", "artist_genres"]].drop_duplicates("artist_name"),
        left_on="artist_name_lower",
        right_on="artist_name",
        how="left"
    )

    merged["genre"] = (
        merged["artist_genres"]
        .fillna("unknown")
        .str.extract(r"'([^']+)'")[0]
        .fillna("unknown")
    )

    return merged

def plot_heatmap(df):
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    agg = df.groupby(["year", "month"]).size().reset_index(name="plays")

    chart = (
        alt.Chart(agg)
        .mark_rect()
        .encode(
            x=alt.X("month:O", sort=month_order),
            y=alt.Y("year:O"),
            color=alt.Color("plays:Q"),
            tooltip=["year:O", "month:O", "plays:Q"]
        )
        .properties(title="listening activity by month and year")
    )

    chart.save("heatmap.html")

def plot_sankey(df):
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    agg = (
        df[df["genre"] != "unknown"]
        .groupby(["month", "genre"])
        .size()
        .reset_index(name="plays")
    )

    top_genres = agg.groupby("genre")["plays"].sum().nlargest(8).index.tolist()
    agg = agg[agg["genre"].isin(top_genres)]

    months = [m for m in month_order if m in agg["month"].values]
    nodes = months + top_genres
    node_idx = {n: i for i, n in enumerate(nodes)}

    fig = go.Figure(go.Sankey(
        node=dict(label=nodes),
        link=dict(
            source=[node_idx[m] for m in agg["month"]],
            target=[node_idx[g] for g in agg["genre"]],
            value=agg["plays"].tolist()
        )
    ))

    fig.write_html("sankey.html")

if __name__ == "__main__":
    df = load_data()
    df = add_genres(df)
    plot_heatmap(df)
    plot_sankey(df)