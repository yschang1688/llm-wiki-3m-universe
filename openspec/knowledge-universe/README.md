# OpenSpec：知識宇宙 Pipeline

**規格版本：** [`SPEC_VERSION.md`](SPEC_VERSION.md) · **v1.0-baseline**（凍結後續任務對照此版，避免漂移）

本目錄為 **ingest-service × AI_LLM_Wiki** 的規格文件（OpenSpec），建議閱讀順序：

1. [`SPEC_VERSION.md`](SPEC_VERSION.md) — 版本與權威 trio 索引  
2. [`gate-checklist.md`](gate-checklist.md) — **Gate A / B** 獨立勾選表  
3. [proposal.md](proposal.md) — 問題、範圍、名詞、問卷決議、三神祇願景摘要  
4. [**pantheon-pkm.md**](pantheon-pkm.md) — 三神祇產品規格（願景、模組、**12 指令**、路線圖）  
5. [**requirements.md**](requirements.md) — **7 US** + **3 NFR** + 附錄 A（十二指令）  
6. [**design.md**](design.md) — 架構、資料合約、雙路徑、Pantheon §11、**§12–16** 路由／Gate／風險  
7. [**tasks.md**](tasks.md) — **65** 項任務（T-0001～T-0065）  
8. [`phase1-ac.md`](phase1-ac.md) — Phase 1 第一輪最小閉環驗收  
9. [mnemosyne-stage1-audit.md](mnemosyne-stage1-audit.md) — 第一階段完成度基線與缺口  
10. [stages.md](stages.md) — 三階段契約與開發藍圖對標  
11. [mvp-acceptance.md](mvp-acceptance.md) — MVP 驗收標準  
12. [**muse-parallel-pilot-roadmap.md**](muse-parallel-pilot-roadmap.md) — **Muse 試跑 MVP**（並行 Gate A／schema／Insight／prompt，可勾選）  
13. [risk-register.md](risk-register.md) — 風險登錄  
14. [metis-action-plan-spec.md](metis-action-plan-spec.md) — Metis 輸出模板
15. [**dashboard-spec.md**](dashboard-spec.md) — Pantheon 三層疊圖 Dashboard 規格（圖例／欄位／更新節奏／AC 對應）  

**指令與腳本入口：** [`commands/wiki-import.md`](commands/wiki-import.md) · [`router/llm-routing.md`](router/llm-routing.md)

**Agent 協作合約：** [`references/agent-collaboration-map.md`](references/agent-collaboration-map.md) — 三神祇 × 三 Agent × 五動作映射、檔案寫入權矩陣、三大指標掛鉤（2026-07-05 新增）

**Mnemosyne 執行參考：** [metadata-validation.md](metadata-validation.md) · [ingest-cli-design-alignment.md](ingest-cli-design-alignment.md) · [ingest-service-contract-status.md](ingest-service-contract-status.md) · [ingest-traceability.md](ingest-traceability.md) · [gate-a-evidence-pack.md](gate-a-evidence-pack.md) · [notion-ingest-conventions.md](notion-ingest-conventions.md) · [gdrive-youtube-poc.md](gdrive-youtube-poc.md) · [index-md-conventions.md](index-md-conventions.md)

**補充：** [templates/](templates/) · [INGEST_SERVICE_ISSUE_DRAFT.md](INGEST_SERVICE_ISSUE_DRAFT.md) · [INTEGRATION_TEST_WEB.md](INTEGRATION_TEST_WEB.md)

**ingest-service 本機路徑（使用者提供）：** `<external-repo-path>`

最後更新：2026-04-14（+Muse 並行試跑路線圖）
