import os
import re
import csv

def main():
    print("=== ADVAD Phase Balancer ===")
    project_path = input("Enter the absolute path to the project:\n> ").strip()
    
    phase_mgr_path = os.path.join(project_path, "Scripts", "phase_manager.gd")
    
    if not os.path.exists(phase_mgr_path):
        print(f"Script not found at: {phase_mgr_path}")
        return
        
    print("\nExtracting numerical variables for phase balancing...")
    
    with open(phase_mgr_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    csv_path = "exported_phases.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Original Line", "Extracted Value (Suggested)"])
        
        for line in lines:
            line_clean = line.strip()
            # Find lines that assign phase values (e.g., speed, spawn_rate, score_req)
            if ("phase" in line_clean.lower() or "score" in line_clean.lower() or "speed" in line_clean.lower()) and "=" in line_clean:
                # Extract the number
                num_match = re.search(r'=.*?([0-9.]+)', line_clean)
                val = num_match.group(1) if num_match else ""
                writer.writerow([line_clean, val])
                
    print(f"\nA draft has been exported to {csv_path} in this directory.")
    print("This tool is a template. Depending on how your phase dictionary is structured in GDScript, you can adjust the regular expressions in this script to rewrite the .gd file automatically.")

if __name__ == "__main__":
    main()
