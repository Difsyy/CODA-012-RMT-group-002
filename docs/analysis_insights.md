# Analysis, Storytelling, and Recommendations (SDG 11 – Road Safety)

## KPI Summary (from dashboard / BigQuery)
- Total accidents: 5,000
- Severe accidents: 1,622 (Severe rate = 32.44%)
- Total injuries: 22,283
- Total fatalities: 5,059
- Total economic loss: 56,080,814

## Key Findings

### 1) Trend over time (Time series)
- Highest accident period: 2022-01-01 (31 accidents)
- Lowest accident period: 2022-01-01 (31 accidents)
- Pattern observed: The monthly accident count appears **stable/flat** across the selected period (accidents are around the same value each month).  
  *This suggests the dataset is likely synthetic or evenly generated, so the time trend is not strongly seasonal.*

### 2) Hotspots (Top locations)
- Top 3 locations by accident count: Location_12, Location_43, Location_325 (each 1 accident)
- Location with highest fatalities: Location_968 (2 fatalities)
- Interpretation: Accident counts are **distributed across many locations** (no single location dominates by accident count).  
  Therefore, the location with the highest fatalities (Location_968) is more meaningful for targeted intervention than accident-count hotspots.

### 3) Risk factors (Weather/Road)
- Highest severe_rate combination:
  - Weather = Clear
  - Road_Condition = Wet
  - Road_Type = Highway
- Evidence: 200 accidents, severe_rate = 0.375 (37.5%), fatalities = 197
- Insight: Even when weather is clear, **wet highway conditions** are associated with higher severity and large fatality counts.  
  This indicates road surface condition + high-speed road type can be more critical than weather alone.

### 4) Speed impact
- Speed bucket with highest severe_rate: 0–20 (severe_rate ≈ 0.3333 = 33.33%)
- Speed bucket with highest fatalities: 41–60 (fatalities = 1,384)
- Interpretation: While the severe rate is high even at low speed bucket in this dataset, the **largest fatality burden** occurs at **moderate speeds (41–60)**.  
  This suggests the 41–60 range is a priority segment for road safety interventions because it combines high exposure and fatal outcomes.

### 5) Economic impact
- Highest economic loss segment (speed): speed bucket 41–60 with total_economic_loss = 14,847,523
- Highest economic loss location: Location_3966 with total_economic_loss = 19,453
- Insight: The largest financial burden is concentrated in the **41–60 speed range**, meaning prevention in this speed segment can reduce both human impact (fatalities) and financial costs (claims/repairs/legal fees) most effectively.

## Recommendations (Actionable)

1) Speed control intervention
- Target: speed bucket 41–60 (highest fatalities and highest total_economic_loss) and monitor 0–20 (highest severe_rate)
- Action:
  - Deploy speed enforcement and monitoring in corridors where drivers commonly operate at 41–60
  - Add warning signage and speed-calming measures (rumble strips, speed display signs) on high-risk segments
  - Run safety campaigns to discourage risky driving behavior within the 41–60 range

2) Hotspot engineering improvements
- Target: Location_968 (highest fatalities)
- Action:
  - Improve road markings, lighting, and hazard signage
  - Review potential dangerous points (intersections/curves/merging lanes) and apply traffic calming where needed
  - Prioritize response-readiness (faster emergency response can reduce fatalities)

3) Weather/road condition preparedness
- Target conditions: Clear + Wet + Highway (highest severe_rate and high fatalities)
- Action:
  - Improve road drainage and apply anti-skid treatments on highway surfaces
  - Provide “slippery road” alerts and temporary reduced speed messaging after rain
  - Increase enforcement and safety messaging during wet-road periods

4) Reduce economic burden
- Target: speed bucket 41–60 (highest total_economic_loss) and Location_3966 (highest loss location)
- Action:
  - Prioritize prevention programs for the 41–60 segment to reduce insurance/repair/legal costs
  - Review high-cost locations for engineering fixes and faster incident handling to reduce downstream costs
  - Improve reporting and claim handling processes (can reduce legal overhead)

## Challenges / Limitations
- The dataset shows relatively uniform monthly accident counts and many locations with similar counts (synthetic-like distribution).  
  Therefore, conclusions focus on the strongest observed risk-factor patterns (wet highways, speed segment 41–60, and severity rate) rather than strong seasonal/hotspot clustering.
