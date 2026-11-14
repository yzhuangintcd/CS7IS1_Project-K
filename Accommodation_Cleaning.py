import pandas as pd 

"""
FILE PURPOSE 

This scirpt explores, validates, and cleans the Accommodation dataset
The original dataset has 2,297 accomodation records with 13 columns 

The script:
1. Loads the original CSV and checks its structure 
2. Removes leading + trailing whitespace from text fields 
3. Standardises county names, fixes typos in town names
4. Converts the numerical fields to their appropriate data types, handling missing values
5. Identifies and corrects likely geographical errors in the coordinates
6. Extracts numerical star ratings, preserving the original Rating column
7. Validates the cleaned dataset, exports it to a new CSV

The cleaned dataset contains an addtional column: Star Rating
"""

#------------------------------------------------------------------------------------------
#LOAD AND EXPLORE DATASET

df = pd.read_csv("Accommodation.csv")

# print(df.shape)
# print(df.columns.tolist())
# print(df.head())
# print(df.isnull().sum())
# print(df["Property Reg Number"].is_unique)
# print(df["Property Reg Number"].duplicated().sum())
# print(df["Sector"].value_counts())
# print(df["Address County"].value_counts())
# print(df["Rating"].value_counts(dropna=False))

#------------------------------------------------------------------------------------------
#CLEAN TEXT FIELDS

text_columns = [
    "Sector",
    "Property Reg Number", 
    "Account Name",
    "Address Line 1",
    "Address City/Town",
    "Address County",
    "Rating",
]

#remove leading and trailing whitespace from text columns
for col in text_columns:
    df[col] = df[col].astype("string").str.strip()
    
#fix typos in town names
town_corrections = {
    "Ballybunnion": "Ballybunion",
    "Ballyvaugan": "Ballyvaughan",
    "Caherciveen": "Cahersiveen",
    "Fethard-On-Sea": "Fethard-on-Sea", 
    "Glencolumkille": "Glencolmcille", 
    "Louisburg": "Louisburgh",
    "MItchelstown": "Mitchelstown",
    "Newmarket on Fergus": "Newmarket-on-Fergus",
    "Newmarket-On-Fergus": "Newmarket-on-Fergus",
    "Enniskerry Village": "Enniskerry",
    "Leenane": "Leenaun", 
    "Inniscrone": "Enniscrone",
    "Carrick-On-Shannon": "Carrick-on-Shannon",
    "Carrick-On-Suir": "Carrick-on-Suir",
    "Carrig-On-Bannow": "Carrig-on-Bannow",
}

df["Address City/Town"] = (
    df["Address City/Town"]
    .replace(town_corrections)
)

#------------------------------------------------------------------------------------------
#CLEAN COORDINATES

#invalid numerical values -> NaN
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

#identify likely swapped latitude and longitude values 
#irish latitude is between 51 and 56, longitude is between -11 and -5
swapped_coords = (
    df["Latitude"].between(5, 11)
    & df["Longitude"].between(51, 56)
)

#store original values before swapping 
original_lat = df.loc[swapped_coords, "Latitude"].copy()
original_lon = df.loc[swapped_coords, "Longitude"].copy()

df.loc[swapped_coords, "Latitude"] = original_lon
df.loc[swapped_coords, "Longitude"] = -original_lat

print("Swapped coordinates corrected:", swapped_coords.sum())

#identify likely missing negative signs in longitude 
#e.g. longitude = 8.5 -> -8.5
positive_longitude = (
    df["Latitude"].between(51, 56)
    & df["Longitude"].between(5, 11)
)

df.loc[positive_longitude, "Longitude"] = -df.loc[positive_longitude, "Longitude"]
print("Positive longitudes corrected:", positive_longitude.sum())

#replace (0,0) coordinates with NaN
zero_coords = (df["Latitude"] == 0) & (df["Longitude"] == 0)
df.loc[zero_coords, ["Latitude", "Longitude"]] = pd.NA
print("Zero coordinates replaced with NaN:", zero_coords.sum())

#------------------------------------------------------------------------------------------
#EXTRACT NUMERICAL STAR RATINGS

#extract a star rating if exactly one is present 
stars = (
    df["Rating"]
    .fillna("")
    .str.findall(r"(?i)\b([1-5])\s*star\b")
) 

#create a new Star Rating columns with extracted values
#original classification is still available in Rating Original 
df["Star Rating"] = stars.apply(
    lambda x: int(x[0]) if len(x) == 1 else pd.NA
).astype("Int64")

#------------------------------------------------------------------------------------------
#VALIDATE CLEANED DATASET

print("\n -- VALIDATION OF CLEANED DATASET --\n")

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate registration numbers:")
print(df["Property Reg Number"].duplicated().sum())

print("\nNumber of counties")
print(df["Address County"].nunique())

print("\nStar rating distribution")
print(df["Star Rating"].value_counts(dropna=False))

#count records with both coordinates complete
complete_coords = df[["Latitude", "Longitude"]].notna().all(axis=1)
print("\nRecords with complete coordinates:")
print(complete_coords.sum())

#check if complete coordinates fall within bounds for Ireland
invalid_coords = (
    complete_coords
    & ~(
        df["Latitude"].between(51, 56)
        & df["Longitude"].between(-11, -5)
    )
)
print("\nPotentially invalid coordinates:")
print(invalid_coords.sum())

#display any records with invalid coordinates
if invalid_coords.any():
    print("\nRecords with invalid coordinates:")
    print(
        df.loc[
            invalid_coords,
            [
                "Account Name",
                "Address County",
                "Address City/Town",
                "Latitude",
                "Longitude"
            ]
        ].to_string(index=False)
    )

#------------------------------------------------------------------------------------------
#SAVE DATASET

#only want these columns
columns = [
    "Sector",
    "Property Reg Number", 
    "Account Name",
    "Rating",
    "Star Rating",
    "Address Line 1",
    "Address City/Town",
    "Address County",
    "Latitude",
    "Longitude"
]

df = df[columns]

#df.to_csv("Accommodation_cleaned.csv", index=False)

print("\nFinal dataset shape:", df.shape)
print("Cleaned dataset saved to Accommodation_cleaned.csv")

#------------------------------------------------------------------------------------------
#CHECK FOR UNIQUE TOWNS

print(sorted(df["Address City/Town"].dropna().unique()))

#inspect Dublin entries 
dublin = df[
    df["Address County"].eq("Dublin")
]

print(sorted(dublin["Address City/Town"].dropna().unique()))
