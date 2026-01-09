import os
import pandas as pd

# =========================================================
# CONFIG
# =========================================================
RAW_1 = "data/raw/road_accident_dataset_1.csv"
RAW_2 = "data/raw/road_accident_dataset_2.csv"
OUT_DIR = "data/processed"

# Join strategy:
# - "inner" keeps only Accident_ID present in BOTH datasets (complete records for cost analysis)
# - "left" keeps ALL accidents from dataset 1, cost fields may be missing -> filled as 0/Unknown
JOIN_TYPE = "inner"

PII_COLS = ["Injured_Person_Name", "Contact_Info"]
UNKNOWN = "Unknown"


# =========================================================
# HELPERS
# =========================================================
def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def clean_text_series(s: pd.Series) -> pd.Series:
    """
    Standardize categorical/text columns:
    - strip spaces
    - replace NaN/None/empty with 'Unknown'
    """
    return (
        s.astype(str)
        .str.strip()
        .replace(
            {
                "nan": UNKNOWN,
                "None": UNKNOWN,
                "": UNKNOWN,
                "NaN": UNKNOWN,
                "NULL": UNKNOWN,
                "null": UNKNOWN,
            }
        )
        .fillna(UNKNOWN)
    )


def to_numeric_fill0(df: pd.DataFrame, cols: list[str]) -> None:
    """
    Convert numeric columns to numeric and fill missing as 0.
    """
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)


def bucket_hour(h) -> str:
    """
    Create time bucket based on hour (0-23)
    """
    if pd.isna(h):
        return UNKNOWN
    h = int(h)
    if 0 <= h <= 5:
        return "00-05"
    if 6 <= h <= 11:
        return "06-11"
    if 12 <= h <= 17:
        return "12-17"
    if 18 <= h <= 23:
        return "18-23"
    return UNKNOWN


def bucket_speed(v) -> str:
    """
    Bucket vehicle speed into ranges (adjust as needed)
    """
    if pd.isna(v):
        return UNKNOWN
    v = float(v)
    if v <= 20:
        return "0-20"
    if v <= 40:
        return "21-40"
    if v <= 60:
        return "41-60"
    if v <= 80:
        return "61-80"
    return "80+"


def missing_report(df: pd.DataFrame, title: str, top_n: int = 12) -> None:
    print(f"\n--- {title} (Top {top_n}) ---")
    miss = df.isna().sum().sort_values(ascending=False)
    print(miss.head(top_n))


def build_dim_from_cols(df: pd.DataFrame, cols: list[str], key_name: str) -> tuple[pd.DataFrame, pd.Series]:
    """
    Build a dimension table from unique combinations of columns.
    Returns:
      - dim table with surrogate key
      - a Series of keys aligned with df rows
    """
    dim = df[cols].drop_duplicates().reset_index(drop=True)
    dim[key_name] = dim.index + 1
    keys = df[cols].merge(dim, on=cols, how="left")[key_name]
    return dim[[key_name] + cols], keys


# =========================================================
# 1) EXTRACT
# =========================================================
def extract() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not os.path.exists(RAW_1):
        raise FileNotFoundError(f"Missing raw dataset: {RAW_1}")
    if not os.path.exists(RAW_2):
        raise FileNotFoundError(f"Missing raw dataset: {RAW_2}")

    df1 = pd.read_csv(RAW_1)
    df2 = pd.read_csv(RAW_2)

    print("✅ Loaded raw datasets")
    print(" - df1 shape:", df1.shape)
    print(" - df2 shape:", df2.shape)

    return df1, df2


# =========================================================
# 2) TRANSFORM (cleaning + feature engineering)
# =========================================================
def transform(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # Drop PII-like columns ASAP
    df2 = df2.drop(columns=PII_COLS, errors="ignore")

    # Merge on Accident_ID
    df = df1.merge(df2, on="Accident_ID", how=JOIN_TYPE)
    print(f"✅ Merged datasets using JOIN_TYPE='{JOIN_TYPE}' -> shape:", df.shape)

    # Missingness BEFORE cleaning (merged)
    missing_report(df, "Missing values BEFORE cleaning (merged)")

    # ---- Parse Date ----
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with missing Date (recommended for time-based dashboard)
    before = len(df)
    df = df.dropna(subset=["Date"])
    dropped = before - len(df)
    print(f"✅ Dropped rows with missing/invalid Date: {dropped} (kept {len(df)})")

    # Create date_key immediately (YYYYMMDD)
    df["date_key"] = df["Date"].dt.strftime("%Y%m%d").astype(int)

    # ---- Parse Time -> Hour ----
    # Your Time may look like "1970-01-01 14:00:00" or "14:00:00" depending on dataset.
    if "Time" in df.columns:
        parsed_time = pd.to_datetime(df["Time"], errors="coerce")
        df["hour"] = parsed_time.dt.hour
    else:
        df["hour"] = pd.NA

    df["time_bucket"] = df["hour"].apply(bucket_hour)

    # ---- Numeric conversions ----
    numeric_cols = ["Injuries", "Fatalities", "Vehicle_Speed", "Claim_Amount", "Repair_Cost", "Lawyer_Fee"]
    to_numeric_fill0(df, numeric_cols)

    # ---- Categorical cleaning ----
    cat_cols = [
        "Location", "Severity", "Weather", "Road_Condition", "Road_Type",
        "Vehicle_Type", "Alcohol_Involved", "Cause",
        "Insurance_Claim", "Investigation_Status", "Legal_Proceedings"
    ]
    for c in cat_cols:
        if c in df.columns:
            df[c] = clean_text_series(df[c])

    # ---- Feature engineering ----
    df["is_severe"] = (df["Severity"].str.lower() == "high").astype(int) if "Severity" in df.columns else 0
    df["speed_bucket"] = df["Vehicle_Speed"].apply(bucket_speed) if "Vehicle_Speed" in df.columns else UNKNOWN
    df["total_economic_loss"] = df.get("Claim_Amount", 0) + df.get("Repair_Cost", 0) + df.get("Lawyer_Fee", 0)

    # Missingness AFTER cleaning
    missing_report(df, "Missing values AFTER cleaning (post-transform)")

    return df


# =========================================================
# 3) BUILD STAR SCHEMA (dim_* + fact)
# =========================================================
def build_star_schema(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # ---------- dim_date ----------
    dim_date = (
        df[["date_key", "Date"]]
        .drop_duplicates()
        .sort_values("date_key")
        .reset_index(drop=True)
    )
    dim_date["full_date"] = dim_date["Date"].dt.date
    dim_date["year"] = dim_date["Date"].dt.year
    dim_date["month"] = dim_date["Date"].dt.month
    dim_date["day"] = dim_date["Date"].dt.day
    dim_date["day_name"] = dim_date["Date"].dt.day_name()
    dim_date = dim_date[["date_key", "full_date", "year", "month", "day", "day_name"]]

    # ---------- dim_time ----------
    dim_time = df[["hour", "time_bucket"]].drop_duplicates().reset_index(drop=True)
    dim_time["time_key"] = dim_time.index + 1
    dim_time = dim_time[["time_key", "hour", "time_bucket"]]

    df = df.merge(dim_time, on=["hour", "time_bucket"], how="left")

    # ---------- dim_location ----------
    dim_location, df["location_key"] = build_dim_from_cols(df, ["Location"], "location_key")
    dim_location = dim_location.rename(columns={"Location": "location"})

    # ---------- dim_vehicle ----------
    dim_vehicle, df["vehicle_key"] = build_dim_from_cols(df, ["Vehicle_Type"], "vehicle_key")
    dim_vehicle = dim_vehicle.rename(columns={"Vehicle_Type": "vehicle_type"})

    # ---------- dim_environment ----------
    env_cols = ["Weather", "Road_Condition", "Road_Type"]
    dim_environment, df["environment_key"] = build_dim_from_cols(df, env_cols, "environment_key")
    dim_environment = dim_environment.rename(columns={
        "Weather": "weather",
        "Road_Condition": "road_condition",
        "Road_Type": "road_type",
    })

    # ---------- dim_cause ----------
    dim_cause, df["cause_key"] = build_dim_from_cols(df, ["Cause"], "cause_key")
    dim_cause = dim_cause.rename(columns={"Cause": "cause"})

    # ---------- fact_accident ----------
    fact_accident = pd.DataFrame({
        "accident_id": df["Accident_ID"].astype(str),

        "date_key": df["date_key"],
        "time_key": df["time_key"],

        "location_key": df["location_key"],
        "vehicle_key": df["vehicle_key"],
        "environment_key": df["environment_key"],
        "cause_key": df["cause_key"],

        "severity": df.get("Severity", UNKNOWN),
        "is_severe": df.get("is_severe", 0),

        "injuries": df.get("Injuries", 0).astype(int),
        "fatalities": df.get("Fatalities", 0).astype(int),

        "vehicle_speed": df.get("Vehicle_Speed", 0),
        "speed_bucket": df.get("speed_bucket", UNKNOWN),
        "alcohol_involved": df.get("Alcohol_Involved", UNKNOWN),

        "insurance_claim": df.get("Insurance_Claim", UNKNOWN),
        "claim_amount": df.get("Claim_Amount", 0),

        "repair_cost": df.get("Repair_Cost", 0),

        "legal_proceedings": df.get("Legal_Proceedings", UNKNOWN),
        "lawyer_fee": df.get("Lawyer_Fee", 0),

        "total_economic_loss": df.get("total_economic_loss", 0),
    })

    # sanity check
    if fact_accident["accident_id"].isna().any():
        raise ValueError("fact_accident has null accident_id. Check Accident_ID.")

    return {
        "dim_date": dim_date,
        "dim_time": dim_time,
        "dim_location": dim_location,
        "dim_vehicle": dim_vehicle,
        "dim_environment": dim_environment,
        "dim_cause": dim_cause,
        "fact_accident": fact_accident,
    }


# =========================================================
# 4) EXPORT
# =========================================================
def export_tables(tables: dict[str, pd.DataFrame]) -> None:
    ensure_dir(OUT_DIR)
    for name, t in tables.items():
        out_path = os.path.join(OUT_DIR, f"{name}.csv")
        t.to_csv(out_path, index=False)
        print(f"✅ Exported {name}: {t.shape} -> {out_path}")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    df1, df2 = extract()
    df_clean = transform(df1, df2)
    tables = build_star_schema(df_clean)
    export_tables(tables)

    print("\n🎉 ETL complete.")
    print("Next: Upload data/processed/*.csv to BigQuery (Step 4).")
    print(f"Note: JOIN_TYPE='{JOIN_TYPE}' (change in script if needed).")
