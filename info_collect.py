import pandas as pd
import yfinance as yf
import numpy as np
import math

table_SP = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df_SP = table_SP[0]
tickers_SP = df_SP.Symbol.to_list()

table_ibov = pd.read_html('https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3')
df_ibov = table_ibov[0]
df_ibov.columns = df_ibov.iloc[0]
df_ibov = df_ibov[1:].reset_index(drop=True)
tickers_ibov = df_ibov.Código.to_list()

def perc_var(values):
    perc_var = []
    for i in range(len(values)-2, -1, -1):
        variation = round((values[i]-values[i+1])/values[i+1],4)
        perc_var.append(variation)
    mean = np.mean(perc_var)
    std = np.std(perc_var)
    return perc_var, mean, std

def ratio(array1, array2):
    ratio_list = []
    for i in range(len(array1)):
        ratio_list.append(round(array1[i]/array2[i],4))
    return ratio_list

def diff(array1, array2):
    diff_list = []
    for i in range(len(array1)):
        diff_list.append(round(array1[i]-array2[i],4))
    return diff_list

columns = ['Ticker',
           'EBITDA', 'EBITDA_mean', 'EBITDA_std',
           'EBITDA_margin', 'EBITDA_margin_mean', 'EBITDA_margin_std',
           'Net_Income', 'Net_Income_mean', 'Net_Income_std',
           'Operating_Income', 'Operating_Income_mean', 'Operating_Income_std',
           'Gross_Profit', 'Gross_Profit_mean', 'Gross_Profit_std',
           'Cost_Revenue', 'Cost_Revenue_mean', 'Cost_Revenue_std',
           'Total_Revenue', 'Total_Revenue_mean', 'Total_Revenue_std',
           'gross_margin', 'gross_margin_mean', 'gross_margin_std',
           'net_margin', 'net_margin_mean', 'net_margin_std',
           'Cash', 'Cash_mean', 'Cash_std',
           'Net_Debt', 'Net_Debt_mean', 'Net_Debt_std',
           'Total_Assets', 'Total_Assets_mean', 'Total_Assets_std',
           'Total_Debt', 'Total_Debt_mean', 'Total_Debt_std',
           'net_debt_EBITDA', 'net_debt_EBITDA_mean', 'net_debt_EBITDA_std',
           'ROA', 'ROA_mean', 'ROA_std']

stocks_df = pd.DataFrame(columns=columns)

for ticker in tickers_ibov:
    try:
        stock = yf.Ticker(ticker + '.SA')

        # Income Statement ############################################################################################################

        income_statement = stock.income_stmt

        income_statement = income_statement.drop(income_statement.columns[4], axis=1)
        income_statement.dropna()

        EBITDA = [x for x in income_statement.loc['EBITDA'].values if not math.isnan(x)]
        Net_Income = [x for x in income_statement.loc['Net Income'].values if not math.isnan(x)]
        Operating_Income = [x for x in income_statement.loc['Operating Income'].values if not math.isnan(x)]
        Gross_Profit = [x for x in income_statement.loc['Gross Profit'].values if not math.isnan(x)]
        Cost_Revenue = [x for x in income_statement.loc['Cost Of Revenue'].values if not math.isnan(x)]
        Total_Revenue = [x for x in income_statement.loc['Total Revenue'].values if not math.isnan(x)]

        gross_margin = ratio(Gross_Profit, Total_Revenue)
        EBITDA_margin = ratio(EBITDA, Total_Revenue)
        net_margin = ratio(Net_Income, Total_Revenue)

        EBITDA_variation, EBITDA_mean, EBITDA_std = perc_var(EBITDA)
        Net_Income_variation, Net_Income_mean, Net_Income_std = perc_var(Net_Income)
        Operating_Income_variation, Operating_Income_mean, Operating_Income_std = perc_var(Operating_Income)
        Gross_Profit_variation, Gross_Profit_mean, Gross_Profit_std = perc_var(Gross_Profit)
        Cost_Revenue_variation, Cost_Revenue_mean, Cost_Revenue_std = perc_var(Cost_Revenue)
        Total_Revenue_variation, Total_Revenue_mean, Total_Revenue_std = perc_var(Total_Revenue)

        EBITDA_margin_variation, EBITDA_margin_mean, EBITDA_margin_std = perc_var(EBITDA_margin)
        gross_margin_variation, gross_margin_mean, gross_margin_std = perc_var(gross_margin)
        net_margin_variation, net_margin_mean, net_margin_std = perc_var(net_margin)

        # Balance Sheet ###############################################################################################################

        balance_sheet = stock.balance_sheet

        Cash = [x for x in balance_sheet.loc['Cash And Cash Equivalents'].values if not math.isnan(x)]
        Total_Assets = [x for x in balance_sheet.loc['Total Assets'].values if not math.isnan(x)]
        Total_Debt = [x for x in balance_sheet.loc['Total Debt'].values if not math.isnan(x)]

        Net_Debt = diff(Total_Debt,Cash)

        net_debt_EBITDA = ratio(Net_Debt, EBITDA)
        ROA = ratio(Total_Assets, Total_Revenue)

        Cash_variation, Cash_mean, Cash_std = perc_var(Cash)
        Net_Debt_variation, Net_Debt_mean, Net_Debt_std = perc_var(Net_Debt)
        Total_Assets_variation, Total_Assets_mean, Total_Assets_std = perc_var(Total_Assets)
        Total_Debt_variation, Total_Debt_mean, Total_Debt_std = perc_var(Total_Debt)

        net_debt_EBITDA_variation, net_debt_EBITDA_mean, net_debt_EBITDA_std = perc_var(net_debt_EBITDA)
        ROA_variation, ROA_mean, ROA_std = perc_var(ROA)

        new_line = pd.DataFrame([[ticker,
                                  EBITDA, EBITDA_mean, EBITDA_std,
                                  EBITDA_margin, EBITDA_margin_mean, EBITDA_margin_std,
                                  Net_Income, Net_Income_mean, Net_Income_std,
                                  Operating_Income, Operating_Income_mean, Operating_Income_std,
                                  Gross_Profit, Gross_Profit_mean, Gross_Profit_std,
                                  Cost_Revenue, Cost_Revenue_mean, Cost_Revenue_std,
                                  Total_Revenue, Total_Revenue_mean, Total_Revenue_std,
                                  gross_margin, gross_margin_mean, gross_margin_std,
                                  net_margin, net_margin_mean, net_margin_std,
                                  Cash, Cash_mean, Cash_std,
                                  Net_Debt, Net_Debt_mean, Net_Debt_std,
                                  Total_Assets, Total_Assets_mean, Total_Assets_std,
                                  Total_Debt, Total_Debt_mean, Total_Debt_std,
                                  net_debt_EBITDA, net_debt_EBITDA_mean, net_debt_EBITDA_std,
                                  ROA, ROA_mean, ROA_std]], columns=columns)

        stocks_df = pd.concat([stocks_df, new_line], ignore_index=True)
    
    except:

        continue

for ticker in tickers_SP:
    try:
        stock = yf.Ticker(ticker)

        # Income Statement ############################################################################################################

        income_statement = stock.income_stmt

        EBITDA = [x for x in income_statement.loc['EBITDA'].values if not math.isnan(x)]
        Net_Income = [x for x in income_statement.loc['Net Income'].values if not math.isnan(x)]
        Operating_Income = [x for x in income_statement.loc['Operating Income'].values if not math.isnan(x)]
        Gross_Profit = [x for x in income_statement.loc['Gross Profit'].values if not math.isnan(x)]
        Cost_Revenue = [x for x in income_statement.loc['Cost Of Revenue'].values if not math.isnan(x)]
        Total_Revenue = [x for x in income_statement.loc['Total Revenue'].values if not math.isnan(x)]

        gross_margin = ratio(Gross_Profit, Total_Revenue)
        EBITDA_margin = ratio(EBITDA, Total_Revenue)
        net_margin = ratio(Net_Income, Total_Revenue)

        EBITDA_variation, EBITDA_mean, EBITDA_std = perc_var(EBITDA)
        Net_Income_variation, Net_Income_mean, Net_Income_std = perc_var(Net_Income)
        Operating_Income_variation, Operating_Income_mean, Operating_Income_std = perc_var(Operating_Income)
        Gross_Profit_variation, Gross_Profit_mean, Gross_Profit_std = perc_var(Gross_Profit)
        Cost_Revenue_variation, Cost_Revenue_mean, Cost_Revenue_std = perc_var(Cost_Revenue)
        Total_Revenue_variation, Total_Revenue_mean, Total_Revenue_std = perc_var(Total_Revenue)

        EBITDA_margin_variation, EBITDA_margin_mean, EBITDA_margin_std = perc_var(EBITDA_margin)
        gross_margin_variation, gross_margin_mean, gross_margin_std = perc_var(gross_margin)
        net_margin_variation, net_margin_mean, net_margin_std = perc_var(net_margin)

        # Balance Sheet ###############################################################################################################

        balance_sheet = stock.balance_sheet

        Cash = [x for x in balance_sheet.loc['Cash And Cash Equivalents'].values if not math.isnan(x)]
        Total_Assets = [x for x in balance_sheet.loc['Total Assets'].values if not math.isnan(x)]
        Total_Debt = [x for x in balance_sheet.loc['Total Debt'].values if not math.isnan(x)]

        Net_Debt = diff(Total_Debt,Cash)

        net_debin_EBITDA = ratio(Net_Debt, EBITDA)
        ROA = ratio(Total_Assets, Total_Revenue)

        Cash_variation, Cash_mean, Cash_std = perc_var(Cash)
        Net_Debt_variation, Net_Debt_mean, Net_Debt_std = perc_var(Net_Debt)
        Total_Assets_variation, Total_Assets_mean, Total_Assets_std = perc_var(Total_Assets)
        Total_Debt_variation, Total_Debt_mean, Total_Debt_std = perc_var(Total_Debt)

        net_debt_EBITDA_variation, net_debt_EBITDA_mean, net_debt_EBITDA_std = perc_var(net_debin_EBITDA)
        ROA_variation, ROA_mean, ROA_std = perc_var(ROA)

        new_line = pd.DataFrame([[ticker,
                                  EBITDA, EBITDA_mean, EBITDA_std,
                                  EBITDA_margin, EBITDA_margin_mean, EBITDA_margin_std,
                                  Net_Income, Net_Income_mean, Net_Income_std,
                                  Operating_Income, Operating_Income_mean, Operating_Income_std,
                                  Gross_Profit, Gross_Profit_mean, Gross_Profit_std,
                                  Cost_Revenue, Cost_Revenue_mean, Cost_Revenue_std,
                                  Total_Revenue, Total_Revenue_mean, Total_Revenue_std,
                                  gross_margin, gross_margin_mean, gross_margin_std,
                                  net_margin, net_margin_mean, net_margin_std,
                                  Cash, Cash_mean, Cash_std,
                                  Net_Debt, Net_Debt_mean, Net_Debt_std,
                                  Total_Assets, Total_Assets_mean, Total_Assets_std,
                                  Total_Debt, Total_Debt_mean, Total_Debt_std,
                                  net_debt_EBITDA, net_debt_EBITDA_mean, net_debt_EBITDA_std,
                                  ROA, ROA_mean, ROA_std]], columns=columns)


        stocks_df = pd.concat([stocks_df, new_line], ignore_index=True)
    
    except:

        continue

stocks_df.to_csv('stocks_df.csv', index=False)