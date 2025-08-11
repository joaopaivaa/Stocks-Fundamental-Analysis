import re
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

evaluation = {
        "EV/revenue": {"positive": "< 3", "negative": "> 5"},
        "EV/ebitda": {"positive": "< 10", "negative": "> 20"},
        "gross_margin": {"positive": "> 0.4", "negative": "< 0.2"},
        "ebitda_margin": {"positive": "> 0.3", "negative": "< 0.15"},
        "ebit_margin": {"positive": "> 0.2", "negative": "< 0.1"},
        "net_margin": {"positive": "> 0.15", "negative": "< 0.05"},
        "roa": {"positive": "> 0.07", "negative": "< 0.03"},
        "roe": {"positive": "> 0.15", "negative": "< 0.1"},
        "general_liquidity": {"positive": "> 1.5", "negative": "< 1"},
        "current_liquidity": {"positive": "> 1.5", "negative": "< 1"},
        "dry_liquidity": {"positive": "> 1", "negative": "< 0.8"},
        "participation_of_third_party_capital": {"positive": "< 0.5", "negative": "> 0.7"},
        "net_debt_ebitda": {"positive": "< 2", "negative": "> 4"},
        "dividend_yield": {"positive": "> 4", "negative": "< 2"},
        "dividend_rate": {"positive": "> 30", "negative": "< 15"}
    }

priority = ['EV/ebitda','net_margin','ebitda_margin','roe','net_debt_ebitda','general_liquidity']

size = 'Nano'
stocks_df = pd.read_csv(f"bronze/stocks_df_usa_{size}.csv", decimal='.', sep=';')

stocks_df = stocks_df.loc[stocks_df['negative_ebitda'] != 1]
stocks_df = stocks_df.loc[stocks_df['negative_ebit'] != 1]
stocks_df = stocks_df.loc[stocks_df['negative_net_income'] != 1]
stocks_df = stocks_df.loc[stocks_df['negative_operating_income'] != 1]

stocks_df = stocks_df.loc[stocks_df['ebitda_mean'] > 0]
stocks_df = stocks_df.loc[stocks_df['ebit_mean'] > 0]
stocks_df = stocks_df.loc[stocks_df['net_income_mean'] > 0]
stocks_df = stocks_df.loc[stocks_df['operating_income_mean'] > 0]

stocks_df = stocks_df.reset_index(drop=True)

grades_df = stocks_df[['ticker','country','industry','sector']]

for key in evaluation.keys():

    grade = 2 if key in priority else 1

    positive_metric = float(re.findall(r'\d+', evaluation[key]['positive'])[0])
    negative_metric = float(re.findall(r'\d+', evaluation[key]['negative'])[0])

    if '<' in evaluation[key]['positive']:
        for column in [key, key+'_mean']:
            try:
                grades_df.loc[stocks_df[column] < positive_metric, column] = grade
                grades_df.loc[stocks_df[column] > negative_metric, column] = -grade
                grades_df.loc[(stocks_df[column] > positive_metric) & (stocks_df[column] < negative_metric), column] = 0
            except:
                pass

    elif '>' in evaluation[key]['positive']:
        for column in [key, key+'_mean']:
            try:
                grades_df.loc[stocks_df[column] > positive_metric, column] = grade
                grades_df.loc[stocks_df[column] < negative_metric, column] = -grade
                grades_df.loc[(stocks_df[column] < positive_metric) & (stocks_df[column] > negative_metric), column] = 0
            except:
                pass

    try:
        scaler = MinMaxScaler(feature_range=(-0.2,0.2))
        grades_df[key+'_std'] = -1 * scaler.fit_transform(stocks_df[key+'_std'].values.reshape(-1, 1))
        grades_df[key+'_std'] = grades_df[key+'_std'].astype(float)
    except Exception as e:
        pass

stocks_df.to_csv(f'silver/stocks_df_us_{size}.csv', index=False, decimal='.', sep=';')

grades_df['Grade'] = grades_df.iloc[:, 4:].sum(axis=1)
grades_df = grades_df.sort_values(by='Grade', ascending=False).reset_index(drop=True)

grades_df.to_csv(f'silver/grades_df_us_{size}.csv', index=False, decimal='.', sep=';')