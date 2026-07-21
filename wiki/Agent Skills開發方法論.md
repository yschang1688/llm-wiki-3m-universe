# Agent Skills 開發方法論

> Google Gemini 團隊主管 Addy Osmani 開源的 Agent Skills：把資深工程師的軟體開發紀律，編碼成 6 階段 × 20 核心技能的標準化工作流——`/spec → /plan → /build → /test → /review → /ship`，讓 AI coding 從「能跑但不可維護」升級到「可維護、可擴展、可上線」的專業等級。

## 重點

- **核心定位**：把工程紀律「**產品化**」，不再依賴語言模型即時推論——將最佳實踐編碼為可重複使用的 skill
- **解決問題**：傳統 AI coding 工具（Claude Code、Cursor）生成程式碼缺乏一致流程與品質標準，容易「能跑但不可維護」
- **6 階段開發鏈**：Define → Plan → Build → Verify → Review → Ship；每階段對應一個簡短指令（`/spec`、`/plan` 等）
- **約 20 個核心技能**散布於 6 階段
- **Context Engineering**：透過 skill 控制 AI 在不同階段看到哪些資訊，避免資訊過載或不足

## 細節

### 6 階段開發鏈

| 階段 | 指令 | 階段重點 |
|------|------|---------|
| **Define**（需求定義）| `/spec` | 強調先寫 Spec |
| **Plan**（任務規劃）| `/plan` | 拆解任務、依賴排序 |
| **Build**（實作）| `/build` | **Incremental implementation**——小步迭代、測試驅動 |
| **Verify**（驗證）| `/test` | **結構化 debugging** 找出問題根因 |
| **Review**（審查）| `/review` | 可讀性、安全性、效能的全面 code review |
| **Ship**（上線）| `/ship` | 確保部署具備 rollback 與監控機制 |

### 核心價值

#### 1. 工程紀律產品化

不再「希望 AI 自己會記得最佳實踐」，而是**把紀律外化成 skill**——AI 在不同情境下自動選擇合適的做法。

#### 2. Context Engineering

AI 輸出品質取決於**提供給模型的上下文是否精準、結構化**：
- 透過 skill 設計，控制 AI 在不同階段看到哪些資訊
- 避免資訊過載（context 太雜亂）或不足（缺關鍵背景）

#### 3. 開發者體驗簡化

輸入簡短指令（`/spec` 等）即觸發背後複雜的技能組合：
- 大幅降低使用門檻
- 提升一致性
- 隱藏複雜度

### 整體意義：新型態的開發方法論

> Agent Skills 並不是單純的工具，而更像是一種**新型態的開發方法論**——將「工程最佳實踐」與「AI 自動化能力」結合，讓開發流程從**人主導 → 人與 AI 協作**。

### 效益階梯

| 開發模式 | 產出品質 |
|---------|---------|
| 純 Vibe Coding | 能跑（運氣好的話）|
| 加上 IDE + 反饋迴路 | 能跑且測試通過 |
| **導入 Agent Skills** | **可維護、可擴展、可上線**（專業等級）|

### 對應 [[AGENTS.md倉庫設計]]

Agent Skills 是**動詞**（流程編排），[[AGENTS.md倉庫設計]] 是**名詞**（倉庫狀態）——兩者互補：
- 倉庫先 AI-Ready，Agent Skills 才能發揮
- Skill 在執行時讀取倉庫 context，倉庫品質決定 Skill 效果

## 相關概念

- [[Agent Skills設計模式]]
- [[Claude Skill蒸餾風潮]]
- [[AGENTS.md倉庫設計]]
- [[Claude Code專業開發實踐]]
- [[Vibe Coding]]
- [[Agentic Engineering四層架構]]

---
來源：`raw/Notion/Addy Osmani Agent Skills開源.md`
最後更新：2026-04-19
