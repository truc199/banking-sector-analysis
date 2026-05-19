import os
import glob
import re

def update_fonts_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Pattern 1: replace matplotlib/plt font.sans-serif assignment
    # e.g., plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
    # or matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
    pattern_sans = r"(\bmatplotlib|\bplt)\.rcParams\['font\.sans-serif'\]\s*=\s*\[[^\]]+\]"
    replacement_sans = r"\1.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']"
    
    new_content, count = re.subn(pattern_sans, replacement_sans, content)
    if count > 0:
        content = new_content
        modified = True

    # Pattern 2: replace matplotlib/plt font.family assignment when set to DejaVu Sans
    # e.g., matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
    # we want to set it to 'sans-serif' and add the font.sans-serif configuration
    pattern_family = r"(\bmatplotlib|\bplt)\.rcParams\['font\.family'\]\s*=\s*'DejaVu Sans'"
    replacement_family = r"\1.rcParams['font.family'] = 'sans-serif'\n\1.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']"
    
    new_content, count = re.subn(pattern_family, replacement_family, content)
    if count > 0:
        content = new_content
        modified = True

    # Also check for dictionary configurations in style setup if any
    # e.g., 'font.family': 'sans-serif' or similar
    # We can also add 'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans'] next to it
    if "'font.family': 'sans-serif'" in content and "'font.sans-serif'" not in content:
        content = content.replace(
            "'font.family': 'sans-serif'",
            "'font.family': 'sans-serif',\n        'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']"
        )
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated font settings in: {os.path.basename(filepath)}")
        return True
    return False

def main():
    search_dirs = [
        r'd:\uni\gcontest\slidev',
        r'd:\uni\gcontest'
    ]
    
    updated_count = 0
    for directory in search_dirs:
        py_files = glob.glob(os.path.join(directory, '*.py'))
        for filepath in py_files:
            if os.path.abspath(filepath) == os.path.abspath(__file__):
                continue
            if update_fonts_in_file(filepath):
                updated_count += 1
                
    print(f"Finished updating fonts. Total files updated: {updated_count}")

if __name__ == '__main__':
    main()
