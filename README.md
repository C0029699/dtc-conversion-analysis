# dtc-conversion-analysis
[README.md](https://github.com/user-attachments/files/30241506/README.md)
# DTC Subscription Conversion Analysis


 Overview

Cross-brand heuristic and behavioral analysis of DTC supplement subscription conversion funnels. Identified Seed Health's risk-free guarantee as an under-surfaced trust signal, and designed a structured A/B experiment to test earlier guarantee placement.


 Problem Statement

First-time supplement buyers unfamiliar with a brand face high perceived risk when committing to a subscription. Seed offers a **30-day risk-free guarantee**, but it appears below the fold on the product page — after the "Start Now" CTA. For new visitors, this means the most powerful trust signal is never seen before the decision point.

Hypothesis: Surfacing the guarantee above the fold (closer to the primary CTA) would increase add-to-cart rate for new visitors without negatively impacting revenue per session or AOV.

 Repository Structure

```
project2_dtc_conversion_analysis/
│
├── data/
│   └── generate_data.py              # Simulated visitor/conversion dataset
│
├── sql/
│   ├── new_vs_returning_baseline.sql # Segment new vs. returning visitor metrics
│   └── experiment_results.sql        # Query A/B test arm performance
│
├── analysis/
│   ├── brand_comparison.py           # Cross-brand funnel heuristic scoring
│   ├── conversion_analysis.py        # New vs. returning visitor drop-off
│   └── experiment_simulation.py      # CTA placement A/B test simulation
│
├── outputs/
│   ├── brand_comparison_chart.png
│   ├── conversion_by_visitor_type.png
│   └── experiment_results.png
│
└── README.md

 Above-fold vs. below-fold guarantee CTA placement for new visitors

| | Control | Variant |
|---|---|---|
| CTA placement | Below fold (current) | Above fold, near "Start Now" |
| Audience | New visitors only (Amplitude segmentation) | New visitors only |
| Primary metric | Add-to-cart rate | Add-to-cart rate |
| Guardrail metrics | Revenue per session, AOV | Revenue per session, AOV |
| Runtime | 2 weeks | 2 weeks |
| Statistical power | 80% at α = 0.05 | — |

---

 How to Run

```bash
pip install pandas matplotlib scipy numpy seaborn
python data/generate_data.py
python analysis/brand_comparison.py
python analysis/conversion_analysis.py
python analysis/experiment_simulation.py
```
