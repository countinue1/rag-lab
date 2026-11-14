from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 打开已有的向量库
embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma(
    persist_directory="./chroma_db_lc",
    embedding_function=embeddings,
    collection_name="english_chunks",
)
print("LangChain 看到的条数:", vectorstore._collection.count())

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. 把捞回的块标号拼成一大段
def format_docs(docs):
    return "\n\n".join(f"[{i+1}] {d.page_content}" for i, d in enumerate(docs))

# 3. Prompt 模板
prompt = ChatPromptTemplate.from_template("""请只根据下面资料回答问题，每条信息后面标出资料编号。
只要资料里有相关内容，就根据资料总结回答；只有资料和问题完全无关时，才回答“文档里没提到”，不要自己编。
回答示例：文化遗产面临自然和人为两方面的威胁[1]。

资料：
{context}

问题：{question}""")

# 4. 模型
llm = ChatOllama(model="qwen2.5:7b")

docs = retriever.invoke("What threats does the cultural heritage face?")
print(len(docs))
if docs:
    print(docs[0].page_content[:100])


for i, d in enumerate(docs):
    print(i + 1, d.page_content[:60].replace("\n", " "))




# 5. 串成一条链
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke("What is the capital of France?"))

