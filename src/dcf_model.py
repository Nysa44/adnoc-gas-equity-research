from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT/"data", ROOT/"outputs"
FIG = OUT/"figures"
FIG.mkdir(parents=True, exist_ok=True)

hist = pd.read_csv(DATA/"historical_financials.csv").sort_values("fiscal_year")
a = pd.read_csv(DATA/"dcf_assumptions.csv").set_index("assumption")["value"].astype(float).to_dict()
latest = hist.iloc[-1]
wacc, g = a["wacc"], a["terminal_growth"]
if wacc <= g:
    raise ValueError("WACC must be greater than terminal growth.")
if not 0 <= a["tax_rate"] <= 1:
    raise ValueError("Tax rate must be between 0 and 1.")

rows, prev_rev, prev_nwc = [], float(latest.revenue_usd_m), 0.0
for i in range(1, 6):
    growth = a[f"revenue_growth_y{i}"]
    rev = prev_rev * (1 + growth)
    ebitda = rev * a["ebitda_margin"]
    da = rev * a["da_pct_revenue"]
    ebit = ebitda - da
    nopat = ebit * (1-a["tax_rate"])
    capex = rev * a["capex_pct_revenue"]
    nwc_balance = max(0, (rev-prev_rev) * a["nwc_pct_incremental_revenue"])
    change_nwc = nwc_balance - prev_nwc
    fcff = nopat + da - capex - change_nwc
    discount_factor = 1 / ((1+wacc)**i)
    rows.append({
        "fiscal_year": int(latest.fiscal_year)+i, "revenue_growth_pct": growth*100,
        "revenue_usd_m": rev, "ebitda_usd_m": ebitda, "da_usd_m": da,
        "ebit_usd_m": ebit, "tax_on_ebit_usd_m": ebit*a["tax_rate"],
        "nopat_usd_m": nopat, "capex_usd_m": capex, "change_nwc_usd_m": change_nwc,
        "fcff_usd_m": fcff, "discount_factor": discount_factor, "pv_fcff_usd_m": fcff*discount_factor
    })
    prev_rev, prev_nwc = rev, nwc_balance

forecast = pd.DataFrame(rows)
forecast.to_csv(OUT/"dcf_forecast.csv", index=False)
terminal_fcff = forecast.iloc[-1].fcff_usd_m*(1+g)
terminal_value = terminal_fcff/(wacc-g)
pv_terminal = terminal_value*forecast.iloc[-1].discount_factor
pv_explicit = forecast.pv_fcff_usd_m.sum()
ev = pv_explicit + pv_terminal
tv_share = pv_terminal/ev if ev else np.nan

# Scenario grid: vary WACC and terminal growth. This is enterprise value, not share price.
sens = []
for discount_rate in np.arange(0.07, 0.111, 0.01):
    row = {"wacc_pct": round(discount_rate*100, 1)}
    for tg in [0.01, 0.015, 0.02, 0.025, 0.03]:
        if discount_rate <= tg:
            row[f"terminal_growth_{tg*100:.1f}pct"] = np.nan
            continue
        pv_flows = sum(float(fcff)/((1+discount_rate)**period)
                       for period, fcff in enumerate(forecast.fcff_usd_m, start=1))
        tv = float(forecast.iloc[-1].fcff_usd_m)*(1+tg)/(discount_rate-tg)
        pv_tv = tv/((1+discount_rate)**5)
        row[f"terminal_growth_{tg*100:.1f}pct"] = pv_flows+pv_tv
    sens.append(row)
sens_df = pd.DataFrame(sens)
sens_df.to_csv(OUT/"dcf_sensitivity.csv", index=False)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(forecast.fiscal_year, forecast.revenue_usd_m/1000, marker="o", label="Revenue")
ax.plot(forecast.fiscal_year, forecast.ebitda_usd_m/1000, marker="o", label="EBITDA")
ax.plot(forecast.fiscal_year, forecast.fcff_usd_m/1000, marker="o", label="FCFF")
ax.set_title("Illustrative DCF forecast")
ax.set_ylabel("USD billions")
ax.set_xticks(forecast.fiscal_year)
ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG/"dcf_forecast.png", dpi=180)
plt.close(fig)

summary = f"""# DCF valuation summary — illustrative enterprise value

| Output | Value |
|---|---:|
| Present value of explicit FCFF | US${pv_explicit:,.0f} million |
| Present value of terminal value | US${pv_terminal:,.0f} million |
| **Enterprise value** | **US${ev:,.0f} million** |
| Terminal value as % of enterprise value | {tv_share:.1%} |
| WACC | {wacc:.1%} |
| Terminal growth | {g:.1%} |

## Interpretation
This DCF estimates enterprise value from a five-year forecast of free cash flow to the firm. Terminal value represents {tv_share:.1%} of total enterprise value in the base case, so the output is meaningfully sensitive to long-term assumptions.

## Important model boundaries
- This is a **scenario model**, not a price target or investment recommendation.
- No equity value or per-share value is presented because net debt, lease treatment, joint-venture treatment, and a current diluted share count need to be reconciled from filings before a credible equity bridge is possible.
- The FY2025 EBITDA margin is held constant in the base case; capex, D&A, tax, working capital, WACC and growth are assumptions.
- Company-reported figures include proportionate consolidation of joint ventures in the published alternative performance measures. Ensure the DCF cash flows and valuation perimeter are consistent before using this model for a formal report.
"""
(OUT/"dcf_summary.md").write_text(summary, encoding="utf-8")
print(summary)
