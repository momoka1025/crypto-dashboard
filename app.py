import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from typing import Optional  # ← 【追加】typing（型ヒント）を使うための準備

# ページの設定
st.set_page_config(page_title="Crypto Dashboard", page_icon="📈", layout="wide")
st.title("🚀 仮想通貨ダッシュボード (改修版)")

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
    "過去7日間": "7", "過去30日間": "30", "過去90日間": "90", "過去1年間": "365"
}
selected_days_name = st.sidebar.selectbox("期間を選択", list(days_dict.keys()))
selected_days = days_dict[selected_days_name]


# --- 🌟 ここからがWeek1の学習目標（class, typing, exception）の統合です ---
class CryptoAPIClient:
    
    # 引数と戻り値のルールを typing で明記
    def fetch_data(self, crypto_id: str, days: str) -> Optional[pd.DataFrame]:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
        
        try: # 例外処理（とりあえずやってみる）
            response = requests.get(url, params={"vs_currency": "jpy", "days": days})
            response.raise_for_status() # 通信エラーがないかチェック
            
            # 成功したらデータを加工して返す
            data = response.json()
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
            return df.drop(columns=['timestamp'])
            
        except requests.exceptions.RequestException as e:
            # 失敗したら赤い画面で強制終了せず、メッセージを出して None を返す
            st.error("通信エラーが発生しました。時間を置いてから再度お試しください。")
            return None
# --- 🌟 ここまで ---


# Streamlitのキャッシュ機能を使ってクラスを呼び出す
@st.cache_data(ttl=600)
def get_crypto_dataframe(crypto_id: str, days: str):
    client = CryptoAPIClient()
    return client.fetch_data(crypto_id, days)

# データの取得
with st.spinner(f"{selected_crypto_name} のデータを取得中..."):
    df = get_crypto_dataframe(selected_crypto_id, selected_days)

# データが無事に取れた（Noneや空っぽではない）場合のみ、グラフを描画する
if df is not None and not df.empty:
    current_price = df['price'].iloc[-1]
    start_price = df['price'].iloc[0]
    change_rate = ((current_price - start_price) / start_price) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("現在の価格 (JPY)", f"¥{current_price:,.0f}")
    col2.metric(f"{selected_days_name}の変化", f"{change_rate:+.2f}%")
    
    fig = px.line(df, x='datetime', y='price', title=f"{selected_crypto_name} の価格推移 ({selected_days_name})")
    fig.update_layout(xaxis_title="日時", yaxis_title="価格 (JPY)")
    st.plotly_chart(fig, use_container_width=True)