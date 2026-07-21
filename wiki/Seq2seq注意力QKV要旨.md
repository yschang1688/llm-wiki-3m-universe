# Seq2seq注意力QKV要旨

> **TL;DR**：QKV 機制是注意力核心：透過 Query 與 Key 的對齊分數來加權 Value，實現了從 RNN 的隱狀態對齊到 Transformer 並行自注意力的數學抽象演進。

| 欄位 | 內容 |
|---|---|
| 類別 | 神經網路機制 / 注意力計算 |
| 提出年 | 2015 (RNN Attention) / 2017 (Transformer QKV) |
| 主要應用 | NLP、Seq2seq 模型、Transformer 基礎 |
| 父頁 | [[Transformer架構]] |
| 子頁 | [[Transformer架構核心機制]]、[[注意力機制]] |
| 難度 | ★★★★☆ |
| 別名 | QKV Mechanism, Attention Weighting |

## 重點

- **【核心發現】：QKV 機制將「序列比對」轉化為「矩陣運算」，Query (問) 與 Key (索引) 的相似度決定了對 Value (內容) 的關注程度，是實現並行化注意力計算的底層數學骨架。**
- Seq2seq 含 Encoder（壓縮輸入序列）與 Decoder（依序生成）；有 Attention 時每一步 Decoder 狀態會對全部 Encoder 狀態算相關性。
- 對齊分數：將 Encoder 狀態 \(h_i\) 經 \(W_K\) 得 \(k_i\)，Decoder 狀態 \(s_j\) 經 \(W_Q\) 得 \(q_j\)；所有 \(k\) 可排成矩陣 \(K\)，與 \(q\) 比對得到注意力權重。
- 權重對應的 \(h_i\) 經值映射（與 V 概念銜接）加權後即 context vector，供 Decoder 產生下一符元。

## 細節

### 從 RNN 到 Transformer 的 QKV 演進
在傳統的 RNN + Attention 架構中，注意力是用來改善 Seq2seq 模型中長距離依賴問題的。
- **RNN 時代**：Encoder 的隱狀態 \(h_1 \ldots h_m\) 被直接視為被比對的對象。Decoder 的當前狀態 \(s_j\) 則去跟所有 \(h_i\) 做對比。
- **Transformer 時代**：將此過程進一步抽象化，引入三個可學習矩陣 \(W_Q, W_K, W_V\)。
  - **Query (Q)**：由目前狀態映射而來，代表「我想找什麼」。
  - **Key (K)**：由候選狀態映射而來，代表「我有什麼特徵可供比對」。
  - **Value (V)**：由候選狀態映射而來，代表「我實際包含的內容」。

### 矩陣運算流程
計算 context vector (c) 的步驟如下：
1. **Query 與 Key 的比對**：將 $m$ 個 $k$ 向量排成矩陣 $K$，計算 $q_j \cdot K^T$，得到一個 $m$ 維的分數向量。
2. **Softmax 歸一化**：透過 $\text{softmax}(\text{score})$ 得到 $\alpha_{1j} \ldots \alpha_{mj}$，代表對輸入各位置的關注程度。
3. **Value 加權和**：將分數與對應的 $v_i$ 相乘並加總，$c_j = \sum_{i=1}^m \alpha_{ij} v_i$。

### Attention Layer vs. Self-Attention Layer
- **Attention Layer (跨注意力)**：用於 Seq2seq 的 Encoder-Decoder 橋接。Q 來自 Decoder 輸入 $X'$，K 和 V 來自 Encoder 輸入 $X$。
- **Self-Attention Layer (自注意力)**：僅有一個輸入序列 $X$，Q、K、V 皆由同一組 $X$ 映射而來。這使得序列中的每個位置都能考慮到全域資訊，取代了 RNN 的時序依賴。

## 相關概念

- [[Transformer架構]]
- [[Transformer編碼器區塊結構]]
- [[CrossAttention編解碼橋接]]

---
來源：`raw/web/【深度學習與神經網路】5.1 Transformer — Attention Is All You Need.md`
最後更新：2026-05-22

