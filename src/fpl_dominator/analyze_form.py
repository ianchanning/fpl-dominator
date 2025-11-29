import pandas as pd

def analyze_player_form(gw_past, gw_current):
    """
    Analyzes and compares player data between two gameweeks to identify
    players with the most significant performance changes.

    Args:
        gw_past (int): The previous gameweek number (e.g., 6).
        gw_current (int): The current gameweek number (e.g., 12).
    """
    try:
        # Define file paths
        past_db_path = f"gw{gw_past}/fpl_master_database_prophetic.csv"
        current_db_path = f"gw{gw_current}/fpl_master_database_prophetic.csv"

        # Load dataframes
        df_past = pd.read_csv(past_db_path)
        df_current = pd.read_csv(current_db_path)

    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure you are in the correct project root directory.")
        return

    # Merge the dataframes on player identifiers
    # Using an inner merge to only include players present in both gameweeks
    df_merged = pd.merge(
        df_past,
        df_current,
        on=["Surname", "Team", "Position"],
        suffixes=(f"_gw{gw_past}", f"_gw{gw_current}")
    )

    # Calculate the change in Total Points (TP) and Price
    df_merged['TP_delta'] = df_merged[f'TP_gw{gw_current}'] - df_merged[f'TP_gw{gw_past}']
    df_merged['Price_delta'] = df_merged[f'Price_gw{gw_current}'] - df_merged[f'Price_gw{gw_past}']

    # Sort by the change in points to find top performers
    df_form = df_merged.sort_values(by='TP_delta', ascending=False)

    # --- Display the results ---
    print("--- FPL DOMINATOR: FORM ANALYSIS ---")
    print(f"Comparing GW{gw_past} with GW{gw_current} to find top performers.")
    print("-" * 40)

    # Select and rename columns for a clean output
    output_df = df_form[[
        'Surname',
        'Team',
        'Position',
        'TP_delta',
        f'TP_gw{gw_past}',
        f'TP_gw{gw_current}',
        'Price_delta',
        f'Price_gw{gw_past}',
        f'Price_gw{gw_current}',
    ]].copy()
    
    output_df.rename(columns={
        'TP_delta': 'Points_Gained',
        f'TP_gw{gw_past}': f'Points_GW{gw_past}',
        f'TP_gw{gw_current}': f'Points_GW{gw_current}',
        'Price_delta': 'Price_Change',
        f'Price_gw{gw_past}': f'Price_GW{gw_past}',
        f'Price_gw{gw_current}': f'Price_GW{gw_current}',
    }, inplace=True)
    
    # Round the price change for cleaner display
    output_df['Price_Change'] = output_df['Price_Change'].round(2)

    print(f"Top 15 Players by Points Gained (GW{gw_past}-GW{gw_current}):")
    print(output_df.head(15).to_string(index=False))


if __name__ == "__main__":
    # We are comparing gw6 and gw12 as per the new strategic phase
    analyze_player_form(gw_past=6, gw_current=12)
