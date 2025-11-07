from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")


index="ir_index"
def get_reponse(query):
    response = es.search(
    index=index,
    query={
	
		"bool": {
			"should": [
				{
					"match": {
						"title": {
							"query": query,
							"operator": "or"
						}
					}
				},
				{
					"match": {
						"document": {
							"query": query,
							"operator": "or"
						}
					}
				}
			],
			"minimum_should_match": 1
		}
	})
    if response['hits']['hits']:
        response_list = response['hits']['hits']
        output_list = [[response["_source"]['title'], response['_source']['document']] for response in response_list]
        print(output_list)
        return output_list
        

def create_index(es):
     
    index_settings = {
        "settings": {
            "number_of_replicas": 0,
            "index.max_ngram_diff": 20,
            "analysis": {
                "tokenizer": {
                    "custom_tokenizer": {
                        "type": "pattern",
                        "pattern": "[()-._ ]"
                    }
                },
                "analyzer": {
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "custom_tokenizer",
                        "filter": [
                            "lowercase",
                            "stop",
                            "custom_filter"
                        ]
                    }
                },
                "filter": {
                    "custom_filter": {
                        "type": "ngram",
                        "min_gram": 1,
                        "max_gram": 20
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "document": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "module_title": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "german_title": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "module_id": {
                    "type": "keyword"
                },
                "lsf_link": {
                    "type": "keyword"
                },
                "responsibility": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "lecturer": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "classes": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "applicability_in_curriculum": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "abbreviation": {
                    "type": "keyword"
                },
                "credit_points": {
                    "type": "integer"
                },
                "semester": {
                    "type": "keyword"
                },
                "term": {
                    "type": "keyword"
                },
                "duration": {
                    "type": "keyword"
                },
                "language": {
                    "type": "keyword"
                },
                "level": {
                    "type": "keyword"
                },
                "intended_learning_outcomes": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "content": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "workload": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "pre_examination_requirements": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "type_of_examination": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "teaching_method_sws": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "prerequisites_according_to_examination_regulations": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "recommended_prerequisites": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "media": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "literature": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "comments": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "embedding": {
                "type": "dense_vector",
                "dims": 768, 
                "index": True,
                "similarity": "cosine"
            }

            }
        }
    }

    index_name = "chat_bot_index"
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)  # Delete the index if it already exists
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created successfully with custom analyzer!")


if __name__ == "__main__":
    create_index(es) 
# get_reponse("machin")

    # Create the index
