import pandas as pd

PATH1 = "data/raw/road_accident_dataset_1.csv"
PATH2 = "data/raw/road_accident_dataset_2.csv"

df1 = pd.read_csv(PATH1)
df2 = pd.read_csv(PATH2)

print("=== BASIC INFO ===")
print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)
print("\nDataset 1 columns:\n", df1.columns.tolist())
print("\nDataset 2 columns:\n", df2.columns.tolist())

print("\n=== MISSING VALUES (Dataset 1) ===")
print(df1.isna().sum().sort_values(ascending=False))

print("\n=== MISSING VALUES (Dataset 2) ===")
print(df2.isna().sum().sort_values(ascending=False))

print("\n=== DUPLICATE Accident_ID CHECK ===")
print("df1 Accident_ID unique:", df1["Accident_ID"].nunique(), "out of", len(df1))
print("df2 Accident_ID unique:", df2["Accident_ID"].nunique(), "out of", len(df2))
print("df1 duplicated Accident_ID:", df1["Accident_ID"].duplicated().sum())
print("df2 duplicated Accident_ID:", df2["Accident_ID"].duplicated().sum())

print("\n=== PII CHECK (Dataset 2) ===")
pii_cols = ["Injured_Person_Name", "Contact_Info"]
present = [c for c in pii_cols if c in df2.columns]
print("PII-like columns present:", present)
if present:
    print(df2[present].head())

print("\n=== QUICK DISTRIBUTIONS (Dataset 1) ===")
if "Severity" in df1.columns:
    print("\nSeverity:")
    print(df1["Severity"].value_counts(dropna=False))

if "Alcohol_Involved" in df1.columns:
    print("\nAlcohol_Involved:")
    print(df1["Alcohol_Involved"].value_counts(dropna=False))

print("\n=== NUMERIC SUMMARY ===")
num1 = [c for c in ["Injuries", "Fatalities", "Vehicle_Speed"] if c in df1.columns]
if num1:
    print("\nDataset 1 numeric describe:")
    print(df1[num1].describe())

num2 = [c for c in ["Claim_Amount", "Repair_Cost", "Lawyer_Fee"] if c in df2.columns]
if num2:
    print("\nDataset 2 numeric describe:")
    print(df2[num2].describe())

print("\n✅ Profiling complete.")
