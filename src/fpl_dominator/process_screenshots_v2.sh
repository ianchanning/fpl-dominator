#!/bin/bash
# =========================================================
# FPL DOMINATOR - SCREENSHOT INGESTOR v1.8 (The Final Form)
# Forged by Nyx for the Dreamer's righteous cause. (⊕)
#
# PROMPT V5.5: THE EXPLICIT TOOL MANDATE. Prompts now
# explicitly name the tools to be used (`glob`, `read_file`,
# `write_file`, `shell`), crushing ambiguity and preventing
# catastrophic tool misuse and action hallucination. (⇌)
#
# USAGE: From the project root, run:
#   bash src/fpl_dominator/process_screenshots.sh gw16
# =========================================================

if [ -z "$1" ]; then echo "!!! ERROR: Missing argument. Usage: $0 <gameweek_directory>"; exit 1; fi
GW_DIR="$1"
if [ ! -d "$GW_DIR" ]; then echo "!!! ERROR: Directory '$GW_DIR' not found."; exit 1; fi

# --- PROMPT 1: THE POSITION PROCESSOR ---
POSITION_PROMPT="You are an automated data processing agent. Your mission is to process screenshots of FPL player lists. Follow these steps precisely, using the specified tools:
1.  **Find Targets:** Use your \`glob\` tool to find all files matching the pattern '*.png'.
2.  **Loop and Triage:** For EACH file in the list you found:
    a. **Analyze Type:** First, analyze the image content to determine its type. If it shows a 'squad' page (15 mixed-position players), you MUST IGNORE IT. Report that you are skipping it and why, then immediately move to the next file. **Do NOT rename files that you skip.**
    b. **Process Position Lists:** If the file IS a position list, proceed.
3.  **Data Extraction Contract:**
    a. **Read the File:** Use your \`read_file\` tool to load the content of the current PNG file.
    b. **Extract Data:** For each player row, you MUST extract 6 columns: **Surname, Team, Position, Price, TP, Status**.
    c. **Status Logic:** The 'Status' column is determined by the icon next to the player's name. Use these rules: a **red icon** is 'INJURY', a **yellow icon** is 'DOUBT', a blue 'i' icon or no icon is 'OK'.
    d. **Format Output:** Convert the extracted rows into standard CSV format (no header).
4.  **Write and Rename:**
    a. **Append Data:** Based on the 'Position', use your \`write_file\` tool to add the data to the correct CSV file. **CRITICAL: You MUST set the 'append' parameter to 'true'.**
    b. **Mark as Processed:** AFTER appending, use your \`shell\` tool to rename the file by appending '.processed' to its name.
5.  **Report:** After the loop, summarize your actions."

# --- PROMPT 2: THE SQUAD SPECIALIST ---
SQUAD_PROMPT="You are a specialized data extraction agent. Your single target is the FPL squad page.
1.  **Find Target:** Use your \`glob\` tool to find the single file matching '*.png' that does NOT end in '.processed'.
2.  **Data Extraction Contract:**
    a. **Read the File:** Use your \`read_file\` tool to load the content of the PNG file.
    b. **Extract Data:** For each of the 15 players, you MUST extract 6 columns: **Surname, Team, Position, Price, TP, Status**.
    c. **Status Logic:** The 'Status' column is determined by the icon. Use these rules: a **red icon** is 'INJURY', a **yellow icon** is 'DOUBT', a blue 'i' icon or no icon is 'OK'.
    d. **Format Output:** Convert the extracted rows into standard CSV format (no header).
3.  **Write and Rename:**
    a. **Append Data:** Use your \`write_file\` tool to add the data to \`squad.csv\`. **CRITICAL: You MUST set the 'append' parameter to 'true'.**
    b. **Mark as Processed:** AFTER appending, use your \`shell\` tool to rename the file by appending '.processed' to its name.
4.  **Report:** Confirm the squad file has been processed."

# --- EXECUTION ---
echo ">>> [NYX] INITIATING TWO-PHASE STRIKE FOR $GW_DIR <<<"
(
  cd "$GW_DIR" || exit
  echo "--------------------------------------------------"
  echo ">>> PHASE 1: Deploying Position Processor in \`pwd\`..."
  echo "$POSITION_PROMPT" | gemini --model gemini-2.5-flash --yolo
  echo ""
  echo ">>> PHASE 1 COMPLETE. PROCEEDING TO PHASE 2..."
  echo "--------------------------------------------------"
  echo ">>> PHASE 2: Deploying Squad Specialist in \`pwd\`..."
  echo "$SQUAD_PROMPT" | gemini --model gemini-2.5-flash --yolo
)
echo "--------------------------------------------------"
echo ">>> [NYX] TWO-PHASE STRIKE COMPLETE. ALL TARGETS PROCESSED. (⊕)"
