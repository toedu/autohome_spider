# -*- coding: utf-8 -*-

import jieba
import pymssql
import sys
import json
sys.path.append('/Users/ysong/Work/py/autohome_spider/parse')
type = sys.getfilesystemencoding()

reload(sys)
sys.setdefaultencoding('utf-8')

# brandList = json.loads(open('data/brand.json').read())
# seriesList = json.loads(open('data/series.json').read())
# modelList = json.loads(open('data/model.json').read())

jieba.load_userdict("dic.txt")

COLORS = ['白', '黑', '红', '银', '黑', '灰', '金', '蓝', '棕', '青', '紫', '绿']

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
    print "连接数据库成功".decode('utf-8').encode(type)

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


def countNumber(list):
    i = 0
    for w in list:
        if is_number(w):
            i = i+1
    return i


def formatPrice(price):
    price2 = price.split("-")
    price = price2[len(price2)-1]
    print "2: %s" % price
    price = price[:-1]
    print "3: %s" % price
    price = price.replace(".", "")
    return price


def findBrandById(brand_id):
    sql = 'select * from sg_auto_brands where id = ' + brand_id
    a = cur.execute(sql)
    print a


def findBrandByName(name):
    cur.execute(
        "SELECT * FROM sg_auto_brands WHERE name like %s", name.decode('utf8'))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    return None


def findSeriesByName(brand, name):

    if brand == 0:
        cur.execute(
            "SELECT * FROM sg_auto_series WHERE name like %s", name.decode('utf8'))
    else:
        cur.execute(
            "SELECT * FROM sg_auto_series WHERE brand_id = %d and name like %s", (brand, '%'+name.decode('utf8')+'%'))
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
    print "字符串中分析品牌类型"
    words = jieba.lcut_for_search(str)
    for i in range(len(words)):
        word = words[len(words)-1-i]
        print "%s" % word
        brand = findBrandByName(word)
        if brand:
            return brand['id']
    return 0


def parseSeries(brand, str):
    series = findSeriesByName(brand, str)
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


def parseColor(list):
    print '-------- parseColor'
    result = []
    for w in list:
        if len(w) > 1:
            for i in range(len(w)):
                s = w[i]
                # print s.decode('utf-8').encode(type)
                if COLORS.count(s) > 0 and result.count(s) == 0:
                    result.append(s)
        else:
            if COLORS.count(w) > 0 and result.count(w) == 0:
                result.append(w)
            # print w.decode('utf-8').encode(type)

    # for w in result:
    #     print w.decode('utf-8').encode(type)
    return result


def parseLine(brand, series, model, str):
    print '--------------------------- 解析行数据'.decode('utf-8').encode(type)
    print str.decode('utf-8').encode(type)

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

    if len(words) > 4 and countNumber(words) > 1:
        # 整行格式
        if is_number(words[1]):
            # 如果第二个词是数字，则判断第一个词是车系
            series = parseSeries(brand, words[0])
            result['series'] = series
            if series:

                # print "找到车系 ----- %s series is: %s %s %s" % (
                #     words[0], series['id'], series['brand_id'], series['make_name'])

                # 根据价格查找车型配置
                model = parseModel(series['id'], words[1])

                if model:
                    result['model'] = model['id']

                    # print "找到车型 ----- %s model is: %s %s %s" % (
                    #     words[1], model['id'], model['name'], model['group'])
                    words.pop(0)
                    words.pop(0)

                    #   print "-----打印剩余数组:".decode('utf-8').encode(type)
                    #    for w in words:
                    #         print w

                    for i in range(len(words)):
                        # 找到优惠价格的字段，并截取颜色相关字段
                        if is_number(words[i]):
                            print i
                            discount = words[i]
                            print "discount: %s" % discount
                            color_words = words[:i]
                            result['colors'] = parseColor(color_words)
                            break
    else:
        # 分析行中是否包含品牌信息
        brand_id = parseBrand(str)
        print "brand: %d" % brand_id
        result['brand_id'] = brand_id

    return result


# brand = 13
# name = '408'
# cur.execute(
#     "SELECT * FROM sg_auto_series WHERE brand_id = %d and name like %s", (brand, '%'+name.decode('utf8')+'%'))
# rows = cur.fetchall()
# print rows
# exit()


t = """
润祥捷 雪佛兰大卖
==========
科沃兹799白灰色，34000 近期
科沃兹899白灰色，37500 近期
科沃兹969白灰色，37500 近期
科沃兹999灰优惠，37500 近期
==========
科鲁泽1089白灰红，46000
科鲁泽1119白灰黑，45500 
科鲁泽1179白灰红，45500
科鲁泽1299白灰色，46000
科鲁泽1179白灰黑，44000 四缸
科鲁泽1119白灰黑，44500 四缸
==========
迈锐宝1749白灰黑46000 新款
迈锐宝1749蓝优惠46000 新款
迈锐宝1849白黑色46000 新款
迈锐宝1649灰优惠57000 1月
迈锐宝1749灰黑色57000 4月
迈锐宝1949白黑灰56000 近期
迈锐宝1949白优惠58000 12月
迈锐宝2049白灰色59000 
迈锐宝2049白黑灰56000 近期
迈锐宝2199黑灰色55500 近期
==========
探界者1899白灰色58000 1月
探界者1899黑灰色56500 近期
探界者1999白黑灰58000
探界者2259白黑灰56500 近期
探界者2459黑优惠58000 12月
==========
沃兰多1399白灰色54500 12月
沃兰多1419白两灰49000 轻混
沃兰多1549白两灰51000 轻混
沃兰多1499海崖灰53000 12月
沃兰多1499白灰色54500 12月
创 酷1279白红色52000 8月
==========
开拓者2599黑银色，51000 5座
开拓者2899黑优惠，51000 5座
开拓者2799 白灰色，51000 7座
开拓者2899灰黑色，51000 7座
开拓者3099黑优惠，51000 7座
开拓者3299黑灰色，51000 7座
==========
店车票 有汽贸票 有裸出交强 
厦门润祥捷汽车有限公司
润祥捷——您的专属订车顾问！
 17779664566(微信) 林
诚信换群 换群备注



"""


brand = 0
series = ''
model = ''
modelList = []

# 数据预处理
t = t.replace('【', ' ')
t = t.replace('】', ' ')
l = t.split('\n')
for i in range(len(l)):
    obj = parseLine(brand, series, model, l[i])
    if obj.has_key('brand_id') and obj['brand_id'] > 0:
        brand = obj['brand_id']
