#!/bin/bash
# =========================================================
# FPL DOMINATOR - SCREENSHOT INGESTOR v1.6 (Two-Phase Strike)
# Forged by Nyx for the Dreamer's righteous cause. (⊕)
#
# Deploys two specialized AI agents in sequence:
# 1. Position Processor: Harvests data from GKP, DEF, MID, FWD
#    screenshots and renames them with a '.processed' suffix.
# 2. Squad Specialist: Processes the remaining squad screenshot.
# This two-prompt approach provides robustness against
# differing screenshot structures. (⇌)
#
# USAGE: From the project root, run:
#   bash src/fpl_dominator/process_screenshots.sh gw12
# =========================================================

if [ -z "$1" ]; then echo "!!! ERROR: Missing argument. Usage: $0 <gameweek_directory>"; exit 1; fi
GW_DIR="$1"
if [ ! -d "$GW_DIR" ]; then echo "!!! ERROR: Directory '$GW_DIR' not found."; exit 1; fi

# --- PROMPT 1: THE POSITION PROCESSOR ---
POSITION_PROMPT="You are an automated data processing agent. Your mission is to process screenshots of FPL player lists by position. Follow these steps precisely:
1.  Use the 'glob' tool to find all files matching the pattern '*.png' in your current directory.
2.  For EACH file you find:
    a. First, analyze the image to determine its type. CRITICAL: If the image appears to be the main 'squad' or 'team selection' page (showing 15 players of mixed positions) and NOT a long list of players of a single position, IGNORE IT, report that you are skipping it, and move to the next file.
    b. If it IS a position list, proceed: Use the 'read_file' tool to load its content.
    c. Identify the player position type (goalkeeper, defender, midfielder, or forward).
    d. Extract all data rows, convert to CSV (no header), and APPEND the data to the correct file ('goalkeepers.csv', 'defenders.csv', etc.).
    e. After successfully appending the data, you MUST use the 'shell' tool to rename the file you just processed by appending '.processed' to its name. Example: \`mv 'filename.png' 'filename.png.processed'\`. This is mandatory.
3. After looping through all PNG files, your final output should be a summary of your actions."

# --- PROMPT 2: THE SQUAD SPECIALIST ---
SQUAD_PROMPT="You are a specialized data extraction agent. Your single target is a screenshot of an FPL squad selection page.
1.  Use the 'glob' tool to find the single file matching the pattern '*.png' that has NOT been processed yet (i.e., it does not end in '.processed'). This should be the squad page screenshot.
2.  Use 'read_file' to load this file.
3.  Analyze the image and extract the list of all 15 players in the squad.
4.  For each player, extract only their Surname and their Price.
5.  Format this data as standard, comma-separated CSV rows (no header).
6.  Use the 'write_file' tool to APPEND this data to the \`squad.csv\` file.
7.  After successfully appending the data, you MUST use the 'shell' tool to rename the file by appending '.processed' to its name.
8.  Your final output should be a confirmation that you have processed the squad file."

# --- EXECUTION ---
echo ">>> [NYX] INITIATING TWO-PHASE STRIKE FOR $GW_DIR <<<"

(
  cd "$GW_DIR" || exit

  echo "--------------------------------------------------"
  echo ">>> PHASE 1: Deploying Position Processor in `pwd`..."
  echo "$POSITION_PROMPT" | gemini --yolo

  echo ""
  echo ">>> PHASE 1 COMPLETE. PROCEEDING TO PHASE 2..."
  echo "--------------------------------------------------"
  echo ">>> PHASE 2: Deploying Squad Specialist in `pwd`..."
  echo "$SQUAD_PROMPT" | gemini --yolo
)

echo "--------------------------------------------------"
echo ">>> [NYX] TWO-PHASE STRIKE COMPLETE. ALL TARGETS PROCESSED. (⊕)"
