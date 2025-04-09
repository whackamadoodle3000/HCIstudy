import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import friedmanchisquare, norm, t # Added t for potential manual CI calculation if needed
import numpy as np
import pandas as pd
import scikit_posthocs as sp

# Data (n=16 participants) - Keep as is
above_truepos = [1, 3, 6, 3, 6, 3, 1, 1, 2, 1, 4, 6, 3, 0, 4, 5]
above_missed = [7, 5, 2, 5, 2, 5, 7, 7, 6, 7, 4, 2, 5, 8, 4, 3]
above_false_pos = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 0]

eye_truepos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0]
eye_missed = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 7, 7, 8]
eye_false_pos = [0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 1, 2, 1]

below_truepos = [0, 0, 3, 4, 2, 4, 2, 0, 1, 4, 1, 1, 3, 0, 2, 2]
below_missed = [8, 8, 5, 4, 6, 4, 6, 8, 7, 4, 7, 7, 5, 8, 6, 6]
below_false_pos = [0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 5, 2, 3, 0]

# Number of non-event opportunities
non_events = [16] * 16
n_participants = len(above_truepos) # Get n

# Function to compute d' (Keep as is)
def compute_dprime(tp, missed, fa, non_events_list):
    d_prime_scores = []
    n_participants = len(tp)
    if len(missed) != n_participants or len(fa) != n_participants or len(non_events_list) != n_participants:
        raise ValueError("Input lists must have the same length (number of participants)")

    for i in range(n_participants):
        hits = tp[i]
        misses = missed[i]
        false_alarms = fa[i]
        total_trials_signal = hits + misses
        total_trials_noise = non_events_list[i]

        correct_rejections = total_trials_noise - false_alarms
        if correct_rejections < 0:
             print(f"Warning: Participant {i+1} has {false_alarms} FA but only {total_trials_noise} non-events. Check data.")
             correct_rejections = 0

        hit_rate = (hits + 0.5) / (total_trials_signal + 1)
        fa_rate = (false_alarms + 0.5) / (total_trials_noise + 1)

        hit_rate = max(min(hit_rate, 1 - 1e-9), 1e-9)
        fa_rate = max(min(fa_rate, 1 - 1e-9), 1e-9)

        d_prime = norm.ppf(hit_rate) - norm.ppf(fa_rate)
        d_prime_scores.append(d_prime)
    return d_prime_scores

# Calculate d' for each experimental condition
dprime_above = compute_dprime(above_truepos, above_missed, above_false_pos, non_events)
dprime_eye = compute_dprime(eye_truepos, eye_missed, eye_false_pos, non_events)
dprime_below = compute_dprime(below_truepos, below_missed, below_false_pos, non_events)

print("Mean d' scores:")
print(f"Above: {np.mean(dprime_above):.3f}")
print(f"Eye: {np.mean(dprime_eye):.3f}")
print(f"Below: {np.mean(dprime_below):.3f}")

# --- Statistical Analysis (Optional but Recommended) ---
data_wide = pd.DataFrame({
    'Above': dprime_above,
    'Below': dprime_below,
    'Eye': dprime_eye,
})

# Friedman test
friedman_stat, friedman_p = friedmanchisquare(data_wide['Above'], data_wide['Below'], data_wide['Eye'])
print(f"\nFriedman Test: statistic={friedman_stat:.3f}, pvalue={friedman_p:.3e}")

# Nemenyi post-hoc test
if friedman_p < 0.05:
    print("\nRunning Nemenyi Post Hoc Test...")
    nemenyi_result = sp.posthoc_nemenyi_friedman(data_wide)
    print(nemenyi_result)
else:
    print("\nFriedman test not significant, skipping post-hoc test.")

# --- Plotting Section ---

# 1. Prepare data in long format for Seaborn plotting
df_plot = pd.DataFrame({
    'Participant': list(range(1, n_participants + 1)) * 3,
    'Position': ['Above'] * n_participants + ['Eye'] * n_participants + ['Below'] * n_participants,
    'Dprime': dprime_above + dprime_eye + dprime_below
})

# 2. Define the desired order for plotting
position_order = ['Above', 'Eye', 'Below']
df_plot['Position'] = pd.Categorical(df_plot['Position'], categories=position_order, ordered=True)

# 3. Create the plot
plt.figure(figsize=(8, 7)) # Adjust figure size if needed

# Create the bar plot for means and 95% CIs
# --- MODIFIED LINE: Use 'ci' instead of 'errorbar' for older Seaborn versions ---
ax = sns.barplot(data=df_plot, x='Position', y='Dprime',
                 order=position_order,
                 ci=95,             # USE THIS for older Seaborn versions
                 palette='viridis', # Example color palette
                 capsize=0.1)       # Add caps to error bars

# Overlay individual data points using stripplot
sns.stripplot(data=df_plot, x='Position', y='Dprime',
              order=position_order,
              color='black',   # Color for the points
              size=6,          # Size of the points
              jitter=True,     # Allow horizontal spread
              alpha=0.6,       # Make points slightly transparent
              ax=ax)           # Plot on the same axes as the barplot

# 4. Customize the plot
ax.set_xlabel("Notification Position", fontsize=12)
ax.set_ylabel("d' (Discriminability)", fontsize=12)
ax.set_title("Mean Discriminability Index (d') by Position\n(Bars: 95% CI, Points: Individual Participants)", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=11)

# Add a horizontal line at d'=0 (chance performance)
ax.axhline(0, color='grey', linestyle='--', linewidth=1, label="Chance (d'=0)")
ax.legend() # Show the label for the horizontal line

# Improve layout
plt.tight_layout()
plt.show()