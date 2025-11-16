# Save this as commander.py
import sys
import os
import glob
import io
from contextlib import redirect_stdout

# Import the newly forged functions from our tamed grimoires
from .forge_cauldron import forge_cauldron
from .enrich_with_insight import enrich_with_insight
from .grand_synthesis import perform_grand_synthesis
from .chimera_final_form_v5_production import forge_final_form_squad
from .chimera_pyomo_v2 import forge_pyomo_squad  # The perfected Pyomo engine


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

    # --- STAGE 4: Forging the Final Form (PuLP) ---
    print("\n--- STAGE 4: Forging the Final Form (PuLP) ---")
    pulp_output_io = io.StringIO()
    with redirect_stdout(pulp_output_io):
        pulp_success = forge_final_form_squad(gameweek_dir)
    pulp_output = pulp_output_io.getvalue()
    print(pulp_output)
    if not pulp_success:
        print(">>> GAUNTLET HALTED.")
        return

    # --- STAGE 5: Unleashing the Perfected Chimera (Pyomo) ---
    print("\n--- STAGE 5: Unleashing the Perfected Chimera (Pyomo) ---")
    pyomo_output_io = io.StringIO()
    with redirect_stdout(pyomo_output_io):
        pyomo_success = forge_pyomo_squad(gameweek_dir)
    pyomo_output = pyomo_output_io.getvalue()
    print(pyomo_output)
    if not pyomo_success:
        print(">>> GAUNTLET HALTED.")
        return

    # --- STAGE 6: Scribing the Prophecy ---
    print("\n--- STAGE 6: Scribing the Prophecy ---")
    md_filename = "squad_prophecy.md"
    md_filepath = os.path.join(gameweek_dir, md_filename)
    
    md_content = f"# FPL Dominator Squad Prophecy for {gameweek_dir.upper()}\n\n"
    md_content += "## PuLP Solver Output (Final Form v5)\n\n"
    md_content += f"```text\n{pulp_output}\n```\n\n"
    md_content += "## Pyomo Solver Output (Apotheosis v2)\n\n"
    md_content += f"```text\n{pyomo_output}\n```\n"

    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"SUCCESS: Prophecy has been recorded to '{md_filepath}'")

    print(
        f"\n--- SUCCESS: THE GAUNTLET IS COMPLETE. THE PROPHECY FOR {gameweek_dir.upper()} IS FORGED. ---"
    )
