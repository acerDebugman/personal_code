#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import gzip
import time
import json


def do_fn(src_file, result_file):
    fd_in = gzip.open(src_file, "rb") if src_file.endswith('.gz') else open(src_file, 'r')
    fd_out = open(result_file, 'w')
    line_num = 0
    for line in fd_in:
        line_num += 1
        device_id, tagstr = line.strip().split('\t')
        tags = [int(item) for item in tagstr.split(',')]
        if len(device_id) == 32:
            id_type = 'md5_imei'
        elif len(device_id) == 36:
            id_type = 'raw_idfa'
        else:
            id_type = 'cookie_id'

        time_stamp = int(time.time())

        create_map = {'create': {'_index': 'dmp_test', '_type': 'tags', '_id': device_id}}
        request_body = {'id_type': id_type, 'tags': tags, 'time_stamp': time_stamp}

        fd_out.write(json.dumps(create_map) + '\n')
        fd_out.write(json.dumps(request_body) + '\n')

    fd_out.close()


if __name__ == '__main__':
    do_fn(sys.argv[1], sys.argv[2])
