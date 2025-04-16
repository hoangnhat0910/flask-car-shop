from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

product = {
    "name": "Ford Explorer 2024",
    "description": "A powerful SUV with modern design and spacious interior",
    "price": 40000
}

es.index(index="products", id=1, body=product)

res = es.search(index="products", body={"query": {"match_all": {}}})
for hit in res["hits"]["hits"]:
    print(hit["_source"])
es.delete(index="products", id="<_id>")
