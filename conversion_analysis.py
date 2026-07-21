"""
conversion_analysis.py
Analyzes conversion funnel drop-off by visitor type (new vs. returning)
and device. Outputs: conversion_by_visitor_type.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('outputs', exist_ok=True)
df = pd.read_csv('data/visitor_conversion_data.csv')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- Chart 1: Funnel by Visitor Type ---
ax1 = axes[0]
stages = ['add_to_cart', 'checkout_started', 'subscribed']
labels = ['Add to Cart', 'Checkout Started', 'Subscribed']
colors = {'new': '#F4A261', 'returning': '#2C5F2E'}

for vtype in ['new', 'returning']:
    sub = df[df['visitor_type'] == vtype]
    rates = [sub[s].mean() for s in stages]
    ax1.plot(labels, rates, marker='o', label=f'{vtype.title()} visitors',
             color=colors[vtype], linewidth=2.5, markersize=8)
    for j, (label, rate) in enumerate(zip(labels, rates)):
        ax1.annotate(f'{rate:.1%}', (label, rate),
                     textcoords='offset points', xytext=(5, 5),
                     fontsize=9, color=colors[vtype])

ax1.set_title('Conversion Funnel: New vs. Returning Visitors\n(Control: Guarantee Below Fold)',
              fontweight='bold', fontsize=11)
ax1.set_ylabel('Conversion Rate')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax1.set_ylim(0, 0.95)
ax1.legend(fontsize=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

gap = (df[df['visitor_type'] == 'returning']['add_to_cart'].mean() -
       df[df['visitor_type'] == 'new']['add_to_cart'].mean())
ax1.text(0, 0.82, f'Add-to-cart gap:\n{gap:.1%} between segments',
         fontsize=8.5, color='#c0392b',
         bbox=dict(boxstyle='round', facecolor='#fdecea', edgecolor='#c0392b', alpha=0.8))

# --- Chart 2: Add-to-Cart by Device + Visitor Type ---
ax2 = axes[1]
pivot = df.groupby(['device', 'visitor_type'])['add_to_cart'].mean().unstack()
x = np.arange(len(pivot.index))
width = 0.35
for i, vtype in enumerate(['new', 'returning']):
    if vtype in pivot.columns:
        bars = ax2.bar(x + i * width, pivot[vtype], width,
                       label=f'{vtype.title()} visitors',
                       color=colors[vtype], alpha=0.85, edgecolor='white')
        for bar, val in zip(bars, pivot[vtype]):
            ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.005,
                     f'{val:.1%}', ha='center', fontsize=8.5, fontweight='bold')

ax2.set_xticks(x + width / 2)
ax2.set_xticklabels([d.title() for d in pivot.index], fontsize=10)
ax2.set_ylabel('Add-to-Cart Rate')
ax2.set_title('Add-to-Cart Rate by Device & Visitor Type', fontweight='bold', fontsize=11)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax2.legend(fontsize=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.suptitle('Seed Health — New Visitor Conversion Gap Analysis', fontsize=13,
             fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/conversion_by_visitor_type.png', dpi=150, bbox_inches='tight')
print("Saved: outputs/conversion_by_visitor_type.png")
plt.close()

print("\n=== Conversion Summary by Visitor Type ===")
print(df.groupby('visitor_type')[['add_to_cart', 'subscribed', 'revenue']].agg(
    {'add_to_cart': 'mean', 'subscribed': 'mean', 'revenue': 'mean'}
).round(3).to_string())
