import os
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index name
index_name = "ir_index"


list_of_documents = [f for f in os.listdir("documents")]
for x in list_of_documents:
    with open(os.path.join("documents",x), "r", encoding= "utf-8") as file:
        document = {
            "title": x.replace(".txt", ""),
            "document": file.read()
        }
        response = es.index(index=index_name, document=document)
        # print("Document added:", response["_id"])



