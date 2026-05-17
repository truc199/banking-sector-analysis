import csv

out = []

with open("d:/uni/gcontest/[G'Contest 2026] Đề Vòng 2_GDP.csv", encoding="utf-8") as f:
    r = csv.reader(f)
    for i, row in enumerate(r):
        if i == 2:
            out.append("GDP 2024: " + row[2])
        if i == 18:
            out.append("GDP 2020: " + row[2])

with open("d:/uni/gcontest/[G'Contest 2026] Đề Vòng 2_Monetary.csv", encoding="utf-8") as f:
    r = list(csv.reader(f))
    out.append("Monetary headers: " + str(r[0]))
    out.append("Monetary sub: " + str(r[1]))

with open("d:/uni/gcontest/[G'Contest 2026] Đề Vòng 2_Tỷ giá.csv", encoding="utf-8") as f:
    r = list(csv.reader(f))
    out.append("FX headers: " + str(r[0]))
    out.append("FX sub: " + str(r[1]))

with open("d:/uni/gcontest/macro_headers.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
