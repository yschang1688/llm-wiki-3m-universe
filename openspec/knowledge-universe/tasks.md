# Tasks — 知識宇宙系統（OpenSpec SDD）

> **v1.0-baseline** · 對應 [`requirements.md`](requirements.md)、[`design.md`](design.md)  
> 方法：proposal → apply（requirements/design/tasks）→ archive

**任務編號：** T-0001～T-0065（共 **65** 項；T-0059／T-0060／T-0061 拆細子任務見 Phase 4）

---

## Phase 0：規格凍結與基線（T-0001～T-0008）

- [x] **T-0001**：建立並凍結 [`SPEC_VERSION.md`](SPEC_VERSION.md)（`v1.0-baseline`）
- [x] **T-0002**：凍結 [`requirements.md`](requirements.md)（7 US + 3 NFR + 附錄 A 十二指令）
- [x] **T-0003**：凍結 [`design.md`](design.md)（Pipeline + Pantheon + LLM 路由 + Gates 索引）
- [x] **T-0004**：建立本檔 **65** 項任務清單並與版本綁定
- [x] **T-0005**：建立 [`gate-checklist.md`](gate-checklist.md)（Gate A/B 獨立勾選）
- [x] **T-0006**：更新 [`README.md`](README.md)（版本、閱讀順序、`SPEC_VERSION` / `gate-checklist`）
- [x] **T-0007**：[`proposal.md`](proposal.md) 與 `SPEC_VERSION`／`pantheon-pkm.md` 交叉引用一致
- [x] **T-0008**：規格評審紀錄（會議或書面）— *可選；通過後勾選*

**DoD：** 無開放之「版本漂移」— 變更須標新版本並更新 `SPEC_VERSION.md`。

---

## Phase 1：Mnemosyne（記憶與輸入）— T-0009～T-0028

- [x] **T-0009**：建立 `raw/journal/` 與說明（`/journal-write` 落地）
- [x] **T-0010**：建立 `raw/wellness/` 與說明（`/wellness-log` 落地）
- [x] **T-0011**：建立 `export/web-dashboard/.gitkeep`（匯出層預留，對齊 US-007）
- [x] **T-0012**：新增 [`templates/journal-write.stub.md`](templates/journal-write.stub.md)
- [x] **T-0013**：新增 [`templates/wellness-log.stub.md`](templates/wellness-log.stub.md)
- [x] **T-0014**：新增 [`router/llm-routing.md`](router/llm-routing.md)（LLM 路由策略）
- [x] **T-0015**：新增 [`commands/wiki-import.md`](commands/wiki-import.md) + [`tools/wiki-import.sh`](../../tools/wiki-import.sh)（`/wiki-import` 最小閉環）
- [x] **T-0016**：新增 [`phase1-ac.md`](phase1-ac.md) 並執行**第一輪**勾選
- [x] **T-0017**：實作或文件化 **metadata 抽樣檢核**（N=20，一致率計算方式）— [`tools/validate_raw_frontmatter.py`](../../tools/validate_raw_frontmatter.py)、[`metadata-validation.md`](metadata-validation.md)
- [x] **T-0018**：`ingest-cli` 與 `design` §5 持續對齊（欄位／主標 C／噪音裁切）— [`ingest-cli-design-alignment.md`](ingest-cli-design-alignment.md)
- [x] **T-0019**：ingest-service 寫入契約落地追蹤（`ingest_path=ingest-service`）— [`ingest-service-contract-status.md`](ingest-service-contract-status.md)（實作仍待 ingest-service Repo）
- [x] **T-0020**：雙路徑去重手動／半自動驗收 — [`INTEGRATION_TEST_WEB.md`](INTEGRATION_TEST_WEB.md) §B 已補第二路徑步驟
- [x] **T-0021**：NotebookLM 批次與 `raw/notebooklm/` 命名策略一致化 — [`raw/notebooklm/README.md`](../../raw/notebooklm/README.md)
- [x] **T-0022**：Notion 匯出路徑與 page id 規則抽樣驗證 — [`notion-ingest-conventions.md`](notion-ingest-conventions.md)
- [x] **T-0023**：Google Drive 連接器 PoC（類型與轉換表）— [`gdrive-youtube-poc.md`](gdrive-youtube-poc.md) §Drive
- [x] **T-0024**：YouTube metadata／逐字稿目錄與節流策略 — [`gdrive-youtube-poc.md`](gdrive-youtube-poc.md) §YouTube、[`raw/youtube/README.md`](../../raw/youtube/README.md)
- [x] **T-0025**：`index.md` 多來源標籤規則（若需要）文件化 — [`index-md-conventions.md`](index-md-conventions.md)
- [x] **T-0026**：「整理」流程與 `log.md` 多來源 id 全鏈路可追溯 — [`ingest-traceability.md`](ingest-traceability.md)
- [x] **T-0027**：更新 [`mnemosyne-stage1-audit.md`](mnemosyne-stage1-audit.md) 至最新基線（2026-04-14）
- [x] **T-0028**：**Gate A** 預演：抽樣與證據包 — [`gate-a-evidence-pack.md`](gate-a-evidence-pack.md)

**DoD（階段，與 [`stages.md`](stages.md) Stage 1 完全一致）：**

- 至少 **3 種來源**可穩定落地；
- **metadata 一致率 ≥ 95%**（抽樣範圍與計算方式以 [`metadata-validation.md`](metadata-validation.md)、[`mnemosyne-stage1-audit.md`](mnemosyne-stage1-audit.md) 為準）；
- **`source_type` + `source_id` 去重**與重跑 **idempotency** 可驗證（見 [`design.md`](design.md) §3.3、[`INTEGRATION_TEST_WEB.md`](INTEGRATION_TEST_WEB.md)）；
- **`log.md` 可回推來源檔**（見 [`ingest-traceability.md`](ingest-traceability.md)）。

**是否通過 Stage 1／Gate A，以 [`gate-checklist.md`](gate-checklist.md)（Gate A）與 [`mnemosyne-stage1-audit.md`](mnemosyne-stage1-audit.md) 為準**；本節任務全數勾選代表 **交付物已就緒**，**不**等同審計上已宣告整條 DoD 全部達成（見 audit「缺口清單」）。

---

## Phase 2：Muse（洞見）— T-0029～T-0043

- [x] **T-0029**：定義 Insight schema（summary、reason、confidence、evidence_links）→ `muse-insight-spec.md` v0.1（2026-05-01）
- [x] **T-0030**：建立 cross-pollination 掃描流程（3-hops）→ **全 scope 完成（2026-05-09）**：層 1 cross-domain ✅ + shared-evidence proxy（+0.10 若 ≥3）✅ + 層 2 same-cluster unidirectional ✅（183 對候選）+ `--validate-batch <dir>` 子命令 ✅（batch-06 命中 5/5 = 100%）；`tools/muse_scanner.py` 完整實作
- [x] **T-0031**：建立孤兒頁配對流程（orphan rescue）→ `tools/muse_scanner.py --orphan-rescue` ✅；spec [`muse-orphan-rescue-spec.md`](muse-orphan-rescue-spec.md) v1.0；首次基線 2/913 孤兒（0.2%），手動分流預計 batch-07
- [x] **T-0032**：定義採納流程（adopted/watch/rejected）→ `muse-insight-spec.md` §11（v0.2, 2026-05-01）；首批 5/5 全採納閉環驗證
- [x] **T-0033**：建立置信度閾值與降噪規則（版本號）→ [`confidence-threshold-spec.md`](confidence-threshold-spec.md) v1.0（2026-05-09）：三檔 confidence + N-1～N-6 降噪規則 + 4 階段升級門檻 + 4 觀測指標；scanner 內建 `--min-shared K`；亦於 [`muse-prompts/v2.md`](muse-prompts/v2.md) 表頭落地閾值參數
- [x] **T-0034**：Prompt／指令版本庫（可重現）→ `muse-prompts/v1.md`（2026-05-01）
- [x] **T-0035**：首批 Insight 產出管線（批次腳本或手冊）→ [`commands/insight-pipeline.md`](commands/insight-pipeline.md) v1.0（2026-05-16；端到端 7 步驟：scanner → 覆核 → 寫主文 → 落地 → 審核 → adopted 動作 → 指標+log；對齊 Gate B G-B-2～G-B-5；Session 3e）
- [x] **T-0036**：完成首批 ≥3 則 Insight（跨領域／跨來源／意外連結）→ `audit/insights/2026-05-01-batch-01/`（trend / cross-domain / cross-source 各一；MUS-BATCH-1/2 達標）；達成度延伸至 **6 批 24+ 則**（含 `2026-05-03-meta-batch-01/` meta-Insight 提煉），遠超 baseline（2026-05-17 補註）
- [x] **T-0037**：Insight 審核紀錄模板 → [`templates/insight-review.stub.md`](templates/insight-review.stub.md)（2026-05-16；繼承 [`templates/review-skeleton.md`](templates/review-skeleton.md) §2 五段；Session 3a）
- [x] **T-0038**：與 Obsidian Graph／匯出圖譜對接評估 → [`obsidian-graph-eval.md`](obsidian-graph-eval.md) v1.0（2026-05-19；現況盤點 + 分工建議 + 對接邊界 + 反模式 + 後續鉤子；結論：兩者互補不取代，無需開發整合層；Session 4a-tail）
- [x] **T-0039**：低置信度過濾單元／抽樣測試 → [`tools/test_confidence_filter.py`](../../tools/test_confidence_filter.py)（2026-05-15）；5/5 單元測試通過（N-1/N-2/N-3/強提案門檻/降噪扣分）；全庫抽樣統計 53 主檔 confidence ≥ 0.70 佔 73.6%、< 0.40 佔 **0%**（**N-1 規則 100% 生效**）
- [x] **T-0040**：Muse 觀測指標：採納率、平均引用數（`design` §15）→ [`muse-metrics-spec.md`](muse-metrics-spec.md) v1.0（2026-05-16；合併三處散落定義為單一權威；補邊界情境、批次/全域/季度三粒度、與 Metis 完成率對稱骨架；對稱性稽核缺口 #6 處置；Session 3d）
- [x] **T-0041**：`/wiki-link`、`/wiki-orphan`、`/wiki-graph` 最小實作或執行手冊 → 三命令手冊版上線 [`commands/wiki-link.md`](commands/wiki-link.md)（手冊；機械化 v1.x）、[`commands/wiki-orphan.md`](commands/wiki-orphan.md)（手冊 + `muse_scanner.py --orphan-rescue` 機械化於 T-0031）、[`commands/wiki-graph.md`](commands/wiki-graph.md)（手冊 + `wiki_to_graphify.py` 機械化於 T-0060c）；批次版亦見 [`commands/insight-pipeline.md`](commands/insight-pipeline.md) §11
- [x] **T-0042**：`/journal-route` 語義分流 PoC → [`commands/journal-route.md`](commands/journal-route.md)（2026-05-15）；5 條 PoC 規則表（R1-R5：決策／wellness／學習／情緒／其他）；對接 [[流程顆粒度與決策瓶頸]] #M1 可分類顆粒度範式；機械化分類器留 v1.x
- [x] **T-0043**：**Gate B** 預演（證據包）→ [`gate-b-evidence-pack.md`](gate-b-evidence-pack.md)（2026-05-09）；G-B-1～G-B-5 五項全綠；累積 30 Insight + 2 meta + 採納率 82%；觀測指標全達標；T-0057 可立即簽核

**DoD：** 見 [`mvp-acceptance.md`](mvp-acceptance.md) MUS 區段。

---

## Phase 3：Metis（落地）— T-0044～T-0058

- [x] **T-0044**：Action Plan 模板與 `metis-action-plan-spec.md` 對齊檢查 → 首份 PoC `audit/action-plans/2026-05-01-batch-01/20260501-050000-personal-time-granularity-audit.md`（從 Insight #2 派生）；對稱性稽核 `muse-metis-symmetry-audit.md` 列 8 處缺口
- [x] **T-0045**：Insight → Action Plan 轉換流程 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §2 轉換決策樹（2026-05-09；Insight conf 三檔 + meta-Insight 升級門檻分流）；落地手冊見 [`commands/metis-project.md`](commands/metis-project.md) §1 `/project-new` 三文檔起手 + [`commands/insight-pipeline.md`](commands/insight-pipeline.md) Step 6 adopted 必跑動作；對稱性稽核缺口 #3 已處置
- [x] **T-0046**：紅隊風險與 rollback 欄位必填檢查 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §3 紅隊必填檢查（Risks ≥ 3／Rollback 至少 1／DoD 含反駁 hard requirement）；模板層見 [`metis-action-plan-spec.md`](metis-action-plan-spec.md) §6/§7；註：lint 機械化檢查仍未實作（屬 `tools/lint_wiki.py` Pass 擴充或新 audit 工具範疇）
- [x] **T-0047**：KPI 與 `project-review` 更新機制 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §4 週 retro + 月 review；模板與手冊：[`templates/project-review.stub.md`](templates/project-review.stub.md) §C.1 KPI 實測表 + [`commands/metis-project.md`](commands/metis-project.md) §3.2 KPI 回填 + [`metis-action-plan-spec.md`](metis-action-plan-spec.md) §4.3 status 變更時機
- [x] **T-0048**：trigger → action 提醒表 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §5 五類觸發（T-NEW/T-WEEK/T-BLOCKED/T-DONE/T-DRIFT）
- [x] **T-0049**：`/project-new`、`/project-start`、`/project-review` 最小實作或手冊 → [`commands/metis-project.md`](commands/metis-project.md) v1.0（2026-05-16）；`/project-review` 紀錄走 [`templates/project-review.stub.md`](templates/project-review.stub.md)（與 T-0037 共用 `review-skeleton.md` 骨架；Session 3a）
- [x] **T-0050**：`/project-dashboard` 靜態儀表板雛形 → [`commands/project-dashboard.md`](commands/project-dashboard.md) v1.0（2026-05-16；單一專案視角的 Markdown 切片；與 vault 級 Pantheon Dashboard 分工明確；Session 3c）
- [x] **T-0051**：`/wellness-report` 與 wellness 資料最小欄位 → [`wellness-schema.md`](wellness-schema.md) v1.0 + [`commands/wellness.md`](commands/wellness.md) v1.0（2026-05-16；五指標最小欄位、過載警示四規則、隱私邊界與 Metis 弱耦合；Session 3b）
- [x] **T-0052**：Metis 狀態機（draft/active/blocked/done）稽核 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §6 status 機審計（stale-active / orphan-done / missing-DoD / broken-link 四類漂移檢測）；內部流轉 SOP 見 [`metis-action-plan-spec.md`](metis-action-plan-spec.md) §4 + [`commands/metis-project.md`](commands/metis-project.md) §3.3；symmetry-audit 缺口 #8 已標 ✅
- [x] **T-0053**：與 Web 匯出／任務系統整合評估 → [`integration-eval.md`](integration-eval.md) v1.0（2026-05-16；A 軸不新增匯出格式、B 軸採路徑 1 `.ics` 匯出；明確拒絕雙向同步與 wellness 外傳；Session 3c）
- [x] **T-0054**：Metis 觀測指標：完成率、逾期率（`design` §15）→ [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §7（6 條指標：完成率 ≥ 60% / 逾期率 ≤ 30% / 轉換率 ≥ 30% / 平均週期 ≤ 8 週 / 回流率 ≥ 90% / 反駁比例誠實指標）；對稱骨架見 [`muse-metrics-spec.md`](muse-metrics-spec.md) §3、卡片落地見 [`dashboard-spec.md`](dashboard-spec.md) §2
- [x] **T-0055**：行動方案過度抽象之紅隊測試用例 → [`metis-conversion-workflow-spec.md`](metis-conversion-workflow-spec.md) §8（三紅隊問句：抽象過頭 trap / 缺 KPI trap / 缺 rollback trap）；PoC 範本 #M1 Action Plan 已過三紅隊
- [x] **T-0056**：資源與 API 中斷之降級路徑 → [`degradation-paths.md`](degradation-paths.md) v1.0（2026-05-16；八種中斷情境 D-1～D-8 + 三原則「永不靜默失敗／拒絕污染 SoT／本地優先」+ 各情境 recipe + 降級紀錄格式；新增 log op 鍵 `degrade`；Session 3d）
- [x] **T-0057**：**Gate B** 正式簽核（`gate-checklist.md`）→ 2026-05-09 user 簽核；五項全綠（G-B-1～5），可啟動 Phase 3 Metis MVP 量產
- [x] **T-0058**：Metis MVP Demo 錄影或截圖存證 → [`metis-mvp-demo.md`](metis-mvp-demo.md) v1.0（2026-05-16；五閉環 E1～E5 存證清單；以 commit hash 為錨；含重現性檢查 bash 步驟；錄影／截圖為輔；Session 3e）

**DoD：** 見 [`mvp-acceptance.md`](mvp-acceptance.md) MET 區段。

---

## Phase 4：閉環、可視化、端到端 — T-0059～T-0065

- [~] **T-0059**：retrospective 回流至 `raw` →「整理」路徑文件化（US-006）→ [`retrospective-flow.md`](retrospective-flow.md) v1.0（2026-05-19；端到端流程鳥瞰 + retrospective 格式（frontmatter + 五段主文）+ 整理路徑 + Muse 再觸發 + 觀測指標（閉環率／二階洞見產出率／反駁誠實率）；對齊 US-006 三 AC；Session 4b-tail）。**規格已落地**，但**工具實作 5 缺口未補**（見 T-0059a-e；2026-06-09 PoC 階段 A 手動 dogfood loop 發現）；status 暫 `[~]` 直到 a-e 全綠
  - [x] **T-0059a**：`lint_retrospective` → 已落地為 `tools/lint_wiki.py` Pass 12（commit `24f265d`，2026-06-09）；驗 `raw/retrospective/*.md` frontmatter 必填欄位 + plan_id/insight_id 上游存在性 + author ∈ ALLOWED_AGENTS 白名單；故意拔 plan_id 測試正確抓 error 並可在 commit `40a4c59` 重構後信任（Pass 6→7 改在 Pass 12 之前跑）
  - [x] **T-0059b**：`tools/promote_action_plan.py`（2026-07-07）— 從 retrospective frontmatter `plan_status_after` 反向更新 `audit/action-plans/<id>.md` frontmatter `status` + `### Status 變更紀錄`表 + `## Status`清單；預設 dry-run（`--apply` 才寫）、`--author` 必填且驗 ALLOWED_AGENTS 白名單（朔源協定 v1）；`done_with_caveat` 收斂為 canonical `done` + caveat 註記入變更紀錄（保 enum 純淨）；直接模式 `--plan-id/--status`；內建 `--selftest`（4 cases：映射/白名單/enum/缺檔全綠）。**真 plan 未 promote**（首例 retrospective 標 DEMO 假資料，避免污染 audit；待 owner 產真 retrospective 再跑）。**最小可閉環 MVP 達成**（T-0059a lint + T-0059b promote）
  - [x] **T-0059c**：`tools/update_insight_decision.py`（2026-07-07）— 更新 `audit/insights/<id>.md` frontmatter `confidence`（+ 選用 `status`）+ `## 決議` 段追加 retrospective 後驗註記；**flags 為真相源**（不解析 retrospective 散文表格，避免啟發式脆弱），`--source` 僅作溯源；`--confidence-delta`（下調用負值，clamp [0,1]）/ `--add-decision-note`（必填）/ `--set-status`（enum 驗證）；**紅隊門檻**：`|Δ| ≥ 0.20`（反駁級）需明示 `--allow-rebuttal`；預設 dry-run、`--author` 白名單（朔源協定 v1）；內建 `--selftest`（6 cases：下調/反駁擋/反駁放行/clamp/白名單/缺檔全綠）。**真 Insight 未 apply**（DEMO retrospective，0.55 源自虛構結果，避免污染）
  - [ ] **T-0059d**：`tools/muse_scanner.py --queue-from-retrospective <path>`（**L1**，🟡 中優先級）— 擴 [`muse_scanner.py`](../../tools/muse_scanner.py) 介面，從 retrospective `Unexpected Findings` 段抽 Muse 候選並寫入 `audit/muse-queue/pending.yaml`（新檔，schema 待 §[muse-insight-spec.md](muse-insight-spec.md) 補定）；下次 batch run 從此檔取 seeds
  - [ ] **T-0059e**：`tools/append_retrospective_to_wiki.py`（**L2**，🟡 中優先級）— 把 retrospective `wiki 變動建議` 段內容寫入 `wiki/<target>.md` 指定 anchor（如 `## 修訂歷史` 之前）+ 自動更新 footer 日期；**關鍵**：自動寫 Pass 11 比較文（`### 🟧 v3 升級修改：wiki/<stem>`）到當日 log 避免人工漏寫；含 `--anchor` / `--section-title` / `--auto-bless`（後者需 owner 確認）
  - [ ] **T-0059f**：Dashboard Loop 卡片（**L1**，🟢 低優先級）— 在 [`build_dashboard.py`](../../tools/build_dashboard.py) 加第六張卡（Loop）顯示：done plan 數 / 已寫 retrospective 數 / 已轉入 Muse 候選數 / 平均 plan-to-retrospective 延遲（天）；對應 [`retrospective-flow.md`](retrospective-flow.md) §5 觀測指標
- [x] **T-0060**：`wiki` → `graph.json`／HTML 匯出管線（graphify 或等效）— 三層疊圖見 [`design.md`](design.md) §7.1（2026-05-16；三子任務 a/b/c 全綠）
  - [x] **T-0060a**：frontmatter 白名單擴充（`stage` / `status` / `linked_insight` / `linked_action_plan`）+ `tools/lint_wiki.py` Pass 10 同步（2026-05-16；Pass 10 新增 (d) 子檢查：stage/status enum + linked_* 解析至 `audit/{insights,action-plans}/`，warn-only；首跑 916 wiki 全綠 0 error）
  - [x] **T-0060b**：`tools/build_pantheon_overlay.py`（讀 wiki frontmatter + `audit/insights/` + `audit/action-plans/` → `pantheon-overlay.json`）（2026-05-16；首跑 wiki=916 / insight=57 / action_plan=6，落地 `export/web-dashboard/pantheon-overlay.json`；補 UTF-8 解碼容錯）
  - [x] **T-0060c**：Graphify wrapper — 採方案 B（markdown→graphify-extraction adapter，零 LLM 成本）：[`tools/wiki_to_graphify.py`](../../tools/wiki_to_graphify.py) 抓 `[[wikilink]]` → graphify build/cluster/export，落地 829 nodes / 3234 edges / 12 communities。Makefile `graphify` target 已串接（2026-05-06）
- [x] **T-0061**：`export/web-dashboard/` 定期建置（cron／手動）（2026-05-16；五子任務 a–e 全綠；自動化掛載延後至 ledger 連 3 ok）
  - [x] **T-0061a**：`tools/build_dashboard.py` 五張卡片（Mnemosyne／Muse／Metis／Gate／Tasks）+ 內嵌 L1 graph iframe（2026-05-16；首跑落地 `export/web-dashboard/index.html` 6.5KB，五卡完整 + graph iframe 雙視圖切換 + footer `generated_at`／git hash／overlay 年齡；修掉 f-string 反斜線跑不過的舊 bug）
  - [x] **T-0061b**：[`dashboard-spec.md`](dashboard-spec.md)（圖例、欄位、更新節奏、AC 對應）（2026-05-16；§1–§7 含三層架構、五卡欄位/來源、frontmatter 白名單、更新節奏、AC 對應、失效模式、不在範圍）
  - [x] **T-0061c**：`make dashboard` Makefile target（鏈式 graphify → overlay → dashboard）（2026-05-16；`Makefile` `dashboard: overlay graphify` 依賴鏈正常，graphify 未安裝時印 fallback 不擋鏈）
  - [x] **T-0061d**：HTML footer 顯示 `generated_at` + git commit hash（US-007 AC-4），>7 日標紅（2026-05-16；`build_dashboard.py::render()` footer 三欄齊全；合成 10 日舊 overlay 驗 `class="stale"` 紅字觸發）
  - [x] **T-0061e**：週度 cron／hook（先手動穩 2–3 次再自動化，符合 skill 晉升路徑）（2026-05-16；scaffold `.cursor/hooks/weekly-dashboard.sh` + `log/dashboard-runs.md` 帳本；首跑 ok size=6889B；cron/launchd 待連續 3 次 ok 後再掛）
- [~] **T-0062**：端到端演練：raw → wiki → insight → action → retrospective（[`mvp-acceptance.md`](mvp-acceptance.md) E2E）→ **MVP 級已達**：[`demo-evidence/metis-mvp-e2e.md`](demo-evidence/metis-mvp-e2e.md) v1.1（2026-05-19）以現有 #M1 鏈為證；**E1/E2/E4 完整、E5 未觸發**；E2 status 漂移已修復（Plan `draft → active`、Plan §Status 變更紀錄補表、meta-Insight `## 決議` 段補「已啟動 Action Plan」回流，依 spec §4.2/§4.3）；**E3 屬時間閘控未到**而非缺口（Plan KR4 截止 2026-07-15，現在第 14/42 天、進度約 33%）；done 結算待 2026-07-15 後 owner 親自執行，屆時可升級為 `[x]`；Session 4d-tail closure
- [x] **T-0063**：可追溯性抽樣審計（每節點回推來源）→ [`traceability-audit-spec.md`](traceability-audit-spec.md) v1.0（2026-05-19；四層 L1-L4 抽樣方法、N=20 / N=20 / 全掃 / 全掃；判定標準 ✅/⚠️/❌；升級條件 ≥95%/90-95%/<90%；spec 已備，首次實跑作為單獨 commit 落地；Session 4b-tail）
- [x] **T-0064**：風險登錄 [`risk-register.md`](risk-register.md) 與實際狀態對表 → 對表落地於 `risk-register.md` 末段（2026-05-19）；逐 R-001～R-009 對照「曾觸發否／緩解是否生效／當前狀態」+ 新識別 R-010～R-012（流程／隱私／工具鏈層）；判讀：無紅燈、無實質損害；Session 4a-tail
- [x] **T-0065**：**v1.x 規劃**：下版需求後選清單（不修改 v1.0-baseline 語意）→ [`v1.x-roadmap.md`](v1.x-roadmap.md) v1.0（2026-05-19；20 項候選分 A/B/C/D 四類：A 既有後續鉤子 / B 新風險衍生 / C 工具鏈經驗 / D 規模擴張瓶頸；含三維分類嚴重度/成本/價值 + 排序建議 + v1.1 升級流程；Session 4c-tail）

**DoD：** SoT 維持 `wiki/`；匯出層單向預設。

---

## 依賴與里程碑

```text
Phase0 → Phase1 → Phase2 → Phase3 → Phase4
                  ↑ Gate A   ↑ Gate B
```

| Phase | 目標 | 建議工期（參考） |
|-------|------|------------------|
| Phase 0 | 規格凍結 | 0.5 週 |
| Phase 1 | Mnemosyne MVP | 2 週 |
| Phase 2 | Muse MVP | 2 週 |
| Phase 3 | Metis MVP | 2 週 |
| Phase 4 | 閉環與可視化 | 1.5 週 |

---
最後更新：2026-05-19（v1.0-baseline · 65 tasks · **Phase 4 收尾 + T-0062 closure**：Session 4a/4b/4c/4d-tail 完成；T-0062 由 owner 授權代理完成 E2 status 漂移修復（`draft → active`、Plan §Status 變更紀錄補表、Insight `## 決議` 回流），E3 時間閘控待 2026-07-15 後升級；其餘 64 任務全綠）
