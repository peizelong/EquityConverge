import akshare as ak

stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date="20250303")
stock_hot_rank_wc_df.to_csv('a.csv')