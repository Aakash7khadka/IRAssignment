from elasticsearch import Elasticsearch


class CustomElasticSearch:

    def __init__(self):
        self.es = Elasticsearch ("http://localhost:9200")
        

    def get_reponse(self, query):
        response = self.es.search(
        index="ir_index",
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
            print("test")
            response_list = response['hits']['hits']
            output_list = [[response["_source"]['title'], response['_source']['document']] for response in response_list]
            #print(output_list)
            return output_list
            