#!/usr/bin/env python3
"""
wifevivi_ Instagram 自動抓取與分析腳本
每天檢查新貼文，自動下載、轉錄、分析，並更新網站

環境變數:
- APIFY_TOKEN: Apify API Token
- GEMINI_API_KEY: Google Gemini API Key
"""

import os
import json
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path

# 從環境變數獲取 API Keys
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 設定路徑
WORKSPACE = Path("/root/.openclaw/workspace/wifevivi-analysis")
DATA_FILE = WORKSPACE / "wifevivi_data.json"
LOG_FILE = WORKSPACE / "update.log"
TEMP_DIR = WORKSPACE / "temp"

# Instagram 帳號
INSTAGRAM_USER = "wifevivi_"

def log(message):
    """記錄日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def check_api_keys():
    """檢查 API Keys 是否設定"""
    if not APIFY_TOKEN:
        log("❌ 錯誤：未設定 APIFY_TOKEN 環境變數")
        return False
    if not GEMINI_API_KEY:
        log("❌ 錯誤：未設定 GEMINI_API_KEY 環境變數")
        return False
    return True

def load_data():
    """載入現有資料"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "account": INSTAGRAM_USER,
        "account_name": "李彩雞滴",
        "total_posts_analyzed": 0,
        "posts": [],
        "investment_themes": {},
        "trading_strategies": [],
        "key_insights": []
    }

def save_data(data):
    """儲存資料"""
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_new_posts():
    """使用 Apify Instagram Profile Scraper 檢查新貼文"""
    log(f"使用 Apify 檢查 {INSTAGRAM_USER} 的新貼文...")
    
    try:
        from apify_client import ApifyClient
        
        client = ApifyClient(APIFY_TOKEN)
        
        run_input = {
            "usernames": [INSTAGRAM_USER],
            "resultsLimit": 10,
        }
        
        run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]
        items = list(client.dataset(dataset_id).iterate_items())
        
        if not items:
            log("沒有找到貼文")
            return []
        
        data = load_data()
        existing_urls = {post.get("url", "") for post in data.get("posts", [])}
        
        new_posts = []
        for item in items:
            post_url = item.get("url", "")
            if post_url and post_url not in existing_urls:
                new_posts.append({
                    "url": post_url,
                    "shortCode": item.get("shortCode", ""),
                    "caption": item.get("caption", ""),
                    "timestamp": item.get("timestamp", ""),
                    "type": item.get("type", "")
                })
        
        log(f"找到 {len(new_posts)} 篇新貼文")
        return new_posts
        
    except Exception as e:
        log(f"❌ Apify 抓取失敗: {e}")
        return []

def analyze_with_gemini(transcript, caption=""):
    """使用 Gemini 分析投資內容"""
    log("使用 Gemini 分析內容...")
    
    try:
        from google import genai
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""你是一位專業的投資分析師。請分析以下 Instagram 財經內容，提取關鍵投資資訊。

內容文字：
{transcript}

貼文描述：
{caption}

請以 JSON 格式回傳以下資訊：
{{
    "title": "貼文標題（簡短總結主題）",
    "summary": "內容摘要（100-200字）",
    "key_points": ["關鍵觀點1", "關鍵觀點2", ...],
    "stock_mentions": [
        {{
            "symbol": "股票代碼",
            "name": "公司名稱",
            "action": "買入/賣出/觀察",
            "price_range": "價格區間",
            "reason": "理由"
        }}
    ],
    "investment_themes": ["主題1", "主題2"],
    "trading_strategies": ["策略1", "策略2"],
    "tags": ["標籤1", "標籤2"],
    "techniques": [
        {{
            "title": "技巧名稱",
            "description": "技巧描述",
            "priority": "高/中/低"
        }}
    ]
}}

請確保輸出是有效的 JSON 格式。"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        response_text = response.text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
            log("✅ Gemini 分析完成")
            return analysis
        else:
            log("❌ 無法解析 Gemini 回應")
            return None
            
    except Exception as e:
        log(f"❌ Gemini 分析失敗: {e}")
        return None

def deploy_to_github():
    """部署到 GitHub Pages"""
    log("部署到 GitHub Pages...")
    
    try:
        os.chdir(WORKSPACE)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        
        if not result.stdout.strip():
            log("沒有變更需要提交")
            return True
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(
            ["git", "commit", "-m", f"Update analysis - {timestamp}"],
            check=True, capture_output=True
        )
        
        subprocess.run(["git", "push", "origin", "main"], 
                      check=True, capture_output=True)
        
        log("✅ 部署成功")
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"❌ 部署失敗: {e}")
        return False

def main():
    """主函數"""
    log("=" * 50)
    log("開始 wifevivi_ 自動更新流程")
    log("=" * 50)
    
    if not check_api_keys():
        return
    
    TEMP_DIR.mkdir(exist_ok=True)
    
    data = load_data()
    log(f"已載入資料，目前分析 {data['total_posts_analyzed']} 篇貼文")
    
    new_posts = check_new_posts()
    
    if not new_posts:
        log("沒有發現新貼文")
        save_data(data)
        deploy_to_github()
        log("完成")
        return
    
    log(f"發現 {len(new_posts)} 篇新貼文，開始處理...")
    # TODO: 實現完整的下載、轉錄、分析流程
    
    save_data(data)
    deploy_to_github()
    
    log("=" * 50)
    log("更新流程完成")
    log("=" * 50)

if __name__ == "__main__":
    main()