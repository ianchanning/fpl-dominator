import os
import re
import sys
import glob
from typing import List, Dict, Any, Optional, Union, cast
import pandas as pd
from bs4 import BeautifulSoup, Tag

def parse_players_html(file_path: str, position: str) -> pd.DataFrame:
    """
    Parses an FPL HTML players list file and returns a DataFrame with player data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    players_data: List[Dict[str, Any]] = []
    
    # Each player row has class '_1trl5ao0'
    rows = soup.select('tr._1trl5ao0')

    for row in rows:
        # 1. Player Name
        name_element = row.select_one('span.rfkqam4')
        if not name_element:
            continue
        name = name_element.text.strip()
        
        # 2. Team
        team_element = row.select_one('span.rfkqam3')
        if not team_element:
            continue
        
        team_span = team_element.select_one('span')
        if not team_span:
            continue
        team = team_span.text.strip()
        
        # 3. Price
        # Look for the td that contains the £ symbol
        price_td: Optional[Tag] = None
        for td in row.select('td'):
            if '£' in td.text:
                price_td = td
                break
        
        price = 0.0
        if price_td:
            # Extract number from £7.2m
            price_match = re.search(r'£([\d.]+)', price_td.text)
            if price_match:
                price = float(price_match.group(1))
            
        # 4. Total Points (TP)
        # It's a td with class _1trl5ao6 _1trl5ao1 and only digits
        tp = 0
        all_tds = row.select('td')
        for i, td in enumerate(all_tds):
            if '£' in td.text:
                # The next one is likely TP
                if i + 1 < len(all_tds):
                    tp_text = all_tds[i+1].text.strip()
                    if tp_text.isdigit():
                        tp = int(tp_text)
                break

        # 5. Status
        status = "OK"
        info_button = row.select_one('th button[aria-label]')
        if info_button:
            # aria-label can be str or list[str] or None
            raw_aria = info_button.get('aria-label', '')
            if isinstance(raw_aria, list):
                aria_label = " ".join(raw_aria).lower()
            else:
                aria_label = str(raw_aria).lower()

            if 'chance of playing' in aria_label:
                match = re.search(r'(\d+)%', aria_label)
                if match:
                    chance = int(match.group(1))
                    if chance < 100:
                        status = "DOUBT"
                    if chance == 0:
                        status = "INJURY"
                else:
                    status = "DOUBT"
            elif 'injury' in aria_label or 'suspended' in aria_label:
                status = "INJURY"

        players_data.append({
            'Surname': name,
            'Team': team,
            'Position': position,
            'Price': price,
            'TP': tp,
            'Status': status
        })

    return pd.DataFrame(players_data)

def parse_squad_html(file_path: str) -> pd.DataFrame:
    """
    Parses the FPL Current Squad HTML rip and returns a DataFrame.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    squad_data: List[Dict[str, Any]] = []
    
    # Squad rows have class 'rweppyb'
    rows = soup.select('tr.rweppyb')

    for row in rows:
        # 1. Name, Team, Position
        name_element = row.select_one('span.rfkqam4')
        if not name_element:
            continue
        name = name_element.text.strip()

        team_pos_element = row.select_one('span.rfkqam3')
        if not team_pos_element:
            continue
        
        spans = team_pos_element.select('span')
        team = spans[0].text.strip() if len(spans) > 0 else ""
        pos = spans[1].text.strip() if len(spans) > 1 else ""

        # 2. Prices: CP, SP, PP are in td.rweppyf
        # Headers: Player, CP, SP, PP, F, TP, Fix, Remove
        tds = row.select('td.rweppyf')
        if len(tds) < 3:
            continue
        
        def extract_price(text: str) -> float:
            match = re.search(r'£([\d.]+)', text)
            return float(match.group(1)) if match else 0.0

        cp = extract_price(tds[0].text)
        sp = extract_price(tds[1].text)
        pp = extract_price(tds[2].text)

        # 3. Status
        status = "OK"
        info_button = row.select_one('th button[aria-label]')
        if info_button:
            raw_aria = info_button.get('aria-label', '')
            aria_label = " ".join(raw_aria).lower() if isinstance(raw_aria, list) else str(raw_aria).lower()
            
            if 'chance of playing' in aria_label:
                match = re.search(r'(\d+)%', aria_label)
                if match:
                    chance = int(match.group(1))
                    if chance < 100: status = "DOUBT"
                    if chance == 0: status = "INJURY"
                else:
                    status = "DOUBT"
            elif 'injury' in aria_label or 'suspended' in aria_label:
                status = "INJURY"

        squad_data.append({
            'Surname': name,
            'Team': team,
            'Position': pos,
            'CP': cp,
            'SP': sp,
            'PP': pp,
            'Status': status
        })

    return pd.DataFrame(squad_data)

def process_players_for_gameweek(gameweek_dir: str):
    """
    Processes all player HTML files (including multi-page rips and squad) and creates position CSVs.
    """
    print(f"--- [RITUAL OF THE GRID] Forging {gameweek_dir} Player Data from HTML ---")
    
    # 1. Process standard position rips
    pos_mappings = [
        ('goalkeepers', 'goalkeepers.csv', 'GKP'),
        ('defenders', 'defenders.csv', 'DEF'),
        ('midfielders', 'midfielders.csv', 'MID'),
        ('forwards', 'forwards.csv', 'FWD')
    ]
    
    for pattern, csv_file, pos_code in pos_mappings:
        csv_path = os.path.join(gameweek_dir, csv_file)
        html_files = glob.glob(os.path.join(gameweek_dir, f"{pattern}*.html"))
        
        if not html_files:
            print(f"    - SKIP: No HTML files found for {pattern}.")
            continue
            
        print(f"[+] Processing {len(html_files)} file(s) for {pattern}...")
        all_players_df = []
        for html_path in sorted(html_files):
            df = parse_players_html(html_path, pos_code)
            if not df.empty:
                all_players_df.append(df)
                print(f"      - Scanned {html_path}: {len(df)} players found.")

        if all_players_df:
            final_df = pd.concat(all_players_df, ignore_index=True)
            initial_count = len(final_df)
            final_df = final_df.drop_duplicates(subset=['Surname', 'Team'])
            removed = initial_count - len(final_df)
            final_df.to_csv(csv_path, index=False)
            print(f"    - SUCCESS: {csv_file} forged with {len(final_df)} unique players. (Purged {removed} duplicates)")

    # 2. Process Current Squad rip
    squad_html = os.path.join(gameweek_dir, 'squad.html')
    squad_csv = os.path.join(gameweek_dir, 'squad.csv')
    if os.path.exists(squad_html):
        print(f"[+] Processing {squad_html}...")
        squad_df = parse_squad_html(squad_html)
        if not squad_df.empty:
            squad_df.to_csv(squad_csv, index=False)
            print(f"    - SUCCESS: {squad_csv} forged with {len(squad_df)} squad members.")
        else:
            print(f"    - WARNING: No squad data found in {squad_html}.")
    else:
        print("    - SKIP: squad.html not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python process_players_html.py gw29")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    process_players_for_gameweek(gameweek_directory)
