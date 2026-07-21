"""
experiment_simulation.py
Simulates A/B test: above-fold vs. below-fold guarantee CTA placement.
Audience: new visitors only.
Primary KPI: add-to-cart rate.
Guardrail metrics: revenue per session, AOV.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

os.makedirs('outputs', exist_ok=True)
np.random.seed(21)

# --- Parameters ---
N_PER_ARM = 800
CONTROL_ATC = 0.13        # current add-to-cart for new visitors
VARIANT_ATC = 0.17        # hypothesis: +4pp lift from surfacing guarantee above fold
CONTROL_REV_PER_SESSION = 6.50
VARIANT_REV_PER_SESSION = 6.80   # small lift expected
ALPHA = 0.05

# --- Simulate arms ---
control_atc = np.random.binomial(1, CONTROL_ATC, N_PER_ARM)
variant_atc = np.random.binomial(1, VARIANT_ATC, N_PER_ARM)
control_rev = np.random.exponential(CONTROL_REV_PER_SESSION, N_PER_ARM)
variant_rev = np.random.exponential(VARIANT_REV_PER_SESSION, N_PER_ARM)

# --- Two-proportion z-test for ATC ---
p_c = control_atc.mean()
p_v = variant_atc.mean()
p_pool = (control_atc.sum() + variant_atc.sum()) / (N_PER_ARM * 2)
se = np.sqrt(p_pool * (1 - p_pool) * (2 / N_PER_ARM))
z = (p_v - p_c) / se
p_val = 1 - stats.norm.cdf(z)

# --- Revenue t-test (guardrail) ---
t_stat, p_rev = stats.ttest_ind(variant_rev, control_rev)

print("=" * 55)
print("A/B TEST: Above-Fold vs. Below-Fold Guarantee Placement")
print("=" * 55)
print(f"PRIMARY KPI — Add-to-Cart Rate:")
print(f"  Control:   {p_c:.1%}  (n={N_PER_ARM})")
print(f"  Variant:   {p_v:.1%}  (n={N_PER_ARM})")
print(f"  Lift:      {(p_v - p_c) / p_c * 100:+.1f}%")
print(f"  Z-stat:    {z:.2f}   P-value: {p_val:.4f}")
print(f"  Result:    {'✅ SIGNIFICANT' if p_val < ALPHA else '❌ NOT SIGNIFICANT'}")
print()
print(f"GUARDRAIL — Revenue per Session:")
print(f"  Control:   ${control_rev.mean():.2f}")
print(f"  Variant:   ${variant_rev.mean():.2f}")
print(f"  P-value:   {p_rev:.4f}  {'✅ No harm' if p_rev > ALPHA else '⚠️ Check impact'}")
print("=" * 55)

# --- Visualization ---
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

# Chart 1: Add-to-Cart Rate
ax1 = axes[0]
bars = ax1.bar(['Control\n(Below Fold)', 'Variant\n(Above Fold)'],
               [p_c, p_v], color=['#97BC62', '#2C5F2E'], width=0.45, edgecolor='white')
ax1.set_ylim(0, 0.30)
ax1.set_ylabel('Add-to-Cart Rate')
ax1.set_title('Primary KPI\nAdd-to-Cart Rate', fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for bar, val in zip(bars, [p_c, p_v]):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 0.003,
             f'{val:.1%}', ha='center', fontsize=12, fontweight='bold')
sig = f'p={p_val:.3f} {"✓" if p_val < ALPHA else "✗"}'
ax1.text(0.5, 0.93, sig, transform=ax1.transAxes, ha='center', fontsize=9,
         color='#2C5F2E' if p_val < ALPHA else '#c0392b',
         bbox=dict(boxstyle='round', facecolor='#f0f8f0', edgecolor='#2C5F2E', alpha=0.7))

# Chart 2: Revenue per Session (Guardrail)
ax2 = axes[1]
bars2 = ax2.bar(['Control', 'Variant'],
                [control_rev.mean(), variant_rev.mean()],
                color=['#97BC62', '#2C5F2E'], width=0.45, edgecolor='white')
ax2.set_ylabel('Revenue per Session ($)')
ax2.set_title('Guardrail Metric\nRevenue per Session', fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
for bar, val in zip(bars2, [control_rev.mean(), variant_rev.mean()]):
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.05,
             f'${val:.2f}', ha='center', fontsize=11, fontweight='bold')
ax2.text(0.5, 0.93, f'No harm (p={p_rev:.3f})', transform=ax2.transAxes,
         ha='center', fontsize=9, color='#2C5F2E',
         bbox=dict(boxstyle='round', facecolor='#f0f8f0', edgecolor='#2C5F2E', alpha=0.7))

# Chart 3: Revenue Impact Projection
ax3 = axes[2]
monthly_new_visitors = [5000, 10000, 25000, 50000]
rev_lift = [(p_v - p_c) * 0.80 * 49.99 * mv for mv in monthly_new_visitors]
bars3 = ax3.bar([f'{v//1000}K' for v in monthly_new_visitors], rev_lift,
                color='#2C5F2E', edgecolor='white')
ax3.set_xlabel('Monthly New Visitors')
ax3.set_ylabel('Monthly Revenue Lift ($)')
ax3.set_title('Projected Revenue Impact\nAbove-Fold Guarantee', fontweight='bold')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'${y:,.0f}'))
for bar, val in zip(bars3, rev_lift):
    ax3.text(bar.get_x() + bar.get_width() / 2, val + 50,
             f'${val:,.0f}', ha='center', fontsize=8.5, fontweight='bold')

plt.suptitle('Seed Health — A/B Test: Guarantee CTA Placement (New Visitors Only)',
             fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/experiment_results.png', dpi=150, bbox_inches='tight')
print("\nSaved: outputs/experiment_results.png")
plt.close()
