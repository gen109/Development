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

st.sidebar.write("""
# 日経225株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示期間選択
""")

start = st.sidebar.date_input(
    "Fromを選択してください。",
    )

st.write("""
### 銘柄選択
""")

filename = 'nikkei.csv'
df = pd.read_csv(filename, encoding='shift-jis')

names = df['銘柄名']

company = st.selectbox(
        '銘柄を選択してください。',
        names,
    )


def get_historical_data(start, company):
    filename = 'nikkei.csv'
    df = pd.read_csv(filename, encoding='shift-jis')

    names = df['銘柄名']

    code = df[df['銘柄名']==company]['コード'].iloc[-1]
    stockCode = str(code) + '.T'
    type(stockCode)

    _df =yf.download(tickers=stockCode, start=start, end=datetime.now())
    date = _df.index

    high = _df['High']
    low = _df['Low']

    max26 = high.rolling(window=26).max()
    min26 = low.rolling(window=26).min()

    _df['basic_line'] = (max26 + min26) / 2

    # 転換線
    high9 = high.rolling(window=9).max()
    low9 = low.rolling(window=9).min()

    _df['turn_line'] = (high9 + low9) / 2
    # 先行スパン1
    
    _df['span1'] = (_df['basic_line'] + _df['turn_line']) / 2

    # 先行スパン2
    high52 = high.rolling(window=52).max()
    low52 = low.rolling(window=52).min()

    _df['span2'] = (high52 + low52) / 2

    # 遅行線
    _df['slow_line'] = _df['Adj Close'].shift(-25)

    return _df

try:
    data = get_historical_data(start, company)
    lines = [mpf.make_addplot(data['basic_line'], color='b'), # 基準線
            mpf.make_addplot(data['turn_line'], color='y'), # 転換線
            mpf.make_addplot(data['slow_line'], color='g') # 遅行線
            ]

    # labels = ['basic', 'turn', 'slow', 'span']

    fig, ax = mpf.plot(data, type='candle', figsize=(16,6),style='yahoo', xrotation=0, addplot=lines, returnfig=True,
                        fill_between=dict(y1=data['span1'].values, y2=data['span2'].values, alpha=0.5, color='gray'))
    # ax[0].legend()
    st.pyplot(fig)
except:
    st.error(
        "35日以上の期間を指定してください！"
    )


col1, col2 = st.columns(2)
with col1:
    st.write("""
    ### 5つの線
    ##### 1 基準線：青折れ線

    過去26日間の最高値と最安値の中心値を結んだ線で、中期的な相場の方向性を示します。

    ##### 2 転換線：黄色折れ線

    過去9日間の最高値と最安値の中心値を結んだ線で、短期的な相場の方向性を示します。

    ##### 3 先行スパン1

    基準線と転換線の中心を、26日先に先行させて記入します。

    基準線は過去26日間の中心、転換線は過去9日間の中心ですが、先行スパン1はそれぞれの中心となります。

    ##### 4 先行スパン2

    過去52日間の最高値と最安値の中心を、26日先に先行させて記入します。

    ※先行スパン1と先行スパン2に囲まれた部分を「雲」（span：グレー部分）と呼びます。

    ##### 5 遅行スパン：緑折れ線

    当日の終値を26日前に記入します。

    「前日比」は当日の価格と前日の価格を比較したものですが、「遅行線」は当日の価格と26日前の価格を比較していることになります。
""")

with col2:
    st.write("""
    ### 一目均衡表の使い方
    次のときは、買いシグナルとなり「好転した」と言います。

    ①転換線が基準線を上抜けたとき

    ②遅行スパンがローソク足を上抜けたとき

    ③ローソク足が雲を上抜けたとき

    さらに、①②③の買いシグナルが3つそろった場合を「三役好転」と言い、より強い買いシグナルとなります。

    また、①②③と逆の向きへ動いた場合は売りシグナルとなり、「逆転した」と言います。

    さらに、3つの売りシグナルがそろった場合は「三役逆転」と言い、より強い売りシグナルとなります
    """)

