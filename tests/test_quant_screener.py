import unittest

import pandas as pd

from src.data_fetch import fetch_all_data, get_stock_data
from src.filter import filter_stocks


class TestQuantStockScreener(unittest.TestCase):

    def setUp(self):
        """테스트 실행 전 샘플 데이터를 준비합니다."""
        self.sample_data = pd.DataFrame(
            [
                {
                    "Ticker": "AAPL",
                    "Market Cap": 250000000000,
                    "ROIC": 0.2,
                    "Debt/Equity": 30,
                    "PER": 20,
                    "PSR": 5,
                    "Revenue Growth YoY": 0.1,
                    "Net Income Growth YoY": 0.12,
                },
                {
                    "Ticker": "MSFT",
                    "Market Cap": 2200000000000,
                    "ROIC": 0.18,
                    "Debt/Equity": 25,
                    "PER": 25,
                    "PSR": 6,
                    "Revenue Growth YoY": 0.09,
                    "Net Income Growth YoY": 0.11,
                },
                {
                    "Ticker": "TSLA",
                    "Market Cap": 50000000000,
                    "ROIC": 0.05,
                    "Debt/Equity": 70,
                    "PER": 60,
                    "PSR": 10,
                    "Revenue Growth YoY": 0.3,
                    "Net Income Growth YoY": 0.25,
                },
                {
                    "Ticker": "NVDA",
                    "Market Cap": 80000000000,
                    "ROIC": 0.16,
                    "Debt/Equity": 40,
                    "PER": 15,
                    "PSR": 4,
                    "Revenue Growth YoY": 0.15,
                    "Net Income Growth YoY": 0.14,
                },
                {
                    "Ticker": "AMD",
                    "Market Cap": 90000000000,
                    "ROIC": 0.17,
                    "Debt/Equity": 35,
                    "PER": 18,
                    "PSR": 4.5,
                    "Revenue Growth YoY": 0.12,
                    "Net Income Growth YoY": 0.13,
                },
                {
                    "Ticker": "SMALL1",
                    "Market Cap": 5000000000,
                    "ROIC": 0.20,
                    "Debt/Equity": 20,
                    "PER": 12,
                    "PSR": 3,
                    "Revenue Growth YoY": 0.18,
                    "Net Income Growth YoY": 0.16,
                },
                {
                    "Ticker": "SMALL2",
                    "Market Cap": 4000000000,
                    "ROIC": 0.22,
                    "Debt/Equity": 18,
                    "PER": 14,
                    "PSR": 3.5,
                    "Revenue Growth YoY": 0.20,
                    "Net Income Growth YoY": 0.17,
                },
            ]
        )

    def test_get_stock_data(self):
        """개별 주식 데이터 수집이 정상적으로 동작하는지 확인합니다."""
        data = get_stock_data("AAPL")
        self.assertIn("Ticker", data)
        self.assertIn("Market Cap", data)

    def test_filter_stocks(self):
        """필터링 기능이 정상적으로 동작하는지 확인합니다."""
        filtered_df = filter_stocks(self.sample_data)
        self.assertGreater(len(filtered_df), 0)
        self.assertTrue(all(filtered_df["ROIC"] >= 0.15))
        self.assertTrue(all(filtered_df["Debt/Equity"] <= 50))

    def test_fetch_all_data(self):
        """여러 개의 주식 데이터를 가져오는 함수가 정상적으로 작동하는지 확인합니다."""
        tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMD", "SMALL1", "SMALL2"]
        df = fetch_all_data(tickers)
        self.assertGreater(len(df), 0)
        self.assertIn("Ticker", df.columns)
        self.assertIn("Market Cap", df.columns)


if __name__ == "__main__":
    unittest.main()
