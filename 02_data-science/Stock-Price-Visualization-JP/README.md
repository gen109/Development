<h1 align="center">日経株価化可視化アプリ - Stock Price Visualization JP</h1>
<h2 align="left">概要 - Summary</h2>
本アプリは、Yahooファイアンスから情報を取得し株価の変動を可視化したものです。

This application acquires information from Yahoo Faience and visualizes stock price fluctuations.

<h2 align="left">事前準備 - Advance preparation</h2>
本アプリは、「Streamlit」のフレームワークを使用しているので、事前にStreamlitのインストールをお願いいたします。

Pythonの環境構築が完了している方であれば、以下のコマンドを実行していただければアプリケーションが起動します。

This application uses the "Streamlit" framework, so please install Streamlit in advance.  
If the Python environment construction is completed, the application will be started by executing the following command.

・インストール - install
```
pip3 install streamlit
```

・アプリケーション起動 - Application launch
```
streamlit hello
```

<h2 align="left">使用方法 - How to use</h2>
必ず「nikkei.csv」に1件以上の情報を登録してください。

登録がない場合、エラーとなります。

Be sure to register at least one item of information in "nikkei.csv".  
An error will occur if there is no registration.

<h3 align="left">・nikkei.csv</h3>
csvファイル内に「コード」、「銘柄名」、「社名」、「業種」、「株式市場」の項目があるので

Yahooファイアンスから情報を取得してください。（https://finance.yahoo.co.jp/）

<h3 align="left">・app.py</h3>
メインファイルとなっております。

ターミナルで以下のコマンドを実行していただければ、可視化アプリが起動します。

It is the main file.  
If you run the following command in the terminal, the visualization app will start.

・実行コマンド - execution command
```
streamlit run app.py
```

<h1 align="center"></h1>