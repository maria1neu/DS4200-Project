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

def plot_sankey(df):
    semester_map = {
        "Jan": "Spring Semester", "Feb": "Spring Semester", "Mar": "Spring Semester",
        "Apr": "Spring Finals", "May": "Spring Finals",
        "Jun": "Summer", "Jul": "Summer", "Aug": "Summer",
        "Sep": "Fall Semester", "Oct": "Fall Semester",
        "Nov": "Fall Finals", "Dec": "Fall Finals",
    }
    finals_groups = {"Spring Finals", "Fall Finals"}
    semester_order = ["Spring Semester", "Spring Finals", "Summer", "Fall Semester", "Fall Finals"]
    df = df.copy()
    df["semester"] = df["month"].map(semester_map)
    agg = (
        df[df["genre"] != "unknown"]
        .groupby(["semester", "genre"])
        .size()
        .reset_index(name="plays")
    )
    top_genres = agg.groupby("genre")["plays"].sum().nlargest(8).index.tolist()
    agg = agg[agg["genre"].isin(top_genres)]
    agg["semester"] = pd.Categorical(agg["semester"], categories=semester_order, ordered=True)
    agg = agg.sort_values("semester")
    skip_df = (
        df[df["genre"].isin(top_genres)]
        .groupby("genre")
        .apply(lambda x: round(x["Skipped"].fillna(0).astype(float).mean() * 100, 1), include_groups=False)
        .reset_index(name="skip_rate")
    )
    skip_map = dict(zip(skip_df["genre"], skip_df["skip_rate"]))
    genre_labels = [f"{g} ({skip_map.get(g, '?')}% skipped)" for g in top_genres]
    genre_label_map = dict(zip(top_genres, genre_labels))
    semesters = [s for s in semester_order if s in agg["semester"].values]
    nodes = semesters + genre_labels
    node_idx = {n: i for i, n in enumerate(nodes)}
    node_colors = []
    for n in nodes:
        if n in finals_groups:
            node_colors.append("rgba(255, 80, 80, 0.8)")
        elif n in semester_order:
            node_colors.append("rgba(29, 185, 84, 0.8)")
        else:
            node_colors.append("rgba(150, 150, 150, 0.6)")
    fig = go.Figure(go.Sankey(
        node=dict(label=nodes, color=node_colors, pad=15, thickness=20),
        link=dict(
            source=[node_idx[s] for s in agg["semester"]],
            target=[node_idx[genre_label_map[g]] for g in agg["genre"]],
            value=agg["plays"].tolist()
        )
    ))
    fig.update_layout(
        title_text="Listening Flow by Semester & Genre (with Spotify Skip Rate) — Red = Finals Periods",
        font=dict(size=12)
    )
    fig.write_html("sankey_new.html")

if __name__ == "__main__":
    df = load_data()
    df = add_genres(df)
    plot_sankey(df)
