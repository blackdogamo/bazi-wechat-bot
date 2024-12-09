import plugins
from plugins import *
#省略原代码里其他库的引用


@plugins.register(
    name="bazi_plugin",
    desire_priority=100,
    hidden=True,
    desc="判断消息中是否有敏感词、决定是否回复。",
    version="1.0",
    author="lanvent",
)

#class bazi_plugin(Plugin):
#这里我不知道该怎么编写了，毕竟我不是程序员，我不会编程



#这是《bazi_plugin》开头部分的函数，用来与《__init__.py》联动，处理微信消息里发来的命盘的“公历输入”or“四柱八字输入”


def process_bazi_data(
sizhubazi_input,  # True表示四柱八字输入法，False表示公历/农历输入法
gongli_input,     # True表示公历输入，False表示农历输入
leap_month,       # True表示闰月，False表示非闰月（仅当农历输入时有用）
gender,           # 性别 "男" 或 "女"
year=None, month=None, day=None, hour=None, 
year_gan=None, year_zhi=None,
month_gan=None, month_zhi=None,
day_gan=None, day_zhi=None,
hour_gan=None, hour_zhi=None
):
global 本命盘四个天干名字列表, 本命盘四个地支名字列表
global 性别, global_ba
性别 = gender  # 在显示命主关键信息函数中需要用到性别，所以这里赋值给全局变量

if not sizhubazi_input:
    # sizhubazi_input=False表示使用公历(或农历)生日输入法（原来的 if options.b: 分支）
    if gongli_input:
        # 公历输入
        # 使用lunar_python库将公历转换为农历，然后获取八字
        solar = Solar.fromYmdHms(int(year), int(month), int(day), int(hour), 0, 0)
        lunar = solar.getLunar()
        ba = lunar.getEightChar()
        本命盘四个天干名字列表 = Gans(
            year=ba.getYearGan(),
            month=ba.getMonthGan(),
            day=ba.getDayGan(),
            time=ba.getTimeGan()
        )
        本命盘四个地支名字列表 = Zhis(
            year=ba.getYearZhi(),
            month=ba.getMonthZhi(),
            day=ba.getDayZhi(),
            time=ba.getTimeZhi()
        )
        global_ba = ba
    else:
        # 农历输入
        # 如果是闰月，需要将月数设为负数
        if leap_month:
            month_ = -int(month)
        else:
            month_ = int(month)
        lunar = Lunar.fromYmdHms(int(year), month_, int(day), int(hour), 0, 0)
        solar = lunar.getSolar()
        ba = lunar.getEightChar()
        本命盘四个天干名字列表 = Gans(
            year=ba.getYearGan(),
            month=ba.getMonthGan(),
            day=ba.getDayGan(),
            time=ba.getTimeGan()
        )
        本命盘四个地支名字列表 = Zhis(
            year=ba.getYearZhi(),
            month=ba.getMonthZhi(),
            day=ba.getDayZhi(),
            time=ba.getTimeZhi()
        )
        global_ba = ba

else:
    本命盘四个天干名字列表 = Gans(
        year=year_gan,
        month=month_gan,
        day=day_gan,
        time=hour_gan
    )
    本命盘四个地支名字列表 = Zhis(
        year=year_zhi,
        month=month_zhi,
        day=day_zhi,
        time=hour_zhi
    )
    global_ba = None
return


# 我就省略了中间的一大堆函数计算，我直接粘贴与《__init__.py》联动的函数的部分



# 创建命主关键信息按钮
def 显示命主关键信息():

    result_str = ""  # 用来存储所有原本print的内容
    result_str += "\n命主关键信息罗列如下：\n"

    # 存储作用结论的字典
    日干作用结论字典 = {}
    被日干作用结论字典 = {}
    日支作用结论字典 = {}
    被日支作用结论字典 = {}

    # 获取日干作用其他天干的结论
    for 位置 in ['年干', '月干', '时干']:
        结论 = 自动获取作用结论('日干', 位置)
        日干作用结论字典[位置] = 结论['作用结论']

    # 获取其他天干作用日干的结论
    for 位置 in ['年干', '月干', '时干']:
        结论 = 自动获取作用结论(位置, '日干')
        被日干作用结论字典[位置] = 结论['作用结论']

    # 获取日支作用其他地支的结论
    for 位置 in ['年支', '月支', '时支']:
        结论 = 自动获取作用结论('日支', 位置)
        日支作用结论字典[位置] = 结论['作用结论']

    # 获取其他地支作用日支的结论
    for 位置 in ['年支', '月支', '时支']:
        结论 = 自动获取作用结论(位置, '日支')
        被日支作用结论字典[位置] = 结论['作用结论']

    # 输出关键结论
    result_str += f"\n·{'男命' if 性别 == '男' else '女命'}，出生地[未知]\n"

    # 输出命局透出十神
    result_str += "\n·命局透出十神：\n"
    for 位置 in ['年干', '月干', '时干']:
        天干 = 八字信息主字典[位置]
        result_str += f"{位置}-{天干['名字']}-{天干['十神']}-{天干['忌用神归属']}  "
    for 位置 in ['年支', '月支', '时支']:
        地支 = 八字信息主字典[位置]
        result_str += f"{位置}-{地支['名字']}-{地支['忌用神归属']}  "

    # 输出所有未现十神
    result_str += "\n\n·所有未现十神：\n"
    for 天干, 信息 in 未现正偏十神主字典.items():
        result_str += f"{天干}-{信息['十神']}-{信息['忌用神归属']}  "

    # 输出命局透出十神的环境吉凶
    result_str += "\n\n·命局透出十神的环境的吉凶：\n"
    for 位置 in ['年干', '月干', '时干']:
        天干 = 八字信息主字典[位置]
        result_str += f"{天干}-{信息['十神']}-{信息['忌用神归属']}："
        result_str += f"外环境【{信息['外环境']}】、内环境【{信息['内环境']}】、社会环境【{信息['左环境']}】、内心环境【{信息['右环境']}】、内环境的左环境【{信息['内环境左环境']}】、内环境的右环境【{信息['内环境右环境']}】\n"


    # 输出未现十神的环境吉凶
    result_str += "\n·未现十神的环境的吉凶：\n"
    for 天干, 信息 in 未现正偏十神主字典.items():
        result_str += f"{天干}-{信息['十神']}-{信息['忌用神归属']}："
        result_str += f"外环境【{信息['外环境']}】、内环境【{信息['内环境']}】、社会环境【{信息['左环境']}】、内心环境【{信息['右环境']}】、内环境的左环境【{信息['内环境左环境']}】、内环境的右环境【{信息['内环境右环境']}】\n"

    # 输出日干作用结论
    result_str += "\n·【日干】作用所有命局透出十神后的吉凶：\n"
    for 位置, 结论 in 日干作用结论字典.items():
        result_str += f"【日干】让【{八字信息主字典[位置]['十神']}】【结论}\n"

    # 输出被日干作用结论
    result_str += "\n·每个透出十神让【日干】应吉凶：\n"
    for 位置, 结论 in 被日干作用结论字典.items():
        result_str += f"【{八字信息主字典[位置]['十神']}】让【日干】【{结论}】\n"

    # 输出日支作用结论
    result_str += "\n·【日支】让每个透出十神的根应吉凶：\n"
    for 位置, 结论 in 日支作用结论字典.items():
        相应天干位置 = 位置.replace('支', '干')
        result_str += f"【日支】让【{八字信息主字典[相应天干位置]['十神']}】的根【{结论}】\n"

    # 输出被日支作用结论
    result_str += "\n·每个透出十神的根让【日支】应吉凶：\n"
    for 位置, 结论 in 被日支作用结论字典.items():
        相应天干位置 = 位置.replace('支', '干')
        result_str += f"【{八字信息主字典[相应天干位置]['十神']}】的根让【日支】【{结论}】\n"

    # 输出所有未现十神的窗口十神
    result_str += "\n·所有未现十神的'窗口十神'：\n"
    for 天干, 信息 in 未现正偏十神主字典.items():
        result_str += f"{天干}的窗口十神是【{信息['窗口十神']}】(位于{信息['窗口位置']}的{信息['窗口名字']})\n"
    
    return result_str