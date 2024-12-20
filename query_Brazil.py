import pandas as pd
from sklearn.preprocessing import MinMaxScaler

stocks_df = pd.read_csv("stocks_df_brazil.csv")

stocks_df_scaled = pd.DataFrame(index=range(len(stocks_df)), columns=stocks_df.columns)
stocks_df_scaled['grade'] = 0
for column in stocks_df.columns[:4]:
    stocks_df_scaled[column] = stocks_df[column]

for sector in stocks_df['sector'].unique():

    sector_index = stocks_df[stocks_df['sector'] == sector].index

    if sector == 'Technology':
        pass

    for column in stocks_df.columns[4:]:
        stocks_df.loc[sector_index, column] = stocks_df.loc[sector_index, column].fillna(stocks_df.loc[sector_index, column].mean()) if not pd.isna(stocks_df.loc[sector_index, column].mean()) else 0

        scaler = MinMaxScaler()
        stocks_df_scaled.loc[sector_index, column] = scaler.fit_transform(stocks_df.loc[sector_index, [column]])
        if (not 'std' in column) and (column in ['participation_of_third_party_capital','debit_composition','net_debt_ebitda','assets_net_worth','EV/revenue','EV/ebitda']):
            stocks_df_scaled.loc[sector_index, column] = 1 - stocks_df_scaled.loc[sector_index, column]
        if 'std' in column:
            stocks_df_scaled.loc[sector_index, column] = 0.5*(1 - stocks_df_scaled.loc[sector_index, column])
        stocks_df_scaled.loc[sector_index, 'grade'] += stocks_df_scaled.loc[sector_index, column]

stocks_df_scaled.sort_values('EV/ebitda', ascending=False)