name: Daily Rain Check

on:
  schedule:
    
    - cron: '0 23 * * *'
  workflow_dispatch: 

jobs:
  check-weather:
    runs-on: ubuntu-latest
    steps:
      - name: 簽出程式碼
        uses: actions/checkout@v4

      - name: 設定 Python 環境
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: 安裝相依套件
        run: pip install requests

      - name: 執行降雨偵測腳本
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python check_rain.py
