from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")


def fetch_data_from_elasticsearch(index_name):
    """
    Fetch all documents from the specified Elasticsearch index.
    """
    query = {"query": {"match_all": {}}}
    results = scan(es, index=index_name, query=query)
    department_data = []

    for result in results:
        source = result["_source"]
        department_id = source.get("Department ID")
        threat_score = source.get("Threat Score")
        importance = source.get("Importance")
        if department_id is not None and threat_score is not None and importance is not None:
            department_data.append((department_id, [threat_score], importance))

    return department_data
