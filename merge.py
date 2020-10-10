#!/usr/bin/python
# coding=utf-8

import json
import csv
import codecs
import types
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')

brandList = json.loads(open('data/brand.json').read())
seriesList = json.loads(open('data/series.json').read())
modelList = json.loads(open('data/model.json').read())
# specList = json.loads(open('spec_2017-07-19T10-09-46.json').read())

# print brandList

# brandDict = {brand['id']: brand for brand in brandList}

obj = {}
for i in range(26):
    x = chr(ord("A") + i)
    obj[x] = []
    print '------------------------' + x
    for brand in brandList:
        series_obj = []
        if brand['tag'] == x:
            tempBrand = brand.copy()
            del tempBrand['imgUrl']
            del tempBrand['tag']

            obj[x].append(tempBrand)
            # print brand['name']
# 保存brand分类文件
emb_filename = ('./output/brand.json')
jsObj = json.dumps(obj, indent=4, sort_keys=True)
with open(emb_filename, "w") as f:
    f.write(jsObj)
    f.close()


###################################################################
# 合并车系数据
series_ids = []
for brand in brandList:
    series_obj = {}
    print '--------------------------' + brand['name']

    # 循环该品牌有多少个厂商
    makes = []

    for serie in seriesList:

        # if makes.count(serie['make_name']) == 0:
        #     makes.append(serie['make_name'])
        # print serie['make_name']
        series_ids.append(serie['id'])
        if serie['brand_id'] == brand['id']:
            makeName = serie['make_name']
            if series_obj.has_key(makeName):
                tempSerie = serie.copy()
                del tempSerie['url']
                series_obj[makeName].append(tempSerie)
            else:
                tempSerie = serie.copy()
                del tempSerie['url']
                series_obj[makeName] = [tempSerie]

    # 每个文件保存一个品牌下的所有车系
    series_filename = ('./output/brand/b_' + brand['id'] + '.json')
    seriesObj = json.dumps(series_obj, indent=4, sort_keys=True)
    with open(series_filename, "w") as f:
        f.write(seriesObj)
        f.close()

###################################################################
# 合并车型数据，将每个车系下的车型存成一个json文件
for series_id in series_ids:
    model_obj = {}
    for model in modelList:
        if model['series_id'] == series_id:
            group_name = model['group']
            tempModel = model.copy()
            if model_obj.has_key(group_name):
                model_obj[group_name].append(tempModel)
            else:
                model_obj[group_name] = [tempModel]
    # 分别保存品牌的车系
    model_filename = ('./output/series/' + series_id + '.json')
    modelObj = json.dumps(model_obj, indent=4, sort_keys=True)
    with open(model_filename, "w") as f:
        f.write(modelObj)
        f.close()


# print brandDict
# seriesDict = {series['id'].strip('s'): series for series in seriesList}
# modelDict = {model['id']: model for model in modelList}
# specDict = {spec['id']: spec for spec in specList}


# specKeys = []
# for spec in specList:
#     detail = spec['spec']
#     for key in detail.keys():
#         if key not in specKeys:
#             specKeys.append(key)


# f = codecs.open('merge.csv', 'w+', 'utf-8')
# writer = csv.writer(f)

# titles = ['品牌ID', '品牌名称', '车系ID', '车系名称', '车型ID', '车型名称']

# for key in specKeys:
#     titles.append(key)

# writer.writerow(titles)

# for model in modelList:
#     modelId = model['id']
#     modelName = model['name']
#     seriesId = model['series_id']
#     # print seriesId
#     series = seriesDict[seriesId]
#     seriesName = series['name']
#     brandId = series['brand_id']
#     brand = brandDict[brandId]
#     brandName = brand['name']

#     row = [brandId, brandName, seriesId, seriesName, modelId, modelName]

#     spec = specDict[unicode(modelId)]
#     if spec:
#         detail = spec['spec']
#         for key in specKeys:
#             value = ""
#             if key in detail:
#                 value = detail[key]
#             row.append(value)

#     writer.writerow(row)

print 'finish..'
