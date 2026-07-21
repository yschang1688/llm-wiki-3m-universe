# OpenSpec：三神祇角色（The Pantheon PKM System）

> 本文件為 **產品敘事與定位** 的單頁規格；技術合約與管線細節見 [`design.md`](design.md)；階段門檻與 DoD 見 [`stages.md`](stages.md)。  
> **規格版本：** [`SPEC_VERSION.md`](SPEC_VERSION.md) **v1.0-baseline**。

---

## 1. 產品願景與執行摘要（Product Vision & Executive Summary）

**「藉由 Mnemosyne 蓄積能量，透過 Muse 閃現火花，最終依靠 Metis 將夢想精準落地。」**

本規格書定義新一代 **「三神祇知識宇宙系統」** 的底層架構。系統跳脫傳統筆記軟體的靜態框架，以希臘神話中三位核心神祇的職能為隱喻，打造從 **「記憶（過去）」** 到 **「靈感（當下）」**，最後抵達 **「規劃（未來）」** 的動態流轉生態系。系統在 Obsidian 中運行，由三位 AI 代理人負責不同階段的任務，實現從知識碎片到具體行動的完整閉環。

**與本 Vault OpenSpec 的對標：** Mnemosyne 對應 **AI_LLM_Wiki**（擷取、raw、`wiki/` 編譯）；Muse／Metis 對應後續 **AI_Insight**／**AI_Strategy** 能力與產物，並受 [`stages.md`](stages.md) 門檻約束。

---

## 2. 系統核心哲學與架構全貌（System Architecture Overview）

本系統依循大腦神經網絡與知識創造的真實軌跡，將模組分為三個遞進階段：

| 階段 | 神話代表 | 功能核心 | 專屬 AI／系統角色 | 核心任務 | 終極產出物 |
|------|----------|----------|-------------------|----------|------------|
| Step 1 | Mnemosyne | 記憶／存儲 | **AI_LLM_Wiki** | 知識自動索引、關聯連結 | 個人知識圖譜（Personal Wiki） |
| Step 2 | Muse | 靈感／洞見 | **AI_Insight** | 跨界聯想、創意生成（Cross-pollination） | 洞見提案（Insight） |
| Step 3 | Metis | 策略／落地 | **AI_Strategy** | 風險評估、執行路徑規劃與 OKR 拆解 | 策略地圖（Action Plan） |

**Pipeline 合約補充（與 design 一致）：** 雙路徑擷取（AISpider 服務 + `tools/web_scraper`）→ `raw/` → 依 CLAUDE「整理」→ `wiki/`；可視化為 Vault SoT + 可選 Web 儀表板匯出。

---

## 3. 模組詳細規格（Module Specifications）

### 3.1 第一階段：Mnemosyne（記憶女神：基石與輸入）

**神話隱喻：** 挖掘「記憶之泉」，確保所有資料都能被隨時喚醒。Mnemosyne 是九位繆思的母親——沒有記憶的積累，就沒有靈感的誕生。

**角色定位：** AI_LLM_Wiki 核心處理器。

**功能描述：** 自動掃描、歸納使用者的碎片資訊、原始素材與每日意識流寫作，建立高度結構化的底層知識庫。

**AI／流程運作機制：**

- **無阻力擷取：** 接收零散文本、筆記、日誌，初步清洗與去冗餘。
- **標準化編譯：** 將碎片轉為標準 Wiki 條目格式，知識粒度均勻。
- **基礎網絡建構：** 建立概念間第一層索引，為後續靈感碰撞準備「彈藥」。

### 3.2 第二階段：Muse（繆思女神：洞見與啟發）

**神話隱喻：** 將沉睡的記憶轉化為閃現的靈感，提供創新的「可能性」。

**角色定位：** AI_Insight 靈感引擎。

**功能描述：** 跳脫節點思維，專注於「連結」。主動掃描 Mnemosyne 的記憶，執行 Cross-pollination（異花授粉）與深層連結探索。

**AI 運作機制：**

- **語義碰撞：** 主動提示跨時間／跨主題的邏輯重疊或同構性。
- **意外連結（Serendipity）：** 針對孤立「孤兒筆記」強制配對，發掘看似無關概念背後的同構性。
- **三層深度漫遊：** 每次觸發沿知識網走三層深，提取超越表象的洞見提案。

### 3.3 第三階段：Metis（機智女神：規劃與落地）

**神話隱喻：** 將靈感從奧林帕斯降落到凡間具體執行——秩序（Kosmos）與可追蹤的權責轉化。

**角色定位：** AI_Strategy 策略軍師。

**功能描述：** 接收 Muse 產出的洞見，轉化為現實世界的 Action Plan 與工作流。

**AI 運作機制：**

- **結構化拆解：** 抽象靈感 → OKR 或 WBS。
- **落地指標（KPIs）：** 進度追蹤表；每任務 Definition of Done。
- **風險評估（紅隊）：** Devil's Advocate——潛在障礙、資源缺口、優缺點。
- **動態提醒與護欄：** 可結合身心狀態數據，過載時建議調整排程（規格見 [`metis-action-plan-spec.md`](metis-action-plan-spec.md)）。

---

## 4. 系統指令集映射（Command Palette Integration）

原有 **12 項系統指令** 融入三神祇管轄範圍，形成連續作業介面（實作可為 Obsidian 外掛、Cursor 指令或腳本入口；**語意對標**如下）。

### 【Mnemosyne｜記憶指令】（數據錄入與基礎建構）

| 指令 | 用途 |
|------|------|
| `/wiki-import` | 匯入原始素材並啟動基礎編譯 |
| `/journal-write` | 傾倒大腦快取，紀錄意識流 |
| `/wellness-log` | 紀錄能量、情緒與基礎數據 |

### 【Muse｜靈感指令】（連結、分流與碰撞）

| 指令 | 用途 |
|------|------|
| `/journal-route` | 日記與碎片語義分流，提取知識精華 |
| `/wiki-link` | 對指定節點觸發深層關聯探索 |
| `/wiki-orphan` | 異花授粉：強制配對孤兒筆記 |
| `/wiki-graph` | 視覺化圖譜，展示跨界碰撞結果 |

### 【Metis｜落地指令】（專案執行與風險控管）

| 指令 | 用途 |
|------|------|
| `/project-new` | 將 Muse 洞見轉為專案（OKR／WBS 檔案） |
| `/project-start` | 啟動工作前強制思考軌跡（思考可視化） |
| `/project-review` | 收工結算，更新 KPIs 與 DoD |
| `/project-dashboard` | 全局策略地圖與進度儀表板 |
| `/wellness-report` | 風險評估報告（進度風險與身心耗損警告） |

---

## 5. 後續開發藍圖（Roadmap）

與 [`stages.md`](stages.md)、[`tasks.md`](tasks.md) 並讀；以下為敘事版週期對標。

| Phase | 週期（敘事） | 重點 |
|-------|----------------|------|
| Phase 1 | Week 1–2 | Wiki 導入 Obsidian Vault 體驗一致化；開發「三層深度連結」腳本（LLM API 整合）→ 對應 Mnemosyne→Muse 橋接 |
| Phase 2 | Week 3–4 | 實作 `/project*` 指令集與三文檔模板（OKR／WBS／儀表板）→ Metis 最小可用 |
| Phase 3 | Week 5–6 | 日記撰寫介面與語義分流引擎（Prompt 調校）；個人身心監控機制與 `/wellness-*` 閉環 |

**備註：** 實際排程以 `tasks.md` 階段與資源為準；本藍圖為產品敘事節奏，不作為硬性截止承諾。

---

最後更新：2026-04-14
