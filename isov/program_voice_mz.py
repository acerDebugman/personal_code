# -*- coding:utf-8 -*-
import argparse
import collections

parse = argparse.ArgumentParser()
parse.add_argument("program_file", help="program file path")
parse.add_argument("mz_all_file", help="mz all file")
parse.add_argument("out_file", help="output file")
args = parse.parse_args()
program_file = args.program_file
mz_all = args.mz_all_file
out_file = args.out_file

brand_dict = collections.defaultdict()
result_dict = collections.defaultdict(int)


#brandfile schema: caid#brand#media
#program file schema: caid#content
with open(program_file) as program_fp, open(mz_all) as mz_all_fd, \
        open(out_file, "w") as out_fd:
    for line in mz_all_fd:
        #caid, brand, media = line.strip().split('#')
        company, caid, spid, industry, brand, goods, media_type, media, province, \
        city, datestr, gender, age, edu, income, device_model = line.strip().split("#")

        #brand_media = industry + "#" + brand + '#' + goods + '#' + media
        brand_media = ",".join((industry, brand, goods, media))
        brand_dict[caid] = brand_media
    total_lines = 0
    count = 0
    for line in program_fp:
        #caid, content = line.strip().split('#', 1)

        time, router_mac, media_1, caid, spid, title, content, top, sub, *others = line.strip().split(",")
        if others:
            #print(others)
            continue

        total_lines  += 1
        if caid in brand_dict.keys():
            industry_brand_goods_media = brand_dict[caid]
            #brand, media = brand_media.split('#')
            #industry, brand, goods, media = industry_brand_goods_media.split('#')
            dim = industry_brand_goods_media + "," + content
            result_dict[dim] += 1

            '''
            if brand in result_dict.keys():
                if media in result_dict[brand].keys():
                    if content in result_dict[brand][media].keys():
                        count = result_dict[brand][media][content]
                        result_dict[brand][media][content] = count + 1
                    else:
                        result_dict[brand][media][content] = 1

                else:
                    result_dict[brand][media] = dict()
                    result_dict[brand][media][content] = 1
            else:
                result_dict[brand] = dict()
                result_dict[brand][media] = dict()
                result_dict[brand][media][content] = 1
            '''

    print(total_lines)
    sum = 0
    for all_dim, cnt in result_dict.items():
        sum += cnt
        out_fd.write(all_dim + "," + str(cnt) + "\n")


    '''
    sum = 0
    for brand, media_dict in result_dict.items():
        for media, program_dict in media_dict.items():
            for program, count in program_dict.items():
                sum += count
                #print(brand + '#' + media + '#' + program + '#' + str(count))
                out_fd.write(brand + '#' + media + '#' + program + '#' + str(count) + "\n")
    '''

    print(sum)
