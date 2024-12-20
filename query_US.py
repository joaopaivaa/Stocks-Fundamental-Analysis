from info_collect import stocks_df_usa

stocks_df = stocks_df_usa

stocks_df = stocks_df[stocks_df.EBITDA > 0][stocks_df.EBITDA_mean > 0.1]
stocks_df = stocks_df[stocks_df.Net_Income > 0][stocks_df.Net_Income_mean > 0.1]
stocks_df = stocks_df[stocks_df.Total_Revenue > 0][stocks_df.Total_Revenue_mean > 0.1]
stocks_df = stocks_df[stocks_df.gross_margin > 0.4][stocks_df.gross_margin_mean > 0.1]
stocks_df = stocks_df[stocks_df.net_margin > 0.2][stocks_df.net_margin_mean > 0.05]
stocks_df = stocks_df[stocks_df.net_debin_EBITDA < 2]
stocks_df = stocks_df[stocks_df.Total_Debt_mean < 0]
stocks_df = stocks_df[stocks_df.ROA > 0.1][stocks_df.Net_Income_mean > 0.1]

pass