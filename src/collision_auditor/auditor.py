import os
import re

def main():
    print("=== ADVAD Collision Auditor ===")
    project_path = input("Enter the absolute path to the project (e.g., C:\\Users\\Usuario\\Desktop\\ADVAD1D):\n> ").strip()
    if not os.path.exists(project_path): 
        print("Path does not exist.")
        return
    
    print("\n--- Scanning Physics Nodes in Scenes ---")
    
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.tscn'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for Area2D, CharacterBody2D, StaticBody2D, etc.
                nodes = re.finditer(r'\[node name="([^"]+)" type="(Area2D|CharacterBody2D|StaticBody2D|RigidBody2D)"[^\]]*\](.*?)(?=\n\[node|\Z)', content, re.DOTALL)
                
                for match in nodes:
                    name = match.group(1)
                    ntype = match.group(2)
                    props = match.group(3)
                    
                    layer = re.search(r'\ncollision_layer\s*=\s*([0-9]+)', props)
                    mask = re.search(r'\ncollision_mask\s*=\s*([0-9]+)', props)
                    
                    l_val = layer.group(1) if layer else "1 (Default)"
                    m_val = mask.group(1) if mask else "1 (Default)"
                    
                    print(f"[{file}] Node: '{name}' ({ntype}) -> Layer: {l_val} | Mask: {m_val}")
                    
    print("\nAudit finished. Check if any node has been assigned a wrong collision layer or mask.")

if __name__ == "__main__":
    main()
