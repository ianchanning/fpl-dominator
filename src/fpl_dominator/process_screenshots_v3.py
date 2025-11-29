#!/usr/bin/env python3

import glob
import os
import shlex
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        print("!!! ERROR: Missing argument.")
        print(
            "!!! Usage: python3 process_screenshots_v3.py <gameweek_directory_name> [--debug]"
        )
        print("!!! Example: python3 process_screenshots_v3.py gw12")
        sys.exit(1)

    gw_dir = sys.argv[1]
    debug_mode = "--debug" in sys.argv

    if not os.path.isdir(gw_dir):
        print(f"!!! ERROR: Directory '{gw_dir}' not found.")
        print(
            "!!! Make sure you are running this script from the project root and the gameweek directory exists."
        )
        sys.exit(1)

    print(f">>> [NYX] INITIATING FPL SCREENSHOT INGESTION FOR {gw_dir} <<<")
    if debug_mode:
        print(">>> DEBUG MODE ENGAGED. Will process one file and print raw output.")
    print(">>> Mycelial network active... unleashing the flash model... (⁂)")

    processed_count = 0
    skipped_count = 0
    errors_count = 0

    # Find all PNG files in the target directory that haven't been processed
    png_files = [
        f
        for f in glob.glob(os.path.join(gw_dir, "*.png"))
        if not f.endswith(".processed")
    ]

    if not png_files:
        print(f"No unprocessed PNG files found in '{gw_dir}'. Exiting.")
        sys.exit(0)

    for screenshot_path in png_files:
        print("--------------------------------------------------")
        print(f">>> Processing Target: {screenshot_path}")

        # Construct the prompt for the gemini CLI
        master_prompt = f"""From the provided FPL screenshot of a position list, extract player data into CSV format.
The CSV must have these 6 columns: Surname, Team, Position, Price, TP, Status.
The 'Status' column is based on the icon next to the player's name:
- A red icon means 'INJURY'.
- A yellow icon means 'DOUBT'.
- A blue 'i' icon or no icon means 'OK'.
CRITICAL: Your entire output must be ONLY the raw CSV data. Do NOT include a header row or any other explanatory text.
"""

        command = [
            "gemini",
            screenshot_path,
            master_prompt,
            "--model",
            "gemini-2.5-pro",
            "--yolo",
        ]

        if debug_mode:
            # Construct a shell-safe command string for easy copy-pasting
            debug_command_str = " ".join(shlex.quote(arg) for arg in command)
            print("\n>>> DEBUG COMMAND:\n")
            print(debug_command_str)
            print("\n>>> EXECUTING DEBUG COMMAND...\n")

            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, check=True
                )
                print(">>> RAW STDOUT FROM GEMINI CLI:\n")
                print(result.stdout)
                print("\n>>> END OF RAW STDOUT <<<\n")
            except subprocess.CalledProcessError as e:
                print("!!! DEBUG: Gemini CLI failed.")
                print(">>> RAW STDERR:\n")
                print(e.stderr)
                print("\n>>> END OF RAW STDERR <<<\n")

            # In debug mode, only process the first file and then exit.
            print(">>> DEBUG MODE FINISHED. Exiting.")
            sys.exit(0)

        # UNLEASH GEMINI CLI (Normal Mode)
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            model_output = result.stdout.strip()

            # Assuming the model output is CSV data
            # Determine target CSV file based on position (first row's position)
            first_line = model_output.splitlines()[0]
            if first_line:
                try:
                    position = first_line.split(",")[2].strip().lower()
                    target_csv_file = ""
                    if "gkp" in position:
                        target_csv_file = os.path.join(gw_dir, "goalkeepers.csv")
                    elif "def" in position:
                        target_csv_file = os.path.join(gw_dir, "defenders.csv")
                    elif "mid" in position:
                        target_csv_file = os.path.join(gw_dir, "midfielders.csv")
                    elif "fwd" in position:
                        target_csv_file = os.path.join(gw_dir, "forwards.csv")
                    else:
                        raise ValueError(
                            f"Unknown position in model output: {position}"
                        )

                    with open(target_csv_file, "a") as f:
                        f.write(model_output + "\n")
                    print(f">>> Appended data to {target_csv_file}")

                    # Rename the processed file
                    os.rename(screenshot_path, screenshot_path + ".processed")
                    print(
                        f">>> Renamed {screenshot_path} to {screenshot_path}.processed"
                    )
                    processed_count += 1

                except IndexError:
                    print(
                        f"!!! ERROR: Could not parse position from model output for {screenshot_path}. Output: {model_output[:100]}..."
                    )
                    errors_count += 1
                except ValueError as ve:
                    print(
                        f"!!! ERROR: {ve} for {screenshot_path}. Output: {model_output[:100]}..."
                    )
                    errors_count += 1
            else:
                print(f"!!! ERROR: Model returned empty output for {screenshot_path}.")
                errors_count += 1

        except subprocess.CalledProcessError as e:
            print(
                f"!!! ERROR: Gemini CLI failed for {screenshot_path}. Stderr: {e.stderr}"
            )
            errors_count += 1
        except Exception as e:
            print(f"!!! UNEXPECTED ERROR: {e} for {screenshot_path}")
            errors_count += 1

        print(f">>> Target Processed: {screenshot_path}")

    print("--------------------------------------------------")
    print(
        f">>> [NYX] ALL SCREENSHOTS PROCESSED. FPL DOMINATOR DATA FORGE IS COMPLETE. (⊕)"
    )
    print(
        f">>> Summary: Processed {processed_count} files, Skipped {skipped_count} files, Errors {errors_count} files."
    )
    print(">>> Go forth and conquer, Dreamer. (⇌)")


if __name__ == "__main__":
    main()
