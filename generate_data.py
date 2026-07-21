"""
generate_data.py
Simulates visitor-level conversion data for Seed Health product page.
New vs. returning visitors, with and without above-fold guarantee.
"""
import pandas as pd
import numpy as np
import os

np.random.seed(7)
N = 5000

visitor_type = np.random.choice(['new', 'returning'], size=N, p=[0.60, 0.40])
device = np.random.choice(['mobile', 'desktop', 'tablet'], size=N, p=[0.58, 0.36, 0.06])
traffic_source = np.random.choice(
    ['paid_social', 'organic_search', 'direct', 'email', 'influencer'],
    size=N, p=[0.30, 0.25, 0.20, 0.15, 0.10]
)

# Baseline conversion rates (control: guarantee below fold)
add_to_cart = []
checkout_started = []
subscribed = []
revenue = []

for vtype, dev in zip(visitor_type, device):
    base_atc = 0.22 if vtype == 'returning' else 0.13  # new visitors convert lower
    mobile_penalty = 0.03 if dev == 'mobile' else 0
    atc = np.random.binomial(1, base_atc - mobile_penalty)
    chk = np.random.binomial(1, 0.72) if atc else 0
    sub = np.random.binomial(1, 0.80) if chk else 0
    rev = round(49.99 + np.random.normal(0, 2), 2) if sub else 0.0
    add_to_cart.append(atc)
    checkout_started.append(chk)
    subscribed.append(sub)
    revenue.append(rev)

df = pd.DataFrame({
    'visitor_id': [f'V{str(i).zfill(6)}' for i in range(N)],
    'visitor_type': visitor_type,
    'device': device,
    'traffic_source': traffic_source,
    'add_to_cart': add_to_cart,
    'checkout_started': checkout_started,
    'subscribed': subscribed,
    'revenue': revenue
})

os.makedirs('data', exist_ok=True)
df.to_csv('data/visitor_conversion_data.csv', index=False)
print(f"Generated {N} visitor records.")
print("\nConversion rates by visitor type:")
print(df.groupby('visitor_type')[['add_to_cart', 'checkout_started', 'subscribed']].mean().round(3))
