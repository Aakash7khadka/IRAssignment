import requests
from elasticsearch import Elasticsearch

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
        "_source": [
            "module_title", "lecturer", "content", "intended_learning_outcomes"
        ]
    }
    resp = es.search(index=index_name, body=body)
    print(resp)
    return [hit["_source"] for hit in resp["hits"]["hits"]]


def build_prompt(question, docs):
    context = "\n\n".join([
        f"Module: {d['module_title']}\nLecturer: {d['lecturer']}\nContent: {', '.join(d['content'])}\nOutcomes: {', '.join(d['intended_learning_outcomes'])}"
        for d in docs
    ])
    return f"""You are a helpful assistant.
                Answer the question using only the context below.
                If the answer is not in the context, say you don't know.

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
