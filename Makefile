# Makefile — AI_LLM_Wiki 常用任務
# 對應 openspec/knowledge-universe/dashboard-spec.md。

.PHONY: help overlay graphify dashboard dashboard-clean lint

ROOT := $(shell pwd)
EXPORT_DIR := export/web-dashboard
GRAPHIFY_PATH ?= ../graphify

help:
	@echo "Targets:"
	@echo "  overlay          build pantheon-overlay.json (L2)"
	@echo "  graphify         build graph.json/graph.html via graphify (L1, best-effort)"
	@echo "  dashboard        full chain: overlay → graphify → index.html (L3)"
	@echo "  dashboard-clean  remove generated artefacts (keep .gitkeep)"
	@echo "  lint             run tools/lint_wiki.py"

overlay:
	@python3 tools/build_pantheon_overlay.py

graphify:
	@if python3 -c "import graphify" 2>/dev/null; then \
		python3 tools/wiki_to_graphify.py && \
		python3 tools/build_graph_views.py; \
	else \
		echo "[graphify] not installed; skipping (dashboard will show fallback frame)"; \
		echo "  install: pip install $(GRAPHIFY_PATH)"; \
	fi

dashboard: overlay graphify
	@python3 tools/build_dashboard.py

dashboard-clean:
	@find $(EXPORT_DIR) -type f ! -name '.gitkeep' -delete 2>/dev/null || true
	@echo "[clean] $(EXPORT_DIR)/ purged (kept .gitkeep)"

lint:
	@python3 tools/lint_wiki.py .
