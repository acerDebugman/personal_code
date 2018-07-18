# -*- coding:utf-8 -*-

import argparse
parse = argparse.ArgumentParser()
parse.add_argument("program_file", help="program file path")
parse.add_argument("ad_all", help="ad all log file")
args = parse.parse_args()
program_file = args.program_file
ad_all = args.ad_all

brand_dict = dict()
result_dict = dict()

with open(program_file) as program_fp, open(ad_all) as ad_all_fd:
    for line in ad_all_fd:
        #caid, brand, media = line.strip().split('#')
        company, caid, spid, industry, brand, goods, media_type, media, province, \
        city, datestr, gender, age, edu, income, device_model = line.strip().split("#")
        #brand_media = industry + "#" + brand + '#' + goods + '#' + media
        brand_media = ",".join((industry, brand, goods, media))
        brand_dict[caid + "," + spid] = brand_media

    '''
    for line in brand_fp.readlines():
        caid, spid, brand, media = line.strip().split('#')
        caid_spid = caid + '#' + spid
        brand_media = brand + '#' + media
        brand_dict[caid_spid] = brand_media
    '''

    for line in program_fp.readlines():
        #tmp_array = line.strip().split('#')
        time, Router_MAC, media, campain_id, spid, title, content, top, sub,*others = line.strip().split(",")
        if not others:
            continue

        #caid_spid = 'a' + tmp_array[0] + '#b' + tmp_array[1]
        caid_spid = 'a' + campain_id + ',b' + spid
        if caid_spid in brand_dict.keys():
            brand_media = brand_dict[caid_spid]
            #brand, media = brand_media.split(',')
            program = content
            dims = ",".join((brand_media, program))
            result_dict[dims]
            '''
            if brand in result_dict.keys():
                if media in result_dict[brand].keys():
                    if program in result_dict[brand][media].keys():
                        count = result_dict[brand][media][program]
                        result_dict[brand][media][program] = count + 1
                    else:
                        result_dict[brand][media][program] = 1

                else:
                    result_dict[brand][media] = dict()
                    result_dict[brand][media][program] = 1
            else:
                result_dict[brand] = dict()
                result_dict[brand][media] = dict()
                result_dict[brand][media][program] = 1
            '''
    sum = 0
    for brand, media_dict in result_dict.items():
        for media, program_dict in media_dict.items():
            for program, count in program_dict.items():
                sum += count
                print(brand + '#' + media + '#' + program + '#' + str(count))

    print(sum)
