import pandas as pd

df = pd.read_parquet("m2m100.parquet")
df.to_csv("m2m100.csv", index=False)
