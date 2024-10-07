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

def perc_var(array):
    perc_var = []
    for i in range(len(array)-2, -1, -1):
        variation = round((array[i] - array[i+1]) / array[i+1], 4)
        perc_var.append(variation)
    mean = round(np.mean(perc_var), 4)
    std = round(np.std(perc_var), 4)
    return perc_var, mean, std

columns = ['ticker',                    
           'ebitda', 'ebitda_mean', 'ebitda_std',
           'ebit', 'ebit_mean', 'ebit_std',
           'net_income', 'net_income_mean', 'net_income_std',
           'operating_income', 'operating_income_mean', 'operating_income_std',
           'gross_profit', 'gross_profit_mean', 'gross_profit_std',
           'total_revenue', 'total_revenue_mean', 'total_revenue_std',
           'gross_margin', 'gross_margin_mean', 'gross_margin_std',
           'ebitda_margin', 'ebitda_margin_mean', 'ebitda_margin_std',
           'ebit_margin', 'ebit_margin_mean', 'ebit_margin_std',
           'net_margin', 'net_margin_mean', 'net_margin_std',

           'roa', 'roa_mean', 'roa_std',
           'roe', 'roe_mean', 'roe_std',
           'assets_net_worth', 'assets_net_worth_mean', 'assets_net_worth_std',
           'participation_of_third_party_capital', 'participation_of_third_party_capital_mean', 'participation_of_third_party_capital_std',
           'debit_composition', 'debit_composition_mean', 'debit_composition_std',
           'net_debt',
           'net_debt_ebitda', 'net_debt_ebitda_mean', 'net_debt_ebitda_std',
           'general_liquidity', 'general_liquidity_mean', 'general_liquidity_std',
           'current_liquidity', 'current_liquidity_mean', 'current_liquidity_std',
           'dry_liquidity', 'dry_liquidity_mean', 'dry_liquidity_std']

stocks_df_brazil = pd.DataFrame(columns=columns)
stocks_df_usa = pd.DataFrame(columns=columns)

for ticker in tickers_ibov:
    
    stock = yf.Ticker(ticker + '.SA')

    income_statement = stock.income_stmt
    balance_sheet = stock.balance_sheet

    if (not income_statement.empty) and (not balance_sheet.empty) and len(income_statement.columns) >= 4 and len(balance_sheet.columns) >= 4:
        
        # Income Statement ############################################################################################################

        income_statement = income_statement.drop(income_statement.columns[4], axis=1) if len(income_statement.columns) == 5 else income_statement
        income_statement = income_statement.dropna()

        ebitda = income_statement.loc['EBITDA'].values if 'EBITDA' in income_statement.axes[0] else [None, None, None, None]
        ebit = income_statement.loc['EBIT'].values if 'EBIT' in income_statement.axes[0] else [None, None, None, None]
        net_income = income_statement.loc['Net Income'].values if 'Net Income' in income_statement.axes[0] else [None, None, None, None]
        operating_income = income_statement.loc['Operating Income'].values if 'Operating Income' in income_statement.axes[0] else [None, None, None, None]
        gross_profit = income_statement.loc['Gross Profit'].values if 'Gross Profit' in income_statement.axes[0] else [None, None, None, None]
        total_revenue = income_statement.loc['Total Revenue'].values if 'Total Revenue' in income_statement.axes[0] else [None, None, None, None]

        # Income Indicators

        if (not None in total_revenue) and (not 0 in total_revenue):

            if (not None in gross_profit) and (not 0 in gross_profit):
                gross_margin = [round(value, 4) for value in (gross_profit / total_revenue)]
            else:
                gross_margin = [None, None, None, None]

            if (not None in ebitda) and (not 0 in ebitda):
                ebitda_margin = [round(value, 4) for value in (ebitda / total_revenue)]
            else:
                ebitda_margin = [None, None, None, None]

            if (not None in ebit) and (not 0 in ebit):
                ebit_margin = [round(value, 4) for value in (ebit / total_revenue)]
            else:
                ebit_margin = [None, None, None, None]

            if (not None in net_income) and (not 0 in net_income):
                net_margin = [round(value, 4) for value in (net_income / total_revenue)]
            else:
                net_margin = [None, None, None, None]

        else:
            gross_margin = [None, None, None, None]
            ebitda_margin = [None, None, None, None]
            ebit_margin = [None, None, None, None]
            net_margin = [None, None, None, None]

        (ebitda_variation, ebitda_mean, ebitda_std) = (perc_var(ebitda) if (not None in ebitda) and (not 0 in ebitda) else (None, None, None))
        (ebit_variation, ebit_mean, ebit_std) = (perc_var(ebit) if (not None in ebit) and (not 0 in ebit) else (None, None, None))
        (net_income_variation, net_income_mean, net_income_std) = (perc_var(net_income) if (not None in net_income) and (not 0 in net_income) else (None, None, None))
        (operating_income_variation, operating_income_mean, operating_income_std) = (perc_var(operating_income) if (not None in operating_income) and (not 0 in operating_income) else (None, None, None))
        (gross_profit_variation, gross_profit_mean, gross_profit_std) = (perc_var(gross_profit) if (not None in gross_profit) and (not 0 in gross_profit) else (None, None, None))
        (total_revenue_variation, total_revenue_mean, total_revenue_std) = (perc_var(total_revenue) if (not None in total_revenue) and (not 0 in total_revenue) else (None, None, None))

        (gross_margin_variation, gross_margin_mean, gross_margin_std) = (perc_var(gross_margin) if (not None in gross_margin) and (not 0 in gross_margin) else (None, None, None))
        (ebitda_margin_variation, ebitda_margin_mean, ebitda_margin_std) = (perc_var(ebitda_margin) if (not None in ebitda_margin) and (not 0 in ebitda_margin) else (None, None, None))
        (ebit_margin_variation, ebit_margin_mean, ebit_margin_std) = (perc_var(ebit_margin) if (not None in ebit_margin) and (not 0 in ebit_margin) else (None, None, None))
        (net_margin_variation, net_margin_mean, net_margin_std) = (perc_var(net_margin) if (not None in net_margin) and (not 0 in net_margin) else (None, None, None))

        # Balance Sheet ###############################################################################################################

        balance_sheet = balance_sheet.drop(balance_sheet.columns[4], axis=1) if len(balance_sheet.columns) == 5 else balance_sheet
        balance_sheet = balance_sheet.dropna()

        total_assets = balance_sheet.loc['Total Assets'].values if 'Total Debt' in balance_sheet.axes[0] else [None, None, None, None]
        current_assets = balance_sheet.loc['Current Assets'].values if 'Current Assets' in balance_sheet.axes[0] else [None, None, None, None]
        cash_equivalents = balance_sheet.loc['Cash And Cash Equivalents'].values if 'Cash And Cash Equivalents' in balance_sheet.axes[0] else [None, None, None, None]
        non_current_assets = balance_sheet.loc['Total Non Current Assets'].values if 'Total Non Current Assets' in balance_sheet.axes[0] else [None, None, None, None]
        inventory = balance_sheet.loc['Inventory'].values if 'Inventory' in balance_sheet.axes[0] else [None, None, None, None]

        total_debt = balance_sheet.loc['Total Debt'].values if 'Total Debt' in balance_sheet.axes[0] else [None, None, None, None]
        current_debt = balance_sheet.loc['Current Debt'].values if 'Current Debt' in balance_sheet.axes[0] else [None, None, None, None]
        long_term_debt = balance_sheet.loc['Long Term Debt'].values if 'Long Term Debt' in balance_sheet.axes[0] else [None, None, None, None]

        if (not None in total_assets) and (not None in total_debt):
            net_worth = [round(value, 4) for value in (total_assets - total_debt)]
        else:
            net_worth = [None, None, None, None]

        if (not None in total_debt) and (not None in cash_equivalents):
            net_debt = [round(value, 4) for value in (total_debt - cash_equivalents)]
        else:
            net_debt = [None, None, None, None]

        # Return Indicators

        if (not None in net_income) and (not None in total_assets) and (not 0 in total_assets):
            roa = [round(value, 4) for value in (net_income / total_assets)]
        else:
            roa = [None, None, None, None]

        if (not None in net_income) and (not None in net_worth) and (not 0 in net_worth):
            roe = [round(value, 4) for value in (net_income / net_worth)]
        else:
            roe = [None, None, None, None]
        
        if (not None in total_assets) and (not None in net_worth) and (not 0 in net_worth):
            assets_net_worth = [round(value, 4) for value in (total_assets / net_worth)]
        else:
            assets_net_worth = [None, None, None, None]

        # Structure Indicators

        if (not None in current_debt) and (not None in long_term_debt) and (not None in net_worth) and (not 0 in net_worth):
            participation_of_third_party_capital = [round(value, 4) for value in ((current_debt + long_term_debt) / net_worth)]
        else:
            participation_of_third_party_capital = [None, None, None, None]

        if (not None in current_debt) and (not None in long_term_debt) and (not None in (current_debt + long_term_debt)):
            debit_composition = [round(value, 4) for value in (current_debt / (current_debt + long_term_debt))]
        else:
            debit_composition = [None, None, None, None]

        if (not None in net_debt) and (not None in ebitda) and (not 0 in ebitda):
            net_debt_ebitda = [round(value, 4) for value in (net_debt / ebitda)]
        else:
            net_debt_ebitda = [None, None, None, None]

        # Liquidity Indicators

        if (not None in current_assets) and (not None in non_current_assets) and (not None in current_debt) and (not None in long_term_debt) and (not None in (current_debt + long_term_debt)):
            general_liquidity = [round(value, 4) for value in ((current_assets + non_current_assets) / (current_debt + long_term_debt))]
        else:
            general_liquidity = [None, None, None, None]

        if (not None in current_assets) and (not None in current_debt) and (not 0 in current_debt):
            current_liquidity = [round(value, 4) for value in (current_assets / current_debt)]
        else:
            current_liquidity = [None, None, None, None]
        
        if (not None in current_assets) and (not None in inventory) and (not None in current_debt) and (not 0 in current_debt):
            dry_liquidity = [round(value, 4) for value in ((current_assets - inventory) / current_debt)]
        else:
            dry_liquidity = [None, None, None, None]

        (roa_variation, roa_mean, roa_std) = (perc_var(roa) if (not None in roa) and (not 0 in roa) else (None, None, None))
        (roe_variation, roe_mean, roe_std) = (perc_var(roe) if (not None in roe) and (not 0 in roe) else (None, None, None))
        (assets_net_worth_variation, assets_net_worth_mean, assets_net_worth_std) = (perc_var(assets_net_worth) if (not None in assets_net_worth) and (not 0 in assets_net_worth) else (None, None, None))

        (participation_of_third_party_capital_variation, participation_of_third_party_capital_mean, participation_of_third_party_capital_std) = (perc_var(participation_of_third_party_capital) if (not None in participation_of_third_party_capital) and (not 0 in participation_of_third_party_capital) else (None, None, None))
        (debit_composition_variation, debit_composition_mean, debit_composition_std) = (perc_var(debit_composition) if (not None in debit_composition) and (not 0 in debit_composition) else (None, None, None))
        (net_debt_ebitda_variation, net_debt_ebitda_mean, net_debt_ebitda_std) = (perc_var(net_debt_ebitda) if (not None in net_debt_ebitda) and (not 0 in net_debt_ebitda) else (None, None, None))

        (general_liquidity_variation, general_liquidity_mean, general_liquidity_std) = (perc_var(general_liquidity) if (not None in general_liquidity) and (not 0 in general_liquidity) else (None, None, None))
        (current_liquidity_variation, current_liquidity_mean, current_liquidity_std) = (perc_var(current_liquidity) if (not None in current_liquidity) and (not 0 in current_liquidity) else (None, None, None))
        (dry_liquidity_variation, dry_liquidity_mean, dry_liquidity_std) = (perc_var(dry_liquidity) if (not None in dry_liquidity) and (not 0 in dry_liquidity) else (None, None, None))

        new_line = pd.DataFrame([[ticker,
                                
                                ebitda, ebitda_mean, ebitda_std,
                                ebit, ebit_mean, ebit_std,
                                net_income, net_income_mean, net_income_std,
                                operating_income, operating_income_mean, operating_income_std,
                                gross_profit, gross_profit_mean, gross_profit_std,
                                total_revenue, total_revenue_mean, total_revenue_std,
                                gross_margin, gross_margin_mean, gross_margin_std,
                                ebitda_margin, ebitda_margin_mean, ebitda_margin_std,
                                ebit_margin, ebit_margin_mean, ebit_margin_std,
                                net_margin, net_margin_mean, net_margin_std,

                                roa, roa_mean, roa_std,
                                roe, roe_mean, roe_std,
                                assets_net_worth, assets_net_worth_mean, assets_net_worth_std,
                                participation_of_third_party_capital, participation_of_third_party_capital_mean, participation_of_third_party_capital_std,
                                debit_composition, debit_composition_mean, debit_composition_std,
                                net_debt,
                                net_debt_ebitda, net_debt_ebitda_mean, net_debt_ebitda_std,
                                general_liquidity, general_liquidity_mean, general_liquidity_std,
                                current_liquidity, current_liquidity_mean, current_liquidity_std,
                                dry_liquidity, dry_liquidity_mean, dry_liquidity_std
                                
                                ]], columns=columns)

        stocks_df_brazil = pd.concat([stocks_df_brazil, new_line], ignore_index=True)

for ticker in tickers_SP:

    stock = yf.Ticker(ticker)

    income_statement = stock.income_stmt
    balance_sheet = stock.balance_sheet

    if (not income_statement.empty) and (not balance_sheet.empty) and len(income_statement.columns) >= 4 and len(balance_sheet.columns) >= 4:
        
        # Income Statement ############################################################################################################

        income_statement = income_statement.drop(income_statement.columns[4], axis=1) if len(income_statement.columns) == 5 else income_statement
        income_statement = income_statement.dropna()

        ebitda = income_statement.loc['EBITDA'].values if 'EBITDA' in income_statement.axes[0] else [None, None, None, None]
        ebit = income_statement.loc['EBIT'].values if 'EBIT' in income_statement.axes[0] else [None, None, None, None]
        net_income = income_statement.loc['Net Income'].values if 'Net Income' in income_statement.axes[0] else [None, None, None, None]
        operating_income = income_statement.loc['Operating Income'].values if 'Operating Income' in income_statement.axes[0] else [None, None, None, None]
        gross_profit = income_statement.loc['Gross Profit'].values if 'Gross Profit' in income_statement.axes[0] else [None, None, None, None]
        total_revenue = income_statement.loc['Total Revenue'].values if 'Total Revenue' in income_statement.axes[0] else [None, None, None, None]

        # Income Indicators

        if (not None in total_revenue) and (not 0 in total_revenue):

            if (not None in gross_profit) and (not 0 in gross_profit):
                gross_margin = [round(value, 4) for value in (gross_profit / total_revenue)]
            else:
                gross_margin = [None, None, None, None]

            if (not None in ebitda) and (not 0 in ebitda):
                ebitda_margin = [round(value, 4) for value in (ebitda / total_revenue)]
            else:
                ebitda_margin = [None, None, None, None]

            if (not None in ebit) and (not 0 in ebit):
                ebit_margin = [round(value, 4) for value in (ebit / total_revenue)]
            else:
                ebit_margin = [None, None, None, None]

            if (not None in net_income) and (not 0 in net_income):
                net_margin = [round(value, 4) for value in (net_income / total_revenue)]
            else:
                net_margin = [None, None, None, None]

        else:
            gross_margin = [None, None, None, None]
            ebitda_margin = [None, None, None, None]
            ebit_margin = [None, None, None, None]
            net_margin = [None, None, None, None]

        (ebitda_variation, ebitda_mean, ebitda_std) = (perc_var(ebitda) if (not None in ebitda) and (not 0 in ebitda) else (None, None, None))
        (ebit_variation, ebit_mean, ebit_std) = (perc_var(ebit) if (not None in ebit) and (not 0 in ebit) else (None, None, None))
        (net_income_variation, net_income_mean, net_income_std) = (perc_var(net_income) if (not None in net_income) and (not 0 in net_income) else (None, None, None))
        (operating_income_variation, operating_income_mean, operating_income_std) = (perc_var(operating_income) if (not None in operating_income) and (not 0 in operating_income) else (None, None, None))
        (gross_profit_variation, gross_profit_mean, gross_profit_std) = (perc_var(gross_profit) if (not None in gross_profit) and (not 0 in gross_profit) else (None, None, None))
        (total_revenue_variation, total_revenue_mean, total_revenue_std) = (perc_var(total_revenue) if (not None in total_revenue) and (not 0 in total_revenue) else (None, None, None))

        (gross_margin_variation, gross_margin_mean, gross_margin_std) = (perc_var(gross_margin) if (not None in gross_margin) and (not 0 in gross_margin) else (None, None, None))
        (ebitda_margin_variation, ebitda_margin_mean, ebitda_margin_std) = (perc_var(ebitda_margin) if (not None in ebitda_margin) and (not 0 in ebitda_margin) else (None, None, None))
        (ebit_margin_variation, ebit_margin_mean, ebit_margin_std) = (perc_var(ebit_margin) if (not None in ebit_margin) and (not 0 in ebit_margin) else (None, None, None))
        (net_margin_variation, net_margin_mean, net_margin_std) = (perc_var(net_margin) if (not None in net_margin) and (not 0 in net_margin) else (None, None, None))

        # Balance Sheet ###############################################################################################################

        balance_sheet = balance_sheet.drop(balance_sheet.columns[4], axis=1) if len(balance_sheet.columns) == 5 else balance_sheet
        balance_sheet = balance_sheet.dropna()

        total_assets = balance_sheet.loc['Total Assets'].values if 'Total Debt' in balance_sheet.axes[0] else [None, None, None, None]
        current_assets = balance_sheet.loc['Current Assets'].values if 'Current Assets' in balance_sheet.axes[0] else [None, None, None, None]
        cash_equivalents = balance_sheet.loc['Cash And Cash Equivalents'].values if 'Cash And Cash Equivalents' in balance_sheet.axes[0] else [None, None, None, None]
        non_current_assets = balance_sheet.loc['Total Non Current Assets'].values if 'Total Non Current Assets' in balance_sheet.axes[0] else [None, None, None, None]
        inventory = balance_sheet.loc['Inventory'].values if 'Inventory' in balance_sheet.axes[0] else [None, None, None, None]

        total_debt = balance_sheet.loc['Total Debt'].values if 'Total Debt' in balance_sheet.axes[0] else [None, None, None, None]
        current_debt = balance_sheet.loc['Current Debt'].values if 'Current Debt' in balance_sheet.axes[0] else [None, None, None, None]
        long_term_debt = balance_sheet.loc['Long Term Debt'].values if 'Long Term Debt' in balance_sheet.axes[0] else [None, None, None, None]

        if (not None in total_assets) and (not None in total_debt):
            net_worth = [round(value, 4) for value in (total_assets - total_debt)]
        else:
            net_worth = [None, None, None, None]

        if (not None in total_debt) and (not None in cash_equivalents):
            net_debt = [round(value, 4) for value in (total_debt - cash_equivalents)]
        else:
            net_debt = [None, None, None, None]

        # Return Indicators

        if (not None in net_income) and (not None in total_assets) and (not 0 in total_assets):
            roa = [round(value, 4) for value in (net_income / total_assets)]
        else:
            roa = [None, None, None, None]

        if (not None in net_income) and (not None in net_worth) and (not 0 in net_worth):
            roe = [round(value, 4) for value in (net_income / net_worth)]
        else:
            roe = [None, None, None, None]
        
        if (not None in total_assets) and (not None in net_worth) and (not 0 in net_worth):
            assets_net_worth = [round(value, 4) for value in (total_assets / net_worth)]
        else:
            assets_net_worth = [None, None, None, None]

        # Structure Indicators

        if (not None in current_debt) and (not None in long_term_debt) and (not None in net_worth) and (not 0 in net_worth):
            participation_of_third_party_capital = [round(value, 4) for value in ((current_debt + long_term_debt) / net_worth)]
        else:
            participation_of_third_party_capital = [None, None, None, None]

        if (not None in current_debt) and (not None in long_term_debt) and (not None in (current_debt + long_term_debt)):
            debit_composition = [round(value, 4) for value in (current_debt / (current_debt + long_term_debt))]
        else:
            debit_composition = [None, None, None, None]

        if (not None in net_debt) and (not None in ebitda) and (not 0 in ebitda):
            net_debt_ebitda = [round(value, 4) for value in (net_debt / ebitda)]
        else:
            net_debt_ebitda = [None, None, None, None]

        # Liquidity Indicators

        if (not None in current_assets) and (not None in non_current_assets) and (not None in current_debt) and (not None in long_term_debt) and (not None in (current_debt + long_term_debt)):
            general_liquidity = [round(value, 4) for value in ((current_assets + non_current_assets) / (current_debt + long_term_debt))]
        else:
            general_liquidity = [None, None, None, None]

        if (not None in current_assets) and (not None in current_debt) and (not 0 in current_debt):
            current_liquidity = [round(value, 4) for value in (current_assets / current_debt)]
        else:
            current_liquidity = [None, None, None, None]
        
        if (not None in current_assets) and (not None in inventory) and (not None in current_debt) and (not 0 in current_debt):
            dry_liquidity = [round(value, 4) for value in ((current_assets - inventory) / current_debt)]
        else:
            dry_liquidity = [None, None, None, None]

        (roa_variation, roa_mean, roa_std) = (perc_var(roa) if (not None in roa) and (not 0 in roa) else (None, None, None))
        (roe_variation, roe_mean, roe_std) = (perc_var(roe) if (not None in roe) and (not 0 in roe) else (None, None, None))
        (assets_net_worth_variation, assets_net_worth_mean, assets_net_worth_std) = (perc_var(assets_net_worth) if (not None in assets_net_worth) and (not 0 in assets_net_worth) else (None, None, None))

        (participation_of_third_party_capital_variation, participation_of_third_party_capital_mean, participation_of_third_party_capital_std) = (perc_var(participation_of_third_party_capital) if (not None in participation_of_third_party_capital) and (not 0 in participation_of_third_party_capital) else (None, None, None))
        (debit_composition_variation, debit_composition_mean, debit_composition_std) = (perc_var(debit_composition) if (not None in debit_composition) and (not 0 in debit_composition) else (None, None, None))
        (net_debt_ebitda_variation, net_debt_ebitda_mean, net_debt_ebitda_std) = (perc_var(net_debt_ebitda) if (not None in net_debt_ebitda) and (not 0 in net_debt_ebitda) else (None, None, None))

        (general_liquidity_variation, general_liquidity_mean, general_liquidity_std) = (perc_var(general_liquidity) if (not None in general_liquidity) and (not 0 in general_liquidity) else (None, None, None))
        (current_liquidity_variation, current_liquidity_mean, current_liquidity_std) = (perc_var(current_liquidity) if (not None in current_liquidity) and (not 0 in current_liquidity) else (None, None, None))
        (dry_liquidity_variation, dry_liquidity_mean, dry_liquidity_std) = (perc_var(dry_liquidity) if (not None in dry_liquidity) and (not 0 in dry_liquidity) else (None, None, None))

        new_line = pd.DataFrame([[ticker,
                                
                                ebitda, ebitda_mean, ebitda_std,
                                ebit, ebit_mean, ebit_std,
                                net_income, net_income_mean, net_income_std,
                                operating_income, operating_income_mean, operating_income_std,
                                gross_profit, gross_profit_mean, gross_profit_std,
                                total_revenue, total_revenue_mean, total_revenue_std,
                                gross_margin, gross_margin_mean, gross_margin_std,
                                ebitda_margin, ebitda_margin_mean, ebitda_margin_std,
                                ebit_margin, ebit_margin_mean, ebit_margin_std,
                                net_margin, net_margin_mean, net_margin_std,

                                roa, roa_mean, roa_std,
                                roe, roe_mean, roe_std,
                                assets_net_worth, assets_net_worth_mean, assets_net_worth_std,
                                participation_of_third_party_capital, participation_of_third_party_capital_mean, participation_of_third_party_capital_std,
                                debit_composition, debit_composition_mean, debit_composition_std,
                                net_debt,
                                net_debt_ebitda, net_debt_ebitda_mean, net_debt_ebitda_std,
                                general_liquidity, general_liquidity_mean, general_liquidity_std,
                                current_liquidity, current_liquidity_mean, current_liquidity_std,
                                dry_liquidity, dry_liquidity_mean, dry_liquidity_std
                                
                                ]], columns=columns)

        stocks_df_brazil = pd.concat([stocks_df_brazil, new_line], ignore_index=True)

stocks_df_brazil.to_csv('stocks_df_brazil.csv', index=False)
stocks_df_usa.to_csv('stocks_df_usa.csv', index=False)