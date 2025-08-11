import requests
import pandas as pd
import numpy as np

url = "https://api.nasdaq.com/api/screener/stocks?tableonly=false&limit=25&download=true"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "origin": "https://www.nasdaq.com",
    "referer": "https://www.nasdaq.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    stocks_df_us = pd.DataFrame(data['data']['rows'])
    stocks_df_us = stocks_df_us[~stocks_df_us['symbol'].str.contains(r'[\/^]', regex=True, na=False)]
    stocks_df_us['marketCap'] = stocks_df_us['marketCap'].replace('','0').astype(float)
    stocks_df_us = stocks_df_us[stocks_df_us['marketCap'] > 0]
    stocks_df_us['marketCap (Bi)'] = stocks_df_us['marketCap'].replace('','0').astype(float) / 1000000000
    stocks_df_us['marketCap category'] = np.where(stocks_df_us['marketCap (Bi)'] > 200, 'Mega',
                                         np.where(stocks_df_us['marketCap (Bi)'] > 10, 'Large',
                                         np.where(stocks_df_us['marketCap (Bi)'] > 2, 'Medium',
                                         np.where(stocks_df_us['marketCap (Bi)'] > 0.3, 'Small',
                                         np.where(stocks_df_us['marketCap (Bi)'] > 0.05, 'Micro', 'Nano')))))
    stocks_df_us.reset_index(drop=True, inplace=True)

    for size in ['Mega', 'Large', 'Medium', 'Small', 'Micro', 'Nano']:
        stocks_df_us_size = stocks_df_us[stocks_df_us['marketCap category'] == size]
        stocks_df_us_size.reset_index(drop=True, inplace=True)
        us_stocks_list_size = pd.DataFrame(stocks_df_us_size['symbol'].values, columns=['ticker'])
        us_stocks_list_size.to_csv(f'stocks list/us_stocks_list_{size}.csv', index=False, sep=';')
        
else:
    print(f"Erro ao acessar API: {response.status_code}")
