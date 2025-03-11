from scipy.stats import friedmanchisquare
from scipy.stats import wilcoxon
from scipy.stats import binom
import numpy as np

# Define the positions in order (Eye, Above, Right, Below)
positions = ["Eye", "Above", "Right", "Below"]

# Dataset with participants' rankings
data_raw_1 = [
    ["Above", "Below", "Eye", "Right"],
    ["Eye", "Below", "Right", "Above"],
    ["Right", "Above", "Eye", "Below"],
    ["Eye", "Right", "Below", "Above"],
    ["Above", "Right", "Below", "Eye"],
    ["Above", "Eye", "Right", "Below"],
    ["Right", "Eye", "Above", "Below"]
]

data_raw_2 = [
    ["Above", "Right", "Below", "Eye"],
    ["Below", "Eye", "Right", "Above"],
    ["Above", "Eye", "Right", "Below"],
    ["Eye", "Right", "Below", "Above"],
    ["Above", "Right", "Eye", "Below"],
    ["Above", "Right", "Eye", "Below"],
    ["Right", "Eye", "Above", "Below"]
]

# Initialize an empty list to store the rankings for each participant
data_raw = []

# Convert the rankings into numerical values
for ranking in data_raw_2: #TODO - toggle
    # Create a list of ranks for the current participant
    ranks = [ranking.index(pos) + 1 for pos in positions]
    data_raw.append(ranks)

# Convert the list of ranks to a numpy array
data = np.array(data_raw)

# Print the final result
print(data)



# Running the Friedman test
statistic, p_value = friedmanchisquare(*data.T)

print(f"Statistic: {statistic}")
print(f"P-value: {p_value}")
print("Friedman Stat sig: YES\n\n" if p_value < 0.05 else "Stat sig: NO\n")



print("\n\n Paired tests - 6 variations")
# Perform Wilcoxon paired tests for each pair of positions
#but just treating them like numbers, not like a < or > ordered ranking
pairs = [
    ("Eye vs Above", data[:, 0], data[:, 1]),
    ("Eye vs Right", data[:, 0], data[:, 2]),
    ("Eye vs Chest", data[:, 0], data[:, 3]),
    ("Above vs Right", data[:, 1], data[:, 2]),
    ("Above vs Chest", data[:, 1], data[:, 3]),
    ("Right vs Chest", data[:, 2], data[:, 3]),
]

# Run Wilcoxon test and print results
for pair_name, rank1, rank2 in pairs:
    stat, p = wilcoxon(rank1, rank2)
    print(f"Wilcoxon test for {pair_name}:")
    print(f"Test statistic = {stat}, p-value = {p}")
    print("Stat sig: YES\n\n" if p < 0.05 else "Stat sig: NO\n")



#binomial test of chest against other things (lumped together, not one by one pairwise)
print("\n\n Binomial test where win condition is chest is the worst")

# Data: Each row corresponds to a participant's ranking for the positions (Eye, Above, Right, Chest)
# Count the number of times "Chest" (rank 4) is ranked 4th
chest_rank_4_count = np.sum(data[:, 3] == 4)

# Total number of participants
n = len(data)

# Perform a binomial test for the probability of "Chest" being ranked 4th by random chance (p = 0.25)
# The hypothesis is: If random, we'd expect "Chest" to be ranked 4th approximately 25% of the time
p_value = 1 - binom.cdf(chest_rank_4_count - 1, n=n, p=0.25)

# Print the result
print(f"Chest was ranked 4th by {chest_rank_4_count} participants.")
print(f"P-value (chance of Chest being ranked 4th by random chance): {p_value}")



