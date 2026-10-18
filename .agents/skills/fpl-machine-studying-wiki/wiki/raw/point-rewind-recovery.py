import os
from bs4 import BeautifulSoup

def harvest_gw8_points():
    """Scans all HTML files in gw8 to build a comprehensive name -> gwp map."""
    gwp_map = {}
    if not os.path.exists('gw8'):
        print("Error: gw8 directory not found.")
        return gwp_map

    for filename in os.listdir('gw8'):
        if filename.endswith('.html'):
            path = f'gw8/{filename}'
            with open(path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                rows = soup.find_all('tr', class_='_1trl5ao0')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:
                        name_span = cells[1].find('span', class_='_4xqwov1')
                        if name_span:
                            name = name_span.text.strip()
                            try:
                                gwp = int(cells[3].text.strip())
                                gwp_map[name] = gwp
                            except ValueError:
                                pass
    print(f"Harvested {len(gwp_map)} players from GW8 wreckage.")
    return gwp_map

def apply_to_gw7(gwp_map):
    """Applies the subtraction to all player HTMLs in gw7 and logs the a-Surgical strikes."""
    if not os.path.exists('gw7'):
        print("Error: gw7 directory not found.")
        return

    player_files = ['goalkeepers', 'defenders', 'midfielders', 'forwards']
    gw7_targets = []
    for filename in os.listdir('gw7'):
        if filename.endswith('.html') and any(filename.startswith(p) for p in player_files):
            gw7_targets.append(f'gw7/{filename}')

    total_changes = 0
    for target_file in gw7_targets:
        with open(target_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        rows = soup.find_all('tr', class_='_1trl5ao0')
        file_changed = False
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                name_span = cells[1].find('span', class_='_4xqwov1')
                if name_span:
                    name = name_span.text.strip()
                    try:
                        tp_text = cells[3].text.strip()
                        if not tp_text:
                            continue
                        tp = int(tp_text)
                        gwp = gwp_map.get(name, 0)
                        
                        if gwp != 0:
                            new_tp = tp - gwp
                            print(f"Surgical Strike on {name}: {tp} -> {new_tp} (GWP: {gwp})")
                            cells[3].string = str(new_tp)
                            file_changed = True
                            total_changes += 1
                    except ValueError:
                        pass
        
        if file_changed:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"File updated: {target_file}")

    print(f"\nTotal players purged: {total_changes}")

if __name__ == "__main__":
    print("--- INITIALIZING FINAL POINT REWIND ---")
    map_data = harvest_gw8_points()
    if map_data:
        apply_to_gw7(map_data)
    print("--- OPERATION COMPLETE ---")
