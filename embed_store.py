import json
import httpx
import chromadb

#都 chunks.json
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


# 调用ollama的bge-m3，把一段文字变成向量
def embed(text:str):
    resp = httpx.post(
       "http://localhost:11434/api/embeddings",
        json={"model": "bge-m3", "prompt": text},
        timeout=120, 
    )
    return resp.json()["embedding"]
 
#存进Choma
client = chromadb.PersistentClient(path="./chroma-db")
collection = client.get_or_create_collection("english_chunks")

ids = [f"chunk-{i}" for i in range(len(chunks))]
embeddings = [embed(c) for c in chunks]
collection.add(documents=chunks, embeddings=embeddings, ids=ids)
print(f"已入库 {collection.count()} 块")

# 4. 试一次检索
question = "What is cultural heritage?"  # 改成你想问的
q_emb = embed(question)
result = collection.query(query_embeddings=[q_emb], n_results=3)
for i, doc in enumerate(result["documents"][0]):
    print(f"\n--- 第 {i+1} 名 ---")
    print(doc[:200])