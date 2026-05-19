with open("slides.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("search_results.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if "giả thuyết" in line.lower() or "gt" in line.lower():
            out.write(f"{idx+1}: {line.strip()}\n")
print("Done searching slides.md!")
