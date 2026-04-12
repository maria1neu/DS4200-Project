import pandas as pd
import plotly.express as px
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


def plot_device_usage(df):
    device = (
        df.groupby("Platform Clean")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)  # 🔥 highest → lowest
    )

    fig = px.bar(
        device,
        x="Platform Clean",
        y="count",
        title="Overall Platform Usage",
        text="count"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        xaxis_title="Platform",
        yaxis_title="Number of Plays"
    )

    fig.write_image("platform_usage_bar.png")


    return device


def main():
    df = load_final_data()
    df = clean_platform(df)

    plot_devices = plot_device_usage(df)


if __name__ == "__main__":
    main()