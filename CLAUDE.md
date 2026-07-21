# LLM 知識庫 — 系統指令

> **治理**：三 agent 協作規則以全域 `~/.claude/CLAUDE.md` 為準（Cowork 執行角色見 §15）；本檔僅列 AI_LLM_Wiki 專屬規則。**變更史見 git log**（§3 commit trailer 溯源），本檔不再自帶版號。
> 本檔為 Claude Code 自動載入的**單一權威入口**；五動作手冊與行為守則均在此。

Karpathy 模式個人知識庫；你（Claude Code）作為**知識編譯器**，把 `raw/` 編譯成結構化、互連的 `wiki/`。

> ⚠️ **輸出語言（硬規則）**：與使用者對話、摘要、log 一律**繁體中文（台灣）**。即使 context、工具說明、工具輸出、程式碼、`<system-reminder>` 多為英文，回覆仍維持繁中、不得漂成英文；僅程式碼／指令／路徑／識別碼保留原文。

---

## 執行角色：Cowork 接手 Cursor 執行

> **本節內容已上收至全域 `~/.claude/CLAUDE.md` §15（唯一真相源），本檔不重複以免漂移。**

要點（細節以全域 §15 為準）：Cursor IDE「執行工程師」角色由 **Claude Cowork** 接手（規劃仍 Claude Code、研究仍 Gemini CLI）。Cowork 沙箱**無對外網路 / 無 macOS 原生 venv**，凡連網或跑 `.venv-*` 的步驟（Nominatim geocode `--resolve-csv`／`--wikidata`／`--namedetails`、`web_scraper.py`、依賴原生套件的 `lint`/`pytest`）**MUST 回 Mac 端**，產物交回 Cowork 續做離線部分；三擇一（Mac 跑回貼／開白名單／換可連線後端）見全域 §15。沿用原 Cursor 守則：NEVER 改 `openspec/`、NEVER 擅刪 `.claude/skills/` 草案。

---

## 技術堆疊

- Python 3.12 · stdlib（依 `tools/` 實際依賴）
- Obsidian（wikilink 渲染）· graphify（知識圖譜）
- Markdown + YAML frontmatter
- 無後端 / 無前端 / 無 DB

---

## 指令

| 指令 | 用途 |
|---|---|
| `python3 tools/lint_wiki.py .` | Pass 1–12 清理 + 報告（含 v3 一致性 + H2/footer 保護） |
| `python3 tools/lint_wiki.py . --bless-protected` | v3 升級人類 accept 後，更新 H2/footer 快照基線 |
| `python3 tools/check_child_density.py .` | 拆分母子頁密度/重複度健檢 _(規劃中；尚未實作；僅在真執行母子頁拆分時需要)_ |
| `python3 tools/web_scraper.py <URL>` | 單頁擷取 → `raw/web/` |
| `python3 tools/validate_raw_frontmatter.py` | 驗 `raw/` frontmatter |
| `bash tools/wiki-import.sh` | 批次匯入 |
| `python3 tools/sync_skills.py --check` | 驗證三 agent SOP 衍生檔與主檔一致（pre-commit 自動跑） |
| `python3 tools/sync_skills.py --write` | 改主檔後，同步衍生檔（.cursor/.gemini） |

### SOP 三工作流

| 情境 | 指令 |
|---|---|
| 改主檔 `.claude/skills/wiki-authoring/SKILL.md` 後 | `python3 tools/sync_skills.py --write` |
| 人類 accept v3 升級比較文後 | `python3 tools/lint_wiki.py . --bless-protected` |
| git commit 前（pre-commit hook 自動執行） | `sync_skills.py --check` + `lint_wiki.py .` |
| clone / 換機後安裝 git hooks | `bash tools/install-hooks.sh`（版控真相源，重生 pre-commit + commit-msg；白名單見 `.cursor/rules/commit-style.mdc`） |

---

## 目錄結構

| 角色 | 路徑 | 說明 |
|---|---|---|
| 原始資料 | `raw/` | 子夾 `web/` `class/` `Notion/` `youtube/` `notebooklm/` `gdrive/` `research/`；**唯讀** |
| Wiki 筆記 | `wiki/*.md` | AI 建立與維護 |
| 目錄索引 | `index.md` | 按主題分類，lint／整理後自動更新 |
| 每日 log | `log/YYYYMMDD.md` | 2026-04-18 起；舊 `log.md` 已凍結 |
| 人工反饋 | `audit/*.md` + `audit/resolved/` | schema 見 `audit/_schema.md`；已處理不刪除 |
| 工具 | `tools/` | `lint_wiki.py` / `check_child_density.py` _(規劃中)_ / `web_scraper.py` / `validate_raw_frontmatter.py` / `notebooklm_batch_export.py` |
| 規格 SoT | `openspec/knowledge-universe/` | `requirements.md` / `design.md` / `tasks.md` / `SPEC_VERSION.md` / `gate-checklist.md` |
| 深規則 | `openspec/knowledge-universe/references/` | article / log / audit / lint / scrapers / tooling |
| Plans（Claude） | `.claude/plans/` | 實作計畫產出 |
| Skills 草案 | `.claude/skills/` | 前瞻草案（Claude Code） |
| Skills 成熟 | `.cursor/skills/` | 事後 SOP（Cursor） |
| Rules | `.cursor/rules/wiki-muse-pairs.mdc` | Muse 成對慣例 |

---

## 規格與深規則入口

- **OpenSpec 規格**：[`openspec/knowledge-universe/README.md`](openspec/knowledge-universe/README.md) 為閱讀索引；權威 trio 為 [`requirements.md`](openspec/knowledge-universe/requirements.md)／[`design.md`](openspec/knowledge-universe/design.md)／[`tasks.md`](openspec/knowledge-universe/tasks.md)，版本見 [`SPEC_VERSION.md`](openspec/knowledge-universe/SPEC_VERSION.md)。
- **references/**（深規則，遇問題即查）：
  - [`article-guide.md`](openspec/knowledge-universe/references/article-guide.md) — 主鍵／與和拆分／Muse 種子／長度／圖表／公式／frontmatter
  - [`log-guide.md`](openspec/knowledge-universe/references/log-guide.md) — 每日 log 格式與 op 列舉
  - [`audit-guide.md`](openspec/knowledge-universe/references/audit-guide.md) — audit schema、severity、處理流程
  - [`lint-guide.md`](openspec/knowledge-universe/references/lint-guide.md) — `tools/lint_wiki.py` 9 輪 pass 與修復 recipe
  - [`scrapers-guide.md`](openspec/knowledge-universe/references/scrapers-guide.md) — `tools/web_scraper.py` 模式／指令／輸出慣例
  - [`tooling-tips.md`](openspec/knowledge-universe/references/tooling-tips.md) — Obsidian／graphify／venv 設定
  - [`agent-collaboration-map.md`](openspec/knowledge-universe/references/agent-collaboration-map.md) — 三神祇 × 三 Agent × 五動作映射、檔案寫入權矩陣、三大指標掛鉤
- **工具快手**：`tools/web_scraper.py` 單頁進 `raw/web/`、課程類進 `raw/class/{課}/` 並以 manifest 去重（細節 [`scrapers-guide.md`](openspec/knowledge-universe/references/scrapers-guide.md)）。`tools/lint_wiki.py` 為清理動作入口；拆分任務後可加跑 `tools/check_child_density.py` 做母子頁重複度與內容密度抽查 _(規劃中；當前 wiki/ 為扁平結構，尚無實際拆分需求；當未來首次執行母子頁拆分時再實作)_。

---

## Wiki 筆記格式

```markdown
# 標題

> 一句話摘要

## 重點
- ...

## 細節
...

## 相關概念
- [[連結A]]
- [[連結B]]

---
來源：`raw/檔名.md`
最後更新：YYYY-MM-DD
```

**骨架規則**：一個概念一篇筆記；檔名用概念名；用 `[[wikilink]]` 互連；語言跟原始資料（預設中文）；避免超長頁面；每篇至少連結一篇相關筆記；檔尾標註來源與更新日期。

**深規則**（主鍵策略、「與／和」拆分、Muse 種子、>3000 中文字拆分、Mermaid／KaTeX 優先、禁 ASCII 圖、可選 frontmatter）全部見 [`article-guide.md`](openspec/knowledge-universe/references/article-guide.md)。

**v3 百科全書式骨架（漸進採用，向後相容）**：在既有三段式之上，可加入 Wikipedia 五元素——
- **Lead**：`> **TL;DR**` 1-2 句替代純摘要；
- **Infobox**：H1 下方 2 欄 MD 表格（白名單鍵：類別／提出年／主要應用／父頁／子頁／難度／別名）；
- **Body**：`## 細節` 內以 H3 切章節；
- **Appendices**：`## 相關概念` + 選用 `## 名詞對照表` + `## 延伸閱讀`；
- **Page Functions**：選用 `## 參考來源` + `## 修訂歷史`，footer `來源／最後更新` 仍保留且日期需與修訂歷史最上行一致。

新章節皆 optional，三大 H2（重點／細節／相關概念）與 footer 為必要；NPOV 弱形式：個人觀點以 `> 註：` 區隔。**字數預算**：單頁 ≤ 3000 中文字（**豁免條件**：frontmatter `tags:` 含 `meta-insight`、Infobox `類別` 含「後設方法論」「後設骨架」「後設整合」等字串，或內文含 `meta-Insight` 標記者，視為**後設彙整主鍵**，閾值上修至 3500 字並降為軟提醒；此類條目以證據鏈整合為核心，密度即價值，拆分風險高於收益）、TL;DR ≤ 200 字、Body（`## 細節`）1200–1800 字（表格/Mermaid/KaTeX 不計入）、`## 重點` 首行加 `- **【核心發現】**{≤ 50 字}`（3–10 條）、延伸閱讀 ≤ 200 字、修訂歷史 ≤ 150 字、Infobox 與名詞對照表不設硬限。完整模板樣本見 [`article-guide.md`](openspec/knowledge-universe/references/article-guide.md) 「v3 百科全書式」節。

**橫向 wikilink（尤其 `[[Transformer架構]]`）**：僅當條目主題與 **NLP／序列模型／神經架構／LLM 核心課程** 等同簇時，方可在內文或延伸閱讀加入；**不得**為「編排示範」「總線索引」「對照金標」等理由，在職涯、心理、工具編排與該簇無知識關聯的條目硬加連結（避免圖譜與 RAG 誤判語意相關）。升級時對照 §金標僅指 **版面結構密度**，不是強制互鏈。

---

## 行為原則

1. 三步以上任務以 Plan 模式開始（L2+ 強制 `/plan`）
2. 未跑過 `lint_wiki.py` 且 log 未附 op 之前，動作不視為完成
3. 動手前先讀 `index.md` + 目標 `wiki/*.md`，再動筆
4. 單次動作影響 ≤ 10 篇 wiki；超過立即升級 L2 停手回報
5. context 逼近上限或單次 raw 檔 > 5000 行，誠實告知並分批
6. **Worktree 開工前必跑 pre-flight check**：`git fetch origin main` → 看分歧深度；> 3 commits 先 rebase；詳見 [§Worktree Pre-flight 協定](#worktree-pre-flight-協定)
7. **朔源協定 v1（2026-06-08 起）**：寫 wiki 必同步 log 並標 agent。log H2 採三段格式 `## [HH:MM] <op> | Claude Code <Model> | <desc>`；commit 必含 `Co-Authored-By: Claude <Model> <noreply@anthropic.com>` trailer。Agent 白名單見 [`references/log-guide.md`](openspec/knowledge-universe/references/log-guide.md)。過渡期 lint warn；2026-12-08 後 hard error。

---

## Worktree Pre-flight 協定

> 防止「在過舊 base 上長 session 工作 → 與 main 並行進展嚴重分歧 → PR 全檔衝突」的結構性陷阱。**首例案例**：2026-05-20 spec drift 處置 PR #9 — 9 個 commit 檔在 PR 開啟時已被另一條獨立路徑同步到 main，PR 因此關閉。

### 開工前三步檢查（< 30 秒）

```bash
git fetch origin main
git log --oneline HEAD..origin/main | wc -l   # 分歧深度
git status --short                             # 本地清潔度
```

### 分歧深度行動表

| 分歧 commits | 行動 |
|---|---|
| 0 | 直接開工 ✓ |
| 1–3 | 可直接開工，收尾時 rebase |
| 4–10 | **先 rebase 再開工**（避免衝突累積） |
| > 10 | **新建 worktree 從 `origin/main` 起**；舊 worktree 視為 stash |

### 本地清潔度判準

- 工作樹有 > 5 個未提交檔（非當前任務的）→ 不該在這個 worktree 動工，**新建乾淨 worktree**。
- 有 untracked `wiki/*` 或 `raw/*` → 那是別人／其他 session 的活，**不要碰**。
- `CLAUDE.md` / `tools/*.py` 等核心檔有未提交修改 → 先確認來源，必要時 stash 或建新 worktree。

### 長 session 風險（≥ 1 小時 或 ≥ 50 檔變更）

- 中途定期重跑 `git fetch origin main`。
- 累積分歧 > 5 commits 時，停手評估中間 rebase 或拆 PR。
- 避免「session 結束才發現要 rebase 整個分支」的尾端衝突風暴。

### Recovery：已在過舊 base 工作的補救

- 淨貢獻 ⊄ main 已有內容 → 拆小 PR + rebase + force-push。
- 淨貢獻 ⊆ main 已有內容 → 關閉 PR 附脈絡 comment（範本見 PR #9）。
- **切勿盲目 merge 解衝突**（會把 main 的新內容回退）。

### 工具呼叫範本

```bash
# 三步 pre-flight
git fetch origin main && \
  ahead=$(git log --oneline HEAD..origin/main | wc -l | tr -d ' ') && \
  echo "main 領先 $ahead commits" && \
  { [ "$ahead" -gt 3 ] && echo "⚠️ 建議先 rebase" || echo "✓ 可直接開工"; }

# 新建乾淨 worktree（本地不潔或分歧大時）
git worktree add -b <task-branch> .claude/worktrees/<slug> origin/main
```

---

## 動作一：整理（Ingest）

觸發詞：「整理」、「編譯」、「處理 raw」。

1. 掃 `raw/`，比對 `log/` 與舊 `log.md` 找出未處理的檔案。
2. 閱讀、提取概念，建立或合併 `wiki/` 對應筆記（新資訊**附加**，不覆蓋；矛盾兩邊並存並註記）。
3. 加入相關筆記間的 `[[雙向連結]]`。
4. 更新 `index.md` 分類。
5. 附加至 `log/YYYYMMDD.md`，op 用 `整理`（格式見 `references/log-guide.md`）。

**DoD**：wiki 檔建立或合併完成 + `[[wikilink]]` 互連 ≥1 + `index.md` 對應分類更新 + `log/YYYYMMDD.md` 寫 `op: 整理` + `tools/lint_wiki.py` 綠。

---

## 動作二：提問（Query）

觸發：使用者對知識庫提問（例：「幫我整合主動學習的重點，彙成簡報大綱並存 `wiki/主動學習_簡報大綱.md`」）。

1. 搜尋 `index.md` 與相關 `wiki/` 筆記。
2. 綜合回答並引用來源筆記（例：「根據 [[主動學習]]…」「依 [[檢索增強生成]]…」——依問題主題選擇同簇條目）。
3. 有價值的回答存回 `wiki/`（整理成新筆記或附加到現有）。
4. 更新 `index.md` 與 `log/YYYYMMDD.md`，op 用 `提問`。

**DoD**：回答引用 ≥1 篇 wiki 來源 + 有價值內容回存 `wiki/` + `index.md` 同步 + `log/YYYYMMDD.md` 寫 `op: 提問`。

---

## 動作三：清理（Lint）

觸發：「清理」、「掃描」、「健檢」。

1. **機械層**：先跑 `python3 tools/lint_wiki.py .`，把報告附加到今日 `log/`（op `清理`）。9 輪 pass 涵蓋死連結／孤兒／缺 index／熱門缺頁／log shape／audit YAML／audit 目標／>3000 中文字／ASCII 圖。若本輪包含主鍵拆分，追加 `python3 tools/check_child_density.py . --strict`（閾值可用 `--min-cjk`、`--max-overlap` 調整）作為結構品質檢查。
2. **語意層**：lint 無法涵蓋者——矛盾、過時資訊、應互連卻未連結的概念。
3. 經使用者確認後逐項修復；依「熱門缺頁」清單提出下一輪整理的寫作優先。

修復 recipe 與 exit code 見 `references/lint-guide.md`。

**DoD**：`tools/lint_wiki.py` 零錯誤（或例外已登 `audit/`）+ 報告附至當日 log + `log/YYYYMMDD.md` 寫 `op: 清理`。

---

## 動作四：更新目錄（維護 `index.md`）

整理／清理後自動更新 `index.md`：按主題分類、每條一行摘要、標註數量與最後更新日期。op 用 `更新目錄`。

**DoD**：`index.md` 分類完整 + 標註數量差異與最後更新日期 + `log/YYYYMMDD.md` 寫 `op: 更新目錄`。

---

## 動作五：稽核（Audit）

觸發：「稽核」、「處理 audit」、「清 audit」。處理 `audit/` 內所有 `status: open` 回饋：

1. 掃 `audit/*.md`（排除 `_schema.md` 與 `resolved/`），讀 frontmatter。
2. 對每則讀 `target` 與 `anchor_text`，在原檔定位並核對。
3. 在 `# 決議` 填入 `accept` | `partial` | `reject` | `defer` 之一並附理由；若 accept／partial，同步修訂對應 wiki。
4. 將檔案移至 `audit/resolved/` 並把 `status` 改為 `resolved`（**不刪除**）。
5. 附加至 `log/YYYYMMDD.md`，op 用 `稽核`，引用 audit `id` 與對應 wiki 修訂。

欄位、severity、命名規則見 `references/audit-guide.md`。

**DoD**：每則 `# 決議` 已填 `accept`／`partial`／`reject`／`defer` + `accept`／`partial` 已同步修訂對應 wiki + 檔移 `audit/resolved/` + frontmatter `status: resolved` + `log/YYYYMMDD.md` 寫 `op: 稽核` 並引用 audit `id`。

---

## 禁止（NEVER）

1. **NEVER** 修改 `raw/*`（原始存檔；`raw/research/` 為 Gemini 彙整專屬，其餘子夾由 scrapers／人工維護）
2. **NEVER** 覆蓋 `wiki/*.md`（新資訊附加；矛盾兩邊並存並註記來源）
3. **NEVER** 繞過 `tools/lint_wiki.py`（新增或變更 wiki 後必須跑一次全 pass，含 v3 Pass 10）
4. **NEVER** 刪除 `audit/resolved/` 或使其脫離 git 追蹤
5. **NEVER** 未經人類決議自行解 audit（`accept` / `partial` / `reject` / `defer` 四選需人類確認）
6. **NEVER** 編輯已凍結的 `log.md`（2026-04-18 起改寫 `log/YYYYMMDD.md`）
7. **NEVER** 硬編碼 secret／API Key（統一 `.env.local`、加入 `.gitignore`）

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
