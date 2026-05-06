import pandas as pd
import numpy as np

n_samples = 5000

# Random seed for reproducibility
np.random.seed(42)

# Generate percentages that sum to 100
# Method: draw two random numbers, compute third so sum=100
ni = np.random.uniform(20, 80, size=n_samples)
co = np.random.uniform(10, 50, size=n_samples)
mn = 100.0 - (ni + co)
# For any mn < 5 or negative, regenerate
mask = mn < 5
while mask.any():
    new_co = np.random.uniform(10, 50, size=mask.sum())
    ni[mask] = np.random.uniform(20, 80, size=mask.sum())
    co[mask] = new_co
    mn[mask] = 100.0 - (ni[mask] + co[mask])
    mask = mn < 5

temp = np.random.choice([25, 40, 55, 70], size=n_samples)  # operating temperature
c_rate = np.random.choice([0.5, 1, 2, 5], size=n_samples)    # C-rate

ni_to_co = ni / (co + 1e-3)
ni_to_mn = ni / (mn + 1e-3)

# Define a synthetic accuracy formula
# e.g., accuracy increases with ni up to a point, decreases if co too low or mn too low, plus penalty for high temp & high c_rate
predicted_accuracy = 60 \
    + 0.4 * ni \
    - 0.3 * co \
    + 0.5 * mn \
    - 0.2 * temp \
    - 5 * (c_rate - 1) \
    + np.random.normal(scale=3, size=n_samples)

# Clip to [0, 100]
predicted_accuracy = np.clip(predicted_accuracy, 0, 100)

# Baseline for Ni=Co=Mn≈33.33 at default conditions temp=25, c_rate=1
baseline_accuracy = 60 + 0.4*33.33 - 0.3*33.33 + 0.5*33.33 - 0.2*25 - 5*(1-1)
baseline_accuracy = float(np.round(baseline_accuracy, 2))

improvement_pct = predicted_accuracy - baseline_accuracy

df = pd.DataFrame({
    "ni_pct": np.round(ni,2),
    "co_pct": np.round(co,2),
    "mn_pct": np.round(mn,2),
    "ni_to_co_ratio": np.round(ni_to_co,2),
    "ni_to_mn_ratio": np.round(ni_to_mn,2),
    "dopant_sum": np.round(ni+co+mn,2),
    "temp_C": temp,
    "c_rate": c_rate,
    "predicted_accuracy": np.round(predicted_accuracy,2),
    "baseline_accuracy": baseline_accuracy,
    "improvement_pct": np.round(improvement_pct,2),
})

df.to_csv("synthetic_ncm_dopant_dataset.csv", index=False)

print("Dataset generated: synthetic_ncm_dopant_dataset.csv — shape:", df.shape)
