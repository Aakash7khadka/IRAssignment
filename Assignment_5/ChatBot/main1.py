import requests
from elasticsearch import Elasticsearch

to_parse_fields = ["module_title",
                    "lecturer",
                    "applicability_in_curriculum", 
                    "language"
                    "type_of_examination",
                    "semester",
                    "intended_learning_outcomes",
                    "abbreviation"
                      ]

def ollama_embed(text, model="nomic-embed-text"):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]


def embed_query(question, model="nomic-embed-text"):
    return ollama_embed(question, model=model)

def semantic_search(es, index_name, question, k=3):
    q_emb = embed_query(question)
    body = {
        "knn": {
            "field": "embedding",
            "query_vector": q_emb,
            "k": k,
            "num_candidates": 50
        },
        "_source": to_parse_fields
    }
    resp = es.search(index=index_name, body=body)
    print(resp)
    return [hit["_source"] for hit in resp["hits"]["hits"]]


def build_prompt(question, docs):
    # context = "\n\n".join([
    #     f"Module or course: {d['module_title']}\nLecturer: {d['lecturer']}\nContent: {', '.join(d['content'])}\nOutcomes: {', '.join(d['intended_learning_outcomes'])}"
    #     for d in docs
    # ])
    context = ""
    # context = "\n".join([line + ": " + str(docs[0].get(line, "")) for line in to_parse_fields if len(docs) > 0])
    for i, doc in enumerate(docs):
        doc_name = f"Document {i+1}"
        doc_dict = "\n".join([line + ": " + str(doc.get(line, "")) for line in to_parse_fields])
        context += f"\n\n{doc_name}:\n{doc_dict}"

    return f"""You are a helpful assistant.
                Answer the question using only the context below. Look for all the data fields in the context for applicable documents for the query.
                If the answer is not present or cannot be derived from the context, say you don't know.

                If the user asks using incorrect values that match the field values, correct them using the context.

                Question: {question}

                Context:
                {context}
                """

def ollama_generate(prompt, model="gemma3:1b"):
    """Generate text answer from Ollama LLM."""
    r = requests.post("http://localhost:11434/api/generate",
                      json={"model": model, "prompt": prompt, "stream": False})
    r.raise_for_status()
    # print(r.json()['response'])
    return r.json()["response"]

def chatbot_answer(es, index_name, question):
    docs = semantic_search(es, index_name, question)
    prompt = build_prompt(question, docs)
    return ollama_generate(prompt)



if __name__ == "__main__":
    welcome_message = "Hello! I am your OVGU course assistant. How can I help you today?"

    print(welcome_message)

    while True:
        index_name = "chat_bot_index"
        es = Elasticsearch("http://localhost:9200")
        user_input = input("You: ").lower()
        if user_input in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye! Have a great day!")
            break
        else:
            print(chatbot_answer(es, index_name, user_input))
