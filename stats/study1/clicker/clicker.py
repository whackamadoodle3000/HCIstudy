from scipy.stats import friedmanchisquare
import numpy as np
import pandas as pd

# Data (n=16 participants)
above_truepos = [1, 3, 6, 3, 6, 3, 1, 1, 2, 1, 4, 6, 3, 0, 4, 5]
above_missed = [7, 5, 2, 5, 2, 5, 7, 7, 6, 7, 4, 2, 5, 8, 4, 3]

eye_truepos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0]
eye_missed = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 7, 7, 8]

below_truepos = [0, 0, 3, 4, 2, 4, 2, 0, 1, 4, 1, 1, 3, 0, 2, 2]
below_missed = [8, 8, 5, 4, 6, 4, 6, 8, 7, 4, 7, 7, 5, 8, 6, 6]

control_truepos = [0] * 16
control_missed = [0] * 16  # No notifications

# Calculate accuracy = TP / (TP + Missed)
def safe_accuracy(tp, missed):
    return [tp[i] / (tp[i] + missed[i]) if (tp[i] + missed[i]) > 0 else 0 for i in range(len(tp))]

accuracy_above = safe_accuracy(above_truepos, above_missed)
accuracy_eye = safe_accuracy(eye_truepos, eye_missed)
accuracy_below = safe_accuracy(below_truepos, below_missed)
accuracy_control = safe_accuracy(control_truepos, control_missed)

# Run Friedman test
friedman_result = friedmanchisquare(accuracy_above, accuracy_eye, accuracy_below, accuracy_control)

# Prepare data for review
df_accuracy = pd.DataFrame({
    'Above': accuracy_above,
    'Eye': accuracy_eye,
    'Below': accuracy_below,
    'Control': accuracy_control
})

print(df_accuracy)
print("\nFriedman test result:")
print(friedman_result)


import scikit_posthocs as sp
import pandas as pd

# Prepare data in long format
df_long = pd.DataFrame({
    'Participant': list(range(1, 17)) * 4,
    'Position': ['Above'] * 16 + ['Eye'] * 16 + ['Below'] * 16 + ['Control'] * 16,
    'Accuracy': accuracy_above + accuracy_eye + accuracy_below + accuracy_control
})

# Run Nemenyi post hoc test
posthoc_result = sp.posthoc_nemenyi_friedman(df_long, y_col='Accuracy', block_col='Participant', group_col='Position')

print(posthoc_result)

