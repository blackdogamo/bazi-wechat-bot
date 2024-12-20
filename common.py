import argparse
import collections
import pprint
import datetime

from bidict import bidict

from datas import *
from ganzhi import *
from ganzhi import 十神关系表
from sizi import summarys



'''
《天干间的"合冲"判断》 🤝💥
'''
# 【天干】之间的"合"和"冲"关系判断. (科普：天干合冲典型的有甲己合、乙庚合、甲庚冲等)
# 下面的"十神关系表"是包含了每个天干的"合"和"冲"信息的字典，判断"合"和"冲"就变成了简单的字典查找。
def 天干间合冲关系判断(天干, 天干们):
    result = ''
    if 十神关系表[天干]['合'] in 天干们:           #检查"合"的情况：如果当前天干的"合"干 存在于天干们中，就将"合"和相合的天干添加到结果中。
        result += "合" + 十神关系表[天干]['合']
    if 十神关系表[天干]['冲'] in 天干们:          #检查"冲"的情况：如果当前天干的"冲"干 存在于天干们中，就将"冲"和相冲的天干添加到结果中。
        result += "冲" + 十神关系表[天干]['冲']
    return result



'''
🌞🌙 《阴阳》 👶🏻👧🏻
'''

# 下面“计算阴阳属性”这个函数是用来判断天干或地支【阴阳】属性的。
# 工作原理：1.首先，函数检查输入的 item 是否在 天干列表 中。
# 2.如果 item 在 天干列表中，则根据 天干列表 的索引值来判断阴阳属性。（ 如果天干在列表中的索引是偶数（0, 2, 4, 6, 8），返回 '＋'（阳）；  如果是奇数（1, 3, 5, 7, 9），返回 '－'（阴） ）
# 【命理科普】八字学说中的阴阳划分：甲丙戊庚壬为阳干，乙丁己辛癸为阴干；子寅辰午申戌为阳支，丑卯巳未酉亥为阴支。
# 3.如果 item 不在 天干列表 中，则检查 item 是否在 地支列表。
# 4.根据 地支列表 的索引值来判断阴阳属性。
# 5.返回阴阳属性。
天干列表 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支列表 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
def 计算阴阳属性(item):
    if item in 天干列表:
        return '阳' if 天干列表.index(item)%2 == 0 else '阴'
    else:
        return '阳' if 地支列表.index(item)%2 == 0 else '阴'
    
def yinyangs(地支们):
    result = []
    for item in 地支们:
        result.append(计算阴阳属性(item))
    if set(result) == set('阳'):
        print("四柱全阳")
    if set(result) == set('阴'):
        print("四柱全阴")
    
    

'''
 《空亡》 💀
'''

# "柱"="柱"；  "地支"="支"
# "empties" 是一个预先定义的“地支空亡字典”，穷举了所有天干地支组合的地支空亡情况。（例如： "甲子": ["戌", "亥"]）。"if 地支 in empty": 这行代码检查给定的地支"地支"是否在空亡列表中。
def get_empty(柱, 地支):
    empty = empties[柱]
    if 地支 in empty:
        return "空"         
    return ""               #如果地支在空亡列表中，函数返回"空"，否则返回空字符串。



'''
 《地支藏干》：地支5 
'''

# 获取【地支】如下的详细信息 ↓  （“地支”：要分析的地支。 函数遍历 地支5[地支] 中的每个天干。 "地支5"是一个字典，键是地支，值是与该地支相关的[天干]及其[力量]的字典。→代表了【地支藏干】的概念）
# 1.地支藏干：每个地支都藏有的一到三个天干。 2.这些藏干的五行属性。 3.这些藏干在地支中的力量大小。 4.这些藏干与日主（me）的十神关系。 
# Step1:函数遍历 地支5[地支] 中的每个天干。地支5 是一个字典，包含了每个地支藏的天干及其力量。
# Step2:对于每个藏干，函数构建一个字符串，包含以下信息：1.藏干本身;2.藏干的五行属性（通过 天干5[天干] 获取）;3.藏干在地支中的力量（通过 地支5[地支][天干]*multi 计算）;4.藏干与日主的十神关系（通过 十神关系表[me][天干] 获取）
# Step3:信息被拼接成字符串返回。

# “天干5” 是一个字典，键是天干，值是对应的五行属性。
# “地支5” 是一个嵌套字典，表示了每个地支中【藏干的情况及其力量】。例如，"丑土"藏"己土"、"癸水"、"辛金"，藏干的力量：己土最旺（5分），癸水次之（3分），辛金最弱（2分）。
def get_地支_detail(地支, me, multi=1):
    out = ''
    for 天干 in 地支5[地支]:
        out = out + "{}{}{}{} ".format(天干, 天干5[天干], 地支5[地支][天干]*multi,  
                                       十神关系表[me][天干])
    return out



'''
 《地支拱合》 🤝
'''

# “拱”指的两个地支之间通过一个“空缺”的地支来“隔空”相连“搭桥”暗中相会，使这两地支力量连接作用。并形成一种类似合局的作用力。这种力量不像直接的地支合会明显，相对隐秘。
# （1）地支三合拱局(三合局（亥卯未、申子辰、巳酉丑、寅午戌）是八字命理中最典型的拱局类型.比如：寅、午两支拱戌：寅午相隔一个戌土，通过戌土相会，依然能够产生拱火局的效果)
# （2）地支六合拱局(六合局（子丑合土、寅亥合木、卯戌合火、辰酉合金、巳申合水、午未合火）在拱局中的表现较为隐晦。如果命局中两个地支形成六合关系，但缺少第三个地支，则这两个地支也能“隔空”相会。比如：亥、寅相隔“拱木局”)
# （3）地支三会拱局（三会局（寅卯辰、巳午未、申酉戌、亥子丑）也是拱局中常见的一种。比如：申酉拱戌：申金生酉金，通过戌土的存在（即使没出现在命局中），也能形成暗中的金局力量）
# “拱”的【影响】——（1）补充地支力量；（2）强化格局和成败；（3）流年和大运的引动作用。

#代码实现《地支拱合》判断的步骤：
# Step1：函数接收五个参数：1.地支们：一个包含四个地支的字符串列表。2.n1：第一个地支的索引。3.n2：第二个地支的索引。4.me：日主的天干。5.hes：一个包含所有可能的拱合关系的字典。6.desc：描述拱合的字符串，默认为“三合拱”。
# Step2：函数首先检查 地支们[n1] + 地支们[n2] 是否在 hes 字典中。检查这两个地支是否形成某种特定的组合（如三合）。
# Step3：如果存在拱合关系，函数会从 hes 字典中获取相应的拱合地支 gong，并检查该地支是否在 地支们 列表中。如果不在，则表示拱合关系成立。
# Step4：如果找到了匹配的组合，函数会获取 hes 字典中对应的值，存储在 gong 变量中。这个 gong 可能代表被拱的地支。
# Step5：函数检查 gong 是否不在 地支们 中，确认被拱的地支不在原有的八字地支中。
# Step6：如果找到了匹配的组合，函数会将信息添加到 result 中。 1.描述（默认为 "三合拱"）; 2.形成组合的两个地支（地支们[n1] 和 地支们[n2]）;3.被拱的地支（gong）; 4.被拱地支的详细信息（通过调用 get_地支_detail(gong, me) 获得）
def check_gong(地支们, n1, n2, me, hes, desc='三合拱'):
    result = ''
    if 地支们[n1] + 地支们[n2] in hes:
        gong = hes[地支们[n1] + 地支们[n2]] 
        if gong not in 地支们:
            result += "\t{}：{}{}-{}[{}]".format(
                desc, 地支们[n1], 地支们[n2], gong, get_地支_detail(gong, me))
    return result