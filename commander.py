# Save this as commander.py
import sys
import os

# Import the newly forged functions from our tamed grimoires
from forge_cauldron import forge_cauldron
from enrich_with_insight import enrich_with_insight # Assuming you refactor these
from grand_synthesis import perform_grand_synthesis
from chimera_final_form_v5_production import forge_final_form_squad

def run_the_gauntlet(gameweek_dir: str):
    """
    The one script to rule them all. Executes the entire FPL
    data pipeline in a single, atomic operation.
    """
    print(f"--- COMMANDER ONLINE: INITIATING FULL GAUNTLET FOR {gameweek_dir.upper()} ---")

    # --- Preliminary Checks (Defensive Programming) ---
    if not os.path.isdir(gameweek_dir):
        print(f">>> FATAL ERROR: Directory '{gameweek_dir}' not found.")
        return

    # --- The Symphony of Creation ---
    # Each function is a movement in our symphony. If one fails, the ritual halts.
    
    if not forge_cauldron(gameweek_dir):
        print(">>> GAUNTLET HALTED at Stage 1.")
        return

    if not enrich_with_insight(gameweek_dir): # This function will need to be created
        print(">>> GAUNTLET HALTED at Stage 2.")
        return

    if not perform_grand_synthesis(gameweek_dir): # This function will need to be created
        print(">>> GAUNTLET HALTED at Stage 3.")
        return

    if not forge_final_form_squad(gameweek_dir): # This function will need to be created
        print(">>> GAUNTLET HALTED at Stage 4.")
        return

    print(f"\n--- SUCCESS: THE GAUNTLET IS COMPLETE. THE PROPHECY FOR {gameweek_dir.upper()} IS FORGED. ---")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: The Commander requires a single, sacred argument.")
        print(">>> USAGE: python commander.py gw5")
        sys.exit(1)
    
    gameweek_directory = sys.argv[1]
    run_the_gauntlet(gameweek_directory)
