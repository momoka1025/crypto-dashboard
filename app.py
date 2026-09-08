import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ページの設定
st.set_page_config(page_title="Crypto Dashboard", page_icon="📈", layout="wide")

st.title("📈 仮想通貨 価格ダッシュボード")
st.markdown("StreamlitとCoinGecko APIを活用した仮想通貨の価格推移ダッシュボードです。")

# サイドバーの設定
st.sidebar.header("設定")
crypto_dict = {
    "ビットコイン (BTC)": "bitcoin",
    "イーサリアム (ETH)": "ethereum",
    "リップル (XRP)": "ripple",
    "ソラナ (SOL)": "solana"
}
selected_crypto_name = st.sidebar.selectbox("仮想通貨を選択", list(crypto_dict.keys()))
selected_crypto_id = crypto_dict[selected_crypto_name]

days_dict = {
    "過去7日間": "7",
    "過去30日間": "30",
    "過去90日間": "90",
    "過去1年間": "365"
}
selected_days_name = st.sidebar.selectbox("期間を選択", list(days_dict.keys()))
selected_days = days_dict[selected_days_name]

# データを取得する関数（@st.cache_dataでデータを一時保存し、高速化とAPI制限対策）
@st.cache_data(ttl=600)
def fetch_crypto_data(crypto_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "jpy",
        "days": days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        # 日本時間に変換
        df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
        df = df.drop(columns=['timestamp'])
        return df
    else:
        st.error("データの取得に失敗しました。しばらく待ってから再度お試しください。")
        return pd.DataFrame()

# データの取得
with st.spinner(f"{selected_crypto_name} のデータを取得中..."):
    df = fetch_crypto_data(selected_crypto_id, selected_days)

if not df.empty:
    # 最新価格の取得
    current_price = df['price'].iloc[-1]
    start_price = df['price'].iloc[0]
    change_rate = ((current_price - start_price) / start_price) * 100

    # メトリクス表示（主要な数値を大きく表示）
    col1, col2, col3 = st.columns(3)
    col1.metric("現在の価格 (JPY)", f"¥{current_price:,.0f}")
    col2.metric(f"{selected_days_name}の変化", f"{change_rate:+.2f}%")
    
    # グラフの描画 (Plotlyを使ったインタラクティブなグラフ)
    fig = px.line(df, x='datetime', y='price', title=f"{selected_crypto_name} の価格推移 ({selected_days_name})")
    fig.update_layout(xaxis_title="日時", yaxis_title="価格 (JPY)")
    st.plotly_chart(fig, use_container_width=True)

    # データテーブルの表示
    st.subheader("📋 データ詳細")
    df_display = df.copy()
    df_display['datetime'] = df_display['datetime'].dt.strftime('%Y-%m-%d %H:%M')
    df_display = df_display.sort_values(by='datetime', ascending=False)
    st.dataframe(df_display, use_container_width=True)

    # CSVダウンロードボタン
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 データをCSVでダウンロード",
        data=csv,
        file_name=f"{selected_crypto_id}_prices.csv",
        mime='text/csv',
    )