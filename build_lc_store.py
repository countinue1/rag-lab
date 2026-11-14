import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db_lc",
    collection_name="english_chunks",
)
print("已入库", vectorstore._collection.count(), "块")
