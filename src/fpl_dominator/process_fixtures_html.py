import os
import re
import sys
import pandas as pd
from bs4 import BeautifulSoup

def rgb_to_fdr(rgb_string: str) -> int:
    """
    Converts an RGB color string to its corresponding FDR value based on the reverse-engineered formula.
    FDR = round(1429.6 - 1.8 * C)
    """
    try:
        # Extract the first number from rgb(147, 147, 147)
        color_value = int(re.search(r'\d+', rgb_string).group())
        fdr = round(1429.6 - 1.8 * color_value)
        return int(fdr)
    except (AttributeError, ValueError):
        # Return a default/error value if parsing fails
        return 0

def parse_fixture_html(file_path: str, fdr_col_name: str) -> pd.DataFrame:
    """
    Parses an HTML fixture ticker file and returns a DataFrame with fixture data.
    """
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

    all_fixtures = []
    
    # Extract gameweek headers, skipping any that might be blank
    gw_headers = [h.text.strip() for h in soup.select('.gw-header-btn') if h.text.strip()]

    # Find all team rows
    team_rows = soup.select('.team-row')

    for row in team_rows:
        team_name_element = row.select_one('.team-name')
        if not team_name_element: continue
        team_name = team_name_element.text.strip()
        
        fixtures = row.select('.fixture-cell')
        
        for i, fixture in enumerate(fixtures):
            if i >= len(gw_headers): continue

            opponent = fixture.text.strip()
            location = 'H' if 'home' in fixture.get('class', []) else 'A'
            
            # Extract FDR from style attribute
            style = fixture.get('style', '')
            rgb_match = re.search(r'background-color: rgb\((.*?)\);', style)
            if rgb_match:
                fdr_val = rgb_to_fdr(rgb_match.group(1))
            else:
                fdr_val = 0

            all_fixtures.append({
                'Team': team_name,
                'Gameweek': gw_headers[i],
                'Opponent': opponent,
                'Location': location,
                fdr_col_name: fdr_val,
            })

    return pd.DataFrame(all_fixtures)

def create_fixture_csv_from_html(gameweek_dir: str):
    """
    Parses the three HTML fixture files for a given gameweek and creates a combined fixtures.csv.
    """
    print(f"--- Forging {gameweek_dir} Fixtures from HTML sources ---")
    
    # Define paths
    overall_path = f'{gameweek_dir}/fixtures_5w.html'
    attack_path = f'{gameweek_dir}/fixtures_attack_5w.html'
    defence_path = f'{gameweek_dir}/fixtures_defence_5w.html'
    output_path = f'{gameweek_dir}/fixtures.csv'

    # Check if source files exist
    if not all(os.path.exists(p) for p in [overall_path, attack_path, defence_path]):
        print(f"!!! CRITICAL FAILURE: One or more source HTML files not found in '{gameweek_dir}/'. Aborting.")
        return

    # Parse each HTML file
    print("[+] Parsing Overall FDR...")
    df_overall = parse_fixture_html(overall_path, 'FDR')
    
    print("[+] Parsing Attack FDR...")
    df_attack = parse_fixture_html(attack_path, 'FDR_A')
    
    print("[+] Parsing Defence FDR...")
    df_defence = parse_fixture_html(defence_path, 'FDR_D')
    
    # Merge the dataframes
    print("[+] Merging the three FDR realities...")
    key_cols = ['Team', 'Gameweek', 'Opponent', 'Location']
    
    # Check for empty dataframes before merging
    if df_overall.empty or df_attack.empty or df_defence.empty:
        print("!!! CRITICAL FAILURE: One or more of the parsed dataframes is empty. Cannot merge. Aborting.")
        return
        
    df_merged = pd.merge(
        df_overall,
        df_attack[key_cols + ['FDR_A']],
        on=key_cols
    )
    
    df_final = pd.merge(
        df_merged,
        df_defence[key_cols + ['FDR_D']],
        on=key_cols
    )
    
    # Ensure correct column order
    df_final = df_final[['Team', 'Gameweek', 'Opponent', 'Location', 'FDR', 'FDR_A', 'FDR_D']]
    
    # Save to CSV
    try:
        df_final.to_csv(output_path, index=False)
        print(f"--- SUCCESS: {gameweek_dir} fixtures forged at '{output_path}' ---")
        print("\n--- Verification: First 5 rows of the new fixtures file ---")
        print(df_final.head(5).to_string())
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not save the new fixtures CSV. Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python process_fixtures_html.py gw13")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    create_fixture_csv_from_html(gameweek_directory)
