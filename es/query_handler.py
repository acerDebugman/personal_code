# -*- coding: utf-8 -*-
'''
comments:
'''
__author__ = "joe zhang"
from elasticsearch import Elasticsearch

def main():
    host = "http://localhost:9200"
    es = Elasticsearch(hosts=host)
    index = "dmp"
    doc_type = "tags"
    query_content = ""
    rs = es.search(index=index, doc_type=doc_type, body=query_content)
    print(rs)
    pass


if __name__ == "__main__":
    main()
    print("done")
