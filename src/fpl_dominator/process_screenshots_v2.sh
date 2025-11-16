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
POSITION_PROMPT="You are an automated data processing agent. Your mission is to process screenshots of FPL player lists by position. Follow these steps precisely and in order:

1.  **Find Targets:** Use the 'glob' tool to find all files matching the pattern '*.png'.

2.  **Loop and Triage:** For EACH file you found:
    a. **Analyze Type:** First, analyze the image to determine its type. If it is the main 'squad' page (15 mixed-position players), you MUST IGNORE IT. Report that you are skipping it and why, then immediately move to the next file. **Do NOT rename files that you skip.**
    b. **Process Position Lists:** If the file IS a position list, proceed with the following data extraction contract.

3.  **Data Extraction Contract (MANDATORY):** For each player row in a position list screenshot, you MUST extract the following 6 columns in this exact order: **Surname, Team, Position, Price, TP, Status**.
    a. **Status Column Logic:** The 'Status' column is determined by the icon next to the player's name. Apply these rules without deviation:
        - If you see a **red icon**, the Status is 'INJURY'.
        - If you see a **yellow icon**, the Status is 'DOUBT'.
        - Otherwise, the Status is 'OK'.
    b. **Format Output:** Convert the extracted rows into standard, comma-separated CSV format. CRITICAL: Do NOT include a header row.

4.  **Write and Rename:**
    a. **Append Data:** Based on the identified 'Position', APPEND your generated CSV data to the correct file ('goalkeepers.csv', 'defenders.csv', etc.).
    b. **Mark as Processed:** AFTER successfully appending the data, you MUST use the 'shell' tool to rename the file you just processed by appending '.processed' to its name. Example: `mv 'filename.png' 'filename.png.processed'`.

5.  **Report:** After the loop, provide a summary of your actions."

# --- PROMPT 2: THE SQUAD SPECIALIST ---
SQUAD_PROMPT="You are a specialized data extraction agent. Your single target is a screenshot of an FPL squad selection page.

1.  **Find Target:** Use the 'glob' tool to find the single file matching '*.png' that does NOT end in '.processed'.

2.  **Data Extraction Contract (MANDATORY):** For each of the 15 players in the squad, you MUST extract the following 6 columns in this exact order: **Surname, Team, Position, Price, TP, Status**.
    a. **Status Column Logic:** The 'Status' column is determined by the icon next to the player's name. Apply these rules without deviation:
        - If you see a **red icon**, the Status is 'INJURY'.
        - If you see a **yellow icon**, the Status is 'DOUBT'.
        - Otherwise, the Status is 'OK'.
    b. **Format Output:** Convert the extracted rows into standard, comma-separated CSV format. CRITICAL: Do NOT include a header row.

3.  **Write and Rename:**
    a. **Append Data:** APPEND your generated CSV data to the `squad.csv` file.
    b. **Mark as Processed:** AFTER successfully appending the data, you MUST use the 'shell' tool to rename the file by appending '.processed' to its name.

4.  **Report:** Confirm that you have processed the squad file."

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
