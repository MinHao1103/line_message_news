# 使用官方 Python 映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴檔案進容器
COPY requirements.txt ./ 

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案進容器
COPY lineMessageNews.py ./

# 曝露應用程式的埠（根據 Flask 的埠號）
EXPOSE 8080

# 預設執行指令
CMD ["python", "lineMessageNews.py"]
