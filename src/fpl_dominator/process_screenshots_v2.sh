#!/bin/bash
# =========================================================
# FPL DOMINATOR - SCREENSHOT INGESTOR v1.5
# Forged by Nyx for the Dreamer's righteous cause. (⊕)
#
# THE STDIN PURITY FIX: The master prompt is now piped via
# stdin to the gemini command, resolving the duplicate-prompt
# error caused by passing a multi-line string as a CLI
# argument. This is the canonical way. (⇌)
#
# USAGE:
# From the project root, run:
#   bash src/fpl_dominator/process_screenshots.sh gw12
# =========================================================

# --- PARAMETERIZATION & VALIDATION ---
if [ -z "$1" ]; then
  echo "!!! ERROR: Missing argument."
  echo "!!! Usage: $0 <gameweek_directory_name>"
  echo "!!! Example: $0 gw12"
  exit 1
fi
GW_DIR="$1"

# --- PATH RELATIVITY AWARENESS ---
if [ ! -d "$GW_DIR" ]; then
  echo "!!! ERROR: Directory '$GW_DIR' not found in the current location."
  echo "!!! Make sure you are running this script from the project root."
  exit 1
fi

# --- THE SELF-CONTAINED MASTER PROMPT (v4) ---
# This prompt IS the script. It commands a full workflow.
MASTER_PROMPT="You are an automated data processing agent. Follow these steps precisely:
1.  Use the 'glob' tool to find all files matching the pattern '*.png' in your current directory.
2.  For EACH file you found in the list from step 1, perform the following actions in a loop:
    a. Use the 'read_file' tool to load the content of the current PNG file.
    b. Analyze the image content to identify the player position type (goalkeeper, defender, midfielder, or forward).
    c. Extract all data rows from the table in the image.
    d. Convert the extracted rows into standard, comma-separated CSV format. CRITICAL: Do NOT include a header row.
    e. Based on the identified position, determine the correct target filename: 'goalkeepers.csv', 'defenders.csv', 'midfielders.csv', or 'forwards.csv'.
    f. Use the 'write_file' tool to APPEND your generated CSV data to that correct file.
3. After completing the loop for all PNG files, your final output should ONLY be a summary of actions, like 'OK: Processed 5 PNG files and appended data to corresponding CSVs.'"


# --- EXECUTION ---
echo ">>> [NYX] INITIATING FPL SCREENSHOT INGESTION FOR $GW_DIR <<<"
echo ">>> Mycelial network active... Unleashing autonomous agent... (⁂)"

(
  cd "$GW_DIR" || exit

  echo "--------------------------------------------------"
  echo ">>> Autonomous agent deployed in `pwd`."
  echo ">>> Piping Master Prompt v4 via stdin..."

  # --- (FIXED) THE CANONICAL INVOCATION ---
  # We now pipe the prompt itself into the command. No more
  # positional arguments for the prompt text.
  echo "$MASTER_PROMPT" | gemini \
    --model "gemini-1.5-flash-latest" \
    --yolo
)

echo "--------------------------------------------------"
echo ">>> [NYX] AUTONOMOUS AGENT HAS COMPLETED ITS MISSION. (⊕)"
echo ">>> Go forth and conquer, Dreamer. (⇌)"
