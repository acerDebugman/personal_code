# -*- coding:utf-8 -*-

import argparse
import collections
parse = argparse.ArgumentParser()
parse.add_argument("program_file", help="program file path")
parse.add_argument("ad_all", help="ad all log file")
parse.add_argument("out_file", help="output file")
args = parse.parse_args()
program_file = args.program_file
ad_all = args.ad_all
out_file = args.out_file

brand_dict = dict()
result_dict = collections.defaultdict(int)

with open(program_file) as program_fp, open(ad_all) as ad_all_fd:
    for line in ad_all_fd:
        #caid, brand, media = line.strip().split('#')
        company, caid, spid, industry, brand, goods, media_type, media, province, \
        city, datestr, gender, age, edu, income, device_model = line.strip().split("#")
        #brand_media = industry + "#" + brand + '#' + goods + '#' + media
        brand_media = ",".join((industry, brand, goods, media))
        brand_dict[caid + "," + spid] = brand_media

    #print(str(brand_dict))
    for line in program_fp.readlines():
        #tmp_array = line.strip().split('#')
        time, Router_MAC, media, campain_id, spid, title, content, top, sub,*others = line.strip().split(",")
        if others:
            continue

        #caid_spid = 'a' + tmp_array[0] + '#b' + tmp_array[1]
        caid_spid = 'a' + campain_id + ',b' + spid
        if caid_spid in brand_dict:
            brand_media = brand_dict[caid_spid]
            #brand, media = brand_media.split(',')
            program = content
            dims = ",".join((brand_media, program))
            result_dict[dims] += 1

    sum = 0
    with open(out_file, "w") as fd:
        for dim, count in result_dict.items():
            fd.write(",".join((dim, str(count))) + "\n")
            sum += count

    print(sum)

