# 向量資料庫與ANN檢索要旨

> **TL;DR**：百萬到十億級嵌入下精確 kNN 不可行，需 ANN 以微小精度換吞吐；向量庫封裝索引與查詢 API，並在專用庫與 SQL 向量擴充間做架構取捨。

> 當嵌入筆數達百萬至十億級，精確 kNN 不可行，需 **ANN（近似最近鄰）** 以微小精度換取吞吐；向量資料庫封裝索引、持久化與查詢 API，並在「專用庫 vs 既有 SQL＋向量擴充」間做架構取捨。

| 欄位 | 內容 |
|---|---|
| 類別 | 檢索基礎設施／近似搜尋 |
| 提出年 | — |
| 主要應用 | RAG、推薦、以圖搜圖、多模態索引 |
| 父頁 | [[檢索增強生成]] |
| 子頁 | [[Embeddings語意表徵要旨]]、[[Qdrant圖像向量檢索入門]] |
| 難度 | ★★★★☆ |
| 別名 | Vector DB、ANN 檢索 |

## 重點

- **ANN 家族**：如 HNSW、ScaNN 等，適合高維稀疏／稠密向量的近線上檢索。
- **產品形態**：
    - **專用向量庫**（Qdrant、Milvus、Weaviate）：利於非結構化數據為主的工作負載。
    - **整合式資料庫**（AlloyDB, PostgreSQL）：如 GCP 的 AlloyDB 內建 ScaNN 演算法，能結合 SQL 關聯查詢與向量搜尋，具備事務一致性優勢。
- **治理**：多模態索引、維運成本、標準碎片化、人才與合規（Day2 Q&A 敘事）是企業導入時常見阻力。
- **即時性與漂移**：利用變更數據捕獲（CDC）技術即時反映數據更新，防止 RAG 系統中的數據漂移。

## 細節

### 架構地圖

```mermaid
flowchart LR
  E[嵌入管線] --> I[索引 ANN]
  I --> Q[查詢 API]
  Q --> A[應用 RAG 或搜尋]
```

### 專用 vs. 整合式資料庫取捨
根據專家（Allan, Patricia）分析，企業在選擇向量儲存方案時需權衡架構：
- **AlloyDB (PostgreSQL-compatible)**：GCP 提供的全相容資料庫，內建 **ScaNN** 演算法。其優勢在於能結合 SQL 關聯查詢與向量搜尋，具備事務一致性（Transactional Consistency），能即時反映數據更新。
- **專用向量庫**（如 Qdrant, Milvus）：適合處理超大規模非結構化數據（如數十億張圖片），雖然在極致擴展性上有優勢，但通常伴隨較高維運成本與資料最終一致性（Eventual Consistency）的挑戰。

### 近似最近鄰 (ANN) 核心演算法
- **ScaNN (Scalable Nearest Neighbors)**：Google 開發，針對高維資料設計，在搜尋速度與準確度權衡（Recall-Latency trade-off）上表現卓越。
- **HNSW (Hierarchical Navigable Small World)**：基於圖結構的常見 ANN 索引，具備極高的查詢效率。
- **LSH (Locality Sensitive Hashing)**：透過將相似項目分組到同一個「哈希桶」中來大幅縮小搜尋空間。

### 即時性與漂移管理
在動態或即時應用中，確保 RAG 系統與最新數據保持關聯至關重要：
- **變更數據捕獲 (CDC)**：利用 CDC 技術監控資料庫異動，並搭配即時 RAG 架構（Real-time RAG），可有效應對數據漂移。
- **監測與更新**：持續監控嵌入隨時間產生的語意漂移，並視需求採用增量索引技術以降低更新延遲。

### 來源摘記
...
- 與 [[Qdrant圖像向量檢索入門]] 對讀：後者以圖像嵌入與以圖搜圖 示範具體產品管線。

## 相關概念

- [[Embeddings語意表徵要旨]]
- [[Qdrant圖像向量檢索入門]]
- [[檢索增強生成]]

## Muse 種子：與 [[Embeddings語意表徵要旨]] 成對（原題：Embeddings 與向量資料庫）

## 名詞對照表

| 中文 | 英文 | 縮寫 |
|---|---|---|
| 近似最近鄰 | approximate nearest neighbor | ANN |
| 向量資料庫 | vector database | Vector DB |
| 變更數據捕獲 | change data capture | CDC |
| 事務一致性 | transactional consistency | — |

## 延伸閱讀

- [[檢索增強生成]]｜RAG 主鏈路
- [[Embeddings語意表徵要旨]]｜嵌入與語意

## 修訂歷史

- 2026-05-27：增補 AlloyDB 權衡、CDC 漂移管理與 ScaNN/LSH 演算法細節 (Day 2 內容)
- 2026-04-22：升級 v3（補 TL;DR／Infobox／`## 細節` 內架構地圖與來源摘記；`## 重點` 增延遲召回與資料生命周期；保留原 lead、三條重點、Qdrant 對讀句、Muse）
- 2026-04-17：初稿

---
來源：`raw/web/[Day 2] Embeddings 與向量資料庫.md`、`raw/web/【大語言模型應用與實戰】[Day 2] Embeddings 與向量資料庫.md`
最後更新：2026-05-27
