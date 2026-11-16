import pandas as pd 

#Load the new, manually classified dataset 
df = pd.read_csv("FoodSpots_Classified2.csv")

food_venues = df[df["Decision"] == "Keep"].copy()
    
#save only columns we need
columns = [
    "Name",
    "Latitude",
    "Longitude",
    "Address",
    "County",
    "Venue Type"
]

food_venues = food_venues[columns]

#unique ID for each row
food_venues.insert(
    0, 
    "FoodSpot_ID",
    [f"FS{i:04d}" for i in range (1, len(food_venues) + 1)]
)

food_venues.to_csv("FoodSpots_cleaned.csv", index=False)

print("Final dataset shape:", food_venues.shape)
print("\nMissing values:")
print(food_venues.isna().sum())
print("\nFinal dataset saved")