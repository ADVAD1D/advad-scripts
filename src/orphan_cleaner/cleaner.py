import os

def main():
    print("=== ADVAD Orphan Asset Cleaner ===")
    project_path = input("Enter the absolute path to the project:\n> ").strip()
    
    if not os.path.exists(project_path):
        print("Path does not exist.")
        return
        
    assets_path = os.path.join(project_path, "Assets")
    if not os.path.exists(assets_path):
        print(f"Assets folder not found at: {assets_path}")
        return
        
    print("\nScanning files...")
    
    # 1. Collect all multimedia files
    all_assets = []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.wav', '.ogg', '.mp3', '.ttf', '.tres')
    
    for root, _, files in os.walk(assets_path):
        for f in files:
            if f.lower().endswith(valid_extensions):
                # Save just the filename (for quick code search)
                all_assets.append(f)
                
    if not all_assets:
        print("No assets found in the directory.")
        return
        
    # 2. Search for references in code (.gd) and scenes (.tscn, .tres, .json)
    used_assets = set()
    search_extensions = ('.gd', '.tscn', '.tres', '.json')
    
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.lower().endswith(search_extensions):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        content = file_obj.read()
                        
                        # Check if the asset name appears in the content
                        for asset in all_assets:
                            if asset in content:
                                used_assets.add(asset)
                except Exception as e:
                    print(f"Could not read {f}: {e}")
                            
    orphans = set(all_assets) - used_assets
    
    print("\n--- RESULTS ---")
    print(f"Total multimedia assets: {len(all_assets)}")
    print(f"Assets referenced in code/scenes: {len(used_assets)}")
    print(f"ORPHAN assets (potentially unused): {len(orphans)}\n")
    
    if orphans:
        print("Orphan list:")
        for o in sorted(list(orphans)):
            print(f" [!] {o}")
        print("\nWARNING: Review manually before deleting. If a file path is built dynamically with strings (e.g., 'res://' + name + '.png'), this script might flag it as an orphan by mistake.")
    else:
        print("Your project is perfectly clean!")

if __name__ == "__main__":
    main()
