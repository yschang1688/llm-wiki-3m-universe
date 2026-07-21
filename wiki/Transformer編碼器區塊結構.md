# Transformer編碼器區塊結構

> **TL;DR**：Transformer Encoder 由多個 Block 堆疊而成，每個 Block 整合了多頭自注意力、殘差連接、層正規化與前饋網路，是實現並行語義理解的核心單元。

| 欄位 | 內容 |
|---|---|
| 類別 | 神經網路架構 / Encoder 元件 |
| 主要應用 | BERT、Transformer 編碼端、特徵提取 |
| 父頁 | [[Transformer架構]] |
| 子頁 | [[Transformer架構核心機制]]、[[注意力機制]] |
| 難度 | ★★★★☆ |
| 別名 | Transformer Encoder Block, BERT Block |

## 重點

- **【核心發現】：Encoder Block 透過「殘差連接 (Residual Connection)」與「層正規化 (Layer Normalization)」確保了深層網路的梯度穩定性，並利用自注意力機制實現了非序列性的平行運算。**
- 每個 block「輸入一排向量、輸出一排向量」，但內部是多層組合，不宜直接等同單一 `layer`。
- 典型流程：Self-Attention → 殘差加回輸入 → Layer Norm → FFN → 再殘差加回 → Layer Norm；輸入端另有位置編碼。
- 與 Post-LN／Pre-LN 變體：原始論文 Layer Norm 位置可調整（如論文 *On Layer Normalization in the Transformer Architecture*）；Batch Norm 在 Transformer 中常不如 Layer Norm（可對照 PowerNorm 等討論）。

## 細節

### Block 內部架構與運算流
在 Transformer 的 Encoder 中，輸入序列會經過多個 Block 的處理。每個 Block 內部並非單一網路層，而是由以下兩大核心組件構成：
1. **Multi-Head Self-Attention**：讓序列中的每個位置都能考慮到全域資訊，打破了 RNN 必須依序處理的限制。
2. **Feed-Forward Network (FFN)**：對每個位置的向量進行獨立的非線性變換。

### 穩定性機制：Residual 與 Layer Norm
為了使深度網路易於訓練，Block 引入了以下機制：
- **殘差連接 (Residual Connection)**：運算為 $x + \text{Sublayer}(x)$。這種「捷徑」設計能讓梯度直接流向較淺層，有效緩解梯度消失問題。
- **層正規化 (Layer Normalization)**：針對單一樣本的所有特徵進行歸一化。研究顯示，Layer Norm 在處理變長序列與小 Batch 時，穩定性優於 Batch Norm。

### 位置資訊的注入 (Positional Encoding)
由於 Self-Attention 本質上是「袋中向量」運算，無法分辨輸入的先後順序。因此，在進入第一個 Encoder Block 之前，必須將 **Positional Encoding** 與輸入 Embedding 相加，以提供模型必要的時序座標資訊。

### Seq2seq 的廣義擴展
雖然 Encoder 最初設計用於機器翻譯，但其強大的特徵提取能力使其能應用於多種非典型序列任務：
- **文法剖析 (Grammar Parsing)**：將文法樹視為序列生成問題。
- **物件偵測 (Object Detection)**：如 DETR 模型，將圖像特徵輸入 Encoder，並由 Decoder 輸出物件座標。
- **多標籤分類 (Multi-label Classification)**：讓模型自發決定輸出的標籤數量。

## 相關概念

- [[Transformer架構]]
- [[Seq2seq注意力QKV要旨]]
- [[Decoder遮罩自注意力]]

---
來源：`raw/web/【深度學習與神經網路】5.2 Transformer 機制解說 (上).md`
最後更新：2026-05-22

