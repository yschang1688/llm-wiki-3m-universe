#!/usr/bin/env python3
"""
lint_wiki.py — AI_LLM_Wiki 健檢器（Pass 1–12，含 v3）

用法：
    python3 tools/lint_wiki.py [WIKI_ROOT]
    python3 tools/lint_wiki.py .

無第三方相依，使用 Python 3 標準庫。

十二輪 pass（編號對應終端機輸出與 lint-guide）：
    1. 失效連結：[[目標]] 對應檔案不存在
    2. 孤兒頁：wiki 頁面無任何反向連結
    3. 缺漏 index：wiki 頁面未在 index.md 出現
    4. 熱門缺頁：被 >=3 篇連結但目標不存在（breakdown 建議清單）
    5. log/ 形狀：檔名、H1、H2 op + agent 欄合法性（朔源協定 v1）
    6. audit/ YAML：frontmatter 可解析、必要欄位、enum 合法
    7. audit target：open audit 的 target 檔案實際存在且 anchor_text 可找到
    8. 過長警告：wiki 頁 > 3500 中文字數（meta-insight 條目放寬）
    9. ASCII 圖提示：疑似 ASCII 圖樣（建議改 Mermaid）
    10. v3 一致性（warn-only）：Infobox 七鍵白名單、修訂歷史最上日期 vs footer、TL;DR 長度上限
    11. v3 H2/footer 保護：git diff 偵測三大 H2 既有內容刪減；缺比較文則 error（v1.1.2 協定）
    12. retrospective schema：raw/retrospective/*.md frontmatter 必要欄位 +
        plan_id / insight_id 上游存在性驗證（知識閉環迴路 PoC）

執行順序：**嚴格按編號 1→2→…→12**（2026-06-09 refactor）。Pass 6→7 之間透過 mutable `audit_parsed` list 傳遞解析後的 frontmatter，仍維持單一 passes list-iteration 結構。

> 歷史：原為 1→5、8→10、再 6→7（state passing 拆出 hand-coded）；造成 Pass 12 reads audit/ 跑在 Pass 6 audit YAML 驗證之前的順序盲點（plan_id/insight_id 存在性檢查可能 false-positive）。重構後消除此盲點。

Exit code 0 = 無 error 級 issue，1 = 有 error（warn/info/suggest 不計入）。

參照：openspec/knowledge-universe/references/lint-guide.md
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Iterable, Optional

# ---------- 配置 ----------

WIKI_DIR = "wiki"
INDEX_FILE = "index.md"
LOG_DIR = "log"
AUDIT_DIR = "audit"
AUDIT_RESOLVED_DIR = "resolved"
ALLOWED_OPS = {"整理", "提問", "清理", "更新目錄", "稽核", "升級", "一致化", "handoff", "scaffold", "ingest", "query", "lint", "index", "audit", "upgrade", "wiki-auto-authoring"}
SEVERITY_ENUM = {"info", "suggest", "warn", "error"}
STATUS_ENUM = {"open", "resolved"}
AUDIT_REQUIRED_FIELDS = ("id", "target", "anchor_text", "severity", "author", "created", "status")
LONG_PAGE_CHAR_THRESHOLD = 3500  # 中文字數（2026-05-20 由 3000 放寬；對應 CLAUDE.md「字數預算」段豁免條款）
# 規範脈絡：
#   2026-05-11：2000 → 3000（深概念條目 Body 擴張需求）
#   2026-05-20：3000 → 3500（meta-insight 後設彙整主鍵密度即價值；
#              wiki/ 為扁平結構無母子頁拆分先例；
#              `tools/check_child_density.py` 規劃中尚未實作）
# 後設條目豁免：frontmatter `tags:` 含 `meta-insight`、Infobox `類別` 含
# 「後設方法論／後設骨架／後設整合」字串，或內文含 `meta-Insight` 標記者，
# 視為後設彙整主鍵（如「流程顆粒度與決策瓶頸」、「四軸後設整合範例」），
# 即便超過閾值也僅報 suggest（不報 info）；證據鏈整合條目拆分風險高於收益。
META_INSIGHT_TAG_RE = re.compile(
    r"^(?:type|tags)\s*:.*meta[-_ ]?insight|"
    r"類別\s*[|｜]\s*[^|｜\n]*?後設(?:方法論|骨架|整合|彙整)|"
    r"meta[-_ ]?Insight|后设方法论",
    re.IGNORECASE | re.MULTILINE,
)
MISSING_PAGE_HOT_THRESHOLD = 3   # 被 >=3 篇連結才算熱門缺頁
ORPHAN_EXEMPT_PREFIXES = ("_", "index")  # index.md 等不算孤兒

# ---------- 顏色（TTY 才用） ----------

USE_COLOR = sys.stdout.isatty()
def _c(s: str, code: str) -> str:
    if not USE_COLOR:
        return s
    return f"\033[{code}m{s}\033[0m"
RED = lambda s: _c(s, "31")
YELLOW = lambda s: _c(s, "33")
GREEN = lambda s: _c(s, "32")
CYAN = lambda s: _c(s, "36")
GREY = lambda s: _c(s, "90")

# ---------- Issue 資料結構 ----------

class Issue:
    __slots__ = ("pass_name", "severity", "path", "detail")
    def __init__(self, pass_name: str, severity: str, path: str, detail: str):
        self.pass_name = pass_name
        self.severity = severity  # info | warn | error
        self.path = path
        self.detail = detail

    def fmt(self) -> str:
        sev = self.severity
        tag = {"error": RED("🔴 ERR "), "warn": YELLOW("🟡 WARN"), "info": CYAN("🟢 INFO")}.get(sev, sev)
        return f"  {tag}  {GREY(self.path)}  {self.detail}"

# ---------- 工具 ----------

WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:\|[^\]]*)?(?:#[^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return ""

def extract_wikilinks(text: str) -> list[str]:
    """抓出 [[目標]] 或 [[目標|顯示]] 或 [[目標#錨點]] 的目標部分。"""
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]

def count_chinese_chars(text: str) -> int:
    """粗略計算中文字元數（CJK 統一表意文字範圍）。"""
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")

def parse_yaml_frontmatter(text: str) -> Optional[dict]:
    """最小 YAML 解析器：平鋪 key:value 與簡單 array。不支援巢狀。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    body = m.group(1)
    out: dict = {}
    for line in body.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # 處理陣列 [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                out[key] = []
            else:
                out[key] = [x.strip().strip('"\'') for x in inner.split(",")]
        # 處理字串（去引號）
        elif val.startswith('"') and val.endswith('"'):
            out[key] = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            out[key] = val[1:-1]
        elif val == "":
            out[key] = ""
        else:
            out[key] = val
    return out

# ---------- Pass 實作 ----------

def build_wiki_index(wiki_root: Path) -> dict[str, Path]:
    """掃 wiki/ 下所有 .md，建立 {檔名無副檔: 路徑} 索引。檔名衝突時後者勝。"""
    idx: dict[str, Path] = {}
    wiki_dir = wiki_root / WIKI_DIR
    if not wiki_dir.exists():
        return idx
    for p in wiki_dir.rglob("*.md"):
        name = p.stem
        idx[name] = p
        # 也收錄相對於 wiki/ 的路徑（例：subdir/page）
        rel = p.relative_to(wiki_dir).with_suffix("").as_posix()
        idx[rel] = p
    return idx


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🟦 Module A: wiki 連結完整性 (Pass 1-4)                                 ║
# ║ 可抽離為獨立 lib：純依賴 wiki/ + index.md + 建好的 wiki_idx              ║
# ║ 共用 state：wiki_idx（build_wiki_index 預建一次，4 passes 共讀）         ║
# ║ 複用情境：任何 Obsidian-style vault 的 link integrity 健檢              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def pass_1_dead_links(wiki_root: Path, issues: list[Issue], wiki_idx: dict[str, Path]) -> None:
    wiki_dir = wiki_root / WIKI_DIR
    for p in wiki_dir.rglob("*.md"):
        text = read_text(p)
        for target in extract_wikilinks(text):
            target_clean = target.strip()
            if target_clean in wiki_idx:
                continue
            # 允許子路徑格式 wiki/subdir/page
            if target_clean.startswith(f"{WIKI_DIR}/"):
                alt = target_clean[len(WIKI_DIR) + 1:]
                if alt in wiki_idx:
                    continue
            issues.append(Issue("失效", "warn", str(p.relative_to(wiki_root)), f"[[{target_clean}]] 對應檔案不存在"))


def pass_2_orphans(wiki_root: Path, issues: list[Issue], wiki_idx: dict[str, Path]) -> None:
    wiki_dir = wiki_root / WIKI_DIR
    # 收集所有被連結的目標
    linked: set[str] = set()
    for p in wiki_dir.rglob("*.md"):
        for target in extract_wikilinks(read_text(p)):
            linked.add(target.strip())
    # index.md、log、guidebook 等也可能連結 wiki 頁面
    for extra in ("index.md", "log.md", "guidebook.md"):
        f = wiki_root / extra
        if f.exists():
            for target in extract_wikilinks(read_text(f)):
                linked.add(target.strip())
    # 找孤兒
    for p in wiki_dir.rglob("*.md"):
        name = p.stem
        if any(name.startswith(pfx) for pfx in ORPHAN_EXEMPT_PREFIXES):
            continue
        rel = p.relative_to(wiki_dir).with_suffix("").as_posix()
        if name not in linked and rel not in linked:
            issues.append(Issue("孤兒頁", "info", str(p.relative_to(wiki_root)), f"無任何反向連結"))


def pass_3_missing_index(wiki_root: Path, issues: list[Issue], wiki_idx: dict[str, Path]) -> None:
    index_file = wiki_root / INDEX_FILE
    if not index_file.exists():
        issues.append(Issue("缺漏 index", "error", INDEX_FILE, "index.md 不存在"))
        return
    index_text = read_text(index_file)
    index_links = set(extract_wikilinks(index_text))
    wiki_dir = wiki_root / WIKI_DIR
    for p in wiki_dir.rglob("*.md"):
        name = p.stem
        rel = p.relative_to(wiki_dir).with_suffix("").as_posix()
        if name in index_links or rel in index_links:
            continue
        issues.append(Issue("缺漏 index", "info", str(p.relative_to(wiki_root)), f"未出現在 index.md"))


def pass_4_hot_missing(wiki_root: Path, issues: list[Issue], wiki_idx: dict[str, Path]) -> None:
    wiki_dir = wiki_root / WIKI_DIR
    counter: Counter[str] = Counter()
    for p in wiki_dir.rglob("*.md"):
        for target in extract_wikilinks(read_text(p)):
            if target.strip() not in wiki_idx:
                counter[target.strip()] += 1
    for target, cnt in counter.most_common():
        if cnt < MISSING_PAGE_HOT_THRESHOLD:
            break
        issues.append(Issue("熱門缺頁", "suggest", "(待建立)", f"[[{target}]] 被 {cnt} 篇連結但尚未建立"))


ALLOWED_AGENTS = {
    # Claude Code（與 ~/.claude/CLAUDE.md §7 模型路由表對齊）
    "Claude Code Fable 5",
    "Claude Code Opus 4.8", "Claude Code Opus 4.7",
    "Claude Code Sonnet 4.6", "Claude Code Haiku 4.5",
    # Cowork（接手 Cursor 執行角色，2026-06-26 起；見 ~/.claude/CLAUDE.md §15 v2.6）
    "Cowork Opus 4.8", "Cowork Sonnet 4.6",
    # Cursor（過渡退場，僅維護既有引用）
    "Cursor Sonnet 4.6", "Cursor Haiku 4.5",
    # Antigravity CLI（研究＋連網執行，接手 Gemini CLI，2026-06-18 遷移；見全域 §7）
    "Antigravity Gemini 3.1 Pro", "Antigravity Gemini 3.5 Flash",
    "Antigravity Claude Sonnet 4.6", "Antigravity Claude Opus 4.6", "Antigravity GPT-OSS 120B",
    # Gemini CLI（過渡退場，2026-06-18 個人版 API 停用；保留供歷史 log）
    "Gemini CLI 2.5 Pro", "Gemini CLI Pro 3",
    # Fallback：Ollama 本機離線
    "Ollama Qwen3 8B", "Ollama Qwen3.5 9B", "Ollama Qwen3.5 4B", "Ollama Gemma4 E4B",
    # Ollama 連網備援（:cloud，需外網，非離線）
    "Ollama glm-5.2:cloud", "Ollama kimi-k2.7-code:cloud",
    "Ollama minimax-m3:cloud", "Ollama nemotron-3-super:cloud",
}
# 朔源協定 v1：2026-12-08 後 hard error（過渡期 warn-only）
AGENT_HARD_ERROR_AFTER = datetime(2026, 12, 8)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🟨 Module B: log 工作流 (Pass 5)                                        ║
# ║ 本專案特化：CLAUDE.md 動作五的 log/YYYYMMDD.md 格式                     ║
# ║ 朔源協定 v1 認列 agent 欄；過渡期 → 2026-12-08 hard error                ║
# ║ 複用情境：任何採用「op | agent | desc」H2 格式的 daily log               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def pass_5_log_shape(wiki_root: Path, issues: list[Issue]) -> None:
    log_dir = wiki_root / LOG_DIR
    if not log_dir.exists():
        return
    # 新格式：`## [HH:MM] <op> | <Agent> | <desc>` — 三段管線
    # 舊格式：`## [HH:MM] <op> | <desc>` — 兩段管線（過渡期接受）
    h2_pattern = re.compile(r"^##\s+\[\d{2}:\d{2}\]\s+(.+)$")
    hard_error_now = datetime.now() >= AGENT_HARD_ERROR_AFTER
    missing_agent_level = "error" if hard_error_now else "warn"

    for p in sorted(log_dir.glob("*.md")):
        name = p.stem
        # 檔名應為 YYYYMMDD
        if not re.fullmatch(r"\d{8}", name):
            issues.append(Issue("log 形狀", "warn", str(p.relative_to(wiki_root)), f"檔名不符 YYYYMMDD.md"))
            continue
        # 解析日期
        try:
            dt = datetime.strptime(name, "%Y%m%d")
        except ValueError:
            issues.append(Issue("log 形狀", "warn", str(p.relative_to(wiki_root)), f"無效日期"))
            continue
        text = read_text(p)
        expected_h1 = f"# {dt.strftime('%Y-%m-%d')}"
        first_line = (text.splitlines() or [""])[0].strip()
        if first_line != expected_h1:
            issues.append(Issue("log 形狀", "warn", str(p.relative_to(wiki_root)), f"H1 應為 '{expected_h1}'，實際為 '{first_line}'"))
        # 檢查 H2 op + agent 合法
        rel = str(p.relative_to(wiki_root))
        for line in text.splitlines():
            m = h2_pattern.match(line)
            if not m:
                continue
            payload = m.group(1)
            parts = [s.strip() for s in payload.split("|")]
            op = parts[0]
            if op not in ALLOWED_OPS:
                issues.append(Issue("log 形狀", "warn", rel, f"未知 op '{op}'（允許：{sorted(ALLOWED_OPS)}）"))
            # 朔源協定：3 段（含 agent）為新格式；2 段為舊格式（過渡期 warn）
            # handoff op 例外：<Agent> 欄為方向式 'A→B'（交接來源→去向），非單一 agent，略過白名單檢查
            if op == "handoff":
                pass
            elif len(parts) >= 3:
                agent = parts[1]
                # 多 agent 共寫以 '+' 連接
                agents = [a.strip() for a in agent.split("+")]
                for a in agents:
                    if a and a not in ALLOWED_AGENTS:
                        issues.append(Issue(
                            "log 形狀", "warn", rel,
                            f"未知 agent '{a}'（允許白名單見 references/log-guide.md，或更新 ALLOWED_AGENTS）"
                        ))
            elif len(parts) == 2:
                issues.append(Issue(
                    "log 形狀", missing_agent_level, rel,
                    f"H2 缺 agent 欄（朔源協定 v1，過渡期 2026-06-08 → 2026-12-08）：'{line.strip()[:80]}'"
                ))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🟨 Module C: audit 工作流 (Pass 6-7)                                    ║
# ║ 本專案特化：audit/*.md 人工反饋流程（schema + target anchor 驗證）       ║
# ║ State passing：Pass 6 → Pass 7 透過 audit_parsed list 傳遞解析結果       ║
# ║ 複用情境：任何採用「audit + resolved」雙資料夾的內容稽核工作流           ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def pass_6_audit_yaml(wiki_root: Path, issues: list[Issue]) -> list[tuple[Path, dict]]:
    """回傳 (path, frontmatter) 清單供 pass 7 使用。"""
    audit_dir = wiki_root / AUDIT_DIR
    parsed: list[tuple[Path, dict]] = []
    if not audit_dir.exists():
        return parsed
    for p in audit_dir.rglob("*.md"):
        # 略過範本檔
        if p.name.startswith("_"):
            continue
        # 略過 Muse Insight 與 Metis Action Plan 目錄
        # （spec §2：自成子目錄，YAML 規約分別見 muse-insight-spec.md / metis-action-plan-spec.md，非 audit schema）
        try:
            rel_parts = p.relative_to(audit_dir).parts
            if rel_parts and rel_parts[0] in {"insights", "action-plans"}:
                continue
        except ValueError:
            pass
        rel = str(p.relative_to(wiki_root))
        text = read_text(p)
        fm = parse_yaml_frontmatter(text)
        if fm is None:
            issues.append(Issue("audit YAML", "error", rel, "無 YAML frontmatter 或解析失敗"))
            continue
        missing = [k for k in AUDIT_REQUIRED_FIELDS if k not in fm]
        if missing:
            issues.append(Issue("audit YAML", "error", rel, f"缺欄位：{missing}"))
        if fm.get("severity") and fm["severity"] not in SEVERITY_ENUM:
            issues.append(Issue("audit YAML", "error", rel, f"severity='{fm['severity']}' 不在 {sorted(SEVERITY_ENUM)}"))
        if fm.get("status") and fm["status"] not in STATUS_ENUM:
            issues.append(Issue("audit YAML", "error", rel, f"status='{fm['status']}' 不在 {sorted(STATUS_ENUM)}"))
        parsed.append((p, fm))
    return parsed


def pass_7_audit_targets(wiki_root: Path, issues: list[Issue], parsed: list[tuple[Path, dict]]) -> None:
    for p, fm in parsed:
        rel = str(p.relative_to(wiki_root))
        if fm.get("status") == "resolved":
            continue
        target = fm.get("target")
        if not target:
            continue
        target_path = wiki_root / target
        if not target_path.exists():
            issues.append(Issue("audit target", "error", rel, f"target 檔案不存在：{target}"))
            continue
        anchor = fm.get("anchor_text", "")
        if anchor and anchor not in read_text(target_path):
            issues.append(Issue("audit target", "warn", rel, f"anchor_text 在 {target} 中找不到（已失效）"))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🟪 Module D: wiki 內容與 v3 結構 (Pass 8-11)                            ║
# ║ wiki/ 內容掃描 + v3 百科全書式骨架保護                                   ║
# ║   Pass 8  過長警告（中文字數，meta-insight 條目放寬）                    ║
# ║   Pass 9  ASCII 圖偵測（建議改 Mermaid）                                 ║
# ║   Pass 10 v3 一致性（Infobox 白名單 / TL;DR / 修訂歷史 vs footer）       ║
# ║   Pass 11 v3 H2/footer 保護（snapshot 比對 + 比較文協定 v1.1.2）         ║
# ║ 注意：源碼順序為 8, 10, 9, 11（執行順序仍透過 passes list 嚴格 1→12）    ║
# ║ 複用情境：8 / 9 可獨立抽離；10 / 11 為 wiki v3 骨架特化                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def pass_8_long_pages(wiki_root: Path, issues: list[Issue]) -> None:
    """Pass 8：單頁中文字超過 LONG_PAGE_CHAR_THRESHOLD 時警告。

    豁免邏輯（2026-05-20 加入）：
      偵測到 meta-insight 標記（tags、Infobox 類別含「後設」字串、或內文 meta-Insight）
      的頁面，降級為 suggest（軟提醒），不阻擋日常 lint；
      其餘超長條目維持 info（建議拆分）。
    背景：後設彙整主鍵（如「流程顆粒度與決策瓶頸」整合 batch-02→batch-10
    證據鏈）密度即價值，硬拆會切斷可追溯性；wiki/ 為扁平結構，當前無
    母子頁協定，`tools/check_child_density.py` 規劃中尚未實作。
    """
    wiki_dir = wiki_root / WIKI_DIR
    for p in wiki_dir.rglob("*.md"):
        text = read_text(p)
        n = count_chinese_chars(text)
        if n <= LONG_PAGE_CHAR_THRESHOLD:
            continue
        is_meta = bool(META_INSIGHT_TAG_RE.search(text))
        if is_meta:
            issues.append(Issue(
                "過長警告", "suggest", str(p.relative_to(wiki_root)),
                f"{n} 中文字 > {LONG_PAGE_CHAR_THRESHOLD}（meta-insight 後設彙整主鍵豁免；密度即價值，拆分非優先）"
            ))
        else:
            issues.append(Issue(
                "過長警告", "info", str(p.relative_to(wiki_root)),
                f"{n} 中文字 > {LONG_PAGE_CHAR_THRESHOLD}，建議拆分為資料夾 + 子頁"
            ))


INFOBOX_KEYS = {"類別", "提出年", "主要應用", "父頁", "子頁", "難度", "別名"}
TLDR_MAX_CHARS = 200  # 複雜概念可用較長白話 Lead（2026-05-11 由 150 放寬）

# Pantheon overlay 白名單（T-0060a；對齊 design.md §7.1）
WIKI_FRONTMATTER_WHITELIST = {"stage", "status", "linked_insight", "linked_action_plan"}
STAGE_ENUM = {"MNE", "MUS", "MET"}
WIKI_STATUS_ENUM = {"draft", "active", "done"}


def _audit_ref_exists(base_dir: Path, ref: str) -> bool:
    """linked_insight / linked_action_plan 值可能是：
       (a) `batch/file_id`（無 .md）— 拼 .md 後檢查
       (b) 純 file_id — 在 base_dir 下任何子夾遞迴尋
       (c) 完整路徑（含 .md）— 直接 base_dir / ref
       存在即 True；base_dir 不存在則一律 False。"""
    if not base_dir.exists():
        return False
    ref = ref.strip().strip('"\'')
    if not ref:
        return False
    cand = base_dir / ref
    if cand.exists():
        return True
    cand_md = base_dir / (ref + ".md") if not ref.endswith(".md") else None
    if cand_md and cand_md.exists():
        return True
    # 純 id 比對 stem
    target = ref.rsplit("/", 1)[-1].removesuffix(".md")
    for p in base_dir.rglob("*.md"):
        if p.stem == target:
            return True
    return False


def pass_10_v3_consistency(wiki_root: Path, issues: list[Issue]) -> None:
    """v3 百科全書式骨架一致性檢查（warn-only）。

    僅對含 v3 元素（Infobox 表格、`## 修訂歷史` 或 `> **TL;DR**：`）的頁面檢查：
      a) Infobox 欄位必在白名單七鍵內
      b) `## 修訂歷史` 最上一行日期 == footer `最後更新：YYYY-MM-DD`
      c) `> **TL;DR**：…` 內文 ≤ 150 中文字
    無 v3 元素的舊頁面跳過，不報。

    額外（T-0060a）：對含 frontmatter 的 wiki 頁，驗證 Pantheon overlay 白名單鍵
    （`stage` / `status` / `linked_insight` / `linked_action_plan`）：
      d) stage ∈ {MNE, MUS, MET}；status ∈ {draft, active, done}；linked_* 指向存在的 audit 檔
    """
    wiki_dir = wiki_root / WIKI_DIR
    date_re = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
    footer_re = re.compile(r"^最後更新[:：]\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
    tldr_re = re.compile(r"^>\s*\*\*TL;DR\*\*[:：]\s*(.+)$", re.MULTILINE)
    insights_dir = wiki_root / AUDIT_DIR / "insights"
    plans_dir = wiki_root / AUDIT_DIR / "action-plans"
    for p in wiki_dir.rglob("*.md"):
        text = read_text(p)
        rel = str(p.relative_to(wiki_root))

        # (d) wiki frontmatter 白名單（Pantheon overlay）
        fm = parse_yaml_frontmatter(text)
        if fm:
            stage = fm.get("stage")
            if stage and stage not in STAGE_ENUM:
                issues.append(Issue(
                    "v3 一致性", "warn", rel,
                    f"frontmatter stage='{stage}' 不在 {sorted(STAGE_ENUM)}"
                ))
            status = fm.get("status")
            if status and status not in WIKI_STATUS_ENUM:
                issues.append(Issue(
                    "v3 一致性", "warn", rel,
                    f"frontmatter status='{status}' 不在 {sorted(WIKI_STATUS_ENUM)}"
                ))
            li = fm.get("linked_insight")
            if li and not _audit_ref_exists(insights_dir, li):
                issues.append(Issue(
                    "v3 一致性", "warn", rel,
                    f"linked_insight='{li}' 在 audit/insights/ 找不到對應檔"
                ))
            lap = fm.get("linked_action_plan")
            if lap and not _audit_ref_exists(plans_dir, lap):
                issues.append(Issue(
                    "v3 一致性", "warn", rel,
                    f"linked_action_plan='{lap}' 在 audit/action-plans/ 找不到對應檔"
                ))

        # (a) Infobox：偵測 H1 後 8 行內的 2 欄表格
        lines = text.splitlines()
        h1_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
        if h1_idx is not None:
            window = lines[h1_idx + 1:h1_idx + 20]
            for i, line in enumerate(window):
                if re.match(r"^\|\s*欄位\s*\|\s*內容\s*\|", line):
                    # 取後續表格 row 直到空行
                    for row in window[i + 2:]:
                        if not row.strip().startswith("|"):
                            break
                        cells = [c.strip() for c in row.strip("|").split("|")]
                        if len(cells) < 2:
                            continue
                        key = cells[0]
                        if key and key not in INFOBOX_KEYS:
                            issues.append(Issue(
                                "v3 一致性", "warn", rel,
                                f"Infobox 欄位 `{key}` 不在白名單 {sorted(INFOBOX_KEYS)}"
                            ))
                    break

        # (b) 修訂歷史 vs footer 日期
        if "## 修訂歷史" in text:
            history_match = re.search(r"##\s*修訂歷史\s*\n((?:[-*]\s*.+\n?)+)", text)
            footer_match = footer_re.search(text)
            if history_match and footer_match:
                first_line = history_match.group(1).splitlines()[0]
                hist_dates = date_re.findall(first_line)
                if hist_dates and hist_dates[0] != footer_match.group(1):
                    issues.append(Issue(
                        "v3 一致性", "warn", rel,
                        f"修訂歷史最上日期 {hist_dates[0]} ≠ footer 最後更新 {footer_match.group(1)}"
                    ))

        # (c) TL;DR 長度
        m = tldr_re.search(text)
        if m:
            body = m.group(1)
            cjk = count_chinese_chars(body)
            if cjk > TLDR_MAX_CHARS:
                issues.append(Issue(
                    "v3 一致性", "warn", rel,
                    f"TL;DR 過長：{cjk} 中文字 > {TLDR_MAX_CHARS}"
                ))


def pass_9_ascii_art(wiki_root: Path, issues: list[Issue]) -> None:
    wiki_dir = wiki_root / WIKI_DIR
    ascii_line_re = re.compile(r"^\s*(\||\+\-|\+=)")
    for p in wiki_dir.rglob("*.md"):
        text = read_text(p)
        lines = text.splitlines()
        run = 0
        in_code = False
        for line in lines:
            # 略過 code block
            if line.strip().startswith("```"):
                in_code = not in_code
                run = 0
                continue
            if in_code:
                run = 0
                continue
            # 略過 Markdown 表格（| 分隔）
            if "|" in line and line.count("|") >= 2 and not line.strip().startswith("|"):
                run = 0
                continue
            if ascii_line_re.match(line) and "|" not in line[line.index(line.lstrip()[0]):].strip("| "):
                run += 1
                if run == 3:
                    issues.append(Issue("ASCII 圖提示", "info", str(p.relative_to(wiki_root)), "疑似 ASCII 圖，建議改用 Mermaid"))
                    run = 0
            else:
                run = 0

SNAPSHOT_PATH = "tools/.wiki_h2_snapshot.tsv"
PROTECTED_H2 = {"## 重點", "## 細節", "## 相關概念"}


def _protected_lines(text: str) -> list[str]:
    """取出三大 H2 與 footer 區段的非空行（已 strip、排序）。"""
    out: set[str] = set()
    lines = text.splitlines()
    last_hr = -1
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            last_hr = i
    in_yaml = False
    yaml_seen = False
    cur: Optional[str] = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s == "---":
            if not yaml_seen and i == 0:
                in_yaml = True
                yaml_seen = True
                continue
            if in_yaml:
                in_yaml = False
                continue
        if in_yaml:
            continue
        if s.startswith("## "):
            cur = s if s in PROTECTED_H2 else None
            continue
        if s.startswith("# "):
            cur = None
            continue
        if i == last_hr:
            cur = "FOOTER"
            continue
        if (cur in PROTECTED_H2 or cur == "FOOTER") and s:
            out.add(s)
    return sorted(out)


def _hash_protected(text: str) -> str:
    import hashlib
    joined = "\n".join(_protected_lines(text))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def _load_snapshot(wiki_root: Path) -> dict[str, str]:
    snap = wiki_root / SNAPSHOT_PATH
    out: dict[str, str] = {}
    if not snap.exists():
        return out
    for line in snap.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            out[parts[0]] = parts[1]
    return out


def _save_snapshot(wiki_root: Path, snap_dict: dict[str, str]) -> None:
    snap = wiki_root / SNAPSHOT_PATH
    lines = [
        "# wiki H2/footer 保護快照（lint_wiki.py Pass 11 / v1.1.2 比較文協定）",
        "# 欄位：相對路徑\\tsha256(三大 H2 + footer 排序行)",
        "# 接受變更後，跑 `python3 tools/lint_wiki.py --bless-protected` 重建。",
        "",
    ]
    for path in sorted(snap_dict):
        lines.append(f"{path}\t{snap_dict[path]}")
    snap.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bless_protected_snapshot(wiki_root: Path) -> int:
    """重建 wiki H2/footer 保護快照（人類 accept 後呼叫）。"""
    wiki_dir = wiki_root / WIKI_DIR
    if not wiki_dir.exists():
        print(RED(f"❌ 找不到 {wiki_dir}"), file=sys.stderr)
        return 2
    snap: dict[str, str] = {}
    n = 0
    for p in wiki_dir.rglob("*.md"):
        rel = str(p.relative_to(wiki_root))
        text = read_text(p)
        if not text:
            continue
        snap[rel] = _hash_protected(text)
        n += 1
    _save_snapshot(wiki_root, snap)
    print(GREEN(f"✓ 已寫入 {SNAPSHOT_PATH}（{n} 筆 wiki 條目快照）"))
    return 0


def pass_11_h2_footer_protection(wiki_root: Path, issues: list[Issue]) -> None:
    """Pass 12：三大 H2／footer 既有內容變更需附 v3 升級修改比較文（v1.1.1 協定）。

    機制：以 `tools/.wiki_h2_snapshot.tsv` 為基線（wiki/ 在 .gitignore 內，無法用 git diff），
    對每個 wiki/*.md 計算「三大 H2（重點／細節／相關概念）+ footer 排序行」的 sha256；
    比對快照基線；若漂移，當日 `log/YYYYMMDD.md` 或 `audit/v3-diff-{stem}-*.md` 必須含
    `### 🟧 v3 升級修改：wiki/{stem}` 標題，否則 error。

    重建快照（人類 accept 後）：python3 tools/lint_wiki.py --bless-protected
    """
    wiki_dir = wiki_root / WIKI_DIR
    snapshot = _load_snapshot(wiki_root)
    if not snapshot:
        # 首次使用：提示尚未建立快照（不視為 error，僅 info）
        if not (wiki_root / SNAPSHOT_PATH).exists():
            issues.append(Issue(
                "v3 H2/footer 保護", "info", SNAPSHOT_PATH,
                "尚未建立保護快照；跑 `python3 tools/lint_wiki.py --bless-protected` 初始化",
            ))
        return

    # Pass 11 v1.1.3：認列「最近 N 日」歷史 log（預設 7 日，含 _archive/）。
    # 理由：
    #   (a) 跨 agent / 跨日工作流（Gemini CLI 等）會把比較文寫到變更當日的 log，
    #       lint 若只讀當日 log 會誤判歷史變更為「缺比較文」(v1.1.2 修正)。
    #   (b) 但無上限掃描全部歷史會讓「半年前未 bless 的舊變更」永久豁免，
    #       失去 Pass 12 「強制當下決策」的設計意圖；故限 7 日重觸 error。
    # 覆寫：環境變數 PROTECTED_LOG_DAYS（int）。
    import os as _os
    days_window = int(_os.environ.get("PROTECTED_LOG_DAYS", "7"))
    cutoff = datetime.now().date() - timedelta(days=days_window)
    log_dir = wiki_root / LOG_DIR
    log_text = ""
    if log_dir.is_dir():
        candidates: list[Path] = list(log_dir.glob("*.md"))
        archive = log_dir / "_archive"
        if archive.is_dir():
            candidates.extend(archive.glob("*.md"))
        recent: list[Path] = []
        for q in candidates:
            stem = q.stem
            if len(stem) != 8 or not stem.isdigit():
                continue  # 非 YYYYMMDD 命名（如 log.md 凍結檔）跳過
            try:
                d = datetime.strptime(stem, "%Y%m%d").date()
            except ValueError:
                continue
            if d >= cutoff:
                recent.append(q)
        log_text = "\n".join(read_text(p) for p in recent)
    audit_dir = wiki_root / AUDIT_DIR

    for p in wiki_dir.rglob("*.md"):
        rel = str(p.relative_to(wiki_root))
        text = read_text(p)
        if not text:
            continue
        current = _hash_protected(text)
        old = snapshot.get(rel)
        if old is None or old == current:
            continue

        stem = p.stem
        marker = f"### 🟧 v3 升級修改：wiki/{stem}"
        diff_text = ""
        if audit_dir.exists():
            diff_text = "".join(
                read_text(q) for q in audit_dir.glob(f"v3-diff-{stem}-*.md")
            )

        if marker in log_text or marker in diff_text:
            issues.append(Issue(
                "v3 H2/footer 保護", "info", rel,
                "H2/footer 既有內容變動已附比較文（accept 後跑 --bless-protected 更新快照）",
            ))
        else:
            issues.append(Issue(
                "v3 H2/footer 保護", "error", rel,
                f'三大 H2／footer 既有內容變動但缺 "{marker}" 比較文；'
                f"接受後跑 `python3 tools/lint_wiki.py --bless-protected` 更新快照",
            ))


# ---------- Pass 12：retrospective schema ----------

RETRO_DIR = "raw/retrospective"
RETRO_REQUIRED = ("type", "plan_id", "insight_id", "created", "author", "plan_status_after")
RETRO_PLAN_STATUS_ENUM = {"done", "blocked", "done_with_caveat"}


def _retro_parse_frontmatter(text: str) -> Optional[dict]:
    """支援 `key: value`、`key: [a,b]`、`key:\\n  - item` 列表（同 build_pantheon_overlay.py）。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    body = m.group(1)
    out: dict = {}
    current_list_key: Optional[str] = None
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and current_list_key is not None:
            item = line.lstrip()[2:].strip().strip('"').strip("'")
            out[current_list_key].append(item)
            continue
        if ":" not in line:
            current_list_key = None
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not val:
            out[key] = []
            current_list_key = key
            continue
        current_list_key = None
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()] if inner else []
        else:
            out[key] = val.strip('"').strip("'")
    return out


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🟧 Module E: 知識閉環契約 (Pass 12)                                     ║
# ║ design.md US-006 知識閉環：Metis 完成 → retrospective → wiki → Muse    ║
# ║ 驗 raw/retrospective/*.md schema + 上游 plan/insight 存在性 + 朔源協定   ║
# ║ 複用情境：任何採用 design.md US-006 風格 loop 的 PKM 系統               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def pass_12_retrospective_schema(wiki_root: Path, issues: list[Issue]) -> None:
    """Pass 12：raw/retrospective/*.md frontmatter 必要欄位 + 上游引用存在性。

    對標 design.md US-006 知識閉環（Metis 完成 → retrospective → wiki-import → Muse 佇列）。
    驗證項目：
      a) frontmatter 必含 RETRO_REQUIRED 六鍵
      b) plan_status_after ∈ RETRO_PLAN_STATUS_ENUM
      c) plan_id 對應的 audit/action-plans/*/<plan_id>.md 實際存在
      d) insight_id 對應的 audit/insights/*/<insight_id>.md 實際存在
      e) author 在 ALLOWED_AGENTS 白名單內（朔源協定 v1）
    """
    retro_dir = wiki_root / RETRO_DIR
    if not retro_dir.is_dir():
        return  # 子夾不存在則跳過（PoC 階段允許）

    # 預掃 plans / insights 索引
    plans_dir = wiki_root / "audit" / "action-plans"
    insights_dir = wiki_root / "audit" / "insights"
    plan_ids: set[str] = set()
    if plans_dir.is_dir():
        for p in plans_dir.rglob("*.md"):
            if not p.name.startswith("_"):
                plan_ids.add(p.stem)
    insight_ids: set[str] = set()
    if insights_dir.is_dir():
        for p in insights_dir.rglob("*.md"):
            if not p.name.startswith("_"):
                insight_ids.add(p.stem)

    for p in sorted(retro_dir.rglob("*.md")):
        if p.name == "README.md":
            continue
        rel = str(p.relative_to(wiki_root))
        text = read_text(p)
        fm = _retro_parse_frontmatter(text)
        if fm is None:
            issues.append(Issue("retrospective schema", "error", rel, "缺 YAML frontmatter"))
            continue
        # (a) 必要欄位
        missing = [k for k in RETRO_REQUIRED if k not in fm or fm[k] in ("", None, [])]
        if missing:
            issues.append(Issue(
                "retrospective schema", "error", rel,
                f"frontmatter 缺必填欄位 {missing}（必填集：{list(RETRO_REQUIRED)}）"
            ))
        # (b) plan_status_after enum
        psa = fm.get("plan_status_after")
        if psa and psa not in RETRO_PLAN_STATUS_ENUM:
            issues.append(Issue(
                "retrospective schema", "warn", rel,
                f"plan_status_after '{psa}' 不在 enum {sorted(RETRO_PLAN_STATUS_ENUM)}"
            ))
        # (c) plan_id 上游存在
        plan_id = fm.get("plan_id")
        if plan_id and plan_id not in plan_ids:
            issues.append(Issue(
                "retrospective schema", "warn", rel,
                f"plan_id '{plan_id}' 在 audit/action-plans/ 找不到對應檔（可能尚未建立或拼錯）"
            ))
        # (d) insight_id 上游存在
        insight_id = fm.get("insight_id")
        if insight_id and insight_id not in insight_ids:
            issues.append(Issue(
                "retrospective schema", "warn", rel,
                f"insight_id '{insight_id}' 在 audit/insights/ 找不到對應檔"
            ))
        # (e) author 朔源
        author = fm.get("author")
        if author and author not in ALLOWED_AGENTS:
            agents = [a.strip() for a in author.split("+")]
            for a in agents:
                if a and a not in ALLOWED_AGENTS:
                    issues.append(Issue(
                        "retrospective schema", "warn", rel,
                        f"author '{a}' 不在 ALLOWED_AGENTS 白名單（朔源協定 v1）"
                    ))


# ---------- Runner ----------

def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    wiki_root = Path(args[0] if args else ".").resolve()
    if not (wiki_root / WIKI_DIR).exists():
        print(RED(f"❌ 找不到 {wiki_root}/{WIKI_DIR}/，請在 AI_LLM_Wiki root 執行"), file=sys.stderr)
        return 2
    if "--bless-protected" in flags:
        return bless_protected_snapshot(wiki_root)

    print(CYAN(f"🔍 lint_wiki.py 掃描中：{wiki_root}"))

    wiki_count = len(list((wiki_root / WIKI_DIR).rglob("*.md")))
    if (wiki_root / ".git").exists():
        try:
            result = subprocess.run(
                ["git", "-C", str(wiki_root), "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True,
            )
            git_hash = result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "(no git)"
        except (OSError, subprocess.SubprocessError):
            git_hash = "(no git)"
    else:
        git_hash = "(no git)"
    timestamp = datetime.now().isoformat(timespec="seconds")
    print(f"   wiki 總數：{wiki_count}  |  git：{git_hash}  |  時間：{timestamp}")
    print()

    issues: list[Issue] = []
    wiki_idx = build_wiki_index(wiki_root)

    # Pass 6→7 state passing：Pass 6 解析 audit frontmatter 回傳 list[(path, dict)]，
    # Pass 7 消費；用 mutable container 在 lambda 間傳遞，保持單一 list-iteration 結構。
    audit_parsed: list = []

    # passes 結構：(group_header_or_None, pass_name, fn)
    # group_header 不為 None 表示這是該模組的首個 pass，輸出前印標題。
    passes = [
        ("🟦 Module A｜wiki 連結完整性 (Pass 1-4)",
            "Pass 1｜失效連結",      lambda: pass_1_dead_links(wiki_root, issues, wiki_idx)),
        (None, "Pass 2｜孤兒頁",       lambda: pass_2_orphans(wiki_root, issues, wiki_idx)),
        (None, "Pass 3｜缺漏 index",   lambda: pass_3_missing_index(wiki_root, issues, wiki_idx)),
        (None, "Pass 4｜熱門缺頁",     lambda: pass_4_hot_missing(wiki_root, issues, wiki_idx)),
        ("🟨 Module B｜log 工作流 (Pass 5)",
            "Pass 5｜log 形狀",      lambda: pass_5_log_shape(wiki_root, issues)),
        ("🟨 Module C｜audit 工作流 (Pass 6-7)",
            "Pass 6｜audit YAML",    lambda: audit_parsed.extend(pass_6_audit_yaml(wiki_root, issues))),
        (None, "Pass 7｜audit target", lambda: pass_7_audit_targets(wiki_root, issues, audit_parsed)),
        ("🟪 Module D｜wiki 內容與 v3 結構 (Pass 8-11)",
            "Pass 8｜過長警告",      lambda: pass_8_long_pages(wiki_root, issues)),
        (None, "Pass 9｜ASCII 圖",     lambda: pass_9_ascii_art(wiki_root, issues)),
        (None, "Pass 10｜v3 一致性",   lambda: pass_10_v3_consistency(wiki_root, issues)),
        (None, "Pass 11｜H2/footer 保護", lambda: pass_11_h2_footer_protection(wiki_root, issues)),
        ("🟧 Module E｜知識閉環契約 (Pass 12)",
            "Pass 12｜retrospective", lambda: pass_12_retrospective_schema(wiki_root, issues)),
    ]
    module_before = len(issues)
    module_header: Optional[str] = None
    for group_header, name, fn in passes:
        if group_header is not None:
            # 印前一個模組小計
            if module_header is not None:
                module_n = len(issues) - module_before
                tag = GREEN("✅") if module_n == 0 else YELLOW(f"⚠️  {module_n}")
                print(f"    └─ 模組小計：{tag}")
            print(f"\n  {CYAN(group_header)}")
            module_header = group_header
            module_before = len(issues)
        before = len(issues)
        fn()
        n = len(issues) - before
        tag = GREEN("✅") if n == 0 else YELLOW(f"⚠️  {n}")
        print(f"    {tag}  {name}")
    # 印最後一個模組小計
    if module_header is not None:
        module_n = len(issues) - module_before
        tag = GREEN("✅") if module_n == 0 else YELLOW(f"⚠️  {module_n}")
        print(f"    └─ 模組小計：{tag}")

    print()

    # 按 pass 分組輸出
    by_pass: dict[str, list[Issue]] = defaultdict(list)
    for it in issues:
        by_pass[it.pass_name].append(it)

    for pass_name in sorted(by_pass):
        lst = by_pass[pass_name]
        print(f"▸ {pass_name}（{len(lst)} 則）")
        # 限制每 pass 顯示 30 則
        for it in lst[:30]:
            print(it.fmt())
        if len(lst) > 30:
            print(GREY(f"    … 還有 {len(lst) - 30} 則未顯示"))
        print()

    # 總結
    sev_counter = Counter(it.severity for it in issues)
    total = len(issues)
    print("─" * 60)
    n_error = sev_counter.get("error", 0)
    n_warn = sev_counter.get("warn", 0)
    n_info = sev_counter.get("info", 0)
    n_suggest = sev_counter.get("suggest", 0)
    print(f"總計：{total} 則 issue  |  "
          f"{RED('error=' + str(n_error))}  "
          f"{YELLOW('warn=' + str(n_warn))}  "
          f"{CYAN('info=' + str(n_info))}  "
          f"suggest={n_suggest}")
    print("─" * 60)

    # exit code
    if sev_counter.get("error", 0) > 0:
        print(RED("✖ 存在 error 級 issue（exit 1）"))
        return 1
    if total == 0:
        print(GREEN("✓ 知識庫健康（exit 0）"))
    else:
        print(YELLOW("⚠ 有 warn/info/suggest，請逐項檢視（exit 0）"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
