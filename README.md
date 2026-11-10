# rag-lab：RAG 私有知识库

把 PDF 讲义喂给知识库，让它能带着出处回答问题。这是大模型应用开发路线里的 RAG 项目（W9–W14）。

## 里面有什么

- `chunk_pdf.py`：用 pypdf 解析 PDF，按 500 字一块、重叠 50 字切分，存进 `chunks.json`
- `chunks.json`：切好的文本块（38 块，来自 Unit 4.pdf）
- `Unit 4.pdf`：练习用的英文讲义

## 怎么跑

```bash
pip install pypdf
python chunk_pdf.py
