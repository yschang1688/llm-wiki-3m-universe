---
stage: MNE
---
# Transformer架構

> **TL;DR**：Transformer 是基於自注意力機制 (Self-Attention) 的神經網路架構；它捨棄循環結構實現高度並行化，是現代[[大語言模型]]與[[生成式AI]] 的核心基礎。

| 欄位 | 內容 |
|---|---|
| 類別 | 神經網路架構 / 序列模型 |
| 提出年 | 2017 (Vaswani et al.) |
| 主要應用 | NLP (翻譯/摘要)、多模態、蛋白質摺疊 |
| 父頁 | [[深度學習]] |
| 子頁 | [[Transformer架構核心機制]]、[[注意力機制]] |
| 難度 | ★★★★☆ |
| 別名 | Transformer Model、Attention Is All You Need |

## 重點

- **【核心發現】：Transformer 的革命性在於將「序列關係」轉化為「空間相關性」的計算，透過多頭自注意力機制，實現了對長距離依賴的 $O(1)$ 路徑擷取與高度並行化。**
- **自注意力機制 (Self-Attention)**：讓模型在處理序列中每個位置時，能同時參考序列內所有其他位置的資訊，突破 RNN 的序列瓶頸與長距離依賴問題。
- **多頭注意力 (Multi-Head Attention)**：多組注意力頭 (Attention Heads) 平行運算，每個頭學習不同維度的語義關聯。
- **文字接龍的五個步驟**：(1) Tokenization、(2) Embedding、(3) Positional Encoding、(4) Attention、(5) FFN。
- **Contextualized Embedding**：產出融入上下文資訊的「情境化向量」，大幅提升語義辨識能力。

## 細節

### 核心運算：自注意力機制
自注意力的計算步驟：
1. 將輸入向量線性映射為查詢 Q (Query)、鍵 K (Key)、值 V (Value) 三組矩陣。
2. 計算注意力分數：$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$。
3. 縮放因子 $\sqrt{d_k}$ 防止點積過大導致 softmax 梯度消失。
4. 輸出是 V 的加權平均，權重由 Q 與各 K 的相似度決定。

### Sequence-to-Sequence (Seq2Seq) 的通用性與限制
在李宏毅 2021 課程中，Seq2Seq 被視為一種能處理「機器自行決定輸出長度」任務的強大瑞士刀。
- **應用場景的深度擴展**：
  - **文法剖析 (Grammar Parsing)**：將文法樹轉為帶括號的序列（如 `(S (NP ...) (VP ...))`），使剖析任務轉化為翻譯問題（Grammar as a Foreign Language）。
  - **多標籤分類 (Multi-label Classification)**：輸入文章，讓機器自行決定輸出多少個類別標籤。
  - **物件偵測 (Object Detection)**：即使是圖像任務，亦可將邊框座標視為序列由 Seq2Seq 輸出（如 DETR 模型）。
- **通用 vs. 特化**：雖然 Seq2Seq 能處理大多數問題，但針對特定領域設計的模型（如語音專用的 RNN Transducer）在效率上可能更好。

### Transformer 的運作細節：遮罩與橋接
Transformer 透過 **Encoder** 與 **Decoder** 的分工實現 Seq2Seq：
- **Encoder (編碼器)**：由多層 Self-Attention 與 FFN 組成。採用的「雙向注意力」讓每個 token 都能看到整句資訊。
- **Decoder (解碼器)**：
  - **遮罩自注意力 (Masked Self-Attention)**：在產生第 $t$ 個 token 時，遮蔽 $t$ 之後的位置，確保模型不會「偷看」答案。
  - **交叉注意力 (Cross Attention)**：Decoder 透過此機制從 Encoder 的輸出中「抽取」相關資訊。Query 來自 Decoder，而 Key/Value 來自 Encoder。
- **Autoregressive (AR) 生成**：Decoder 一次產生一個 token，並將其作為下一步的輸入，直到產生 `<END>` 為止。

### Transformer 的層次結構 (2025 視角)

| 元件 | 作用 | 優化面向 |
|------|------|-------------------|
| **Self-Attention** | 融合上下文資訊 | 擴大「函式範圍」(Scope) |
| **FFN (Feed-Forward)** | 逐位置的非線性變換 | 增加非線性逼近能力 |
| **Skip Connection** | 殘差路徑 | 提供 **Optimization** 捷徑 |
| **Normalization** | 數值穩定 | 降低優化難度，穩定梯度 |

### 三大主流衍生架構比較

| 模型類型 | 代表模型 | 結構 | 訓練目標 | 適合任務 |
|----------|----------|------|----------|----------|
| 純 Encoder | BERT、RoBERTa | 雙向注意力 | 遮罩語言模型 (MLM) | 文本分類、問答、NER |
| 純 Decoder | GPT 系列、LLaMA | 因果（單向）注意力 | 下一詞預測 | 文本生成、[[大語言模型]] |
| Encoder-Decoder | T5、BART、mT5 | 完整結構 | 序列到序列 | 翻譯、摘要、對話 |

### 跨領域應用
- **電腦視覺**：Vision Transformer (ViT) 將影像切成圖塊 (Patch) 當作序列輸入。
- **分子科學**：應用於[[聚合物性質預測]]與[[材料機器學習探索]]。
- **計算效率挑戰**：$O(n^2)$ 複雜度。改進方向包含 Flash Attention、稀疏注意力與線性注意力。

### IPAS 中級科目 3 §4.3 視角：位置編碼必要性與三大限制清單
IPAS《AI 應用規劃師（中級）》學習指引 §4.3 補上本頁尚未明列的兩點：位置編碼的必要性、以及與 RNN 對照的三大限制清單。
- **位置編碼（Positional Encoding）為何必要**：Transformer 捨棄循環結構後，模型本身無法直接感知序列的相對位置或順序，需額外注入位置編碼補足這項資訊——這是與本頁「自注意力融合上下文」機制互補、而非取代的必要設計。
- **三大限制**（IPAS 命題常考）：（1）自注意力複雜度與序列長度平方 $O(L^2)$ 成正比；（2）大型 Transformer 需大量標註或未標註資料才能充分訓練；（3）需額外引入位置編碼彌補序列順序感知缺失。
- **考點對映**：「Transformer 為何需要位置編碼」（捨棄循環結構後無法感知順序）、「Transformer 相較 RNN 的核心突破」（並行化 + 直接建立任意兩位置關係，非串接傳遞）。

## 相關概念
- [[注意力機制]] — Transformer 的靈魂運算
- [[大語言模型]] — GPT 系列等 LLM 基礎
- [[生成式AI]] — 核心架構
- [[線性注意力與Mamba架構]] — 超長序列解決方案
- [[李宏毅2025生成式ML課程索引]]

## 名詞對照表
| 中文 | 英文 | 縮寫 |
|---|---|---|
| 自注意力機制 | Self-Attention | — |
| 多頭注意力 | Multi-Head Attention | MHA |
| 前饋網路 | Feed-Forward Network | FFN |
| 殘差連接 | Residual/Skip Connection | — |

## 修訂歷史
- 2026-07-09：補 IPAS 中級科目 3 §4.3 視角（位置編碼必要性 + 三大限制清單）H3。
- 2026-05-13：深度編譯 2021 講義細節，新增 Seq2Seq 通用性應用案例（剖析、多標籤）與編解碼遮罩/橋接機制詳解。
- 2026-05-10：將李宏毅 2021 講義增補細節（Seq2Seq 定義、QA 轉換應用、通用性討論）移至細節欄位。
- 2026-05-09：升級 v3 骨架；整合 2025 講義對殘差連接與生成步驟的定義。

---
來源：`raw/web/【機器學習2021】12-13 Transformer - HackMD.md`、`raw/notebooklm/IPAS-AI應用規劃師中級初級通過筆記-16-AI應用規劃師(中級)-學習指引-科目3機器學習技術與應用_20251222101907.md`
最後更新：2026-07-09