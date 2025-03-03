from scipy.stats import friedmanchisquare
from scipy.stats import wilcoxon

# Data for each position

#6 guys - stat sig for friedman 
#8 guys - stat sig for paired (can include or not include the guy who put 1s for everything)
above_f = [5, 3, 3, 6, 5, 3, 3, 6] #only first 4 are real data points
eye_f = [5, 1, 4, 2, 5, 1, 4, 2]
right_f = [4, 2, 3, 4, 4, 2, 3, 4]
below_f = [6, 2, 6, 6, 6, 2, 6, 6]

# Running the Friedman test
statistic_f, p_value_f = friedmanchisquare(above_f, eye_f, right_f, below_f)

# Printing results with labels
print(f"FEMALE Friedman test statistic: {statistic_f}")
print(f"FEMALE Friedman test p-value: {p_value_f}")
print("Stat sig: YES\n\n" if p_value_f < 0.05 else "Stat sig: NO\n\n")

# Running Wilcoxon paired tests for each pair (below vs. above, below vs. eye, below vs. right)
stat_above, p_above = wilcoxon(below_f, above_f)
stat_eye, p_eye = wilcoxon(below_f, eye_f)
stat_right, p_right = wilcoxon(below_f, right_f)

# stat_stupid, p_stupid = wilcoxon(eye_f, right_f)
# stat_above_right, p_above_right = wilcoxon(above_f, right_f)
# stat_above_eye, p_above_eye = wilcoxon(above_f, eye_f)

# Printing results with labels
print(f"Wilcoxon test between 'below' and 'above':\nTest statistic = {stat_above}, p-value = {p_above}")
print("Stat sig: YES\n\n" if p_above < 0.05 else "Stat sig: NO\n\n")

print(f"Wilcoxon test between 'below' and 'eye':\nTest statistic = {stat_eye}, p-value = {p_eye}")
print("Stat sig: YES\n\n" if p_eye < 0.05 else "Stat sig: NO\n\n")

print(f"Wilcoxon test between 'below' and 'right':\nTest statistic = {stat_right}, p-value = {p_right}")
print("Stat sig: YES\n\n" if p_right < 0.05 else "Stat sig: NO\n\n")




# print(f"Wilcoxon test between 'eye' and 'right':\nTest statistic = {stat_stupid}, p-value = {p_stupid}")
# print("Stat sig: YES\n\n" if p_stupid < 0.05 else "Stat sig: NO\n\n")

# print(f"Wilcoxon test between 'right' and 'above':\nTest statistic = {stat_above_right}, p-value = {p_above_right}")
# print("Stat sig: YES\n\n" if p_above_right < 0.05 else "Stat sig: NO\n\n")

# print(f"Wilcoxon test between 'above' and 'eye':\nTest statistic = {stat_above_eye}, p-value = {p_above_eye}")
# print("Stat sig: YES\n\n" if p_above_eye < 0.05 else "Stat sig: NO\n\n")