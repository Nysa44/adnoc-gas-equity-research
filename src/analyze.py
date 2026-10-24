from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(ROOT / "data" / "historical_financials.csv").sort_values("fiscal_year")

# Year-over-year growth and margins derived from the reported absolute values.
for metric in ["revenue_usd_m", "ebitda_usd_m", "net_income_usd_m", "capex_usd_m"]:
    df[metric.replace("_usd_m", "_growth_pct")] = df[metric].pct_change() * 100
df["calculated_ebitda_margin_pct"] = df["ebitda_usd_m"] / df["revenue_usd_m"] * 100
df["calculated_net_income_margin_pct"] = df["net_income_usd_m"] / df["revenue_usd_m"] * 100
df.to_csv(OUT / "historical_ratio_analysis.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(df["fiscal_year"], df["revenue_usd_m"]/1000, marker="o", linewidth=2, label="Revenue")
ax.plot(df["fiscal_year"], df["ebitda_usd_m"]/1000, marker="o", linewidth=2, label="EBITDA")
ax.plot(df["fiscal_year"], df["net_income_usd_m"]/1000, marker="o", linewidth=2, label="Net income")
ax.set_title("ADNOC Gas — three-year financial performance")
ax.set_ylabel("USD billions")
ax.set_xticks(df["fiscal_year"])
ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False, ncols=3)
fig.tight_layout()
fig.savefig(FIG / "financial_performance.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(df["fiscal_year"].astype(str), df["ebitda_margin_pct"])
ax.set_title("Reported EBITDA margin")
ax.set_ylabel("Percent")
ax.grid(axis="y", alpha=.25)
fig.tight_layout()
fig.savefig(FIG / "ebitda_margin.png", dpi=180)
plt.close(fig)

latest, prior = df.iloc[-1], df.iloc[-2]
rev_change = (latest.revenue_usd_m/prior.revenue_usd_m-1)*100
ebitda_change = (latest.ebitda_usd_m/prior.ebitda_usd_m-1)*100
ni_change = (latest.net_income_usd_m/prior.net_income_usd_m-1)*100
capex_change = (latest.capex_usd_m/prior.capex_usd_m-1)*100
report = f"""# ADNOC Gas — Financial highlights

## FY2025 vs FY2024
- Revenue: **US${latest.revenue_usd_m/1000:.3f}bn**, down **{abs(rev_change):.1f}%** year over year.
- EBITDA: **US${latest.ebitda_usd_m/1000:.3f}bn**, down **{abs(ebitda_change):.1f}%** year over year.
- Net income: **US${latest.net_income_usd_m/1000:.3f}bn**, up **{ni_change:.1f}%** year over year.
- Capital expenditure: **US${latest.capex_usd_m/1000:.3f}bn**, up **{capex_change:.1f}%** year over year.
- EBITDA margin: **{latest.ebitda_margin_pct:.1f}%**, compared with **{prior.ebitda_margin_pct:.1f}%** in FY2024.

## Interpretation
FY2025 shows resilience in earnings despite softer international product-price conditions: revenue and EBITDA were broadly lower, while net income reached a new high. Domestic gas EBITDA growth helped offset weakness in export and traded-liquids contributions. The sharp increase in capex is strategically important for the medium-term cash-flow profile and should not be smoothed away without a clear rationale.

## Analyst questions
1. How much of forecast growth is volume, price/mix, or contractual repricing?
2. How should high strategic capex affect near-term FCFF and terminal assumptions?
3. How sensitive is valuation to WACC, terminal growth, and EBITDA margin?
4. What is the appropriate treatment of joint ventures and alternative performance measures in comparisons?

*Historical figures are based on company results releases. FY2023 headline values are rounded; the dataset is intended for portfolio analysis, not as a substitute for audited filings.*
"""
(OUT/"financial_highlights.md").write_text(report, encoding="utf-8")
print(report)
