# LLM Wiki · 3M Universe（知識宇宙）

> 一套**多 Agent 協作的知識治理系統**——不是筆記合集，而是把「AI 編譯知識」這件事本身當成工程問題來設計：任務分級、職責邊界、規格仲裁、朔源協定，全部可稽核、可重現。
>
> 本 repo 是私人知識庫 [AI_LLM_Wiki](.) 的公開精選子集：51 篇 LLM／深度學習技術條目 + 完整治理框架。

---

## 這是什麼

我用 Claude Code 作為「知識編譯器」，把課程筆記、論文摘要、研究資料等原始材料，持續編譯成一個結構化、互連的 Obsidian 知識庫。過程中遇到的真實問題——AI 產出品質不穩定、多次編輯後規格漂移、無法追溯「這篇是誰寫的」——逼出了一套治理制度，而不是單純的 prompt 技巧。

**核心信念**：知識庫的品質問題，本質上是**協作與治理問題**，跟團隊工程管理是同一類問題。

## 三 Agent 分工架構（3M / 三神祇）

| 代號 | 角色 | 職責 | 產出 |
|---|---|---|---|
| **MNE**（Mnemosyne） | 資料攝取與記憶 | 把原始素材編譯成結構化條目 | `wiki/*.md` |
| **MUS**（Muse） | 語意連結與分流 | 建立條目間 `[[wikilink]]`、偵測孤兒頁 | 知識圖譜 |
| **MET**（Metis） | 策略與品質治理 | 規格仲裁、進度追蹤、風險登記 | `openspec/**` |

三者對應到具體 AI Agent（Claude Code 規劃／執行 Agent 落地／研究 Agent 蒐集），詳細分工邊界見 [`CLAUDE.md`](CLAUDE.md) 與 [`AGENTS.md`](AGENTS.md)。

## 治理機制（這是重點，不是內容本身）

- **任務分級 L0–L3**：從 5 行內的微修到跨服務架構變動，各級有明確的完成定義（DoD）、模型選用與人類介入節點——見 [`CLAUDE.md` §2](CLAUDE.md)
- **Handoff 協定**：跨 Agent 交接必須留痕（誰在何時做了什麼決策），對應到 commit trailer 與 log 格式，讓「這篇是誰寫的」永遠可回答
- **規格偏離仲裁**：執行者發現規格有問題時，不能直接改規格，而是寫偏離報告，由規劃者定期裁決——避免「先斬後奏」侵蝕文件與程式碼的一致性
- **止損協定**：測試連續失敗 3 次、或規劃兩輪仍無解，強制停手升級，禁止無限重試燒 token
- **OpenSpec 規格三件組**：`requirements.md` / `design.md` / `tasks.md`，變更需求前先寫規格，而非邊做邊想——見 [`openspec/knowledge-universe/`](openspec/knowledge-universe/)

完整制度設計見 [`CLAUDE.md`](CLAUDE.md)（全域協作核心）與 [`openspec/knowledge-universe/`](openspec/knowledge-universe/)（本專案規格庫）。

## 自動化品質把關

[`tools/lint_wiki.py`](tools/lint_wiki.py)（1,000+ 行）對每篇條目跑 9 輪檢查：死連結、孤兒頁、缺目錄索引、熱門缺頁、log 格式、字數預算、ASCII 圖表禁令等——確保 AI 產出的內容不會因為「看起來合理」就蒙混過關。

```bash
python3 tools/lint_wiki.py .          # 全 pass 掃描 + 報告
```

## 內容樣本：51 篇 LLM／深度學習技術條目

每篇採用「Wikipedia 式」v3 骨架——TL;DR、Infobox（類別/難度/父子頁關係）、分章節細節、相關概念互連——而非流水帳筆記。完整索引見 [`index.md`](index.md)，涵蓋：

- **Transformer 與注意力機制**（11 篇）：架構、QKV、FlashAttention、Mamba 等
- **LLM 基礎與演進**（7 篇）：GPT、BERT、湧現能力、模型演進史
- **訓練與對齊**（12 篇）：預訓練、LoRA、RLHF、梯度下降、DeepSeek R1 推理訓練
- **RAG／檢索／向量**（6 篇）：檢索增強生成、向量資料庫、Embeddings
- **神經網路基礎**（4 篇）：CNN、RNN、GNN、知識蒸餾
- **生成式／擴散／多模態**（4 篇）：擴散模型、LDM、多模態 AI
- **Agent／工程／評測**（7 篇）：AI Agent 機制、MCP 協議、Context Engineering、評測陷阱

## 技術堆疊

Python 3.12（stdlib）· Obsidian（wikilink 渲染）· Markdown + YAML frontmatter · 無後端 / 無資料庫——刻意保持輕量，治理邏輯不依賴框架鎖定。

## 目錄結構

```
CLAUDE.md / AGENTS.md      多 Agent 協作全域規則（唯一權威入口）
openspec/knowledge-universe/  規格三件組（requirements/design/tasks）
tools/lint_wiki.py         品質把關自動化
wiki/*.md                  51 篇精選技術條目（v3 骨架）
index.md                   分類索引
```

---

> 完整版私人知識庫（1,300+ 條目、含個人研究/生活筆記）不對外公開；本 repo 為求職展示精選的技術子集與治理框架。
