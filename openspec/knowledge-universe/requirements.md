# Requirements — 知識宇宙系統（Mnemosyne / Muse / Metis）

> OpenSpec SDD · **v1.0-baseline**（凍結見 [`SPEC_VERSION.md`](SPEC_VERSION.md)）  
> 願景：藉由 Mnemosyne 留存過去，透過 Muse 啟發現在，最終依靠 Metis 規劃未來。

---

## US-001：多來源記憶輸入（Mnemosyne）

**As a** 知識工作者，**I want** 將 Web / NotebookLM / Notion / Google Drive / YouTube 的內容統一落地到知識庫，**so that** 所有碎片資訊都能被喚醒與追溯。

### 驗收標準

- [ ] AC-1：新進檔案落地於 `raw/<source>/` 並含最小 metadata：`source_type`、`source_id`、`canonical_url`、`retrieved_at`、`ingest_path`（`license_notes` 策略見 `design.md`）。
- [ ] AC-2：同一 `source_type + source_id` 重跑不覆寫舊檔，需保留歷史版本（後綴／hash 規則見 `design.md` §3.3）。
- [ ] AC-3：`web_scraper-cli` 與 `aispider-service` 對同來源資料可並存且可區分（`ingest_path`）。
- [ ] AC-4：來源讀取失敗需有可觀測紀錄（錯誤原因與時間；日誌或 `_errors` 約定見實作階段）。

---

## US-002：知識編譯與索引（Mnemosyne）

**As a** 知識工作者，**I want** 將 raw 資料編譯為可閱讀、可連結的 wiki 條目，**so that** 知識庫保持結構化與可搜尋。

### 驗收標準

- [ ] AC-1：執行「整理」（依 [`CLAUDE.md`](../../CLAUDE.md)）後，`wiki/`、`index.md`、`log.md` 皆同步更新。
- [ ] AC-2：新條目符合標準模板（標題、摘要、重點、細節、相關概念、來源、最後更新）。
- [ ] AC-3：每篇新條目至少含 **1** 個 `[[wikilink]]`（避免孤立頁；與 `stages.md` 協調）。
- [ ] AC-4：重跑相同 raw 批次不產生重複 wiki 結論（idempotent）。

---

## US-003：雙路徑擷取與整合（Integration）

**As a** 維護知識庫的使用者，**I want** 既能從 **AISpider 服務** 進料，也能在 Vault 內執行 **web_scraper**，**so that** 排程／遠端爬取與本機補抓可並存且不互踩。

### 驗收標準

- [ ] AC-1：`design.md` 明確描述兩種路徑的輸入、輸出路徑與觸發方式（API／掛載／CLI）。
- [ ] AC-2：同一 URL／同一 `source_id` 重複進料時，去重策略已文件化且可驗證。
- [ ] AC-3：`web_scraper` 預設輸出 `raw/web/` 與 AISpider 落地之 **metadata 欄位**對齊（至少 `source_type`、`source_id`、`retrieved_at`、`canonical_url`）。

---

## US-004：異花授粉洞見生成（Muse）

**As a** 知識工作者，**I want** AI 主動挖掘跨主題關聯與深層連結，**so that** 能得到超越單篇筆記的洞見提案。

### 驗收標準

- [ ] AC-1：每批至少產出 **3** 則 Insight（跨領域、同主題跨來源、意外連結至少各 **1**）。
- [ ] AC-2：每則 Insight 必須含關聯理由、置信度、與來源鏈接（至少 **2** 筆 wiki 或 raw）。
- [ ] AC-3：每則 Insight 可標記 `adopted` / `watch` / `rejected` 並記錄理由。
- [ ] AC-4：低於置信度門檻的提案不進入 Metis。

---

## US-005：策略落地與行動方案（Metis）

**As a** 知識工作者，**I want** 將 Insight 轉成可執行計畫，**so that** 靈感能在現實中落地。

### 驗收標準

- [ ] AC-1：每份 Action Plan 含 OKR、WBS、KPI、Risk、Definition of Done（模板見 [`metis-action-plan-spec.md`](metis-action-plan-spec.md)）。
- [ ] AC-2：每份 Action Plan 綁定來源 Insight 與原始證據鏈（wiki/raw）。
- [ ] AC-3：每份 Action Plan 有狀態欄位（`draft` / `active` / `blocked` / `done`）。
- [ ] AC-4：系統可定義下一步提醒（trigger + action）。

---

## US-006：知識閉環（Cross-layer）

**As a** 知識工作者，**I want** Metis 的執行成果回流 Mnemosyne，**so that** 系統形成持續增強的學習迴路。

### 驗收標準

- [ ] AC-1：專案完成後可生成 `retrospective`（格式約定於實作階段）。
- [ ] AC-2：`retrospective` 可重新進入 `raw → wiki` 編譯鏈。
- [ ] AC-3：新回流內容可再次觸發 Muse 關聯分析（與 Gate 協調）。

---

## US-007：混合可視化（Vault SoT + 匯出層）

**As a** 知識工作者，**I want** Vault 為內容與連結的真實來源，並能定期匯出至 Web 儀表板，**so that** 日常於 Obsidian 編輯、必要時於瀏覽器檢視同一知識宇宙。

### 驗收標準

- [ ] AC-1：`design.md` 明定 **SoT = Vault**（`wiki/`、`index.md`），儀表板為 **匯出檢視層**（預設單向）。
- [ ] AC-2：匯出物至少包含（a）可重建圖之節點／邊（例如 `graph.json`）與可開啟之 HTML 或等效靜態頁；（b）**三女神階段卡（Mnemosyne／Muse／Metis）+ Gate A/B 進度 + 65 任務勾選進度**（見 `design.md` §15 Dashboard 卡片）。
- [ ] AC-3：定期觸發方式（cron／手動／watch）在 `tasks.md` 可追蹤落地。
- [ ] AC-4：儀表板 footer 標示 `generated_at` 與 git commit hash，超過 7 日未更新需以視覺提示警告（避免 SoT 漂移）。

---

## NFR（非功能需求）

### NFR-1：效能與資源（M1 16GB）

- [ ] NFR-1.1：批次／圖遍歷任務之記憶體峰值控制在可接受範圍（建議上限 **8GB**；見使用者 AGENT 約束）。
- [ ] NFR-1.2：需支援離線降級（Ollama）與線上模式切換（路由見 `design.md` §12）。
- [ ] NFR-1.3：批次任務具節流與重試機制。

### NFR-2：安全與隱私

- [ ] NFR-2.1：API Key 僅從 `.env.local`／secret store 讀取，禁止硬編碼。
- [ ] NFR-2.2：預設 **local-first**，不主動上傳私人 raw 至第三方。
- [ ] NFR-2.3：個人狀態資料（wellness）需可匿名化或摘要化再供模型使用。

### NFR-3：可擴展性

- [ ] NFR-3.1：可新增來源 connector 而不改核心「整理」語意（`CLAUDE.md` 合併策略不變）。
- [ ] NFR-3.2：模型供應商可替換（Anthropic / Google / Ollama 等）。
- [ ] NFR-3.3：模板與 frontmatter 版本可演進並保留向下相容策略。

---

## 附錄 A：十二指令語意（Command Palette）

與 [`pantheon-pkm.md`](pantheon-pkm.md) §4 一致；實作對照 `design.md` §11。

| 分類 | 指令 | 用途摘要 |
|------|------|----------|
| Mnemosyne | `/wiki-import` | 匯入原始素材並啟動基礎編譯流程 |
| Mnemosyne | `/journal-write` | 意識流寫作入口 |
| Mnemosyne | `/wellness-log` | 身心狀態紀錄 |
| Muse | `/journal-route` | 日記／碎片語義分流 |
| Muse | `/wiki-link` | 指定節點深層關聯探索 |
| Muse | `/wiki-orphan` | 孤兒筆記配對 |
| Muse | `/wiki-graph` | 圖譜視覺化／匯出 |
| Metis | `/project-new` | 洞見 → 專案（OKR/WBS） |
| Metis | `/project-start` | 工作前思考軌跡 |
| Metis | `/project-review` | 收工與 KPI/DoD 更新 |
| Metis | `/project-dashboard` | 策略地圖與儀表板 |
| Metis | `/wellness-report` | 風險與身心耗損報告 |

---

## 追蹤矩陣（US ↔ design）

| US | 主題 | design 對照（章節） |
|----|------|---------------------|
| US-001 | 多來源 raw | §3 Raw 合約、§4 AISpider |
| US-002 | 編譯／wiki | §6、§9、`CLAUDE.md` |
| US-003 | 雙路徑 | §1、§4、§5 |
| US-004 | Muse | §11、§12、`stages.md` Stage 2 |
| US-005 | Metis | §11、`metis-action-plan-spec.md` |
| US-006 | 閉環 | §7、§11 |
| US-007 | 可視化 | §7 |

---
最後更新：2026-04-14（v1.0-baseline）
