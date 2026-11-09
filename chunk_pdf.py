from pypdf import PdfReader
import json




reader = PdfReader("Unit 4.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() or ""


print(f"共{len(text)}字,{len(reader.pages)}页")

#切块：每块500字，相邻两块重叠50字
chunk_size = 500
overlap = 50
chunks = []
start = 0
while start <len(text):
    chunks.append(text[start:start + chunk_size])
    start += chunk_size - overlap

print(f"切成{len(chunks)}块")
for i, c in enumerate(chunks[:3]):
    print(f"\n--- 第{i+1}块 （前100字） ---")
    print(c[:100])


with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
print(f"已保存{len(chunks)}块到 chunks.json")