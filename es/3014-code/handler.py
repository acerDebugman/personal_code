import gzip
import json
import os
import time
import sys
from elasticsearch import Elasticsearch


class PushHandler:
    def __init__(self, index, doc_type, host):
        self.index = index
        self.doc_type = doc_type
        self.es = Elasticsearch(host)
        self.time_stamp = int(time.time())

    def push(self, path):
        if os.path.isdir(path):
            self.push_dir(path)
        else:
            self.push_file(path)

    def push_dir(self, dir):
        file_list = os.listdir(dir)
        for file in file_list:
            file_path = os.path.join(dir, file)
            self.push_file(file_path)

    def push_file(self, filename):
        count = 0
        print(filename)
        #with gzip.GzipFile(filename, "r") as fp:
        with open(filename, "r") as fp:
            buffer_list = []
            for line in fp:
                '''
                if count < 342180000:
                    count +=1
                    continue
                '''

                line = line.decode("utf-8")
                device_id, tag_str = line.strip().split('\t')
                tags = [int(item) for item in tag_str.split(',')]
                if len(device_id) == 32:
                    id_type = 'md5_imei'
                elif len(device_id) == 36:
                    id_type = 'raw_idfa'
                else:
                    id_type = 'cookie_id'

                buffer_list.append({
                    'id': device_id,
                    'id_type': id_type,
                    'time_stamp': self.time_stamp,
                    'tags': tags
                })

                count += 1
                if count % 1000 == 0:
                    self.push_bulk(buffer_list)
                    buffer_list.clear()
                    print(count)

            if buffer_list:
                self.push_bulk(buffer_list)
            buffer_list.clear()

    def push_bulk(self, doc_list):
        body_list = []

        for doc in doc_list:
            meta = dict()
            meta['index'] = dict()
            uuid = doc['id']
            meta['index']['_id'] = uuid

            body = {'id_type': doc['id_type'], 'time_stamp': doc['time_stamp'], 'tags': doc['tags']}

            body_list.append(json.dumps(meta, ensure_ascii=False))
            body_list.append(json.dumps(body, ensure_ascii=False))

        request_body = "\n".join(body_list)

        try:
            self.es.bulk(body=request_body, index=self.index, doc_type=self.doc_type, request_timeout=180)
        except Exception as e:
            raise Exception(str(e))


if __name__ == '__main__':
    #host = 'http://localhost:8882'
    #index = 'dmp_tag_test'
    host = 'http://localhost:9200'
    index = 'dmp'
    doc_type = 'tags'
    files = sys.argv[1]
    pusher = PushHandler(index, doc_type, host)
    pusher.push_file(files)
