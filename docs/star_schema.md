# Data Warehouse Modeling (Star Schema)

## Grain
**Fact grain:** 1 row = 1 accident event (Accident_ID).

We use a star schema to separate measures (facts) from descriptive attributes (dimensions) to support fast analytics and clean BI dashboards.

---

## Dimension Tables

### dim_date
- date_key (INT, e.g., 20250109)
- full_date (DATE)
- year (INT)
- month (INT)
- day (INT)
- day_name (STRING)

Source: Dataset 1 `Date`

### dim_time
- time_key (INT)
- hour (INT)
- time_bucket (STRING: 00-05, 06-11, 12-17, 18-23)

Source: Dataset 1 `Time` → extract hour

### dim_location
- location_key (INT)
- location (STRING)

Source: Dataset 1 `Location`

### dim_vehicle
- vehicle_key (INT)
- vehicle_type (STRING)

Source: Dataset 1 `Vehicle_Type`

### dim_environment
- environment_key (INT)
- weather (STRING)
- road_condition (STRING)
- road_type (STRING)

Source: Dataset 1 `Weather`, `Road_Condition`, `Road_Type`

### dim_cause
- cause_key (INT)
- cause (STRING)

Source: Dataset 1 `Cause`

---

## Fact Table

### fact_accident
- accident_id (STRING)  ← business key
- date_key (INT)        ← FK to dim_date
- time_key (INT)        ← FK to dim_time
- location_key (INT)    ← FK to dim_location
- vehicle_key (INT)     ← FK to dim_vehicle
- environment_key (INT) ← FK to dim_environment
- cause_key (INT)       ← FK to dim_cause

Measures/metrics:
- severity (STRING)
- is_severe (INT: 1 if High else 0)
- injuries (INT)
- fatalities (INT)
- vehicle_speed (FLOAT/INT)
- speed_bucket (STRING: 0-20, 21-40, 41-60, 61-80, 80+)
- alcohol_involved (STRING Yes/No)

Cost/impact fields (from Dataset 2):
- insurance_claim (STRING Yes/No)
- claim_amount (FLOAT)
- repair_cost (FLOAT)
- legal_proceedings (STRING Yes/No)
- lawyer_fee (FLOAT)
- total_economic_loss (FLOAT = claim_amount + repair_cost + lawyer_fee)

---

## Data Governance (PII)
Dataset 2 contains PII-like fields:
- Injured_Person_Name
- Contact_Info

These fields are **dropped before loading to the warehouse**.
