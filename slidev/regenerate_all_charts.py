import os
import sys
import subprocess
import glob

# Ensure stdout and stderr use UTF-8 encoding on Windows to prevent UnicodeEncodeError
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def run_script(filepath):
    print(f"Executing: {os.path.basename(filepath)}...")
    try:
        # Run python script with UTF-8 encoding for capturing stdout/stderr
        result = subprocess.run(['python', filepath], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
        print(f"Success: {os.path.basename(filepath)}")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error executing {os.path.basename(filepath)}:")
        print(e.stderr)

def main():
    slidev_dir = r'd:\uni\gcontest\slidev'
    
    # Get all chart generation scripts
    scripts = []
    
    # Match gen_all_*.py and gen_slide_*.py
    for pattern in ['gen_all_*.py', 'gen_slide_*.py', 'gen_charts_ch1.py']:
        found = glob.glob(os.path.join(slidev_dir, pattern))
        scripts.extend(found)
        
    # Sort scripts to run them in order
    scripts = sorted(list(set(scripts)))
    
    print(f"Found {len(scripts)} scripts to execute.")
    for script in scripts:
        # Avoid running our own update or check scripts
        if "update" in script or "check" in script or "centroid" in script or "compute" in script or "regenerate" in script:
            continue
        run_script(script)
        
    print("All chart generation scripts executed.")

if __name__ == '__main__':
    main()
