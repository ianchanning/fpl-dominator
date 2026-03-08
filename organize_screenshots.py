import os
import shutil
import re

# Mapping of date prefixes to gameweeks based on git history and user context
mapping = {
    "2025-09-19": "gw4",
    "2025-09-24": "gw5",
    "2025-11-08": "gw10",
    "2025-11-15": "gw11",
    "2025-11-28": "gw12",
    "2025-12-02": "gw13",
    "2025-12-06": "gw14",
    "2025-12-20": "gw16",
    "2026-01-30": "gw23",
    "2026-01-31": "gw23",
    "2026-02-03": "gw24",
    "2026-02-19": "gw25",
    "2026-02-21": "gw26",
    "2026-02-25": "gw27",
    "2026-03-08": "gw29",
}

base_dir = "screenshots"
files = os.listdir(base_dir)

for filename in files:
    if not filename.endswith(".png"):
        continue
    
    # Extract date part: Screenshot from YYYY-MM-DD HH-MM-SS.png
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if not match:
        continue
    
    date_prefix = match.group(1)
    if date_prefix in mapping:
        gw_dir = os.path.join(base_dir, mapping[date_prefix])
        if not os.path.exists(gw_dir):
            os.makedirs(gw_dir)
        
        src_path = os.path.join(base_dir, filename)
        dst_path = os.path.join(gw_dir, filename)
        
        print(f"Moving {filename} to {gw_dir}")
        shutil.move(src_path, dst_path)
    else:
        print(f"No mapping found for {filename} (date: {date_prefix})")
