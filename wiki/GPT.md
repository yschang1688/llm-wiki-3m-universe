# GPT

> **TL;DR**：GPT (Generative Pre-trained Transformer) 是 OpenAI 以 Transformer Decoder + 大規模自迴歸語言模型預訓練的系列模型；GPT-3/4 的規模化突現催生了 in-context learning 與現代 LLM 時代。

| 欄位 | 內容 |
|---|---|
| 類別 | LLM 預訓練模型 |
| 提出年 | 2018 (GPT-1, OpenAI) |
| 主要應用 | 文字生成、程式碼補全、對話、推理 |
| 父頁 | [[Transformer架構]] |
| 子頁 | — |
| 難度 | ★★★☆☆ |
| 別名 | Generative Pre-trained Transformer、ChatGPT（指令微調版） |

## 重點

- **【核心發現】**：**GPT 系列最大的發現是「規模化突現」：模型大到某臨界點後，會自發出現訓練時未設計的能力（in-context learning、chain-of-thought reasoning），顛覆了 AI 能力邊界的認知。**
- **與 [[BERT]] 的核心差異**：
  - GPT：Decoder-only，單向（從左到右）自迴歸，擅長生成。
  - BERT：Encoder-only，雙向，擅長理解（分類/抽取）。
- **系列演進**：GPT-1（1.17 億）→ GPT-2（15 億）→ GPT-3（1750 億）→ GPT-4（多模態）。
- **In-context Learning**：GPT-3 展示無需梯度更新，僅靠 prompt 中的幾個範例即可執行新任務。

## 細節

### Decoder-only 自迴歸訓練
- 訓練目標：$\max \sum_t \log P(x_t | x_{<t})$（預測下一個 token）。
- 使用 Masked Self-Attention，確保每個 token 只看到前面的序列。
- 推理時依序採樣輸出（Top-k、Nucleus Sampling、Beam Search 等解碼策略）。

### GPT 系列關鍵里程碑

| 版本 | 年份 | 參數 | 里程碑 |
|---|---|---|---|
| GPT-1 | 2018 | 117M | 預訓練+微調範式 |
| GPT-2 | 2019 | 1.5B | 零樣本能力浮現、因強大而延遲發布 |
| GPT-3 | 2020 | 175B | In-context learning、few-shot 無需微調 |
| InstructGPT | 2022 | 1.3B+ | [[RLHF]] 對齊、前身為 ChatGPT |
| GPT-4 | 2023 | 未公開 | 多模態、複雜推理、MMLU 接近人類 |

### 與 [[RLHF]] 的結合
ChatGPT = GPT-3.5 + InstructGPT（[[RLHF]] 對齊），展示了「生成能力 + 人類偏好對齊」的強力組合。

## 相關概念

- [[Transformer架構]] — 直接父架構。
- [[BERT]] — 同時期的 Encoder-only 對照。
- [[RLHF]] — GPT → ChatGPT 的對齊手段。
- [[基礎模型]] — GPT 系列是最知名的基礎模型。

## 修訂歷史

- 2026-05-19：初稿建立。

---
來源：`raw/web/李宏毅_ELMO, BERT, GPT - HackMD.md`
最後更新：2026-05-19
