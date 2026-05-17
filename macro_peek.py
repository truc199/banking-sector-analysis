import pandas as pd

files = [
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_GDP.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_FDI.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Monetary.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Tỷ giá.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Tổng mức bán lẻ.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_PMI.csv'
]

out = []
for f in files:
    try:
        df = pd.read_csv(f, encoding='utf-8')
        out.append(f'=== {f.split("_")[-1]} ===')
        out.append('Columns: ' + str(df.columns.tolist()))
        out.append(str(df.head(3)))
        out.append('')
    except Exception as e:
        out.append(f'Error {f}: {e}')

with open('d:/uni/gcontest/macro_peek.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
