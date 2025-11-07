import parse_handbook
from create_index import create_index
from elasticsearch import Elasticsearch


import requests

#nomic-embed-text
def ollama_embed(text, model="nomic-embed-text"):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]


def add_docs_to_index(es, index_name, docs):

    important_fields_to_embed = [
        "abbreviation",
        "module_title",
        "applicability_in_curriculum",
        "classes",
        "credit_points",
        "duration",
        "german_title",
        "language",
        "lecturer",
        "level",
        "literature",
        "module_title",
        # "pre_examination_requirements",
        # "prerequisites_according_to_examination_regulations",
        # "recommended_prerequisites",
        "responsibility",
        "semester",
        "teaching_method_sws",
        "term",
        "title",
        "type_of_examination",
        "workload"
    ]


    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name) 
        create_index(es)

        for i, doc in enumerate(docs):
            # print(doc)
            combined_parts = []
            for field in important_fields_to_embed:
                if field in doc and doc[field] is not None:
                    value = doc[field]
                    if isinstance(value, (list, tuple)):
                        value_str = ", ".join(
                            ", ".join(map(str, item)) if isinstance(item, (list, tuple)) else str(item)
                            for item in value
                        )
                    else:
                        value_str = str(value)
                    combined_parts.append(f"{field}: {value_str}")
            combined_text = ", ".join(combined_parts)
            embedding = ollama_embed(combined_text)
            doc_with_emb = {**doc, "embedding": embedding}
            print(combined_text)
            es.index(index=index_name, id=i+1, document=doc_with_emb)

    except Exception as e:
        print(f"Error creating index: {e}")
        return



if __name__ == "__main__":
    es = Elasticsearch("http://localhost:9200")
    index_name = "chat_bot_index"
    docs = parse_handbook.get_handbook_data()
    add_docs_to_index(es, index_name, docs)