import matplotlib.pyplot as plt
import numpy as np

# Display order: Control is last
positions = ['Above', 'Eye', 'Below', 'Control']
true_positives = [3.0625, 0.25, 1.8125, 0]
missed = [4.9375, 7.75, 6.1875, 0]
false_positives = [0.75, 0.75, 0.875, 1.6875]

# Reverse for top-down plotting
positions = positions[::-1]
true_positives = true_positives[::-1]
missed = missed[::-1]
false_positives = false_positives[::-1]

# Plot settings
y = np.arange(len(positions))
bar_height = 0.6
notification_limit = 8

fig, ax = plt.subplots(figsize=(10, 6))

# Custom colors
color_tp = '#2e8b57' #dark green
color_missed = '#ff4500' # #red
color_fp = '#ff9966' #light red

# Plot true positives and missed (stacked)
for i in range(len(positions)):
    ax.barh(y[i], true_positives[i], height=bar_height, color=color_tp)
    ax.barh(y[i], missed[i], height=bar_height, left=true_positives[i], color=color_missed)
    ax.barh(y[i], false_positives[i], height=bar_height, left=notification_limit, color=color_fp)

# Vertical reference line
ax.axvline(x=notification_limit, linestyle='--', color='gray')

# Labels and formatting
ax.set_yticks(y)
ax.set_yticklabels(positions)
ax.set_xlabel('Number of Clicks')
ax.set_title('Average Clicker Usage')

# Complete legend
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color=color_tp, label='True Positives'),
    plt.Rectangle((0, 0), 1, 1, color=color_missed, label='Missed'),
    plt.Rectangle((0, 0), 1, 1, color=color_fp, label='False Positives')
]
ax.legend(handles=legend_handles)

plt.tight_layout()
plt.show()
