import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Input data
positions = ['Above', 'Eye', 'Below']
true_positives = np.array([3.0625, 0.25, 1.8125]) #averages
missed = np.array([4.9375, 7.75, 6.1875])

# Calculate accuracy (recall)
accuracy = true_positives / (true_positives + missed)
accuracy = np.nan_to_num(accuracy)  # Handle division by zero

# Create DataFrame for organization
df_metrics = pd.DataFrame({
    'Position': positions,
    'Accuracy': accuracy
})

# Plotting
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df_metrics['Position'], df_metrics['Accuracy'], color='#4e79a7')

# Formatting
ax.set_ylabel('Accuracy')
ax.set_title('Notification Detection Accuracy by Position')
ax.set_ylim(0, 1.1)

# Add value labels to each bar
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # offset
                textcoords='offset points',
                ha='center', va='bottom')

plt.tight_layout()
plt.show()
