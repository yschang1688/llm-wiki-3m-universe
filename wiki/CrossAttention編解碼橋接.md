# CrossAttention編解碼橋接

> **TL;DR**：Cross-attention 連接 Encoder 與 Decoder：Query 來自 Decoder 當前狀態，Key/Value 來自 Encoder 輸出序列，使解碼每一步能「對齊」並抽取來源端語境。

| 欄位 | 內容 |
|---|---|
| 類別 | 神經網路機制／注意力變體 |
| 提出年 | 2017 (Transformer) |
| 主要應用 | 編解碼架構 (E-D)、語音辨識、翻譯 |
| 父頁 | [[Transformer架構]] |
| 子頁 | [[Decoder遮罩自注意力]] |
| 難度 | ★★★★☆ |
| 別名 | Encoder-Decoder Attention |

## 重點

- **【核心發現】：Cross-attention 扮演了編解碼器間的「資訊檢索橋樑」，Decoder 透過發送 Query 主動從 Encoder 的 Key-Value 集合中「抽取」相關特徵，實現了從源序列到目標序列的語義對齊。**
- 計算流程：Decoder 經 masked self-attention 得向量，線性映射為 \(q\)；與 Encoder 各位置的 \(k_1\ldots k_m\) 算分數、softmax 得權重，對 \(v_1\ldots v_m\) 加權和得到 context，再送入 FFN。
- 原始 Transformer 常取 Encoder 最末層作 K/V；亦有研究層級多視角 cross-attention，不必固定最後一層。
- 經典語音 Seq2seq 文獻 *Listen, Attend and Spell* 可視為早期 cross-attention 應用脈絡。

## 細節

- **李宏毅 2021 講義增補細節**：
  - **橋樑機制**：Decoder 透過產生 Q，主動從 Encoder 的 K, V 中抽取資訊。
  - **對齊視覺化**：在 ASR (語音辨識) 中，Attention 權重通常呈對角線分布（由左上到右下），反映時序對齊。
  - **層級連接**：Decoder 每層都與 Encoder 最後一層進行 Cross-attention，確保深層資訊的完整傳遞。
- 與 [[Seq2seq注意力QKV要旨]] 對照：RNN 時代用隱狀態對齊；Transformer 則以堆疊向量與學習到的 Q/K/V 投影實現相同「對齊—加權」邏輯。

## 相關概念

- [[Transformer架構]]
- [[Seq2seq注意力QKV要旨]]
- [[Decoder遮罩自注意力]]

## 修訂歷史

- 2026-05-22：增補【核心發現】並更新來源。
- 2026-05-10：將李宏毅 2021 講義增補細節（抽取機制、對齊視覺化、層級連接方式）移至細節欄位。
- 2026-04-17：初稿。

---
來源：`raw/web/【機器學習2021】12~13 Transformer - HackMD.md`、`raw/web/【深度學習與神經網路】5.3 Transformer 機制解說 (下).md`
最後更新：2026-05-22

