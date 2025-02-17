import logging
import os
import time

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


# 데이터 폴더 설정
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)


def is_valid_ticker(ticker):
    """yfinance에서 조회 가능한 티커인지 확인"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        time.sleep(0.5)  # ✅ 0.5초 딜레이 추가 (요청 속도 제한 방지)
        return not hist.empty  # 데이터가 비어있지 않으면 유효
    except Exception:
        return False


def get_stock_info(ticker):
    """yfinance에서 기업 정보를 가져와 필터링"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        time.sleep(0.5)  # ✅ 0.5초 딜레이 추가 (연속 호출 방지)

        return {
            "Ticker": ticker,
            "Sector": info.get("sector", "Unknown"),
            "Industry": info.get("industry", "Unknown"),
            "MarketPrice": info.get("currentPrice", None),
            "NetIncomeAnnual": info.get("netIncomeToCommon", 1),
            "NetIncomeQuarter": info.get("earningsQuarterlyGrowth", 1),
            "QuoteType": info.get("quoteType", "UNKNOWN"),
        }
    except Exception as e:
        print(f"❌ {ticker} 데이터 조회 실패: {e}")
        return None


def filter_stocks(input_file, output_file):
    """미국 주식 리스트 필터링 (금융주, 지주사, 관리종목, 적자기업, PTP 제외)"""
    # 기존 주식 리스트 로드
    df_stocks = pd.read_csv(input_file)

    # ✅ 유효한 티커만 선택 (404 오류 방지)
    valid_tickers = [ticker for ticker in df_stocks["Ticker"] if is_valid_ticker(ticker)]
    df_valid = pd.DataFrame({"Ticker": valid_tickers})
    df_valid.to_csv(os.path.join(data_folder, "valid_tickers.csv"), index=False)

    print(f"✅ 유효한 티커 개수: {len(valid_tickers)}개")

    # ✅ 모든 주식의 재무 정보 가져오기
    filtered_stocks = []
    for ticker in valid_tickers:
        stock_info = get_stock_info(ticker)
        if stock_info:
            filtered_stocks.append(stock_info)

    # 데이터프레임 변환
    df_filtered = pd.DataFrame(filtered_stocks)

    # ✅ 1. 금융주 제외
    df_filtered = df_filtered[~df_filtered["Sector"].str.contains("Financial", na=False)]

    # ✅ 2. 지주사 제외 (Industry에 'Holding' 포함된 기업 제거)
    df_filtered = df_filtered[~df_filtered["Industry"].str.contains("Holding", na=False)]

    # ✅ 3. 관리종목 제외 (거래 정지 종목)
    df_filtered = df_filtered[df_filtered["MarketPrice"].notna()]

    # ✅ 4. 적자기업 제외 (연간 & 최근 분기)
    df_filtered = df_filtered[(df_filtered["NetIncomeAnnual"] > 0) & (df_filtered["NetIncomeQuarter"] > 0)]

    # ✅ 5. PTP 제외 (Public 회사만 선택)
    df_filtered = df_filtered[df_filtered["QuoteType"] == "EQUITY"]

    # ✅ 결과 저장
    df_filtered.to_csv(output_file, index=False)
    print(f"✅ 필터링 완료! 남은 종목 수: {len(df_filtered)}개")
