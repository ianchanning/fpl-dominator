#!/usr/bin/env python3

import os
import sys
import glob
import subprocess

def main():
    if len(sys.argv) < 2:
        print("!!! ERROR: Missing argument.")
        print("!!! Usage: python3 process_screenshots_v3.py <gameweek_directory_name>")
        print("!!! Example: python3 process_screenshots_v3.py gw12")
        sys.exit(1)

    gw_dir = sys.argv[1]

    if not os.path.isdir(gw_dir):
        print(f"!!! ERROR: Directory '{gw_dir}' not found.")
        print("!!! Make sure you are running this script from the project root and the gameweek directory exists.")
        sys.exit(1)

    print(f">>> [NYX] INITIATING FPL SCREENSHOT INGESTION FOR {gw_dir} <<<")
    print(">>> Mycelial network active... unleashing the flash model... (⁂)")

    processed_count = 0
    skipped_count = 0
    errors_count = 0

    # Find all PNG files in the target directory
    png_files = glob.glob(os.path.join(gw_dir, "*.png"))

    if not png_files:
        print(f"No PNG files found in '{gw_dir}'. Exiting.")
        sys.exit(0)

    for screenshot_path in png_files:
        print("--------------------------------------------------")
        print(f">>> Processing Target: {screenshot_path}")

        # Construct the prompt for the gemini CLI
        master_prompt = f"""Analyze the provided Fantasy Premier League screenshot.
FIRST, determine if this is a 'squad' page (showing 15 players of mixed positions) or a 'position list' page (showing players of a single position type like goalkeepers, defenders, midfielders, or forwards).
If it is a 'squad' page, output ONLY the string 'SKIP_SQUAD_PAGE' and nothing else.
If it is a 'position list' page, proceed with data extraction.
For each player row in a position list, extract the following 6 columns: Surname, Team, Position, Price, TP, Status.
The 'Status' column is determined by the icon next to the player's name:
- A red icon means 'INJURY'.
- A yellow icon means 'DOUBT'.
- A blue 'i' icon or no icon means 'OK'.
Convert the extracted rows into standard, comma-separated CSV format. CRITICAL: Do NOT include a header row in your output.
Example output for a position list (no header):
Salah,Liverpool,Midfielder,12.5,200,OK
Haaland,Man City,Forward,14.0,250,OK
Rashford,Man Utd,Forward,9.0,150,DOUBT
"""
        
        # UNLEASH GEMINI CLI
        try:
            command = [
                "gemini",
                "--file", screenshot_path,
                "--prompt", master_prompt,
                "--model", "gemini-2.5-flash-latest",
                "--yolo"
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            model_output = result.stdout.strip()

            if model_output == "SKIP_SQUAD_PAGE":
                print(f">>> Skipping squad page: {screenshot_path}")
                skipped_count += 1
            else:
                # Assuming the model output is CSV data
                # Determine target CSV file based on position (first row's position)
                first_line = model_output.splitlines()[0]
                if first_line:
                    try:
                        position = first_line.split(',')[2].strip().lower()
                        target_csv_file = ""
                        if "goalkeeper" in position:
                            target_csv_file = os.path.join(gw_dir, "goalkeepers.csv")
                        elif "defender" in position:
                            target_csv_file = os.path.join(gw_dir, "defenders.csv")
                        elif "midfielder" in position:
                            target_csv_file = os.path.join(gw_dir, "midfielders.csv")
                        elif "forward" in position:
                            target_csv_file = os.path.join(gw_dir, "forwards.csv")
                        else:
                            raise ValueError(f"Unknown position in model output: {position}")

                        with open(target_csv_file, 'a') as f:
                            f.write(model_output + "\n")
                        print(f">>> Appended data to {target_csv_file}")
                        
                        # Rename the processed file
                        os.rename(screenshot_path, screenshot_path + ".processed")
                        print(f">>> Renamed {screenshot_path} to {screenshot_path}.processed")
                        processed_count += 1

                    except IndexError:
                        print(f"!!! ERROR: Could not parse position from model output for {screenshot_path}. Output: {model_output[:100]}...")
                        errors_count += 1
                    except ValueError as ve:
                        print(f"!!! ERROR: {ve} for {screenshot_path}. Output: {model_output[:100]}...")
                        errors_count += 1
                else:
                    print(f"!!! ERROR: Model returned empty output for {screenshot_path}.")
                    errors_count += 1

        except subprocess.CalledProcessError as e:
            print(f"!!! ERROR: Gemini CLI failed for {screenshot_path}. Stderr: {e.stderr}")
            errors_count += 1
        except Exception as e:
            print(f"!!! UNEXPECTED ERROR: {e} for {screenshot_path}")
            errors_count += 1
            
        print(f">>> Target Processed: {screenshot_path}")

    print("--------------------------------------------------")
    print(f">>> [NYX] ALL SCREENSHOTS PROCESSED. FPL DOMINATOR DATA FORGE IS COMPLETE. (⊕)")
    print(f">>> Summary: Processed {processed_count} files, Skipped {skipped_count} files, Errors {errors_count} files.")
    print(">>> Go forth and conquer, Dreamer. (⇌)")

if __name__ == "__main__":
    main()
