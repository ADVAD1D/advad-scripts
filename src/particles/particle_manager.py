import os
import re

def find_files(directory, extensions):
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                matched_files.append(os.path.join(root, file))
    return matched_files

def parse_tscn_particles(filepath):
    # Find GPUParticles2D nodes and their lifetimes in scene files
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to find particle nodes and capture their properties section
    node_pattern = re.compile(r'\[node name="([^"]+)" type="GPUParticles2D"[^\]]*\](.*?)(?=\[node|$)', re.DOTALL)
    
    for match in node_pattern.finditer(content):
        node_name = match.group(1)
        properties = match.group(2)
        
        lifetime_match = re.search(r'\blifetime\s*=\s*([0-9.]+)', properties)
        lifetime = lifetime_match.group(1) if lifetime_match else "1.0 (Default)"
        
        results.append({"type": "tscn", "file": filepath, "name": node_name, "lifetime": lifetime})
        
    return results

def parse_gd_particles(filepath):
    # Find lifetime assignments in scripts
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        match = re.search(r'lifetime\s*=\s*([0-9.]+)', line)
        if match:
            results.append({"type": "gd", "file": filepath, "line_num": i+1, "lifetime": match.group(1)})
            
    return results

def main():
    print("=== ADVAD Particle Lifetime Manager ===")
    project_path = input("Enter the absolute path to your Godot project (e.g., C:\\Users\\Usuario\\Desktop\\ADVAD1D):\n> ").strip()
    
    if not os.path.exists(project_path):
        print("Path does not exist.")
        return
        
    print("\nScanning particles...\n")
    
    tscn_files = find_files(project_path, ('.tscn',))
    gd_files = find_files(project_path, ('.gd',))
    
    all_particles = []
    
    for tscn in tscn_files:
        all_particles.extend(parse_tscn_particles(tscn))
        
    for gd in gd_files:
        all_particles.extend(parse_gd_particles(gd))
        
    if not all_particles:
        print("No particles or lifetime variables found.")
        return
        
    for idx, p in enumerate(all_particles):
        if p['type'] == 'tscn':
            print(f"[{idx}] Scene: {os.path.basename(p['file'])} | Node: {p['name']} | Lifetime: {p['lifetime']}")
        else:
            print(f"[{idx}] Script: {os.path.basename(p['file'])} | Line: {p['line_num']} | Lifetime assigned: {p['lifetime']}")
            
    print("\n---\nCurrently, this script is a parser/viewer. If you want to add batch modification/overwrite functionality, just ask.")

if __name__ == "__main__":
    main()
