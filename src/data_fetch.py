import yfinance as yf
import pandas as pd
import logging
import urllib.request
import os

logger = logging.getLogger(__name__)

# 데이터 저장 폴더 설정
data_folder = "data"

# NYSE & NASDAQ CSV 파일 다운로드 링크
nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
nyse_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"

# 저장할 파일 경로
nasdaq_file = os.path.join(data_folder, "nasdaq_listed.csv")
nyse_file = os.path.join(data_folder, "nyse_listed.csv")
all_tickers_file = os.path.join(data_folder, "all_us_stocks.csv")

def download_ftp_file(ftp_url, save_path):
    """FTP에서 파일을 다운로드하여 저장"""
    try:
        urllib.request.urlretrieve(ftp_url, save_path)
        print(f"✅ 다운로드 완료: {save_path}")
    except Exception as e:
        print(f"❌ 다운로드 실패: {ftp_url} (오류: {e})")


def fetch_all_tickers():
    """NASDAQ & NYSE 최신 주식 리스트 다운로드 후 통합"""

    # 기존 파일이 존재하면 API 호출 없이 로드
    if os.path.exists(all_tickers_file):
        df_tickers = pd.read_csv(all_tickers_file)
        tickers = df_tickers["Ticker"].tolist()
        print(f"캐시된 데이터 사용: {len(tickers)}개의 미국 주식 종목 로드됨.")
        return tickers

    # NASDAQ & NYSE 주식 리스트 다운로드
    download_ftp_file(nasdaq_url, nasdaq_file)
    download_ftp_file(nyse_url, nyse_file)

    # NASDAQ 데이터 불러오기
    nasdaq_df = pd.read_csv(nasdaq_file, sep="|")
    nyse_df = pd.read_csv(nyse_file, sep="|")

    # ✅ NASDAQ 주식 리스트 필터링 (ETF 제외)
    if "Symbol" in nasdaq_df.columns and "ETF" in nasdaq_df.columns:
        nasdaq_df = nasdaq_df[nasdaq_df["ETF"] == "N"]  # ETF가 아닌 종목만 선택
        nasdaq_tickers = nasdaq_df["Symbol"].tolist()
    else:
        nasdaq_tickers = []

    # ✅ NYSE 주식 리스트 필터링 (ETF 제외)
    if "ACT Symbol" in nyse_df.columns and "ETF" in nyse_df.columns:
        nyse_df = nyse_df[nyse_df["ETF"] == "N"]  # ETF가 아닌 종목만 선택
        nyse_tickers = nyse_df["ACT Symbol"].tolist()
    else:
        nyse_tickers = []

    # ✅ 최종 티커 리스트 생성 (중복 제거)
    all_tickers = list(set(nasdaq_tickers + nyse_tickers))

    # ✅ 데이터 저장
    df_tickers = pd.DataFrame({"Ticker": all_tickers})
    df_tickers.to_csv(all_tickers_file, index=False)

    print(f"✅ 총 {len(all_tickers)}개의 미국 주식 종목이 저장되었습니다!")
    return all_tickers


def get_stock_data(ticker):
    """주어진 티커의 재무 데이터를 가져오는 함수"""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Ticker": ticker,
        "Market Cap": info.get("marketCap", None),
        "ROIC": info.get("returnOnEquity", None),
        "Debt/Equity": info.get("debtToEquity", None),
        "PER": info.get("trailingPE", None),
        "PSR": info.get("priceToSalesTrailing12Months", None),
        "Revenue Growth YoY": info.get("revenueGrowth", None),
        "Net Income Growth YoY": info.get("netIncomeToCommon", None),
    }

def fetch_all_data(ticker_list):
    """티커 리스트에 대해 데이터를 수집하는 함수"""
    return pd.DataFrame([get_stock_data(ticker) for ticker in ticker_list])
