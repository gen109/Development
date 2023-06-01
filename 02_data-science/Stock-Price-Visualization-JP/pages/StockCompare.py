import pandas as pd
import time
import yfinance as yf
import altair as alt
import streamlit as st
# import matplotlib.pyplot as plt
# import japanize_matplotlib
import mplfinance as mpf
import warnings
from datetime import date, datetime

st.title("同業他社株価比較可視化アプリ")

st.sidebar.write("""
# 日経株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
    """)

days = st.sidebar.slider('日数', 1, 50, 25)

st.write(f"""
### 過去 **{days}日間** の日経株価
""")

@st.cache
def get_data(days, tickers):
    horizonData = pd.DataFrame()
    for company in tickers.keys():
        try:
            tkr = yf.Ticker(tickers[company])
            hist = tkr.history(period=f'{days}d')
            hist.index = hist.index.strftime('%d %B %Y')
            hist = hist[['Close']]
            hist.columns = [company]
            hist = hist.T
            hist.index.name = 'Name'
            horizonData = pd.concat([horizonData, hist])
        except Exception:
            pass
    return horizonData

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 20000.0, (0.0, 20000.0)
    )

    filename = 'nikkei.csv'
    df = pd.read_csv(filename, encoding='shift-jis')

    tickers = {}
    names = df['銘柄名']
    i = 0
    for name in names:
        code = df[df['銘柄名']==name]['コード'][i]
        stockCode = str(code) + '.T'
        ticker = {
            name: stockCode
        }
        tickers.update(ticker)
        i += 1

    horizonData = get_data(days, tickers)

    companies = st.multiselect(
        '銘柄を選択してください。',
        list(horizonData.index),
        ['ヒューマンクリエイションホールディング']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        selectData = horizonData.loc[companies]
        st.write("### 株価（円）", selectData.sort_index())
        verticalData = selectData.T.reset_index()
        verticalData = pd.melt(verticalData, id_vars=['Date']).rename(
            columns={'Date': '日付', 'Name': '銘柄', 'value': '株価（円）'}
        )
        chart = (
            alt.Chart(verticalData)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="日付:T",
                y=alt.Y("株価（円）:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color="銘柄:N"
            )
        )

        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーですよ～"
    )