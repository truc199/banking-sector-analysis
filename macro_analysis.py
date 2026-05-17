import pandas as pd
import numpy as np

out = []

# --- GDP ---
try:
    df_gdp = pd.read_csv("d:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_GDP.csv", header=1)
    df_gdp = df_gdp.rename(columns={"Unnamed: 1": "Date"})
    df_gdp["Date"] = pd.to_datetime(df_gdp["Date"], errors="coerce")
    df_gdp = df_gdp.dropna(subset=["Date"])
    df_gdp["Year"] = df_gdp["Date"].dt.year
    df_gdp["Growth YTD YOY"] = pd.to_numeric(df_gdp["Growth YTD YOY"], errors="coerce")
    df_gdp_yoy = df_gdp.groupby("Year")["Growth YTD YOY"].mean().loc[2020:2024]
    out.append("=== GDP Growth (YTD YOY) ===")
    out.append(df_gdp_yoy.to_string())
except Exception as e:
    out.append(f"GDP error: {e}")

# --- FDI ---
try:
    df_fdi = pd.read_csv("d:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_FDI.csv")
    fdi_thuc_hien = df_fdi[df_fdi["Vốn FDI (Lũy kế_Triệu USD) "] == "Vốn thực hiện"].iloc[0]
    fdi_yearly = {}
    for year in range(20, 25):
        dec_col = f"Dec {year}"
        if dec_col in fdi_thuc_hien.index:
            fdi_yearly[f"20{year}"] = float(str(fdi_thuc_hien[dec_col]).replace(",",""))
    out.append("\n=== FDI Thuc Hien (Trieu USD) ===")
    out.append(str(fdi_yearly))
except Exception as e:
    out.append(f"FDI error: {e}")

# --- PMI ---
try:
    df_pmi = pd.read_csv("d:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_PMI.csv", header=1)
    df_pmi = df_pmi.rename(columns={"Dates": "Date"})
    df_pmi["Date"] = pd.to_datetime(df_pmi["Date"], errors="coerce")
    df_pmi = df_pmi.dropna(subset=["Date"])
    df_pmi["Year"] = df_pmi["Date"].dt.year
    pmi_vn = df_pmi.groupby("Year")["MPMIVNMA Index"].mean()
    out.append("\n=== PMI Vietnam (Average) ===")
    out.append(pmi_vn.to_string())
except Exception as e:
    out.append(f"PMI error: {e}")

# --- Tỷ giá ---
try:
    df_fx = pd.read_csv("d:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Tỷ giá.csv", header=1)
    df_fx = df_fx.rename(columns={"Dates": "Date"})
    df_fx["Date"] = pd.to_datetime(df_fx["Date"], errors="coerce")
    df_fx = df_fx.dropna(subset=["Date"])
    df_fx["Year"] = df_fx["Date"].dt.year
    df_fx["USDVND VN Curncy"] = pd.to_numeric(df_fx["USDVND VN Curncy"], errors="coerce")
    fx_yearly = df_fx.groupby("Year")["USDVND VN Curncy"].mean()
    out.append("\n=== Ty Gia (USDVND) ===")
    out.append(fx_yearly.to_string())
except Exception as e:
    out.append(f"FX error: {e}")

# --- Monetary ---
try:
    df_money = pd.read_csv("d:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Monetary.csv", header=1)
    df_money = df_money.rename(columns={"Dates": "Date", "Cung tiền M2 VN": "M2", "Tín dụng VN": "Credit"})
    df_money["Date"] = pd.to_datetime(df_money["Date"], errors="coerce")
    df_money = df_money.dropna(subset=["Date"])
    df_money["Year"] = df_money["Date"].dt.year
    df_money["M2"] = pd.to_numeric(df_money["M2"], errors="coerce")
    df_money["Credit"] = pd.to_numeric(df_money["Credit"], errors="coerce")
    money_yearly = df_money.groupby("Year")[["M2", "Credit"]].mean()
    out.append("\n=== Monetary (M2 & Credit) ===")
    out.append(money_yearly.to_string())
except Exception as e:
    out.append(f"Monetary error: {e}")

with open("d:/uni/gcontest/macro_analysis.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
