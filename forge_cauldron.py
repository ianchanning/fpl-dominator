import pandas as pd
import os

# --- Configuration ---
# A dictionary mapping the player position to its corresponding CSV file.
# This makes the script easily extendable if we ever get more data types.
DIR = 'gw3'
DATA_SOURCES = {
    'GKP': f'{DIR}/goalkeepers.csv',
    'DEF': f'{DIR}/defenders.csv',
    'MID': f'{DIR}/midfielders.csv',
    'FWD': f'{DIR}/forwards.csv'
}

# The names of the output files we will create.
MASTER_DB_RAW_PATH = f'{DIR}/fpl_master_database_raw.csv'
MASTER_DB_ENRICHED_PATH = f'{DIR}/fpl_master_database_enriched.csv'

# --- Core Functions ---

def forge_master_dataframe(sources: dict) -> pd.DataFrame | None:
    """
    Loads data from multiple CSV files, tags it with a 'Position',
    and concatenates it into a single master DataFrame.
    """
    df_list = []
    print("--- Phase 1: Forging the Data Cauldron ---")
    
    for position, filename in sources.items():
        if not os.path.exists(filename):
            print(f"!!! CRITICAL ERROR: Source file not found: '{filename}'. Aborting.")
            return None
        
        try:
            temp_df = pd.read_csv(filename)
            temp_df['Position'] = position
            df_list.append(temp_df)
            print(f"    [+] Assimilated data from '{filename}' ({len(temp_df)} players)")
        except Exception as e:
            print(f"!!! CRITICAL ERROR: Failed to process '{filename}': {e}")
            return None

    if not df_list:
        print("!!! CRITICAL ERROR: No data was loaded. The cauldron is empty.")
        return None
        
    master_df = pd.concat(df_list, ignore_index=True)
    print(f"--- SUCCESS: Master DataFrame forged. Total players in universe: {len(master_df)} ---")
    return master_df

def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates advanced analytical metrics and adds them as new columns.
    This is the heart of our value engine.
    """
    print("\n--- Phase 2: Enriching the Data with Value Metrics ---")
    
    # Calculate Points Per Million (PPM) - our foundational value metric.
    # We'll round it to 2 decimal places for clarity.
    df['PPM'] = (df['TP'] / df['Price']).round(2)
    print("    [+] Calculated 'PPM' (Points Per Million) for all players.")
    
    print("--- SUCCESS: Data enrichment complete. ---")
    return df

# --- Main Execution Block ---

if __name__ == "__main__":
    # Step 1: Forge the raw, unified database.
    master_df = forge_master_dataframe(DATA_SOURCES)
    
    if master_df is not None:
        # Step 2: Save the raw master database.
        master_df.to_csv(MASTER_DB_RAW_PATH, index=False)
        print(f"\n[*] Raw master database saved to '{MASTER_DB_RAW_PATH}'")

        # Step 3: Enrich the data with our analytical metrics.
        enriched_df = enrich_dataframe(master_df.copy()) # Use a copy to keep raw data clean
        
        # Step 4: Display the top 15 most valuable players in the entire game.
        print("\n--- TOP 15 VALUE PICKS (ALL POSITIONS BY PPM) ---")
        print(enriched_df.sort_values(by='PPM', ascending=False).head(15).to_string())
        
        # Step 5: Save the final, enriched database. This is our primary weapon.
        enriched_df.to_csv(MASTER_DB_ENRICHED_PATH, index=False)
        print(f"\n[*] ENRICHED master database saved to '{MASTER_DB_ENRICHED_PATH}'")
        print("\n*** The Data Cauldron is forged and ready for analysis. ***")
