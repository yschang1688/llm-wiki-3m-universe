# RAG擷取檢索合成實務

> 標準 RAG 管線分 **ingestion（切塊＋嵌入＋索引）→ retrieval（top‑k 相似）→ synthesis（LLM 讀 chunk 作答）**；相輔早期僅參數記憶的領域適配，RAG 常可在**不重新訓練**下接入私有文件。

## 重點

- **動機**：補強 LLM 知識截止、領域缺口與幻覺；可附上引用以利稽核。
- **歷史**：Meta 論文提出以稠密檢索＋非參數記憶結合預訓練 seq2seq；後續 REALM／ORQA 等屬相關混合記憶路線。
- **挑戰**：擷取品質、chunk 粒度、嵌入效率、泛化微調與 rerank 等，需迭代監控。

## 細節

- 概念總覽見 [[檢索增強生成]]；本篇保留課程 raw 的三階段用語方便對照英文教材。

## 相關概念

- [[檢索增強生成]]
- [[Embeddings語意表徵要旨]]
- [[大語言模型]]

---
來源：`raw/web/[Week 4] Retrieval Augmented Generation - HackMD.md`
最後更新：2026-04-17
