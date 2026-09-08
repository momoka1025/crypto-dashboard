# 📈 仮想通貨 価格ダッシュボード

StreamlitとCoinGecko APIを活用した、仮想通貨の価格推移を可視化するWebアプリケーションです。

## 🌟 特徴
- **リアルタイムデータ**: CoinGecko APIを利用し、最新の仮想通貨価格を取得。
- **インタラクティブなグラフ**: Plotlyを利用した見やすい価格推移グラフ。
- **期間変更**: 過去7日間、30日間など期間を自由に選択可能。
- **CSVダウンロード**: 取得したデータをCSV形式でダウンロード可能。

## 🛠️ 使用技術
- Python
- Streamlit (Webフレームワーク)
- Pandas (データ処理)
- Plotly (データ可視化)
- Requests (API通信)

## 🚀 ローカルでの動かし方

1. このリポジトリをクローン（またはダウンロード）します。
2. 作業ディレクトリで仮想環境を作成・有効化します。
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linuxの場合
   # .venv\Scripts\Activate.ps1  # Windowsの場合