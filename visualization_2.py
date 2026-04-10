import pandas as pd
import plotly.graph_objects as go
import itertools
from data import load_final_data


def clean_platform(df):
    df["Platform Type"] = df["Platform Type"].fillna("").str.lower()

    def simplify(platform):
        if "ios" in platform:
            return "iOS"
        elif "android" in platform:
            return "Android"
        elif "windows" in platform or "mac" in platform:
            return "Desktop"
        elif "web" in platform:
            return "Web"
        else:
            return "Other"

    df["Platform Clean"] = df["Platform Type"].apply(simplify)
    return df


def main():
    df = load_final_data()
    df = clean_platform(df)

    df["Time Stamp"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Hour"], unit="h")
    df["Day of Week"] = df["Time Stamp"].dt.day_name()

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    all_hours = list(range(24))

    df["Day of Week"] = pd.Categorical(
        df["Day of Week"],
        categories=week_days,
        ordered=True
    )

    heatmap_data = df.groupby(["Day of Week", "Hour"]).size().reset_index(name="count")

    full_grid = pd.DataFrame(
        list(itertools.product(week_days, all_hours)),
        columns=["Day of Week", "Hour"]
    )

    heatmap_data = full_grid.merge(
        heatmap_data,
        on=["Day of Week", "Hour"],
        how="left"
    )

    heatmap_data["count"] = heatmap_data["count"].fillna(0)

    pivot_data = heatmap_data.pivot(
        index="Day of Week",
        columns="Hour",
        values="count"
    ).reindex(week_days)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_data.values,
            x=all_hours,
            y=week_days,
            colorscale="Blues",
            colorbar=dict(title="Count"),
            hovertemplate="Day: %{y}<br>Hour: %{x}<br>Count: %{z}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Listening Activity by Hour and Day",
        xaxis_title="Hour",
        yaxis_title="Day of Week",
        width=1000,
        height=500
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=all_hours,
        ticktext=[str(h) for h in all_hours]
    )

    fig.write_html("heatmap_days.html")


if __name__ == "__main__":
    main()