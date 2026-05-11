import pandas as pd
import glob

# find all summary files
files = glob.glob("*_summary.csv")

all_data = []

for f in files:
    df = pd.read_csv(f)
    all_data.append(df)

# combine all
combined = pd.concat(all_data, ignore_index=True)

# save file
combined.to_csv("combined_summary.csv", index=False)

print("combined_summary.csv created")
