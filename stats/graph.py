import matplotlib.pyplot as plt
import numpy as np

# Data
positions = ['Eye', 'Above', 'Right', 'Below']  # Positions (X-axis labels)
ratings = [1, 2, 3, 4, 5, 6, 7]  # Ratings (Y-axis segments)


# Above: 1,2,2,5,2
# Eye: 1,3,4,3,1
# right: 4,4,1,3,3
# Below: 4,2,5,2,6

# Count of each rating per position (each position has 7 ratings, one for each rating from 1 to 7)
rating_counts = {
    'Eye': [2, 0, 2, 1, 0, 0, 0],    # Counts for ratings 1, 2, 3, 4, 5, 6, 7 at 'Eye'
    'Above': [1, 3, 0, 0, 1, 0, 0],  # Counts for ratings 1, 2, 3, 4, 5, 6, 7 at 'Above'
    'Right': [1, 0, 2, 2, 0, 0, 0],  # Counts for ratings 1, 2, 3, 4, 5, 6, 7 at 'Right'
    'Below': [0, 2, 0, 1, 1, 1, 0]   # Counts for ratings 1, 2, 3, 4, 5, 6, 7 at 'Below'
}

# Custom color scheme for ratings 1 to 7 (dark green to red)
colors_custom = ['#006400', '#2e8b57', '#66c266', '#ff9966', '#ff7f50', '#ff6347', '#ff4500']

# Plot setup
fig, ax = plt.subplots(figsize=(8, 6))

# X-axis positions for bars
x_pos = np.arange(len(positions))

# Stack the bars
bottoms = np.zeros(len(positions))

# Loop through each rating (1 to 7) and stack the bars
for i, rating in enumerate(ratings):
    counts = [rating_counts[pos][i] for pos in positions]  # Get the counts for each position
    ax.bar(x_pos, counts, bottom=bottoms, color=colors_custom[i], label=str(rating), width=0.5)
    bottoms += counts  # Update the bottom to stack the next color segment

# Set labels, title, and legend
ax.set_xticks(x_pos)
ax.set_xticklabels(positions)
ax.set_ylabel('Count')
ax.set_title('Position Ratings Distribution')
ax.legend(title='Rating')

# Adjust layout and display
plt.tight_layout()
plt.show()
