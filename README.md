# ADNOC Gas — Equity Research & Company Valuation

A reproducible equity-research project covering three years of headline financial performance, ratio analysis, a five-year FCFF discounted cash flow (DCF), and WACC / terminal-growth sensitivity analysis.

## Highlights
- Three-year reported financial dataset (FY2023–FY2025).
- Python-generated historical charts and financial ratios.
- Five-year forecast with explicit revenue, EBITDA, D&A, EBIT, tax, NOPAT, capex, working capital and FCFF.
- DCF enterprise-value estimate and sensitivity grid.
- Written research framework, catalysts, risks and valuation limitations.

## Quick start
```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py
python src/dcf_model.py
```

## Repository map
```text
data/
  historical_financials.csv
  dcf_assumptions.csv
src/
  analyze.py
  dcf_model.py
  common.py
outputs/
  historical_ratio_analysis.csv
  financial_highlights.md
  dcf_forecast.csv
  dcf_sensitivity.csv
  dcf_summary.md
  figures/
reports/
  investment_thesis.md
```

## Key FY2025 observations
ADNOC Gas reported revenue of US$23.473bn, EBITDA of US$8.636bn, net income of US$5.166bn, and capital expenditure of US$3.639bn. Revenue and EBITDA were slightly below FY2024, net income rose to a record, and capex increased sharply as major growth projects progressed.

## Methodology
FCFF = NOPAT + D&A − capital expenditure − change in net working capital. Enterprise value equals the present value of forecast FCFF plus the present value of terminal value, calculated using the Gordon growth formula.

## Data sources
- [ADNOC Gas FY2025 results release](https://www.adnocgas.ae/en/news-and-media/press-releases/2025/q4-2025)
- [ADNOC Gas FY2025 financial highlights](https://adnocgas.ae/-/media/gas/investor-relation/2025/mda-report-q4-2025--english.ashx)
- [ADNOC Gas FY2024 results release](https://adnocgas.ae/en/news-and-media/press-releases/2025/q4-2024)
- [ADNOC Gas FY2023 results release](https://www.adnocgas.ae/en/news-and-media/press-releases/2024/q4-2023-financial-results)

## Data and model caveats
FY2023 headline figures are rounded from the results release. Forecast assumptions are analyst-created scenarios, not management guidance. The model reports enterprise value only; a reliable equity bridge requires reconciliation of net debt, joint ventures, lease liabilities and diluted shares. Figures from company alternative performance measures must be used consistently with the forecast perimeter.

## Disclaimer
Educational portfolio project only. Not investment advice, a price target, or a recommendation to buy, sell or hold securities.
