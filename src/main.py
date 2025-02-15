from data_fetch import fetch_all_data
from filter import filter_stocks
from logging_setup import setup_logging
import logging
import sys
import os

# 현재 경로를 기준으로 src 폴더를 모듈 검색 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_fetch import fetch_all_tickers


logger = logging.getLogger(__name__)
setup_logging()

# 미국 주식 전체 리스트 가져오기
all_tickers = fetch_all_tickers()
logger.info(f"가져온 종목 수: {len(all_tickers)}")

sp500_tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG"]  # 임시 샘플

# 데이터 수집
stock_df = fetch_all_data(sp500_tickers)

# 필터링
filtered_df = filter_stocks(stock_df)

# CSV 파일로 저장
filtered_df.to_csv("data/filtered_stocks.csv", index=False)
logger.info("Filtered stock list saved to data/filtered_stocks.csv")


