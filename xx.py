# -*- coding: utf-8 -*-


import jieba

t = """
麟城【一汽大众】
宝来传奇
【988 白↓36000】
【1088 白↓36000】
【1068 白↓35000】
【1168 白↓35000】
宝来
【1110白黑银金↓37000】
【1220白黑金银↓37000】
【1230白黑金银↓37000】
【1350白黑金银↓37000】
【1390白黑金银↓37000】
【1490白黑金银↓37000】
速腾
【1389白黑↓37000】
【1499白黑金银↓37000】
【1619白黑金银↓37000】
【1759白黑↓36500】
【R-line1699白下34000】
迈腾
【1949黑↓35000】
【2099黑↓35000】
【2199黑金↓35000】
【2339黑↓35000】
【2499灰↓39000】
【2589黑↓34000】
探歌
【1558白金↓41000】
【1608白↓41000】
【1708白金↓38500】
【R-linePro1768白↓37500】
【1858白】
"""


t = t.replace('【', ' ')
t = t.replace('】', ' ')

# print "%s" % t

l = t.split('\n')
for i in range(len(l)):
    print '------------------ %s' % l[i]
    words = jieba.lcut(l[i])
    # print words
    for word in words:
        print "%s" % word


# print '%d' % len(l)

# print '%s' % l[0]
