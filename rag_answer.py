import httpx
import chromadb

#把文字变成向量
def embed(text: str):
    resp = httpx.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "bge-m3", "prompt": text},
        timeout=120,
    )
    return resp.json()["embedding"]

#打开已有的库，只读，不写
client = chromadb.PersistentClient(path="./chroma-db")
collection = client.get_or_create_collection("english_chunks")

#回答问题：先捞，再拼pompt,最后问模型
def ask(question:str):
    q_emb = embed(question)
    result = collection.query(query_embeddings=[q_emb], n_results=3)
    docs = result["documents"][0]
    # print(docs)

    context = "\n\n".join(f"[{i+1}] {d}" for i, d in enumerate(docs))
    prompt = f"""请只根据下面资料回答问题，每条信息后面标出资料编号。回答示例：文化遗产面临自然和人为两方面的威胁[1]。
只要资料里有相关内容，就根据资料总结回答；只有资料和问题完全无关时，才回答“文档里没提到”，不要自己编。

资料：
{context}

问题：{question}"""

    resp = httpx.post(
        "http://localhost:11434/v1/chat/completions",
        json={
            "model": "qwen2.5:7b",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    return resp.json()["choices"][0]["message"]["content"]

print(ask("What is the capital of France?"))





