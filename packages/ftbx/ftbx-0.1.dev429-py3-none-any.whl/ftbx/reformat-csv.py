import pandas as pd

df = pd.read_csv("combined_file.csv") 
df['created'] = pd.to_datetime(df['created'], format='%d %b %Y %H:%M:%S %z').dt.strftime('%Y-%m-%d')
df['name'] = df['name'].str.replace(r'-\d+$', '', regex=True)
df = df.sort_values(by='created')

print(df)
df.to_csv("add.csv", index=False)  # Save to CSV without the index
