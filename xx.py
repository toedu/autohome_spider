# -*- coding: utf-8 -*-

import jieba
import pymssql
import sys
import json
sys.path.append('/Users/ysong/Work/py/autohome_spider/parse')

reload(sys)
sys.setdefaultencoding('utf-8')

brandList = json.loads(open('data/brand.json').read())
seriesList = json.loads(open('data/series.json').read())
modelList = json.loads(open('data/model.json').read())

host = "59.173.13.207"
user = "yunyouche"
pwd = "HsYAfRY9zm"
db = "sqlyunyouche"

conn = pymssql.connect(host=host,
                       user=user,
                       password=pwd,
                       database=db,
                       charset='utf8')
cur = conn.cursor(as_dict=True)  # 将数据库连接信息，赋值给cur。
if not cur:
    raise(NameError, "连接数据库失败")
else:
    print("连接数据库成功")

# cur.executemany(
#     "INSERT INTO sg_auto_brands VALUES (%d, %s, %s)",
#     [(2, 'John Smith', 'A')])

# cur.execute("TRUNCATE TABLE sg_auto_brands")

# for i in range(30):

#     cur.execute("INSERT INTO sg_auto_brands VALUES (%d, %s, %s)",
#                 (30+i, 'ffg', 'A'))
# conn.commit()


def is_Chinese(word):
    # for ch in word.decode('utf-8'):
    for ch in word:
        print "ch: %s" % ch
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def formatPrice(price):
    price2 = price.split("-")
    price = price2[len(price2)-1]
    print "2: %s" % price
    price = price[:-1]
    print "3: %s" % price
    price = price.replace(".", "")
    return price


def findBrandById(brand_id):
    sql = 'select * from sg_auto_brand where id = ' + brand_id
    a = cur.execute(sql)
    print a


def findBrandByName(name):
    brand_id = ''
    # 在品牌列表中找
    for brand in brandList:
        n = brand['name']
        if n == name:
            brand_id = brand['id']
            break
    for series in seriesList:
        if series['make_name'] == name:
            brand_id = series['brand_id']
            break
    return brand_id


def findSeriesByName(name):
    cur.execute(
        "SELECT * FROM sg_auto_series WHERE name = %s", name.decode('utf8'))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    return None


def findModelByName(name):
    for model in modelList:
        if model['name'] == name:
            return model


def findModelByPrice(series_id, price):
    cur.execute(
        "SELECT * FROM sg_auto_model WHERE series_id = %s AND price = %d", (series_id, int(price)))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    return None


def parseBrand(str):
    # 字符串中分析品牌类型
    words = jieba.lcut_for_search(str)
    for i in range(len(words)):
        word = words[len(words)-1-i]
        print "%s" % word
        brand_id = findBrandByName(word)
        print "brand_id: %s" % brand_id
        if len(brand_id) > 0:
            return brand_id
    return ''


def parseSeries(str):
    series = findSeriesByName(str)
    if series:
        # print "'%s' found series %s %s %s %s" % (
        #     str, series['name'], series['price'], series['id'], series['brand_id'])
        return series
    return None


def parseModel(series_id, str):
    model = findModelByPrice(series_id, str)
    if model:
        return model
    return None


def parseColor(str):

    return ''


def parseLine(brand, series, model, str):
    print '--------------------------- 解析行数据'
    print str

    result = {}
    if len(str) < 2:
        return {}

    # 删除字符串首尾空格
    str = str.strip()
    # str = str.replace(' ', '')

    words = jieba.lcut(str)
    # print words
    # 删除数组中的空格元素
    for i in words[:]:
        if i == " ":
            words.remove(i)

    for w in words:
        print w

    if len(words) > 4:
        # 整行格式
        if is_number(words[1]):
            # 如果第二个词是数字，则判断第一个词是车系
            series = parseSeries(words[0])
            if series:
                print "找到车系 ----- %s series is: %s %s %s" % (
                    words[0], series['id'], series['brand_id'], series['make_name'])

                # 根据价格查找车型配置
                model = parseModel(series['id'], words[1])
                if model:
                    print "找到车型 ----- %s model is: %s %s %s" % (
                        words[1], model['id'], model['name'], model['group'])

    # if brand == "":
    #     # 如果还没找到品牌，则搜索品牌
    #     brand_id = parseBrand(str)
    #     if brand_id != '':
    #         result['brand_id'] = brand_id

    return result


# words = jieba.cut_for_search('一汽大众')
# print words

# seg_list = jieba.cut_for_search("一汽大众")  # 搜索引擎模式
# print(", ".join(seg_list))

# str = "麟城一汽大众"
# words = jieba.lcut_for_search(str)
# for w in words:
# print w
# for i in range(len(words)):
#     print i
#     word = words[len(words)-1-i]
#     print "%s" % word
#     brand_id = findBrandByName(word)
#     print "brand_id: %s" % brand_id
# if len(brand_id) > 0:
# break

# str = "408 1477白⬇️35000[玫瑰]
# words = jieba.lcut(str)
# for w in words:
#     print w
#     print is_number(w)

# print findSeriesByName('宝来')
# s = findBrandByName('一汽大众')
# print s

# name = "宝来"
# cur.execute(
#     "SELECT * FROM sg_auto_series WHERE name = %s", name.decode('utf8'))
# rows = cur.fetchall()
# print "ssss %d " % len(rows)
# print rows

# exit()


t = """
宝来1350白 金 银全款36500店保 分期38500
宝来1390白 金 银全款36500店保 分期38500
速腾1389白 银 黑全款36500店保 分期39500
速腾1759白 银 黑全款36500店保 分期39500

探歌1558白 金   全款裸车32000店保38000
探歌1608白 金   全款裸车32000店保38000

探歌1708白 金   全款裸车30000店保36000
迈腾1869黑      全款裸车32000分期38000店保

迈腾2199黑      全款裸车32000分期38000店保
迈腾2339黑      全款裸车32000分期38000店保

探岳2209白 黑   全款裸车33500分期35500裸车

探岳2049白 黑   全款裸车33500分期35500裸车

"""


brand = ''
series = ''
model = ''
modelList = []

# 数据预处理
t = t.replace('【', ' ')
t = t.replace('】', ' ')
l = t.split('\n')
for i in range(len(l)):
    obj = parseLine(brand, series, model, l[i])
    # if obj.hasKey('brand_id'):
    #     brand = obj['brand_id']

    # list = findModelByPrice('2038')
    # for m in list:
    #     print 'name: %s, group: %s, price: %s' % (
    #         m['name'], m['group'], m['price'])
