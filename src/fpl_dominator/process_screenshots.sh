#!/bin/bash

# This script automates the processing of FPL screenshots using the Gemini CLI.
# It automatically identifies the content of the screenshot (position or squad)
# and extracts the data into the correct CSV file.

# Usage: ./process_screenshots.sh <gameweek_dir>
# Example: ./process_screenshots.sh gw11

# --- Configuration ---
GAMEWEEK_DIR="$1"
OUTPUT_DIR="$GAMEWEEK_DIR" # CSVs will be saved in the gameweek directory

# --- Main Logic ---

if [ -z "$GAMEWEEK_DIR" ]; then
    echo "Usage: $0 <gameweek_dir>"
    exit 1
fi

if [ ! -d "$GAMEWEEK_DIR" ]; then
    echo "Error: Gameweek directory '${GAMEWEEK_DIR}' not found."
    exit 1
fi

echo "--- Starting screenshot processing for ${GAMEWEEK_DIR} ---"

# Initialize flags to track if headers have been written for position files
declare -A HEADERS_WRITTEN=(
    ["GOALKEEPERS"]=0
    ["DEFENDERS"]=0
    ["MIDFIELDERS"]=0
    ["FORWARDS"]=0
)

# Clear previous output CSVs to ensure a clean run
rm -f "${OUTPUT_DIR}/goalkeepers.csv" \
      "${OUTPUT_DIR}/defenders.csv" \
      "${OUTPUT_DIR}/midfielders.csv" \
      "${OUTPUT_DIR}/forwards.csv" \
      "${OUTPUT_DIR}/squad_fpl_site.csv"

# Find all PNG files in the gameweek directory
find "${GAMEWEEK_DIR}" -maxdepth 1 -type f -name "*.png" | while read -r image_path; do
    echo "Processing image: ${image_path}"
    
    # Create a temporary file for Gemini's raw output
    TEMP_GEMINI_RAW_OUTPUT=$(mktemp)
    
    # Call Gemini CLI to extract file content. This feeds the image to the agent.
    # The agent's response will be captured in the raw output.
    # Redirect stderr to /dev/null to suppress Node.js deprecation warnings.
    gemini file extract "${image_path}" 2>/dev/null > "${TEMP_GEMINI_RAW_OUTPUT}"
    
    if [ $? -ne 0 ]; then
        echo "Error calling Gemini CLI for ${image_path}. Skipping."
        rm "${TEMP_GEMINI_RAW_OUTPUT}"
        continue
    fi

    # Extract the markdown code block from the Gemini CLI's raw output.
    # This block contains the agent's response (TYPE: and CSV).
    AGENT_RESPONSE_CONTENT=$(awk '/```/{p=!p;next}p' "${TEMP_GEMINI_RAW_OUTPUT}")

    if [ -z "$AGENT_RESPONSE_CONTENT" ]; then
        echo "Warning: No agent response (or empty) found in Gemini output for ${image_path}. Skipping."
        rm "${TEMP_GEMINI_RAW_OUTPUT}"
        continue
    fi

    # Extract the TYPE line and the CSV content from the agent's response
    TYPE_LINE=$(echo "${AGENT_RESPONSE_CONTENT}" | head -n 1)
    CSV_CONTENT=$(echo "${AGENT_RESPONSE_CONTENT}" | tail -n +2)
    
    # Extract the type (e.g., GOALKEEPERS, SQUAD)
    TYPE=$(echo "${TYPE_LINE}" | sed -n 's/^TYPE:\(.*\)/\1/p')

    if [ -z "$TYPE" ]; then
        echo "Warning: Could not determine type from agent's response for ${image_path}. Skipping."
        rm "${TEMP_GEMINI_RAW_OUTPUT}"
        continue
    fi

    echo "Identified type: ${TYPE}"

    case "$TYPE" in
        GOALKEEPERS|DEFENDERS|MIDFIELDERS|FORWARDS)
            # Determine the output CSV filename based on type
            OUTPUT_CSV_FILENAME="${TYPE,,}.csv" # Convert to lowercase
            OUTPUT_CSV_PATH="${OUTPUT_DIR}/${OUTPUT_CSV_FILENAME}"

            if [ "${HEADERS_WRITTEN[$TYPE]}" -eq 0 ]; then
                # Write header and content
                echo "${CSV_CONTENT}" > "${OUTPUT_CSV_PATH}"
                HEADERS_WRITTEN[$TYPE]=1
            else
                # Append content, skipping the header from the new CSV_CONTENT
                echo "${CSV_CONTENT}" | tail -n +2 >> "${OUTPUT_CSV_PATH}"
            fi
            echo "Appended data to ${OUTPUT_CSV_PATH}"
            ;;
        SQUAD)
            OUTPUT_CSV_PATH="${OUTPUT_DIR}/squad_fpl_site.csv"
            # For squad, we assume it's a single file and overwrite/create
            echo "${CSV_CONTENT}" > "${OUTPUT_CSV_PATH}"
            echo "Generated ${OUTPUT_CSV_PATH}"
            ;;
        *)
            echo "Warning: Unknown type '${TYPE}' for ${image_path}. Skipping."
            ;;
    esac
    
    rm "${TEMP_GEMINI_RAW_OUTPUT}" # Clean up temporary file

done

echo "--- Screenshot processing complete for ${GAMEWEEK_DIR} ---"
