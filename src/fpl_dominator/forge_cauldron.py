# In forge_cauldron.py

import os
import sys

import pandas as pd

# Status severity ladder used by squad-page reconciliation. The INJURY purge
# below is order-sensitive, so reconciliation must NEVER downgrade a player's
# risk signal: the pool keeps the MAX severity seen across any source.
_STATUS_SEVERITY = {"OK": 0, "DOUBT": 1, "INJURY": 2}


def _max_severity_status(pool_status: str, squad_status: str) -> str:
    """Return the most severe of two status tokens.

    Unknown tokens yield to the known one, so a malformed value can never
    mask a genuine INJURY signal from either source.
    """
    pool_sev = _STATUS_SEVERITY.get(pool_status)
    squad_sev = _STATUS_SEVERITY.get(squad_status)
    if pool_sev is None:
        return squad_status
    if squad_sev is None:
        return pool_status
    return pool_status if pool_sev >= squad_sev else squad_status


def forge_cauldron(gameweek_dir: str):
    """
    The core logic of this script, now encapsulated in a function.
    """
    print("--- [1/4] Forging the Data Cauldron ---")

    # Define paths dynamically
    ENRICHED_DB_PATH = f"{gameweek_dir}/fpl_master_database_enriched.csv"
    player_sources = {
        "GKP": f"{gameweek_dir}/goalkeepers.csv",
        "DEF": f"{gameweek_dir}/defenders.csv",
        "MID": f"{gameweek_dir}/midfielders.csv",
        "FWD": f"{gameweek_dir}/forwards.csv",
    }

    # ... (the rest of the logic to load, concat, and save) ...
    df_list = []
    for pos, path in player_sources.items():
        # Add a check to ensure files exist
        if not os.path.exists(path):
            print(f"!!! CRITICAL ERROR in forge_cauldron: File not found: {path}")
            return False  # Return a failure state
        df_list.append(pd.read_csv(path).assign(Position=pos))

    enriched_df = pd.concat(df_list, ignore_index=True)

    # --- Squad-Page Status Reconciliation (MAX-severity law) ---
    # The market tables and the FPL squad page are independent scrapes that
    # can disagree (gw9 RUD: the squad page flagged João Pedro and Saka as
    # INJURY while the market table still read OK). The squad page is exactly
    # what the owner sees on the FPL dashboard, so merge its Status column
    # into the pool by (Surname, Position), keeping the most severe signal.
    squad_path = f"{gameweek_dir}/squad.csv"
    if os.path.exists(squad_path):
        squad_df = pd.read_csv(squad_path)
        if not {"Surname", "Position", "Status"} <= set(squad_df.columns):
            print(
                "    - WARNING: squad.csv lacks Surname/Position/Status columns; "
                "skipping reconciliation."
            )
        else:
            squad_status = {
                (str(row["Surname"]).strip(), str(row["Position"]).strip()): str(
                    row["Status"]
                ).strip()
                for _, row in squad_df.iterrows()
                if pd.notna(row["Status"])
            }
            pool_keys = list(
                zip(
                    enriched_df["Surname"].astype(str).str.strip(),
                    enriched_df["Position"].astype(str).str.strip(),
                )
            )
            upgraded = 0
            for idx, key in enumerate(pool_keys):
                squad_sev_status = squad_status.get(key)
                if squad_sev_status is None:
                    continue
                pool_status = str(enriched_df.at[idx, "Status"]).strip()
                merged_status = _max_severity_status(pool_status, squad_sev_status)
                if merged_status != pool_status:
                    enriched_df.at[idx, "Status"] = merged_status
                    upgraded += 1
            if upgraded:
                print(
                    f"    - Squad-page reconciliation: {upgraded} player(s) upgraded "
                    f"to a more severe status."
                )

    # Filter out any players with the 'INJURY' status (post-reconciliation)
    initial_player_count = len(enriched_df)
    enriched_df = enriched_df[enriched_df["Status"] != "INJURY"].copy()
    final_player_count = len(enriched_df)
    removed_count = initial_player_count - final_player_count
    print(f"    - Purged {removed_count} injured players from consideration.")

    enriched_df["PPM"] = (enriched_df["TP"] / enriched_df["Price"]).round(2)
    enriched_df.to_csv(ENRICHED_DB_PATH, index=False)
    print("    - SUCCESS: Enriched DB saved.")
    return True  # Return a success state


# This block now only runs if you execute "python forge_cauldron.py gw5" directly.
# It allows the script to still be used as a standalone tool.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python forge_cauldron.py <gameweek_dir>")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    forge_cauldron(gameweek_directory)
