import matplotlib.pyplot as plt
import numpy as np

# Data
positions = ['Above', 'Eye', 'Below', 'Control']  # Positions (X-axis labels)
ratings = [1, 2, 3, 4, 5, 6, 7]  # Ratings (Y-axis segments)


from collections import Counter

def count_ratings(above, eye, right, below):
    positions = {'Above': above, 'Eye': eye, 'Below': below, 'Control': control}
    rating_counts = {}
    
    for pos, ratings in positions.items():
        count = Counter(ratings)
        rating_counts[pos] = [count.get(i, 0) for i in range(1, 8)]  # Count ratings 1-7
    
    return rating_counts

# Example input
#part 1
above = [6,7,7,7,7,7,7,7,7,7,5,7,7,5,6,6]
eye = [7,7,7,7,7,6,6,6,7,7,7,7,7,6,6,7]
below = [7,7,6,7,7,4,6,5,7,7,7,7,7,6,7,7]
control = [7,7,7,6,7,5,7,7,7,6,6,7,7,4,7,7]

#part 2
# above = [6,7,4,4,7,6,6,5, 7,7,4,6,7,6,5,6]
# eye = [7,7,7,7,7,6,6,7, 7,7,6,7,6,5,7,7]
# below = [7,7,6,7,7,5,5,7, 7,7,6,6,5,5,7,6]
# control = [7,7,6,6,7,6,6,6, 7,7,6,7,6,6,6,4]

# Compute rating counts
rating_counts = count_ratings(above, eye, control, below)
print(rating_counts)

# Custom color scheme for ratings 1 to 7 (dark green to red)
colors_custom = ['#ff4500', '#ff6347', '#ff7f50', '#ff9966', '#66c266', '#2e8b57', '#006400']
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
ax.set_title('Part 1 (Uninformed) Engagement Ratings')
ax.legend(title='Rating')

# Adjust layout and display
plt.tight_layout()
plt.show()