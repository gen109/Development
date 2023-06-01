### 1.使用するライブラリをインポートする。
##----------------------------------------------------
## 1-1 pandas をインポート = データ解析を容易にする機能を提供するPythonのデータ解析ライブラリ
import pandas as pd
## 1-2 yfinance をインポート = Yahoo! Financeから情報を取得するためのAPI ※警告文が出る場合は [ pip install yfinance ] 
import yfinance as yf
## 1-2 altair をインポート = グラフ可視化ライブラリ
import altair as alt
## 1- Streamlit をインポート = PythonでWebアプリケーションを作成するためのFW
import streamlit as st
#-------------------------------------------------------------------------------------------##
## 上記、警告となる場合の参考サイト  https://mebee.info/2022/06/28/post-72202/ 
#-------------------------------------------------------------------------------------------##
##----------------------------------------------------

### 2.メイン部分：タイトルを表示
st.title('米国株価可視化アプリ')

### 3.サイドバーの作成　（複数行に渡る文字列 = 「("""  """)」
##  3-1. サイドバーのタイトル
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

##  3-2.サイドバーの中項目：表示日数選択
st.sidebar.write("""
## 表示日数選択
""")
##  3-2-1. 表示日数のスライダーを表示（スライダーのタイトル：日数、最小:1, 最大:50, デフォルト:20）
days = st.sidebar.slider('日数', 1, 50, 20)

### 4.メイン部分：中項目（選択したdaysによって表示する日数(32行目)が変更させるので f Stringを使用する）
st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

### 5.データ取得箇所
@st.cache # 毎回取ってるのは大変なので 'cache' に貯めて置き高速に読み込む
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        ##hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    ### 6.サイドバーの中項目：株価の範囲指定の表示～株価表示
    ##  6-1.サイドバーの中項目：株価の範囲指定
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ## 6-2.株価のスライダーを表示（スライダーのタイトル：範囲を指定してください。最小:0.0, 最大:3500.0, デフォルト:3500.0）
    # ymin: 下限、ymax: 上限
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0, (0.0, 3500.0)
    )

    ## 6-3.表示する会社 
    tickers = {
            'apple': 'AAPL',
            'google': 'GOOGL',
            'microsoft': 'MSFT',
            'netflix': 'NFLX',
            'amazon': 'AMZN'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 'amazon', 'apple']
    )

    ## 6-4.最低1件は選択するよう警告表示
    if not companies:
        st.error('少なくとも１社は選んでください。')
    else:
        data = df.loc[companies]
        ## 株価 (USD)　の下に成型した状態で表を表示
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
    )
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )
    ### 7.グラフ化
    st.altair_chart(chart, use_container_width=True)
### 8.エラー表示
except:
    st.error(
        "エラーが起きているようです。"
    )