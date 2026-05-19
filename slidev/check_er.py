import pandas as pd, sys, glob, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
bs = pd.read_csv(glob.glob(r'd:\uni\gcontest\*Balance*')[0])

bs_2024 = bs[bs['Năm']==2024].copy()
bs_2024['er'] = bs_2024['A64'] / bs_2024['A1'] * 100
bs_2024 = bs_2024.sort_values('er', ascending=False)

n = len(bs_2024)
print(f"Tổng {n} NH\n")

# Method 1: Max - Min
print(f"1. Max - Min: {bs_2024['er'].max():.2f} - {bs_2024['er'].min():.2f} = {bs_2024['er'].max()-bs_2024['er'].min():.2f}pp")

# Method 2: Top 5 avg - Bottom 5 avg
top5 = bs_2024.head(5)['er'].mean()
bot5 = bs_2024.tail(5)['er'].mean()
print(f"2. Top5 avg - Bottom5 avg: {top5:.2f} - {bot5:.2f} = {top5-bot5:.2f}pp")

# Method 3: Top quartile - Bottom quartile
q1_n = n // 4  # ~6-7
top_q = bs_2024.head(q1_n)['er'].mean()
bot_q = bs_2024.tail(q1_n)['er'].mean()
print(f"3. Top Q ({q1_n}) avg - Bottom Q ({q1_n}) avg: {top_q:.2f} - {bot_q:.2f} = {top_q-bot_q:.2f}pp")

# Method 4: Top 3 avg - Bottom 3 avg
top3 = bs_2024.head(3)['er'].mean()
bot3 = bs_2024.tail(3)['er'].mean()
print(f"4. Top3 avg - Bottom3 avg: {top3:.2f} - {bot3:.2f} = {top3-bot3:.2f}pp")

# Method 5: Percentile P90 - P10
p90 = bs_2024['er'].quantile(0.9)
p10 = bs_2024['er'].quantile(0.1)
print(f"5. P90 - P10: {p90:.2f} - {p10:.2f} = {p90-p10:.2f}pp")

# Method 6: Top tercile avg - Bottom tercile avg
t_n = n // 3  # 9
top_t = bs_2024.head(t_n)['er'].mean()
bot_t = bs_2024.tail(t_n)['er'].mean()
print(f"6. Top tercile ({t_n}) avg - Bottom tercile ({t_n}) avg: {top_t:.2f} - {bot_t:.2f} = {top_t-bot_t:.2f}pp")

# Also check across years
print("\n--- Spread across years ---")
for yr in [2020, 2021, 2022, 2023, 2024]:
    sub = bs[bs['Năm']==yr].copy()
    sub['er'] = sub['A64'] / sub['A1'] * 100
    sub = sub.sort_values('er', ascending=False)
    t5 = sub.head(5)['er'].mean()
    b5 = sub.tail(5)['er'].mean()
    mx = sub['er'].max()
    mn = sub['er'].min()
    print(f"  {yr}: Max-Min={mx-mn:.2f}pp, Top5-Bot5={t5-b5:.2f}pp, Top3-Bot3={sub.head(3)['er'].mean()-sub.tail(3)['er'].mean():.2f}pp")
