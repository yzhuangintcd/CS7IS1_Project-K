import pandas as pd 
from pyproj import Transformer

if __name__ == '__main__':
    
    df = pd.read_csv('Dataset/Museums__Collections___Archives_2015.csv', encoding='latin1')
    
    # Drop unnecessary columns
    cols_to_drop = ['Add1', 'Add2', 'Add3', 'Postcode', 'Phone ', 'Website ', 'Email', 'Blurb']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    # Exclude counties that are not in the Republic of Ireland (Northern Ireland)
    ni_counties = {'antrim', 'armagh', 'down', 'fermanagh', 'derry', 'londonderry', 'tyrone', 'belfast'}
    county_clean = (
        df['County']
        .astype(str)
        .str.lower()
        .str.replace(r'^(co\.?|county)\s+', '', regex=True)  # strip "Co." / "County" prefix
        .str.strip()
    )
    rows_before = len(df)
    df = df[~county_clean.isin(ni_counties)]
    print(f"Removed {rows_before - len(df)} rows outside the Republic of Ireland")
    
    # Handle missing coordinates
    df = df.dropna(subset=['ITM Easting', 'ITM Northing'])
    
    # Reassign OBJECT_ID sequentially from 1 (after all rows have been removed)
    df = df.reset_index(drop=True)
    df['OBJECT_ID'] = range(1, len(df) + 1)
    
    # Coordinate Conversion (ITM to WGS84 Lat/Long)
    transformer = Transformer.from_crs("EPSG:2157", "EPSG:4326", always_xy=True)
    df['LONGITUDE'], df['LATITUDE'] = transformer.transform(
        df['ITM Easting'].values, 
        df['ITM Northing'].values
    )
    
    # Check for missing values and duplicates
    missing_values = df.isnull().sum()
    duplicates_exact = df.duplicated().sum()
    duplicates_name = df.duplicated(subset=['Name of Museum or HC']).sum()

    print("Missing Values Summary:\n", missing_values[missing_values > 0])
    print(f"\nExact duplicate rows: {duplicates_exact}")
    print(f"Name duplicate rows: {duplicates_name}")

    # Save the cleaned output
    df.to_csv('Dataset/Cleaned_Museums.csv', index=False)
    print("\nSuccess: Cleaned dataset saved to 'Cleaned_Museums.csv'")