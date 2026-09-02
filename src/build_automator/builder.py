import os
import subprocess
import zipfile
from datetime import datetime

def main():
    print("=== ADVAD Build Automator (Web) ===")
    project_path = input("Path to the Godot project (e.g., C:\\Users\\Usuario\\Desktop\\ADVAD1D):\n> ").strip()
    
    # On Windows, Godot is usually in a specific folder or added to PATH.
    godot_exe = input("Path to the Godot 4 executable (e.g., C:\\Godot\\Godot_v4.exe):\n> ").strip()
    
    if not os.path.exists(project_path):
        print("Project path does not exist.")
        return
        
    if not os.path.exists(godot_exe):
        print("Godot executable path does not exist.")
        return
        
    build_dir = os.path.join(project_path, "Builds")
    os.makedirs(build_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    export_folder_name = f"ADVAD_Web_{timestamp}"
    export_path = os.path.join(build_dir, export_folder_name)
    os.makedirs(export_path, exist_ok=True)
    
    index_path = os.path.join(export_path, "index.html")
    
    print("\n[1/3] Launching Godot Headless export...")
    # Ensure you have a preset named "Web" in your project.godot
    cmd = [godot_exe, "--headless", "--path", project_path, "--export-release", "Web", index_path]
    
    try:
        subprocess.run(cmd, check=True)
        print("[2/3] Export completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n[Error] Export failed. Return code: {e.returncode}")
        print("Make sure you have an export preset named exactly 'Web' in Godot > Project > Export.")
        return
    except Exception as e:
        print(f"\n[Error] {e}")
        return
        
    print("[3/3] Packaging to ZIP for itch.io...")
    zip_path = os.path.join(build_dir, f"{export_folder_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(export_path):
            for file in files:
                full_path = os.path.join(root, file)
                # Relative path inside the ZIP
                rel_path = os.path.relpath(full_path, export_path)
                zipf.write(full_path, rel_path)
                
    print(f"\nBuild successfully packaged!\nFinal file: {zip_path}")
    print("\n(This script can be extended to connect to itch.io's Butler API for automatic uploads).")

if __name__ == "__main__":
    main()
