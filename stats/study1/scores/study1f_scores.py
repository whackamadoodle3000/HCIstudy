import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM
from scipy.stats import friedmanchisquare
from scipy.stats import wilcoxon
import itertools

#Female - Engagement - Part 1
#"My conversational partner was engaged in the conversation."
data = {
    'Above': [6, 7, 7, 7, 7, 7, 7, 7],
    'Eye': [7, 7, 7, 7, 7, 6, 6, 6],
    'Below': [7, 7, 6, 7, 7, 4, 6, 5],
    'Control': [7, 7, 7, 6, 7, 5, 7, 7]
}

#Female - Engagement - Part 2
# data = {
#     'Above': [7,7,4,6,7,6,5,6],
#     'Eye': [7,7,6,7,6,5,7,7],
#     'Below': [7,7,6,6,5,5,7,6],
#     'Control': [7,7,6,7,6,6,6,4]
# }

#Female - Comfort - Part 1
#"My conversational partner made me feel uncomfortable." 1=false, 7=true
# data = {
#     'Above': [3,1,1,1,1,1,1,2],
#     'Eye': [1,1,1,3,1,5,1,2],
#     'Below': [1,1,1,2,1,4,1,3],
#     'Control': [1,1,1,2,1,1,1,1]
# }

# #Female - Comfort - Part 2
# data = {
#     'Above': [1,1,2,2,1,5,1,2],
#     'Eye': [1,1,1,1,1,5,1,1],
#     'Below': [1,1,1,3,1,6,1,1],
#     'Control': [1,1,1,2,1,6,1,1]
# }

above = data['Above']
eye = data['Eye']
below = data['Below']
control = data['Control']

# Create a DataFrame where each column is a position and rows are participants
df = pd.DataFrame(data)

# Reshape the data for ANOVA with repeated measures
df_long = pd.melt(df, var_name="Position", value_name="Engagement", ignore_index=False)
df_long['Participant'] = df_long.index + 1  # Adding participant as a variable

# Perform the ANOVA with repeated measures
anova = AnovaRM(df_long, 'Engagement', 'Participant', within=['Position'])
anova_result = anova.fit()

print(anova_result.summary())
p_value = anova_result.anova_table['Pr > F'][0]
print(f"P-value: {p_value}")
print("Stat sig: YES\n\n" if p_value < 0.05 else "Stat sig: NO\n")
#note: Greenhouse-Geisser correction is applied automatically in the AnovaRM method in statsmodels

#friedman
statistic_m, p_value_m = friedmanchisquare(above, eye, control, below)
print(f"Friedman test statistic: {statistic_m}")
print(f"Friedman test p-value: {p_value_m}")
print("Stat sig: YES\n\n" if p_value_m < 0.05 else "Stat sig: NO\n\n")


#paired wilcoxan
# stat_above, p_above = wilcoxon(control, above)
# stat_eye, p_eye = wilcoxon(control, eye)
# stat_right, p_right = wilcoxon(control, below)


positions = ['Above', 'Eye', 'Below', 'Control']
pairs = itertools.combinations(positions, 2)
results = {}
for pair in pairs:
    pos1, pos2 = pair
    stat, p_value = wilcoxon(data[pos1], data[pos2])
    results[f"{pos1} vs {pos2}"] = (stat, p_value)
    print(f"Wilcoxon test between {pos1} and {pos2}:\nTest statistic = {stat}, p-value = {p_value}")
    print("Stat sig: YES\n\n" if p_value < 0.05 else "Stat sig: NO\n")


# print(f"Wilcoxon test between 'below' and 'above':\nTest statistic = {stat_above}, p-value = {p_above}")
# print("Stat sig: YES\n\n" if p_above < 0.05 else "Stat sig: NO\n")

# print(f"Wilcoxon test between 'below' and 'eye':\nTest statistic = {stat_eye}, p-value = {p_eye}")
# print("Stat sig: YES\n\n" if p_eye < 0.05 else "Stat sig: NO\n")

# print(f"Wilcoxon test between 'below' and 'right':\nTest statistic = {stat_right}, p-value = {p_right}")
# print("Stat sig: YES\n\n" if p_right < 0.05 else "Stat sig: NO\n")




