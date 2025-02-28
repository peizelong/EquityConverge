import akshare as ak

stock_hot_follow_xq_df = ak.stock_hot_follow_xq(symbol="最热门")
stock_hot_follow_xq_df.to_csv("a.cvs")