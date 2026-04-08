import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
    )

    plt.figure(figsize=(8,6))

    sns.barplot(
        data=device,
        x="Platform Clean",
        y="count"
    )

    plt.title("Overall Platform Usage")
    plt.xlabel("Platform")
    plt.ylabel("Number of Plays")
    plt.tight_layout()
    plt.show()


def main():
    df = load_final_data()
    df = clean_platform(df)
    plot_device_usage(df)

if __name__ == "__main__":
    main()