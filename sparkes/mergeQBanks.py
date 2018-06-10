import pandas as pd

a = pd.read_csv("../data/qbank.csv")
b = pd.read_csv("../data/qbankextra.csv")
b = b.dropna(axis=1)
merged = a.merge(b, on='Question')
merged.to_csv("../data/qbankmerge.csv", index=False)