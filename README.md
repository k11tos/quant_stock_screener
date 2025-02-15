# Quant Stock Screener

## 📌 프로젝트 개요

**Quant Stock Screener**는 미국 주식 시장에서 소형 성장 가치주(Small-Cap Growth-Value Stocks)를 자동으로 스크리닝하는 Python 기반의 주식 선별 도구입니다.

이 프로젝트는 다양한 전략을 적용할 수 있도록 설계되었으며, 데이터를 수집하고 필터링하여 최적의 투자 후보를 제공합니다.

---

## 🛠️ 기능

1. **데이터 수집 (`data_fetch.py`)**
   - Yahoo Finance API를 사용하여 미국 주식 데이터를 수집합니다.
   - 시장 가치(Market Cap), ROIC, 부채비율(Debt-to-Equity), PER, PSR 등 주요 재무 데이터를 가져옵니다.

2. **주식 필터링 (`filter.py`)**
   - ROIC ≥ 15%
   - 부채비율(Debt-to-Equity) ≤ 50%
   - 시가총액 하위 20% (Small-cap)

3. **결과 저장 및 출력 (`main.py`)**
   - 필터링된 종목을 CSV 파일로 저장합니다.
   - Jupyter Notebook에서 분석할 수 있도록 결과를 출력합니다.

---

## 📂 프로젝트 구조

```
quant_stock_screener/
│── data/              # 필터링된 종목 데이터를 저장하는 폴더
│── src/               # 코드 모듈 폴더
│   │── data_fetch.py   # 주식 데이터 수집 모듈
│   │── filter.py       # 필터링 로직 모듈
│   │── main.py         # 실행 스크립트
│── notebooks/         # Jupyter Notebook 파일 저장
│── README.md          # 프로젝트 설명
│── requirements.txt   # 필요한 패키지 목록
```

---

## 🚀 설치 및 실행 방법

### 1️⃣ 환경 설정

```bash
pip install -r requirements.txt
```

### 2️⃣ 실행 방법

```bash
python src/main.py
```

### 3️⃣ 결과 확인

- 필터링된 종목 리스트는 `data/filtered_stocks.csv` 에 저장됩니다.

---

## 🔍 향후 개선 사항

- 전체 미국 주식 대상 스크리닝 기능 추가
- 필터링 조건 커스터마이징 기능 개발
- 모멘텀 기반 랭킹 기능 추가
- 백테스트 기능 추가

---

## 📜 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 📧 문의

- 개발자: **Lee Janghyeon**
- GitHub: [k11tos](https://github.com/k11tos)
