import random
import requests
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time
import logging

# 設置日誌配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

URL = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
CHANNEL_TOKEN=''
GROUP_ID=''

def fetch_google_news_text(count):
    response = requests.get(URL)
    results = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_links = soup.find_all('a', class_='gPFEn')
        random.shuffle(news_links)

        for link in news_links:
            title = link.text.strip()
            href = link['href']
            full_url = unquote(urljoin('https://news.google.com/', href))
            short_url = shorten_url(full_url)  # 縮短網址
            results.append((title, short_url))
            if len(results) >= count:
                break
    else:
        logging.error("Failed to retrieve Google News content.")

    return '\n\n'.join([f"{i+1}. {title}\n{url}" for i, (title, url) in enumerate(results)])

def shorten_url(long_url):
    api_url = "https://tinyurl.com/api-create.php"
    params = {"url": long_url}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        logging.error("URL shortening failed: %s", response.text)
        return long_url
        
def send_line_message_push(channel_token, group_id, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_token}'
    }
    payload = {
        "to": group_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    if res.status_code == 200:
        logging.info("LINE push succeeded.")
    else:
        logging.error("LINE push failed: %s", res.text)
        
def job():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"執行時間：{now}")
    logging.info("開始取得 Google 新聞...")
    newsText = fetch_google_news_text(50)

    logging.info("新聞內容取得完成，準備發送 LINE 訊息...")
    logging.info("------- 傳送內容 -------")
    logging.info(newsText)
    logging.info("------- 傳送開始 -------")

    send_line_message_push(CHANNEL_TOKEN, GROUP_ID, newsText)

    logging.info("程式執行完畢。")

if __name__ == "__main__":
    # 啟動時先執行一次
    job()

    # 設定每天中午 12 點執行
    schedule.every().day.at("12:00").do(job)

    logging.info("定時任務已排定在每天 12:00 執行")

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        logging.info(f"每分鐘檢查任務中，目前時間：{now}")
        
        if not schedule.run_pending():
            logging.info("現在不是中午 12:00，任務不執行")

        time.sleep(10)