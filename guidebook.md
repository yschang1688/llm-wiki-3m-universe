# LLM 知識庫 — 操作手冊

這套系統讓你用 AI 把零散的文章、論文、筆記，編譯成一座結構化的知識庫。以下是四個核心動作的操作方式。
![[AI LLM Wiki 架構圖.png]]
---

## 1. 蒐集（把資料丟進 raw/）

### 網頁文章
1. 安裝 [Obsidian Web Clipper](https://obsidian.md/clipper) 瀏覽器擴充功能
2. 在 Web Clipper 設定中，將儲存路徑指向此 vault 的 `raw/` 資料夾
3. 看到想收藏的文章，點一下 Web Clipper 圖示，文章就會存成 `.md` 檔進入 `raw/`

### 其他資料
直接把檔案拖進 `raw/` 資料夾即可：
- PDF、截圖、逐字稿
- arXiv 論文（建議先轉成 .md 或 .txt）
- GitHub repo 的 README
- 任何文字檔

**重要**：`raw/` 裡的檔案永遠不會被修改或刪除，它是你的原始存檔。

### NotebookLM 匯出

將 Google NotebookLM 的 Notebook 與來源匯出為 .md 檔：

**方法 A — Chrome MCP 自動化**：在 Claude Code 中說「幫我匯出 NotebookLM 的筆記本」，AI 會透過 Chrome MCP 自動擷取。（需要 Chrome 開啟並已登入 Google）

**方法 B — 透過 Google Drive**：NotebookLM 的來源大多來自 Google Drive，可用 Google Drive MCP 直接批次下載並轉換。

**方法 C — 手動匯出**：在 NotebookLM 中複製筆記內容，貼到 `raw/notebooklm/` 下的 .md 檔。

詳見 `tools/notebooklm_export.md`。

### 網站批次爬蟲

用 `tools/web_scraper.py` 批次抓取常讀網站，自動轉成 .md：

```bash
# 單一網頁
python3 tools/web_scraper.py https://example.com/article

# 從網址列表批次抓取
python3 tools/web_scraper.py --file tools/urls_example.txt

# 爬取整個部落格（深度 2 層）
python3 tools/web_scraper.py --crawl https://blog.example.com --depth 2

# 指定子資料夾分類
python3 tools/web_scraper.py -s "AI技術" https://example.com/ai-article
```

抓取的檔案會自動存入 `raw/web/`，之後說「整理」即可編譯進知識庫。

編輯 `tools/urls_example.txt` 可以管理你的常讀網站列表。

**結構化課程輸出（`raw/class/`）**：同一支程式支援 **Koob 線上課**與 **大人學 darencademy** 列表／單課頁，產出分段 `.md`、manifest、選用音訊；圖以 `[圖：alt]` 表示。建議用專案內 venv：`.venv-scraper/bin/python`（依賴見 `requirements-scraper.txt`）。

```bash
# 大人學：列表第 2～4 頁合併、輸出到 raw/class（略過已存在 darencademy_manifest 的課）
.venv-scraper/bin/python tools/web_scraper.py \
  --darencademy-index 'https://www.darencademy.com/course/index/page/2' \
  --darencademy-index-page-to 4 -o raw/class

# 大人學：只補「其他.md」（不覆寫其他分段、不更新總表）
.venv-scraper/bin/python tools/web_scraper.py \
  --darencademy-index 'https://www.darencademy.com/course/index/page/1' \
  --darencademy-max-courses 15 --darencademy-other-only -o raw/class

# Koob：線上課列表批次（略過已爬 slug）
.venv-scraper/bin/python tools/web_scraper.py \
  --koob-online-index 'https://www.koob.com.tw/online' -o raw/class
```

站方 HTML 版型會變，分段與列表連結曾做過多輪修正（表頭掃描、同段「預告＋實際效益」拆分、多頁去重、`listing_urls` 等）；細節見 **`CLAUDE.md`**「工具補充」與 **`log.md`**。

**Pipeline 規格（OpenSpec）**：多來源落地、metadata 與 AISpider 介面說明見 [`openspec/knowledge-universe/README.md`](openspec/knowledge-universe/README.md)；`raw/` 進料 YAML 範本見 [`openspec/knowledge-universe/templates/`](openspec/knowledge-universe/templates/)。

---

## 2. 整理（讓 AI 編譯知識庫）

累積了幾篇新資料後，開啟 Claude Code，在這個資料夾中輸入：

```
整理
```

Claude Code 會自動：
- 讀取 `raw/` 中尚未處理的檔案
- 為每個概念建立或更新 `wiki/` 中的筆記
- 在相關筆記之間加上 `[[雙向連結]]`
- 更新 `index.md` 目錄和 `log.md` 記錄

你也可以指定處理特定檔案：
```
整理 raw/某篇文章.md
```

---

## 3. 提問（對知識庫問問題）

知識庫累積到一定規模後，可以直接問問題：

```
幫我整理 Transformer 架構的重點
```
```
比較 RAG 和 fine-tuning 的優缺點
```
```
我在強化學習這塊還有哪些盲點？
```

AI 會搜尋相關的 wiki 筆記，綜合回答，並把有價值的回答存回 `wiki/`——讓每次提問都成為知識的一部分。

---

## 4. 清理（定期健檢）

每隔一段時間，輸入：

```
清理
```

AI 會掃描整座知識庫，檢查：
- 不同筆記間的矛盾
- 可能過時的資訊
- 沒有被連結到的孤立頁面
- 應該互相連結但沒有的概念
- 值得進一步探索的新方向

---

## 日常工作流程
![[AI LLM Wiki roadmap.png]]
```
看到好文章 → Web Clipper 存進 raw/
           ↓
累積幾篇   → 開 Claude Code 說「整理」
           ↓
有問題想問  → 直接問，答案自動存回 wiki/
           ↓
定期       → 說「清理」，讓 AI 健檢知識庫
```

每一步都讓知識庫成長。問完的問題不會消失，整理過的資料不會散落——這就是 Karpathy 所說的「知識持續累積」。

---

## 在 Obsidian 中瀏覽

- 開啟 `index.md` 可以看到所有文章的分類目錄
- 開啟 `log.md` 可以看到每次整理的時間線
- 使用 Obsidian 的圖譜檢視（Graph View）可以看到概念之間的連結關係
- 所有 `wiki/` 中的筆記都用 `[[wikilink]]` 互相連結，點擊即可跳轉
