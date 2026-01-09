-- Dataset: road_safety_dw
-- Star schema DDL

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_date (
  date_key INT64,
  full_date DATE,
  year INT64,
  month INT64,
  day INT64,
  day_name STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_time (
  time_key INT64,
  hour INT64,
  time_bucket STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_location (
  location_key INT64,
  location STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_vehicle (
  vehicle_key INT64,
  vehicle_type STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_environment (
  environment_key INT64,
  weather STRING,
  road_condition STRING,
  road_type STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.dim_cause (
  cause_key INT64,
  cause STRING
);

CREATE TABLE IF NOT EXISTS road_safety_dw.fact_accident (
  accident_id STRING,
  date_key INT64,
  time_key INT64,
  location_key INT64,
  vehicle_key INT64,
  environment_key INT64,
  cause_key INT64,

  severity STRING,
  is_severe INT64,
  injuries INT64,
  fatalities INT64,

  vehicle_speed FLOAT64,
  speed_bucket STRING,
  alcohol_involved STRING,

  insurance_claim STRING,
  claim_amount FLOAT64,
  repair_cost FLOAT64,

  legal_proceedings STRING,
  lawyer_fee FLOAT64,

  total_economic_loss FLOAT64
);
