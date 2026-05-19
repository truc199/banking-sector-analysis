import pandas as pd
import glob

note_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]
note = pd.read_csv(note_file)

# Let's filter for 2020 and 2021
n20 = note[note['Năm'] == 2020][['Công ty', 'C64', 'C66']]
n21 = note[note['Năm'] == 2021][['Công ty', 'C64', 'C66']]

df = pd.merge(n20, n21, on='Công ty', suffixes=('_20', '_21'))
df['C64_20'] = df['C64_20'].fillna(0)
df['C64_21'] = df['C64_21'].fillna(0)

# Risky banks with non-zero VAMC bonds
banks_with_vamc_20 = df[df['C64_20'] > 0]
banks_with_vamc_21 = df[df['C64_21'] > 0]

print(f"Number of banks with VAMC in 2020: {len(banks_with_vamc_20)}")
print(f"Number of banks with VAMC in 2021: {len(banks_with_vamc_21)}")

print("\nDetail of VAMC bonds in 2021:")
print(banks_with_vamc_21[['Công ty', 'C64_21', 'C66_21']].sort_values(by='C64_21', ascending=False))
