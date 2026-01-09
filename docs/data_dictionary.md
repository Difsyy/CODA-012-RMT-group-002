# Data Dictionary

## Dataset 1: road_accident_dataset_1.csv
- Accident_ID: Unique accident identifier
- Location: Accident location
- Date: Date of accident
- Time: Time of accident
- Severity: Low/Medium/High
- Injuries: Number of injuries
- Fatalities: Number of fatalities
- Weather: Weather condition
- Road_Condition: Road surface condition
- Road_Type: Road type
- Vehicle_Type: Vehicle category
- Vehicle_Speed: Speed at incident
- Alcohol_Involved: Yes/No
- Cause: Main accident cause

## Dataset 2: road_accident_dataset_2.csv
- Accident_ID: Unique accident identifier (join key)
- Investigation_Status: status
- Police_Station: reporting station
- Reported_By: reporter type
- Insurance_Claim: Yes/No
- Claim_Amount: insurance claim amount
- Repair_Cost: estimated repair cost
- Legal_Proceedings: Yes/No
- Lawyer_Involved: Yes/No
- Lawyer_Fee: legal cost
- Injured_Person_Name: (PII-like) removed before warehouse
- Contact_Info: (PII-like) removed before warehouse
