from scipy.stats import friedmanchisquare, norm
import numpy as np
import pandas as pd
import scikit_posthocs as sp

# Data (n=16 participants)
above_truepos = [1, 3, 6, 3, 6, 3, 1, 1, 2, 1, 4, 6, 3, 0, 4, 5]
above_missed = [7, 5, 2, 5, 2, 5, 7, 7, 6, 7, 4, 2, 5, 8, 4, 3]
above_false_pos = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 0]

eye_truepos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0]
eye_missed = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 7, 7, 8]
eye_false_pos = [0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 1, 2, 1]

below_truepos = [0, 0, 3, 4, 2, 4, 2, 0, 1, 4, 1, 1, 3, 0, 2, 2]
below_missed = [8, 8, 5, 4, 6, 4, 6, 8, 7, 4, 7, 7, 5, 8, 6, 6]
below_false_pos = [0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 5, 2, 3, 0]

# control_truepos = [0] * 16
# control_missed = [0] * 16  # No notifications
# control_false_pos = [0, 1, 7, 0, 1, 1, 0, 3, 0, 2, 1, 1, 5, 0, 4, 1]

# Number of opportunities for False Alarms (non-event intervals)
# Assumes 16 non-event intervals for experimental conditions and 24 for control
non_events = [16] * 16
# non_events_control = [24] * 16

# Function to compute d' using Log-Linear correction
# Ref: Stanislaw & Todorov (1999), Behavior Research Methods, Instruments, & Computers
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
        total_trials_noise = non_events_list[i] # Assuming non_events_list[i] = FA + CR for participant i

        # Correct Rejections = Total Noise Trials - False Alarms
        correct_rejections = total_trials_noise - false_alarms
        if correct_rejections < 0:
             # This check is important. non_events should be >= false_alarms
             print(f"Warning: Participant {i+1} has {false_alarms} FA but only {total_trials_noise} non-events. Check data.")
             correct_rejections = 0 # Or handle as appropriate (e.g., skip participant, set FA rate to max)


        # Log-Linear Correction: Add 0.5 to all cells
        hit_rate = (hits + 0.5) / (total_trials_signal + 1)
        fa_rate = (false_alarms + 0.5) / (total_trials_noise + 1)

        # Ensure rates are within (0, 1) for norm.ppf (should be guaranteed by correction)
        hit_rate = max(min(hit_rate, 1 - 1e-9), 1e-9)
        fa_rate = max(min(fa_rate, 1 - 1e-9), 1e-9)

        d_prime = norm.ppf(hit_rate) - norm.ppf(fa_rate)
        d_prime_scores.append(d_prime)
    return d_prime_scores


# Calculate d' for each condition
# **** Note on Control Condition ****
# If control had NO target events (TP=0, Missed=0 is forced), d' is conceptually tricky.
# Hit Rate = (0 + 0.5) / (0 + 0 + 1) = 0.5
# FA Rate = (FA + 0.5) / (NonEvents + 1)
# d' = norm.ppf(0.5) - norm.ppf(FAR) = 0 - norm.ppf(FAR) = -norm.ppf(FAR)
# This measures bias (propensity to click) rather than sensitivity in the control.
# Ensure this interpretation aligns with your research question.
# If control HAD events but they weren't cued by notifications, use the actual TP/Missed counts for those events.
# Based on your control_missed = [0]*16, I'm assuming NO target events in control.

dprime_above = compute_dprime(above_truepos, above_missed, above_false_pos, non_events)
dprime_eye = compute_dprime(eye_truepos, eye_missed, eye_false_pos, non_events)
dprime_below = compute_dprime(below_truepos, below_missed, below_false_pos, non_events)
# dprime_control = compute_dprime(control_truepos, control_missed, control_false_pos, non_events_control)

print(dprime_above)
print(dprime_below)
print(dprime_eye)

print("Mean d' scores:")
print(f"Above: {np.mean(dprime_above):.3f}")
print(f"Eye: {np.mean(dprime_eye):.3f}")
print(f"Below: {np.mean(dprime_below):.3f}")
# print(f"Control: {np.mean(dprime_control):.3f}") # Remember interpretation if HR=0.5

# Run Friedman test
friedman_result = friedmanchisquare(
    dprime_above, dprime_eye, dprime_below)


data = pd.DataFrame({
    'Above': dprime_above,
    'Below': dprime_below,
    'Eye': dprime_eye,
})

# Run Friedman test (optional but good practice before post-hoc)
friedman_stat, friedman_p = friedmanchisquare(data['Above'], data['Below'], data['Eye'])
print(f"Friedman Test on wide data: statistic={friedman_stat:.3f}, pvalue={friedman_p:.3e}")

# Run Nemenyi post-hoc on the wide DataFrame
if friedman_p < 0.05: # Usually only run post-hoc if Friedman is significant
    print("\nRunning Nemenyi Post Hoc Test on wide DataFrame...")
    nemenyi_result = sp.posthoc_nemenyi_friedman(data)
    print(nemenyi_result)
else:
    print("\nFriedman test not significant, skipping post-hoc test.")