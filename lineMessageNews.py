import random
import requests
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time
import logging
import os

# 設置時區
os.environ['TZ'] = 'Asia/Taipei'
time.tzset()

# 設置日誌配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

current_tz = time.tzname
logging.info(f"目前時區設定: {current_tz}")
logging.info(f"目前時間: {datetime.now()}")

URL = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'

# 集中管理所有的配置
CONFIGS = [
    {
        "name": "中午推送",
        "channel_token": "",
        "group_id": "",
        "schedule_time": "12:00",
        "news_count": 50
    },
    {
        "name": "早上推送",
        "channel_token": "",
        "group_id": "",
        "schedule_time": "09:00",
        "news_count": 50
    },
    {
        "name": "下午推送",
        "channel_token": "",
        "group_id": "",
        "schedule_time": "13:00",
        "news_count": 50
    }
]

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
        logging.error(f"Failed to retrieve Google News content: {response.status_code}")
    
    return '\n\n'.join([f"{i+1}. {title}\n{url}" for i, (title, url) in enumerate(results)])

def shorten_url(long_url):
    api_url = "https://tinyurl.com/api-create.php"
    params = {"url": long_url}
    
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"URL shortening failed: {response.status_code} - {response.text}")
            return long_url
    except Exception as e:
        logging.error(f"URL shortening error: {str(e)}")
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
    
    try:
        res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
        if res.status_code == 200:
            logging.info(f"LINE push succeeded to group {group_id[:8]}...")
        else:
            logging.error(f"LINE push failed: {res.status_code} - {res.text}")
    except Exception as e:
        logging.error(f"LINE push error: {str(e)}")
        
def job(config):
    """
    執行定時任務
    
    :param config: 配置字典
    """
    name = config["name"]
    channel_token = config["channel_token"]
    group_id = config["group_id"]
    news_count = config["news_count"]
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"執行時間 ({name})：{now}")
    logging.info(f"開始取得 Google 新聞 ({name})...")
    
    try:
        newsText = fetch_google_news_text(news_count)
        logging.info(f"新聞內容取得完成，準備發送 LINE 訊息 ({name})...")
        logging.info(f"------- 傳送內容 ({name}) -------")
        logging.info(newsText)
        logging.info(f"------- 傳送開始 ({name}) -------")
        send_line_message_push(channel_token, group_id, newsText)
        logging.info(f"{name}程式執行完畢。")
    except Exception as e:
        logging.error(f"執行{name}任務時發生錯誤: {str(e)}")

if __name__ == "__main__":
    # 設定排程
    for i, config in enumerate(CONFIGS):
        schedule_time = config["schedule_time"]
        name = config["name"]
        def create_job(conf):
            return lambda: job(conf)
        task = create_job(config)
        schedule.every().day.at(schedule_time).do(task)
        logging.info(f"定時任務「{name}」已排定在每天 {schedule_time} 執行")
    
    last_log_time = datetime.now()
    while True:
        schedule.run_pending()
        
        # 每小時記錄一次狀態
        current_time = datetime.now()
        if (current_time - last_log_time).total_seconds() >= 3600:
            logging.info(f"排程監控中，目前時間：{current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            last_log_time = current_time
            
        time.sleep(10)