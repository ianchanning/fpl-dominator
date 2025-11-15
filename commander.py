# Save this as commander.py
import sys
import os
import glob

# Import the newly forged functions from our tamed grimoires
from forge_cauldron import forge_cauldron
from enrich_with_insight import enrich_with_insight
from grand_synthesis import perform_grand_synthesis
from chimera_final_form_v5_production import forge_final_form_squad
from chimera_pyomo_v2 import forge_pyomo_squad  # The perfected Pyomo engine


def run_the_gauntlet(gameweek_dir: str):
    """
    The one script to rule them all. Executes the entire FPL
    data pipeline in a single, atomic operation.
    """
    print(
        f"--- COMMANDER ONLINE: INITIATING FULL GAUNTLET FOR {gameweek_dir.upper()} ---"
    )

    # --- Preliminary Checks (Defensive Programming) ---
    if not os.path.isdir(gameweek_dir):
        print(f">>> FATAL ERROR: Directory '{gameweek_dir}' not found.")
        return

    # --- STAGE 0: Cleaning the Cauldron ---
    print("\n--- STAGE 0: Cleaning the Cauldron ---")
    files_to_delete = glob.glob(f"{gameweek_dir}/fpl_master_database_*")
    if files_to_delete:
        print(f"Found and deleting {len(files_to_delete)} old database files...")
        for f in files_to_delete:
            os.remove(f)
            print(f" - Deleted: {f}")
        print("Old databases purged. The cauldron is clean.")
    else:
        print("No old database files found. The cauldron is already clean.")


    # --- The Symphony of Creation ---
    # Each function is a movement in our symphony. If one fails, the ritual halts.

    print("\n--- STAGE 1: Forging the Data Cauldron ---")
    if not forge_cauldron(gameweek_dir):
        print(">>> GAUNTLET HALTED.")
        return

    print("\n--- STAGE 2: Enriching with Prophetic Insight ---")
    if not enrich_with_insight(gameweek_dir):
        print(">>> GAUNTLET HALTED.")
        return

    print("\n--- STAGE 3: Performing the Grand Synthesis ---")
    if not perform_grand_synthesis(gameweek_dir):
        print(">>> GAUNTLET HALTED.")
        return

    print("\n--- STAGE 4: Forging the Final Form (PuLP) ---")
    if not forge_final_form_squad(gameweek_dir):
        print(">>> GAUNTLET HALTED.")
        return

    print("\n--- STAGE 5: Unleashing the Perfected Chimera (Pyomo) ---")
    if not forge_pyomo_squad(gameweek_dir):
        print(">>> GAUNTLET HALTED.")
        return

    print(
        f"\n--- SUCCESS: THE GAUNTLET IS COMPLETE. THE PROPHECY FOR {gameweek_dir.upper()} IS FORGED. ---"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: The Commander requires a single, sacred argument.")
        print(">>> USAGE: python commander.py gw5")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    run_the_gauntlet(gameweek_directory)