#!/bin/bash
# =========================================================
# THE CHRONOCOMPARATOR v1.0
# Forged by Nyx to audit the Dreamer's parallel realities.
#
# Compares the CSV data between two gameweek directories,
# ignoring row order by sorting the content before diffing.
# It preserves headers for readability.
#
# USAGE:
#   ./compare_gws.sh gw12 gw13
# =========================================================

# --- ANSI Color Codes for Glorious Output ---
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

# --- Argument Validation ---
if [ "$#" -ne 2 ]; then
    echo -e "${COLOR_RED}ERROR: Invalid arguments.${COLOR_NC}"
    echo "Usage: $0 <directory1> <directory2>"
    echo "Example: $0 gw12 gw13"
    exit 1
fi

DIR1="$1"
DIR2="$2"

if [ ! -d "$DIR1" ]; then
    echo -e "${COLOR_RED}ERROR: Directory '$DIR1' not found.${COLOR_NC}"
    exit 1
fi

if [ ! -d "$DIR2" ]; then
    echo -e "${COLOR_RED}ERROR: Directory '$DIR2' not found.${COLOR_NC}"
    exit 1
fi

echo -e "${COLOR_YELLOW}>>> [NYX] INITIATING CHRONOCOMPARISON: '$DIR1' vs '$DIR2' <<<${COLOR_NC}"

# --- Find all unique CSV filenames across both directories ---
# This ensures we check every file that exists in at least one of them.
ALL_FILES=$( (ls "$DIR1"/*.csv 2>/dev/null; ls "$DIR2"/*.csv 2>/dev/null) | xargs -n 1 basename | sort -u )

# --- The Main Comparison Loop ---
for filename in $ALL_FILES; do
    echo "--------------------------------------------------"
    echo -e ">>> Auditing Reality for: ${COLOR_YELLOW}$filename${COLOR_NC}"

    FILE1="$DIR1/$filename"
    FILE2="$DIR2/$filename"

    # Check for file existence in both realities
    if [ ! -f "$FILE1" ]; then
        echo -e "${COLOR_RED}MISMATCH: File exists in '$DIR2' but not in '$DIR1'.${COLOR_NC}"
        continue
    fi
    if [ ! -f "$FILE2" ]; then
        echo -e "${COLOR_RED}MISMATCH: File exists in '$DIR1' but not in '$DIR2'.${COLOR_NC}"
        continue
    fi

    # Create temporary files for the sorted content
    SORTED_FILE1=$(mktemp)
    SORTED_FILE2=$(mktemp)

    # --- The Magic Sorting Incantation ---
    # 1. Grab the header line (head -n 1) and put it in the temp file.
    # 2. Grab everything BUT the header (tail -n +2), sort it, and APPEND it.
    head -n 1 "$FILE1" > "$SORTED_FILE1"
    tail -n +2 "$FILE1" | sort >> "$SORTED_FILE1"

    head -n 1 "$FILE2" > "$SORTED_FILE2"
    tail -n +2 "$FILE2" | sort >> "$SORTED_FILE2"

    # --- The Moment of Truth: Diff the sorted realities ---
    if diff -q "$SORTED_FILE1" "$SORTED_FILE2" >/dev/null; then
        echo -e "${COLOR_GREEN}SUCCESS: Content is identical (order-independent).${COLOR_NC}"
    else
        echo -e "${COLOR_RED}MISMATCH DETECTED: Content differs.${COLOR_NC}"
        echo "To see the full diff, run:"
        echo "  diff <(head -n 1 \"$FILE1\" && tail -n +2 \"$FILE1\" | sort) <(head -n 1 \"$FILE2\" && tail -n +2 \"$FILE2\" | sort) | colordiff"
    fi

    # Clean up the ethereal remnants of our spell
    rm "$SORTED_FILE1" "$SORTED_FILE2"
done

echo "--------------------------------------------------"
echo -e "${COLOR_YELLOW}>>> [NYX] CHRONOCOMPARISON COMPLETE. REALITY AUDITED. (⊕)${COLOR_NC}"
