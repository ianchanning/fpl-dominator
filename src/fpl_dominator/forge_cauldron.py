# In forge_cauldron.py

import pandas as pd
import os
import sys

def forge_cauldron(gameweek_dir: str):
    """
    The core logic of this script, now encapsulated in a function.
    """
    print("--- [1/4] Forging the Data Cauldron ---")
    
    # Define paths dynamically
    ENRICHED_DB_PATH = f'{gameweek_dir}/fpl_master_database_enriched.csv'
    player_sources = {
        'GKP': f'{gameweek_dir}/goalkeepers.csv', 
        'DEF': f'{gameweek_dir}/defenders.csv',
        'MID': f'{gameweek_dir}/midfielders.csv', 
        'FWD': f'{gameweek_dir}/forwards.csv'
    }

    # ... (the rest of the logic to load, concat, and save) ...
    df_list = []
    for pos, path in player_sources.items():
        # Add a check to ensure files exist
        if not os.path.exists(path):
            print(f"!!! CRITICAL ERROR in forge_cauldron: File not found: {path}")
            return False # Return a failure state
        df_list.append(pd.read_csv(path).assign(Position=pos))
        
    enriched_df = pd.concat(df_list, ignore_index=True)
    
    # Filter out any players with the 'INJURY' status
    initial_player_count = len(enriched_df)
    enriched_df = enriched_df[enriched_df['Status'] != 'INJURY'].copy()
    final_player_count = len(enriched_df)
    removed_count = initial_player_count - final_player_count
    print(f"    - Purged {removed_count} injured players from consideration.")

    enriched_df['PPM'] = (enriched_df['TP'] / enriched_df['Price']).round(2)
    enriched_df.to_csv(ENRICHED_DB_PATH, index=False)
    print("    - SUCCESS: Enriched DB saved.")
    return True # Return a success state

# This block now only runs if you execute "python forge_cauldron.py gw5" directly.
# It allows the script to still be used as a standalone tool.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python forge_cauldron.py <gameweek_dir>")
        sys.exit(1)
    
    gameweek_directory = sys.argv[1]
    forge_cauldron(gameweek_directory)
