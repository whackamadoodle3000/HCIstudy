import numpy as np
from scipy.stats import friedmanchisquare

#position meanings:
# 0: eye
# 1: above
# 2: right
# 3: below

# Rankings from each participant (from most preferred to least preferred)
data = np.array([
    [1, 2, 3, 4],  # Participant 1
    [2, 1, 3, 4],  # Participant 2
    [3, 1, 2, 4],  # Participant 3
    [1, 2, 4, 3],  # Participant 4
    [1, 2, 3, 4],  # Participant 5
    [2, 1, 3, 3]   # Participant 6 (Tied ranks: Right and Below)
])

# Method 1: Using ranks as they are (without adjusting for ties)
stat1, p_value1 = friedmanchisquare(*data.T)

# Method 2: Averaging tied ranks for participant 6
data_tied_avg = np.array([
    [1, 2, 3, 4],
    [2, 1, 3, 4],
    [3, 1, 2, 4],
    [1, 2, 4, 3],
    [1, 2, 3, 4],
    [2, 1, 3.5, 3.5]  # Averaging tied ranks (3,3) -> (3.5,3.5)
])

stat2, p_value2 = friedmanchisquare(*data_tied_avg.T)
print("part1")
print(stat1,p_value1)
print(stat2,p_value2)



from scipy.stats import rankdata

# New dataset with rankings (from most preferred to least preferred)
data_new = np.array([
    [1, 2, 3, 4],  # Participant 1
    [2, 1, 3, 4],  # Participant 2
    [3, 2, 1, 4],  # Participant 3
    [1, 4, 2, 3],  # Participant 4
    [1, 2, 3, 4],  # Participant 5
    [2, 3, 4, 4]   # Participant 6 (Tied ranks: Below and Eye)
])

# Method 1: Using ranks as they are (without adjusting for ties)
stat1_new, p_value1_new = friedmanchisquare(*data_new.T)

# Method 2: Averaging tied ranks for participant 6
data_new_tied_avg = np.array([
    [1, 2, 3, 4],
    [2, 1, 3, 4],
    [3, 2, 1, 4],
    [1, 4, 2, 3],
    [1, 2, 3, 4],
    [2, 3, 4.5, 4.5]  # Averaging tied ranks (4,4) -> (4.5,4.5)
])

stat2_new, p_value2_new = friedmanchisquare(*data_new_tied_avg.T)

(stat1_new, p_value1_new), (stat2_new, p_value2_new)

print("part2")
print(stat1_new,p_value1_new)
print(stat2_new,p_value2_new)