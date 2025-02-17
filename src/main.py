import logging
import os

from data_fetch import fetch_all_tickers
from filter import filter_stocks
from logging_setup import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

# 데이터 폴더 및 파일 경로 설정
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# 파일 경로 설정
all_stocks_file = os.path.join(data_folder, "all_us_stocks.csv")
filtered_stocks_file = os.path.join(data_folder, "filtered_stocks.csv")

# ✅ 미국 주식 리스트 가져오기
all_tickers = fetch_all_tickers()
logger.info(f"가져온 종목 수: {len(all_tickers)}")

# ✅ 필터링 실행
filter_stocks(all_stocks_file, filtered_stocks_file)

print(f"🎉 최종 필터링 완료! 필터링된 종목 파일: {filtered_stocks_file}")
