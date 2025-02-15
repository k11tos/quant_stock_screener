from data_fetch import fetch_all_data
from filter import filter_stocks

# 대상 종목 리스트 (S&P 500 대신 실제 전체 시장 리스트로 확장 가능)
sp500_tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG"]  # 임시 샘플

# 데이터 수집
stock_df = fetch_all_data(sp500_tickers)

# 필터링
filtered_df = filter_stocks(stock_df)

# CSV 파일로 저장
filtered_df.to_csv("data/filtered_stocks.csv", index=False)
print("Filtered stock list saved to data/filtered_stocks.csv")
