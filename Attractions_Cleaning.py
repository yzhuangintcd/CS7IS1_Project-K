import pandas as pd 

"""
FILE PURPOSE 

This script explores, validates, and cleans the Attractions dataset
The original dataset has 6,250 attraction records and 9 columns

The script:
1. Loads and explores the original dataset
2. Identifies potential restaurants, cafes, pubs, and bars
3. Assigns one or more venue types using the Tags column
4. Classifies records as Keep, Exclude or Review using name based and tag based rules 
5. Exports the classification results

"""

#------------------------------------------------------------------------------------------
#LOAD AND EXPLORE DATASET

df = pd.read_csv("Attractions.csv")

print("Original dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing values:\n", df.isnull().sum())

#------------------------------------------------------------------------------------------
#FILTER FOR FOOD AND DRINK VENUES

#identify food and drink places using the Tags column 
#some records have multiple tags separated by commans, spaces
food_categories = r"Restaurant|Pubs and Bar|Cafe"

food_venues = df[
    df["Tags"].str.contains(food_categories, case=False, regex=True, na=False)
].copy()

print("\nPotential food and drink venues:", len(food_venues))

#------------------------------------------------------------------------------------------
#CLASSIFY VENUE TYPES

#assign 1 or more venue types based on Tags column 
def classify_venue(tags):
    tags = str(tags).casefold()
    types = []
    
    if "restaurant" in tags:
        types.append("Restaurant")
    
    if "pubs and bar" in tags:
        types.append("Pub/Bar")
        
    if "cafe" in tags:
        types.append("Cafe")
        
    return ", ".join(types)

food_venues["Venue Type"] = (
    food_venues["Tags"].apply(classify_venue)
)

print(
    "\nMissing venue classifications:",
    (food_venues["Venue Type"] == "").sum()
)
#------------------------------------------------------------------------------------------
#CLASSIFY RECORDS FOR INCLUSION/EXCLUSION

#these names suggest a restaurant, cafe, pub, etc
dining_patterns = (
    r"\bRestaurant\b|"
    r"\bCaf[eé]\b|"
    r"\bCoffee\s*(Shop|House)\b|"
    r"\bTea\s*Rooms?\b|"
    r"\bPizzeria\b|"
    r"\bPizza\b|"
    r"\bBistro\b|"
    r"\bBrasserie\b|"
    r"\bGastropub\b|"
    r"\bTaproom\b|"
    r"\bPub\b|"
    r"\bBar\b|"
    r"\bFalafel\b|"
    r"\bDining\s*Room\b|"
    r"\bEatery\b|"
    r"\bTavern\b|"
    r"\bGrill\b|"
    r"\bKitchen\b|"
    r"\bDiner\b|"
    r"\bBakery\b|"
    r"\bBakehouse\b|"
    r"\bIce\s*Cream\b|"
    r"\bFish\s*(and|&)\s*Chips\b|"
    r"\bTakeaway\b"
)

#these names suggest places primarily unrelated to food 
non_dining_patterns = (
    r"\bTours?\b|"
    r"\bCookery\s*School\b|"
    r"\bFarmers?\s*Market\b|"
    r"\bFood\s*(Trail|Tour|Producer|Market)\b|"
    r"\bGolf\s*(Club|Course)\b|"
    r"\bSea\s*Salt\b|"
    #r"\bMuseum\b|"
    r"\bPlanetarium\b|"
    r"\bAquarium\b|"
    r"\bMaze\b|"
    r"\bActivity\s*Cent(re|er)\b|"
    r"\bAdventure\s*(Park|Cent(re|er))\b|"
    # r"\bVisitor\s*Cent(re|er)\b|"
    # r"\bHeritage\s*Cent(re|er)\b|"
    # r"\bDistillery\b|"
    # r"\bBrewery\b|"
    # r"\bCastle\b|"
    # r"\bGardens?\b|"
    # r"\bFarm\b|"
    # r"\bTheatre\b|"
    # r"\bZoo\b|"
    r"\bWater\s*Park\b|"
    r"\bTheatre\b|"
    r"\bEntertainment\s*Cent(re|er)\b|"
    r"\bFolklore\s*Experience\b"
)

#these names indicate potentially unrelated activities 
#trigger review 
review_tags = (
    r"\bTour\b|"
    r"\bActivity Operator\b|"
    r"\bFood Shops\b|"
    #r"\bShopping\b|"
    r"\bGolf Course\b|"
    r"\bMuseums and Attraction\b|"
    r"\bVisitor Farm\b|"
    r"\bHistoric Houses and Castle\b|"
    r"\bGardens\b|"
    r"\bAttraction\b|"
    r"\bLearning\b"
)

#patterns in venue names and tags
has_dining_name = food_venues["Name"].str.contains(
    dining_patterns, 
    case=False, 
    regex=True,
    na=False
)

has_non_dining_name = food_venues["Name"].str.contains(
    non_dining_patterns, 
    case=False, 
    regex=True, 
    na=False
)

has_review_tags = food_venues["Tags"].str.contains(
    review_tags,
    case=False,
    regex=True,
    na=False
)

has_shopping_tags = food_venues["Tags"].str.contains(
    r"\bShopping\b",
    case=False, 
    regex=True,
    na=False
)

#default if theres little evidence
food_venues["Decision"] = "Review"
food_venues["Decision Reason"] = "Ambiguous/mixed-use venue"

#exclude records w clear non-dining name
exclude_mask = (
    has_non_dining_name 
    & ~has_dining_name
)

food_venues.loc[exclude_mask, "Decision"] = "Exclude"
food_venues.loc[
    exclude_mask, "Decision Reason"
] = "Name indicates mainly non-dining"

#keep records w no conflicting tags 
#venye does not need restaurant/cafe in name
keep_mask = (
    ~has_non_dining_name
    & ~has_review_tags
    & ~has_shopping_tags
)

food_venues.loc[keep_mask, "Decision"] = "Keep"
food_venues.loc[
    keep_mask, "Decision Reason"
] = "Food/drink tag w no conflicting indcators"

#keep named dining venues w shopping tags 
shopping_dining_mask = (
    has_dining_name
    & has_shopping_tags
    & ~has_non_dining_name
    & ~has_review_tags
)

food_venues.loc[
    shopping_dining_mask, "Decision"
] = "Keep"

food_venues.loc[
    shopping_dining_mask, "Decision Reason"
] = "Dining venue w shopping tag"

#------------------------------------------------------------------------------------------
#VALIDATE CLASSIFICATION RESULTS

print("\n--- FILTERING VALIDATION ---")

print("\nClassification results:")
print(food_venues["Decision"].value_counts())

print("\nVenue type distribution:")
print(food_venues["Venue Type"].value_counts())

print("\nDecision reasons:")
print(food_venues["Decision Reason"].value_counts())

print("\n Examples automatically kept:")
print(
    food_venues.loc[
        food_venues["Decision"] == "Keep",
        ["Name", "Venue Type", "Decision Reason"]
    ].head(15).to_string(index=False)
)

print("\nExamples automatically excluded:")
print(
    food_venues.loc[
        food_venues["Decision"] == "Exclude",
        ["Name", "Venue Type", "Decision Reason"]
    ].head(15).to_string(index=False)
)

print("\nExamples requiring review:")
print(
    food_venues.loc[
        food_venues["Decision"] == "Review",
        ["Name", "Venue Type", "Tags"]
    ].head(15).to_string(index=False)
)

print("\n Total classified records:", len(food_venues))

assert len(food_venues) == (
    food_venues["Decision"].value_counts().sum()
)

assert food_venues["Decision"].isin(
    ["Keep", "Exclude", "Review"]
).all()
#------------------------------------------------------------------------------------------
#SAVE RESULTS 

food_venues.to_csv(
    "Attractions_classified.csv",
    index=False
)

review_venues = food_venues[
    food_venues["Decision"] == "Review"
].copy()

review_venues[
    ["Name", "Venue Type", "Tags", "Decision", "Decision Reason"]
].to_csv(
    "Attractions_review.csv",
    index=False
)

print("\nClassification saved to respective files")
