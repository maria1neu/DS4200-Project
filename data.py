DATA_1 = "listening_history.csv"
DATA_2 = "spotify_history 2.csv"
DATA_3 = "streaming_history.csv"
DATA_4 = "Spotify_Streaming_History.csv"

import pandas as pd

def data_frame(file): 

    data = pd.read_csv(file)
    df = pd.DataFrame(data)

    return df

def column_rename(df): 

    for c in df.columns:
        if c.lower() in ["timestamp", "ts"]:
            df = df.rename(columns={c: "Time Stamp"})
        elif "track_name" in c.lower():
            df = df.rename(columns={c: "Track Name"})
        elif "artist_name" in c.lower():
            df = df.rename(columns={c: "Artist Name"})
        elif "album_name" in c.lower():
            df = df.rename(columns={c: "Album Name"})

    df = df.rename(columns={
        "platform": "Platform Type",
        "reason_start": "Reason Start",
        "reason_end": "Reason End",
        "skipped": "Skipped",
        "shuffle": "Shuffle", 
    })

    return df

def combine_data(df1, df2, df3, df4): 
    dfs = [df1, df2, df3, df4]

    keep_cols = [
        "Time Stamp", "Track Name", "Artist Name", "Album Name",
        "Platform Type", "Reason Start", "Reason End",
        "Skipped", "Shuffle", "Source"
    ]

    cleaned = []
    for i, df in enumerate(dfs, start=1):
        df = column_rename(df)

        # keep only columns that actually exist in this df
        cols_here = [c for c in keep_cols if c in df.columns]
        tmp = df[cols_here].copy()

        # optional: track which file/user it came from
        tmp["Source"] = f"df{i}"

        cleaned.append(tmp)

    new_df = pd.concat(cleaned, ignore_index=True)

    return new_df 

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

def load_final_data():
    df1 = data_frame(DATA_1)  
    df2 = data_frame(DATA_2)
    df3 = data_frame(DATA_3) 
    df4 = data_frame(DATA_4)

    df1 = column_rename(df1)
    df2 = column_rename(df2)  
    df3 = column_rename(df3)  
    df4 = column_rename(df4) 

    final_df = combine_data(df1, df2, df3, df4)
    final_df = clean_platform(final_df)
    final_df["Time Stamp"] = pd.to_datetime(final_df["Time Stamp"], utc=True, errors="coerce")
    final_df["Date"] = final_df["Time Stamp"].dt.date
    final_df["Hour"] = final_df["Time Stamp"].dt.hour

    return final_df

def main(): 

    final_df = load_final_data()
    print(final_df['Platform Clean'].unique())

    final_df.to_csv("data.csv", index=False)


if __name__ == '__main__':
    main()