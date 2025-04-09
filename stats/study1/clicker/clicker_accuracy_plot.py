import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import friedmanchisquare
import numpy as np
import pandas as pd
import scikit_posthocs as sp
import math # Import math for isnan check

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
n_participants = len(above_truepos)

# --- NEW: Function to compute Accuracy ---
def compute_accuracy(tp, missed, fa, non_events_list):
    """
    Calculates accuracy = (Hits + Correct Rejections) / Total Trials
    """
    accuracy_scores = []
    n_participants = len(tp)
    if len(missed) != n_participants or len(fa) != n_participants or len(non_events_list) != n_participants:
        raise ValueError("Input lists must have the same length (number of participants)")

    for i in range(n_participants):
        hits = tp[i]
        misses = missed[i]
        false_alarms = fa[i]
        total_noise_trials = non_events_list[i]

        # Calculate Correct Rejections
        correct_rejections = total_noise_trials - false_alarms
        if correct_rejections < 0:
             print(f"Warning: Participant {i+1} has {false_alarms} FA but only {total_noise_trials} non-events. Check data.")
             correct_rejections = 0 # Avoid negative CRs

        # Calculate Total Trials
        total_signal_trials = hits + misses
        total_trials = total_signal_trials + total_noise_trials

        # Calculate Accuracy
        if total_trials > 0:
            accuracy = (hits + correct_rejections) / total_trials
        else:
            # Handle case where there are no trials (shouldn't happen here)
            accuracy = float('nan') # Assign NaN if no trials

        accuracy_scores.append(accuracy)

    return accuracy_scores

# Calculate Accuracy for each experimental condition
accuracy_above = compute_accuracy(above_truepos, above_missed, above_false_pos, non_events)
accuracy_eye = compute_accuracy(eye_truepos, eye_missed, eye_false_pos, non_events)
accuracy_below = compute_accuracy(below_truepos, below_missed, below_false_pos, non_events)

print("Mean Accuracy scores:")
# Multiply by 100 if you want to report as percentage
print(f"Above: {np.mean(accuracy_above)*100:.1f}%")
print(f"Eye: {np.mean(accuracy_eye)*100:.1f}%")
print(f"Below: {np.mean(accuracy_below)*100:.1f}%")

# --- Statistical Analysis (on Accuracy) ---
data_wide_acc = pd.DataFrame({
    'Above': accuracy_above,
    'Below': accuracy_below,
    'Eye': accuracy_eye,
})

# Check for NaN values before stats
if data_wide_acc.isnull().values.any():
    print("\nWarning: NaN values found in accuracy data. Check calculations or input.")
    # Optional: drop rows with NaN if appropriate, or handle otherwise
    # data_wide_acc = data_wide_acc.dropna()
    # n_participants = len(data_wide_acc) # Update n if rows are dropped

# Friedman test on Accuracy
# Need to handle potential NaNs if they exist
valid_data_for_friedman = [data_wide_acc[col].dropna().tolist() for col in data_wide_acc.columns]
# Ensure all lists have the same length after dropping NaNs (might not if NaN pattern differs)
min_len = min(len(lst) for lst in valid_data_for_friedman)
if all(len(lst) == n_participants for lst in valid_data_for_friedman) and n_participants > 0 : # Run only if complete data
    friedman_stat_acc, friedman_p_acc = friedmanchisquare(*valid_data_for_friedman)
    print(f"\nFriedman Test on Accuracy: statistic={friedman_stat_acc:.3f}, pvalue={friedman_p_acc:.3e}")

    # Nemenyi post-hoc test on Accuracy
    if friedman_p_acc < 0.05:
        print("\nRunning Nemenyi Post Hoc Test on Accuracy...")
        nemenyi_result_acc = sp.posthoc_nemenyi_friedman(data_wide_acc) # Assumes no NaNs for simplicity here
        print(nemenyi_result_acc)
    else:
        print("\nFriedman test on Accuracy not significant, skipping post-hoc test.")
elif min_len > 0:
     print("\nWarning: Friedman test skipped due to missing or inconsistent data after NaN removal.")
else:
     print("\nWarning: Not enough data to run Friedman test.")


# --- Plotting Section (Accuracy) ---

# 1. Prepare data in long format for Seaborn plotting
df_plot_acc = pd.DataFrame({
    # Ensure using potentially modified n_participants if NaNs were handled by dropping
    'Participant': list(range(1, n_participants + 1)) * 3,
    'Position': ['Above'] * n_participants + ['Eye'] * n_participants + ['Below'] * n_participants,
    'Accuracy': accuracy_above + accuracy_eye + accuracy_below
})

# Remove rows with NaN accuracy before plotting if they exist
df_plot_acc = df_plot_acc.dropna(subset=['Accuracy'])


# 2. Define the desired order for plotting
position_order = ['Above', 'Eye', 'Below']
df_plot_acc['Position'] = pd.Categorical(df_plot_acc['Position'], categories=position_order, ordered=True)

# 3. Create the plot
plt.figure(figsize=(8, 7)) # Adjust figure size if needed

# Create the bar plot for means and 95% CIs
# Use ci=95 for older Seaborn compatibility
ax = sns.barplot(data=df_plot_acc, x='Position', y='Accuracy',
                 order=position_order,
                 ci=95,             # Use older 'ci' parameter
                 palette='viridis', # Example color palette
                 capsize=0.1)       # Add caps to error bars

# Overlay individual data points using stripplot
sns.stripplot(data=df_plot_acc, x='Position', y='Accuracy',
              order=position_order,
              color='black',   # Color for the points
              size=6,          # Size of the points
              jitter=True,     # Allow horizontal spread
              alpha=0.6,       # Make points slightly transparent
              ax=ax)           # Plot on the same axes as the barplot

# 4. Customize the plot
ax.set_xlabel("Notification Position", fontsize=12)
ax.set_ylabel("Accuracy", fontsize=12) # Label as proportion
ax.set_title("Mean Accuracy by Position\n(Bars: 95% CI, Points: Individual Participants)", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=11)

# Set y-axis limits to be appropriate for accuracy (proportion 0 to 1)
ax.set_ylim(0, 1.05) # Set ylim from 0 to 1 (or slightly above 1)

# Optional: Format y-axis ticks as percentages if preferred
# from matplotlib.ticker import PercentFormatter
# ax.yaxis.set_major_formatter(PercentFormatter(1.0))
# ax.set_ylabel("Accuracy (%)", fontsize=12) # Change label if using PercentFormatter


# Improve layout
plt.tight_layout()
plt.show()