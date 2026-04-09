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

def main():
    df = load_final_data()
    df = clean_platform(df)

    df["Time Stamp"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Hour"], unit="h") 
    df["Day of Week"] = df["Time Stamp"].dt.day_name()  

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    unique_days = df[["Date", "Day of Week"]].drop_duplicates()

    count = df.drop_duplicates("Date")[~df.drop_duplicates("Date")["Day of Week"].isin(week_days)].shape[0]

    df["Is Weekend"] = ~df["Day of Week"].isin(week_days)

    df.groupby("Is Weekend").size()

    df["Day of Week"] = pd.Categorical(
        df["Day of Week"],
        categories=week_days,
        ordered=True
    )    
    heatmap_data = df.groupby(["Day of Week", "Hour"]).size().unstack(fill_value=0)

    plt.figure(figsize=(12,6))
    sns.heatmap(heatmap_data, cmap="Blues")

    plt.title("Listening Activity by Hour and Day")
    plt.xlabel("Hour")
    plt.ylabel("Day of Week")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()