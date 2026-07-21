# Linear Transformer

> [!abstract] **TL;DR**:
> 透過矩陣乘法結合律的重排，將自注意力的計算量從 $O(N^2)$ 降低至 $O(N)$ 的模型，是高效 Transformer 的代表性流派之一。

## 重點
- **核心思想**：利用 $\text{Attention}(Q, K, V) = \frac{\phi(Q)(\phi(K)^T V)}{\phi(Q) \sum \phi(K)}$ 的分解特性，先計算 $K$ 與 $V$ 的互動，避免產生大的 $N \times N$ 矩陣。

## 相關概念
- `[[長序列自注意力加速技術]]`
- `[[Performer]]`
