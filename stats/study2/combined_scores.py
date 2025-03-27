from scipy.stats import friedmanchisquare
from scipy.stats import wilcoxon

#COMBINED "socially awkward" scores, part 1
#comment these arrays out and uncomment the part 2 arrays below to run tests on part 2 data
# above_m = [1, 2, 3, 5, 3, 3, 1, 2, 5, 3, 3, 6, 2, 2, 4, 2]
# eye_m = [2, 3, 2, 2, 3, 4, 1, 5, 5, 1, 4, 2, 4, 4, 4, 5]
# right_m = [4, 7, 1, 6, 1, 6, 1, 2, 4, 2, 3, 4, 2, 7, 3, 2]
# below_m = [6, 7, 6, 5, 7, 7, 6, 4, 6, 2, 6, 6, 7, 7, 7, 4]


#COMBINED "socially awkward" scores, part 2
above_m = [1, 2, 2, 5, 2, 3, 1, 5, 3, 3, 2, 7, 1, 6, 2, 2]
eye_m = [1, 3, 4, 3, 1, 4, 1, 3, 2, 1, 3, 2, 1, 4, 2, 5]
right_m = [4, 4, 1, 3, 3, 5, 2, 3, 3, 3, 3, 3, 1, 4, 1, 4]
below_m = [4, 2, 5, 2, 6, 7, 6, 6, 3, 2, 6, 5, 2, 7, 6, 4]








# Running the Friedman test
statistic_m, p_value_m = friedmanchisquare(above_m, eye_m, right_m, below_m)

# Printing results with labels
print(f"COMBINED Friedman test statistic: {statistic_m}")
print(f"COMBINED Friedman test p-value: {p_value_m}")
print("Stat sig: YES\n\n" if p_value_m < 0.05 else "Stat sig: NO\n\n")

# Running Wilcoxon paired tests for each pair (below vs. above, below vs. eye, below vs. right)
stat_above, p_above = wilcoxon(below_m, above_m)
stat_eye, p_eye = wilcoxon(below_m, eye_m)
stat_right, p_right = wilcoxon(below_m, right_m)

# Printing results with labels
print(f"Wilcoxon test between 'below' and 'above':\nTest statistic = {stat_above}, p-value = {p_above}")
print("Stat sig: YES\n\n" if p_above < 0.05 else "Stat sig: NO\n\n")

print(f"Wilcoxon test between 'below' and 'eye':\nTest statistic = {stat_eye}, p-value = {p_eye}")
print("Stat sig: YES\n\n" if p_eye < 0.05 else "Stat sig: NO\n\n")

print(f"Wilcoxon test between 'below' and 'right':\nTest statistic = {stat_right}, p-value = {p_right}")
print("Stat sig: YES\n\n" if p_right < 0.05 else "Stat sig: NO\n\n")


