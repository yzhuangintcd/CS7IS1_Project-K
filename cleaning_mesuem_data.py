import pandas as pd 
from pyproj import Transformer

if __name__ == '__main__':
    
    df = pd.read_csv('Dataset/Museums__Collections___Archives_2015.csv', encoding='latin1')
    
    # Drop unnecessary columns
    # Note: The column names have trailing spaces in the raw CSV (e.g., 'Phone ', 'Website ')
    cols_to_drop = ['Add1', 'Add2', 'Add3', 'Postcode', 'Phone ', 'Website ', 'Email', 'Blurb']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    # Handle missing coordinates
    # We must drop rows missing ITM Easting/Northing, otherwise the conversion math will fail
    df = df.dropna(subset=['ITM Easting', 'ITM Northing'])
    
    # 4. Coordinate Conversion (ITM to WGS84 Lat/Long)
    # EPSG:2157 is Irish Transverse Mercator (ITM)
    # EPSG:4326 is standard WGS84 (Latitude/Longitude)
    transformer = Transformer.from_crs("EPSG:2157", "EPSG:4326", always_xy=True)
    
    # always_xy=True means the input is (Easting, Northing) and output is (Longitude, Latitude)
    df['LONGITUDE'], df['LATITUDE'] = transformer.transform(
        df['ITM Easting'].values, 
        df['ITM Northing'].values
    )
    
    # 5. Check for missing values and duplicates
    missing_values = df.isnull().sum()
    duplicates_exact = df.duplicated().sum()
    duplicates_name = df.duplicated(subset=['Name of Museum or HC']).sum()

    print("Missing Values Summary:\n", missing_values[missing_values > 0])
    print(f"\nExact duplicate rows: {duplicates_exact}")
    print(f"Name duplicate rows: {duplicates_name}")

    # 6. Save the cleaned output
    df.to_csv('Dataset/Cleaned_Museums.csv', index=False)
    print("\nSuccess: Cleaned dataset saved to 'Cleaned_Museums.csv'")
