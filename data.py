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
        "Skipped", "Shuffle"
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

def get_months(df):
    df["Time Stamp"] = pd.to_datetime(df["Time Stamp"], utc=True, errors="coerce")
    df["Date"] = df["Time Stamp"].dt.strftime("%Y-%m-%d")
    print(df["Date"].head())

def main(): 

    df1 = data_frame(DATA_1)  
    df2 = data_frame(DATA_2)
    df3 = data_frame(DATA_3) 
    df4 = data_frame(DATA_4)

    df1 = column_rename(df1)
    df2 = column_rename(df2)  
    df3 = column_rename(df3)  
    df4 = column_rename(df4)  

    final_df = combine_data(df1, df2, df3, df4)
    print(final_df.shape)
    print(final_df["Time Stamp"].head())

if __name__ == '__main__':
    main()