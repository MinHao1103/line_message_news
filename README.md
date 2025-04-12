# LINE News Bot

這是一個使用 Python 開發的自動化 LINE 訊息推送機器人，可以每天從 Google News 獲取最新新聞並發送到指定的 LINE 群組

## 功能特點

- 自動抓取 Google News 上的最新新聞
- 定時推送新聞至指定的 LINE 群組
- 可透過 Docker 容器化部署

## 使用方法

1. 修改主程式 `lineMessageNews.py` 中的 `channel_token` 和 `group_id` 變數，填入 LINE 開發者設定
2. 機器人預設會在每天中午 12 點自動抓取並推送最新新聞

## 所需依賴

- `requests`：用於發送 HTTP 請求
- `beautifulsoup4`：用於解析 HTML
- `schedule`：用於定時任務管理

## 安裝方式

使用以下命令安裝所需依賴：

```bash
pip install -r requirements.txt
```

## Docker 部署

1. 在專案目錄中構建 Docker 映像檔：
```bash
docker build -t linemessagenews .
```

2. 運行 Docker 容器：
```bash
docker run -d --name linemessagenews linemessagenews
```