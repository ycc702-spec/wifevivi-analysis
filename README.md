# 李彩雞滴 (wifevivi_) Instagram 投資分析網站

📊 **網站網址**: https://ycc702-spec.github.io/wifevivi-analysis/

這是一個自動化的 Instagram 財經內容分析系統，專門追蹤和分析 wifevivi_ 的投資觀點和交易策略。

## 🎯 功能特色

- **自動抓取**: 每天檢查新貼文
- **AI 分析**: 使用 Gemini 分析投資內容
- **結構化資料**: 提取關鍵觀點、股票標的、交易策略
- **視覺化呈現**: 專業金融風格的網站介面
- **自動部署**: 更新後自動部署到 GitHub Pages

## 📁 檔案結構

```
wifevivi-analysis/
├── index.html              # 主分析報告頁面
├── post-1.html            # 單篇貼文詳細分析
├── wifevivi_data.json     # 結構化分析資料
├── update_wifevivi.py     # 自動更新腳本
└── README.md              # 本檔案
```

## 🔄 自動更新流程

1. **每天 08:00** 執行 `update_wifevivi.py`
2. 檢查 wifevivi_ Instagram 帳號的新貼文
3. 下載影片並使用 Whisper 轉錄
4. 使用 Gemini AI 分析投資內容
5. 更新 `wifevivi_data.json`
6. 重新生成 HTML 頁面
7. 自動部署到 GitHub Pages

## 📊 分析維度

每篇貼文分析包含：

- **核心觀點**: 投資邏輯和論點
- **股票標的**: 提到的股票代碼和建議
- **交易策略**: 進出場時機和倉位管理
- **投資主題**: 產業趨勢和宏觀分析
- **可複製技巧**: 能應用到其他標的的策略

## 🛠️ 技術堆疊

- **前端**: HTML5, CSS3 (無框架，純手寫)
- **配色**: 玫瑰金/粉色金融風格
- **資料**: JSON 結構化儲存
- **部署**: GitHub Pages
- **自動化**: Python + Cron

## 📝 資料來源

- **Instagram**: [@wifevivi_](https://www.instagram.com/wifevivi_/)
- **內容類型**: Reels (短影片)
- **主題**: 投資策略、個股分析、市場觀點

## ⚠️ 免責聲明

本網站僅供學習和參考，內容源自公開的 Instagram 貼文分析。

- 不構成投資建議
- 投資有風險，決策需謹慎
- 過去績效不代表未來表現

## 🤖 自動化狀態

| 項目 | 狀態 |
|------|------|
| 網站部署 | ✅ 已啟用 |
| 自動抓取 | ⏳ 待設定 API |
| AI 分析 | ⏳ 待整合 Gemini |
| 每日更新 | ⏳ 待設定 Cron |

---

由 [Kimi Claw](https://github.com/ycc702-spec) 自動化維護