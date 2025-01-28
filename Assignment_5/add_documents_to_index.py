import os
from elasticsearch import Elasticsearch
from docx import Document

es = Elasticsearch("http://localhost:9200")

# Index name
index_name = "ir_index1"


list_of_documents = [f for f in os.listdir("test2")]
for x in list_of_documents:
    file_path = os.path.join("test2",x)

    if x.endswith(".docx"):
        doc = Document(file_path)
        content = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    elif x.endswith(".csv"):
        with open(file_path, "r", encoding= "utf-8") as file:
            content = file.read()
    else:
        continue
    document = {
        "title": x.replace(".txt", ""),
        "document": content
    }
    response = es.index(index=index_name, document=document)
            # print("Document added:", response["_id"])



