import os
import requests


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


LATITUDE = 25.033
LONGITUDE = 121.5654
THRESHOLD = 0 


def get_rain_probability():
  """透過 Open-Meteo API 取得今天的降雨機率"""
  url = (
      f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}"
      "&daily=precipitation_probability_max&timezone=auto"
  )

  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    
    max_prob = data["daily"]["precipitation_probability_max"][0]
    return max_prob
  except Exception as e:
    print(f"取得氣象資料失敗: {e}")
    return None


def send_telegram_message(message):
  """透過 Telegram Bot 發送通知"""
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("未設定 Telegram Token 或 Chat ID")
    return

  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

  try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
      print("Telegram 通知發送成功！")
    else:
      print(f"發送失敗: {response.text}")
  except Exception as e:
    print(f"連線 Telegram 失敗: {e}")


if __name__ == "__main__":
  rain_prob = get_rain_probability()

  if rain_prob is not None:
    print(f"今天預測最高降雨機率為: {rain_prob}%")

   
    if rain_prob > THRESHOLD:
      message = (
          f"🌧️ 貼心提醒：今天降雨機率高達 {rain_prob}%，超過 {THRESHOLD}%"
          " 囉！出門記得帶把傘喔！"
      )
      send_telegram_message(message)
    else:
      print("降雨機率未達門檻，不需發送通知。")
