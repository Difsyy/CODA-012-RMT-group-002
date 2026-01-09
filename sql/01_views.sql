-- Overall KPI
CREATE OR REPLACE VIEW road_safety_dw.vw_kpi_overall AS
SELECT
  COUNT(*) AS total_accidents,
  SUM(is_severe) AS severe_accidents,
  SUM(injuries) AS total_injuries,
  SUM(fatalities) AS total_fatalities,
  SUM(total_economic_loss) AS total_economic_loss
FROM road_safety_dw.fact_accident;

-- Accidents by month
CREATE OR REPLACE VIEW road_safety_dw.vw_accidents_by_month AS
SELECT
  d.year,
  d.month,
  COUNT(*) AS accidents,
  SUM(f.is_severe) AS severe_accidents,
  SUM(f.fatalities) AS fatalities,
  SUM(f.total_economic_loss) AS total_economic_loss
FROM road_safety_dw.fact_accident f
JOIN road_safety_dw.dim_date d
  ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Hotspots (Top locations)
CREATE OR REPLACE VIEW road_safety_dw.vw_hotspots AS
SELECT
  l.location,
  COUNT(*) AS accidents,
  SUM(f.fatalities) AS fatalities,
  SUM(f.injuries) AS injuries,
  SUM(f.total_economic_loss) AS total_economic_loss
FROM road_safety_dw.fact_accident f
JOIN road_safety_dw.dim_location l
  ON f.location_key = l.location_key
GROUP BY l.location
ORDER BY accidents DESC;

-- Environment risk (severe rate)
CREATE OR REPLACE VIEW road_safety_dw.vw_environment_risk AS
SELECT
  e.weather,
  e.road_condition,
  e.road_type,
  COUNT(*) AS accidents,
  AVG(CAST(f.is_severe AS FLOAT64)) AS severe_rate,
  SUM(f.fatalities) AS fatalities
FROM road_safety_dw.fact_accident f
JOIN road_safety_dw.dim_environment e
  ON f.environment_key = e.environment_key
GROUP BY e.weather, e.road_condition, e.road_type
ORDER BY severe_rate DESC;

-- Speed impact
CREATE OR REPLACE VIEW road_safety_dw.vw_speed_impact AS
SELECT
  speed_bucket,
  COUNT(*) AS accidents,
  AVG(CAST(is_severe AS FLOAT64)) AS severe_rate,
  SUM(fatalities) AS fatalities,
  SUM(total_economic_loss) AS total_economic_loss
FROM road_safety_dw.fact_accident
GROUP BY speed_bucket
ORDER BY speed_bucket;
