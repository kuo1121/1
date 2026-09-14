import os
import requests

# 從 GitHub Secrets 讀取環境變數
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 設定地點（台北）
LATITUDE = 25.033
LONGITUDE = 121.5654


def get_rain_probability():
  """取得今天的降雨機率"""
  url = (
      f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}"
      "&daily=precipitation_probability_max&timezone=auto"
  )
  try:
    response = requests.get(url)
    data = response.json()
    max_prob = data["daily"]["precipitation_probability_max"][0]
    return max_prob
  except Exception as e:
    print(f"取得氣象資料失敗: {e}")
    return None


def send_telegram_message(message):
  """發送 Telegram 通知"""
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
  response = requests.post(url, json=payload)
  print(f"Telegram 回應狀態碼: {response.status_code}")
  print(f"Telegram 回應內容: {response.text}")


if __name__ == "__main__":
  rain_prob = get_rain_probability()
  print(f"今天預測最高降雨機率為: {rain_prob}%")

  # 不管機率多少，強制發送通知給你看！
  message = (
      f"🌧️ 立即通知測試：今天預測降雨機率為 {rain_prob}%，出門記得帶傘喔！"
  )
  send_telegram_message(message)
