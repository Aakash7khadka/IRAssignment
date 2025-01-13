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
            "number_of_replicas": 0,  # Set replication to 0 for local environment
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
                "filter":{
                    "custom_filter":{
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
                "content": {
                    "type": "text",
                    "analyzer": "custom_analyzer"  
                }
            }
        }
    }

    index_name = "ir_index"
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)  # Delete the index if it already exists
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created successfully with custom analyzer!")


   
create_index(es) 
# get_reponse("machin")

    # Create the index
