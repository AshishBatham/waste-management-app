import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Parameters
regions = ["North", "South", "East", "West", "Central"]
facilities = ["Plant A", "Plant B", "Plant C", "Plant D"]
waste_types = ["Organic", "Plastic", "Metal", "Glass"]
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='MS')

# Generate data
data = []
for date in date_range:
    for region in regions:
        record = {
            "Date": date,
            "Region": region,
            "Facility": random.choice(facilities),
            "Organic": np.random.randint(100, 300),
            "Plastic": np.random.randint(50, 200),
            "Metal": np.random.randint(20, 100),
            "Glass": np.random.randint(30, 120),
        }
        record["Total_Waste"] = sum([record[w] for w in waste_types])
        record["Recycled_Waste"] = int(record["Total_Waste"] * np.random.uniform(0.3, 0.7))
        record["Efficiency"] = round(np.random.uniform(0.6, 0.95), 2)
        data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("sample_waste_data.csv", index=False)
print("✅ waste_data.csv generated successfully.")
