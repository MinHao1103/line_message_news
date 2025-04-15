# LINE News Bot

這是一個使用 Python 開發的自動化 LINE 訊息推送機器人，可以每天從 Google News 獲取最新新聞並發送到指定的 LINE 群組。

## 功能特點

- 自動抓取 Google News 最新新聞  
- 多時段、多群組定時推送  
- Docker 容器化部署  
- 自動縮短新聞 URL  

## 所需依賴

- `requests`：用於發送 HTTP 請求  
- `beautifulsoup4`：用於解析 HTML  
- `schedule`：用於定時任務管理  

## 快速設定

### CONFIGS 變數設定：

可在 CONFIGS 中添加多組設定，支援不同時段推送至不同群組：

```python
CONFIGS = [
    {
        "name": "晨間新聞",
        "channel_token": "TOKEN1",
        "group_id": "GROUP_ID1",
        "schedule_time": "09:00",
        "news_count": 10
    },
    {
        "name": "午間新聞",
        "channel_token": "TOKEN2",
        "group_id": "GROUP_ID2",
        "schedule_time": "12:00",
        "news_count": 10
    }
]
```

## 依賴套件安裝

```bash
pip install requests beautifulsoup4 schedule
```

## Docker 部署
```
# 建構映像檔
docker build -t linemessagenews .

# 執行容器
docker run -d --name linemessagenews linemessagenews
```