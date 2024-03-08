# triC-bot
競技プログラミングサークルtriCのDiscordサーバーで使用するbotです。

### 機能一覧
- メンバーのACを通知
- メンバーを追加
- 明日のコンテストを通知
- triC定期バチャの作成・通知 未実装
- triC定期バチャのレーティング計算 未実装

### 使い方
1. このリポジトリをクローン
2. 環境変数を設定
3. `python -m venv .venv`で仮想環境を作成
4. `pip install -r requirements.txt`で依存関係をインストール
5. `python ./src/db_init.py`でdb初期化
6. `python ./src/main.py`でbotを起動