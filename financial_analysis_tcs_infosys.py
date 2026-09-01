import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


# Dates in the financial statement files
year_dates = [
    datetime.datetime(2019, 3, 1),
    datetime.datetime(2020, 3, 1),
    datetime.datetime(2021, 3, 1),
    datetime.datetime(2022, 3, 1),
    datetime.datetime(2023, 3, 1),
]


def get_values(df, metric):
    row = df[df["Metric"] == metric]
    return row[year_dates].values[0].tolist()


# Read the financial statements
tcs_pl = pd.read_excel("TCS_PL_clean.xlsx")
tcs_bs = pd.read_excel("TCS_BS_clean.xlsx")
tcs_cf = pd.read_excel("TCS_CF_clean.xlsx")

infy_pl = pd.read_excel("Infosys_PL_clean.xlsx")
infy_bs = pd.read_excel("Infosys_BS_clean.xlsx")
infy_cf = pd.read_excel("Infosys_CF_clean.xlsx")


# Get the figures needed for the analysis
tcs_revenue = get_values(tcs_pl, "Sales")
tcs_op = get_values(tcs_pl, "Operating Profit")
tcs_profit = get_values(tcs_pl, "Net Profit")
tcs_equity = get_values(tcs_bs, "Shareholders Equity")
tcs_cfo = get_values(tcs_cf, "Cash from Operating Activity")

infy_revenue = get_values(infy_pl, "Sales")
infy_op = get_values(infy_pl, "Operating Profit")
infy_profit = get_values(infy_pl, "Net Profit")
infy_equity = get_values(infy_bs, "Shareholders Equity")
infy_cfo = get_values(infy_cf, "Cash from Operating Activity")


# Combine both companies into one DataFrame
rows = []

for i, year in enumerate(year_dates):
    rows.append({
        "Company": "TCS",
        "Year": year,
        "Revenue": tcs_revenue[i],
        "Operating_Profit": tcs_op[i],
        "Net_Profit": tcs_profit[i],
        "Equity": tcs_equity[i],
        "CFO": tcs_cfo[i],
    })

    rows.append({
        "Company": "Infosys",
        "Year": year,
        "Revenue": infy_revenue[i],
        "Operating_Profit": infy_op[i],
        "Net_Profit": infy_profit[i],
        "Equity": infy_equity[i],
        "CFO": infy_cfo[i],
    })

df = pd.DataFrame(rows)


# Calculate the main ratios
df["Operating_Margin"] = df["Operating_Profit"] / df["Revenue"]
df["Net_Margin"] = df["Net_Profit"] / df["Revenue"]
df["ROE"] = df["Net_Profit"] / df["Equity"]
df["Revenue_Growth_YoY"] = df.groupby("Company")["Revenue"].pct_change()


# Check the main numbers
preview = df[["Company", "Year", "Revenue", "Net_Profit", "ROE"]].copy()
preview["Year"] = preview["Year"].dt.strftime("%Y-%m-%d")
preview["ROE"] = preview["ROE"].map("{:.2%}".format)

print("-" * 62)
print(f"{'Company':<12} {'Year':<14} {'Revenue':>12} {'Net Profit':>12} {'ROE':>8}")
print("-" * 62)

for _, row in preview.iterrows():
    print(
        f"{row['Company']:<12} {row['Year']:<14} "
        f"{row['Revenue']:>12,.0f} {row['Net_Profit']:>12,.0f} "
        f"{row['ROE']:>8}"
    )

print("-" * 62)


# Revenue
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="Year", y="Revenue", hue="Company", marker="o")
plt.title("Revenue Trend: TCS vs Infosys (FY2019–FY2023)")
plt.xlabel("Year")
plt.ylabel("Revenue (Rs. Crore)")
plt.tight_layout()
plt.savefig("chart1_revenue.png", dpi=150)
plt.show()


# Net profit margin
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="Year", y="Net_Margin", hue="Company", marker="o")
plt.title("Net Profit Margin: TCS vs Infosys (FY2019–FY2023)")
plt.xlabel("Year")
plt.ylabel("Net Margin")
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y:.0%}")
)
plt.tight_layout()
plt.savefig("chart2_net_margin.png", dpi=150)
plt.show()


# Operating margin
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="Year", y="Operating_Margin", hue="Company", marker="o")
plt.title("Operating Margin: TCS vs Infosys (FY2019–FY2023)")
plt.xlabel("Year")
plt.ylabel("Operating Margin")
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y:.0%}")
)
plt.tight_layout()
plt.savefig("chart3_operating_margin.png", dpi=150)
plt.show()


# Return on equity
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="Year", y="ROE", hue="Company", marker="o")
plt.title("Return on Equity: TCS vs Infosys (FY2019–FY2023)")
plt.xlabel("Year")
plt.ylabel("ROE")
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y:.0%}")
)
plt.tight_layout()
plt.savefig("chart4_roe.png", dpi=150)
plt.show()


# Operating cash flow
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="Year", y="CFO", hue="Company", marker="o")
plt.title("Operating Cash Flow: TCS vs Infosys (FY2019–FY2023)")
plt.xlabel("Year")
plt.ylabel("Cash from Operations (Rs. Crore)")
plt.tight_layout()
plt.savefig("chart5_cfo.png", dpi=150)
plt.show()


# Year-on-year revenue growth
print("\nYear-on-Year Revenue Growth:")

growth = df[["Company", "Year", "Revenue_Growth_YoY"]].dropna().copy()
growth["Year"] = growth["Year"].dt.strftime("%Y-%m-%d")
growth["Revenue_Growth_YoY"] = growth["Revenue_Growth_YoY"].map("{:.2%}".format)

print("-" * 42)
print(f"{'Company':<12} {'Year':<14} {'Growth':>10}")
print("-" * 42)

for _, row in growth.iterrows():
    print(
        f"{row['Company']:<12} {row['Year']:<14} "
        f"{row['Revenue_Growth_YoY']:>10}"
    )

print("-" * 42)
