import pandas as pd

df = pd.read_csv('Cleaned_Dataset/FoodSpots_cleaned.csv')

df['FoodSpot_ID'] = df['FoodSpot_ID'].str.replace('FS', '').astype(int)

df.to_csv('FoodSpots_cleaned_numeric.csv', index=False)

print("Conversion complete. Saved to FoodSpots_cleaned_numeric.csv")