import pandas as pd
from datetime import datetime

df_grades = pd.read_csv("silver/grades_df_us.csv")

df_grades.sort_values(by='ticker', ascending=True, inplace=True)
df_grades.reset_index(drop=True, inplace=True)

df_evaluated = pd.read_csv("silver/stocks_df_us.csv")

df_evaluated.sort_values(by='ticker', ascending=True, inplace=True)
df_evaluated.reset_index(drop=True, inplace=True)

df_evaluated['Grade'] = df_grades['Grade']

df_evaluated.sort_values(by='Grade', ascending=False, inplace=True)
df_evaluated.reset_index(drop=True, inplace=True)
df_evaluated = df_evaluated.head(10)

df_evaluated['Portfolio %'] = round(100 * df_evaluated['Grade'] / df_evaluated['Grade'].head(10).sum(), 2)

portfolio_total_value = 1000
df_evaluated['Portfolio Value'] = round(df_evaluated['Portfolio %'] * portfolio_total_value / 100, 2)

df_evaluated.to_csv('gold/df_evaluated_us.csv', index=False)

past_portfolios = pd.read_csv('gold/past_portfolios_us.csv')
past_portfolios[f"{datetime.now().strftime('%Y-%m-%d')}"] = df_evaluated['ticker']
past_portfolios.to_csv('gold/past_portfolios_us.csv', index=False)