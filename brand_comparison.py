"""
brand_comparison.py
Heuristic scoring of DTC supplement funnel UX across Seed, Ritual, and Thorne.
Outputs: brand_comparison_chart.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('outputs', exist_ok=True)

brands = ['Seed', 'Ritual', 'Thorne']
criteria = [
    'Trust signals\nabove fold',
    'Risk-free\nmessaging visibility',
    'Social proof\nplacement',
    'Mobile CTA\nclarity',
    'Science/clinical\ncredibility',
    'Subscription\ndefault UX',
]

# Heuristic scores 1-5 based on evaluation (5 = best)
scores = {
    'Seed':   [2, 2, 4, 2, 5, 4],
    'Ritual': [4, 4, 4, 4, 3, 4],
    'Thorne': [4, 2, 3, 4, 5, 3],
}

colors = {'Seed': '#2C5F2E', 'Ritual': '#6A4C93', 'Thorne': '#F4A261'}

fig, ax = plt.subplots(figsize=(11, 5))
x = np.arange(len(criteria))
width = 0.25

for i, (brand, vals) in enumerate(scores.items()):
    bars = ax.bar(x + i * width, vals, width,
                  label=brand, color=colors[brand], alpha=0.88, edgecolor='white')
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.05,
                str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_xticks(x + width)
ax.set_xticklabels(criteria, fontsize=9)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1\nPoor', '2', '3\nAvg', '4', '5\nBest'], fontsize=8)
ax.set_ylabel('Heuristic Score (1–5)')
ax.set_title('DTC Supplement Funnel — Cross-Brand Heuristic Evaluation\n'
             'Seed, Ritual, Thorne', fontweight='bold', fontsize=12)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 6)

# Highlight Seed's gap
ax.annotate('Seed opportunity:\ntrust signals + guarantee\nvisibility below fold',
            xy=(0.2, 2), xytext=(0.8, 5.2),
            fontsize=8, color='#c0392b',
            arrowprops=dict(arrowstyle='->', color='#c0392b'),
            bbox=dict(boxstyle='round', facecolor='#fdecea', edgecolor='#c0392b', alpha=0.8))

plt.tight_layout()
plt.savefig('outputs/brand_comparison_chart.png', dpi=150, bbox_inches='tight')
print("Saved: outputs/brand_comparison_chart.png")
plt.close()

# Summary table
df_scores = pd.DataFrame(scores, index=criteria)
df_scores['avg'] = df_scores.mean(axis=1).round(2)
print("\n=== Heuristic Score Summary ===")
print(df_scores.to_string())
print(f"\nOverall averages: {df_scores[brands].mean().round(2).to_dict()}")
