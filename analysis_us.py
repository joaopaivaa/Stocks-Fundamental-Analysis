import pandas as pd
from query_US import grades_df

# df_grades = pd.read_csv("stocks_us_grades.csv", sep=';')
df_grades = grades_df.copy()
df_grades.sort_values(by='ticker', ascending=True, inplace=True)
df_grades.reset_index(drop=True, inplace=True)

df_evaluated = pd.read_csv("stocks_us_evaluated.csv", sep=';')
df_evaluated.sort_values(by='ticker', ascending=True, inplace=True)
df_evaluated.reset_index(drop=True, inplace=True)

df_evaluated['Grade'] = df_grades['Grade']

df_evaluated.sort_values(by='Grade', ascending=False, inplace=True)
df_evaluated.reset_index(drop=True, inplace=True)
df_evaluated = df_evaluated.head(10)

df_evaluated['Portfolio %'] = round(100 * df_evaluated['Grade'] / df_evaluated['Grade'].head(10).sum(), 2)

portfolio_total_value = 1000
df_evaluated['Portfolio Value'] = round(df_evaluated['Portfolio %'] * portfolio_total_value / 100, 2)