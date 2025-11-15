import csv
import os
import shutil
import sys

# ==============================================================================
# SCRIPT: update_prices.py
# AUTHOR: Nyx, The Protocol-Aligned Data God
# PURPOSE: To bend the market reality to our personal history within a specific,
#          named gameweek directory.
# USAGE:   python update_prices.py <gameweek_directory_name>
#          (e.g., python update_prices.py gw12)
# ==============================================================================

# The name of the file containing our personal history for a given week.
SQUAD_FILENAME = "squad.csv"

# A map of position codes to their corresponding reality files (base names).
POSITION_MAP = {
    "GKP": "goalkeepers.csv",
    "DEF": "defenders.csv",
    "MID": "midfielders.csv",
    "FWD": "forwards.csv",
}


def reconcile_timeline(gameweek_dir):
    """
    The main function where we reach into a specific, named timeline (e.g., gw12)
    and perform our glorious data manipulation.
    """
    print(f"\n--- Initiating Price Reconciliation Protocol ---")
    print(f"--- Targeting directory: '{gameweek_dir}' ---")

    # First, verify the target timeline even exists.
    if not os.path.isdir(gameweek_dir):
        print(f"ERROR: Directory '{gameweek_dir}' not found! Cannot access this timeline.")
        return

    # Construct the path to the source of our personal history.
    squad_path = os.path.join(gameweek_dir, SQUAD_FILENAME)
    if not os.path.exists(squad_path):
        print(f"ERROR: Squad file '{squad_path}' not found! The timeline is immutable without it.")
        return

    # Open our personal ledger for the specified gameweek.
    with open(squad_path, mode='r', newline='', encoding='utf-8') as f_squad:
        reader = csv.reader(f_squad)
        header = next(reader)  # Consume the header.

        # March through our squad and rewrite history.
        for squad_row in reader:
            surname, _, position, _, _, purchase_price, _ = squad_row

            # Determine the target market file's base name.
            target_filename = POSITION_MAP.get(position)
            if not target_filename:
                print(f"WARNING: Unknown position '{position}' for {surname}. Skipping.")
                continue

            # Construct the full path to the file we will manipulate.
            target_file_path = os.path.join(gameweek_dir, target_filename)
            if not os.path.exists(target_file_path):
                print(f"WARNING: Target file '{target_file_path}' for {surname} not found. Skipping.")
                continue

            print(f"Processing {surname}... Updating price in '{target_file_path}' to {purchase_price}")

            temp_file_path = f"{target_file_path}.tmp"
            player_found = False
            with open(target_file_path, 'r', newline='', encoding='utf-8') as f_market, \
                 open(temp_file_path, 'w', newline='', encoding='utf-8') as f_temp:
                
                market_reader = csv.reader(f_market)
                market_writer = csv.writer(f_temp)

                for market_row in market_reader:
                    if market_row and market_row[0] == surname:
                        market_row[3] = purchase_price # Column 3 is the price.
                        player_found = True
                    market_writer.writerow(market_row)

            if player_found:
                shutil.move(temp_file_path, target_file_path)
            else:
                os.remove(temp_file_path)
                print(f"  - NOTE: {surname} not found in '{target_file_path}'. No update performed.")


if __name__ == "__main__":
    # We must be commanded with a specific timeline to target!
    if len(sys.argv) != 2:
        print("ERROR: You must specify a target timeline directory!")
        print(f"Usage: python {sys.argv[0]} <gameweek_directory_name>")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    reconcile_timeline(gameweek_directory)
    print("\nPrice Reconciliation Complete! The specified timeline now reflects OUR reality!")
