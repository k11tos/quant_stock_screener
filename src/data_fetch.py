import yfinance as yf
import pandas as pd

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
