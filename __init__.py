import os
import sys
from bridge.context import Context
from bridge.reply import Reply, ReplyType
from bridge import bridge
from plugins import *
from bridge import context
from channel.wechat.wechat_channel import WechatChannel
import time
from bridge.context import ContextType


# 全局变量（测试用）
LAST_INPUT = None
LAST_USER_ID = None

# bazi_plugin.py的路径 (请根据你的实际路径)
plugin_path = os.path.dirname(__file__)
bazi_plugin_path = os.path.join(plugin_path, "bazi_plugin.py")
print("bazi_plugin_path:", bazi_plugin_path)

def judge_input_type_and_extract_info(input_text):
    """
    根据用户的输入文本来判断输入类型（公历输入法 or 四柱八字输入法），
    并提取出相关的参数（性别、年、月、日、时或干支信息）。
    
    输入格式示例：
    公历生日输入法: "@机器人 男 1990 12 06 22"
    四柱八字输入法: "@机器人 女 甲 子 丙 寅 丁 丑 戌 亥"

    返回: 一个字典infos，可能包含:
    - gender: "男" 或 "女"
    - year, month, day, hour (如果是公历输入法)
    - year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, hour_gan, hour_zhi (如果是四柱八字输入法)
    - gongli_input: True/False (是否为公历输入法)
    - sizhubazi_input: True/False (是否为四柱八字输入法)
    - leap_month: True/False (是否为闰月，这里默认False)
    """

    # 清理输入文本，去除多余空格、中文空格
    cleaned_text = input_text.strip().replace("　", " ").replace("  ", " ")
    parts = cleaned_text.split(" ")

    # 判断输入的parts个数：
    # 公历输入法示例：["@机器人", "男", "1990", "12", "06", "22"]  共6段
    # 四柱八字输入法示例：["@机器人", "女", "甲", "子", "丙", "寅", "丁", "丑", "戌", "亥"] 共10段

    if len(parts) == 6:    # ⭐️ 公历输入法
        
        # parts: ["@机器人", "男", "1990", "12", "06", "22"]
        gender = parts[1]
        year = parts[2]
        month = parts[3]
        day = parts[4]
        hour = parts[5]

        # 尝试将年月日时转为整数
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
        except:
            # 如果无法转换为整数，说明用户输入有误
            return None

        # 公历输入法下参数设定
        gongli_input = True          # 是公历输入
        sizhubazi_input = False      # 不是四柱八字输入
        leap_month = False           # 默认没有闰月的概念

        return {
            "gender": gender,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "gongli_input": gongli_input,
            "sizhubazi_input": sizhubazi_input,
            "leap_month": leap_month
        }

    elif len(parts) == 10:      # ⭐️ 四柱八字输入法
        
        # parts: ["@机器人", "女", "甲", "子", "丙", "寅", "丁", "丑", "戌", "亥"]
        gender = parts[1]
        year_gan = parts[2]
        year_zhi = parts[3]
        month_gan = parts[4]
        month_zhi = parts[5]
        day_gan = parts[6]
        day_zhi = parts[7]
        hour_gan = parts[8]
        hour_zhi = parts[9]

        # 四柱八字输入法下参数设定
        gongli_input = False         # 不是公历输入
        sizhubazi_input = True       # 是四柱八字输入
        leap_month = False           # 默认无闰月，后续可根据需要调整

        return {
            "gender": gender,
            "year_gan": year_gan,
            "year_zhi": year_zhi,
            "month_gan": month_gan,
            "month_zhi": month_zhi,
            "day_gan": day_gan,
            "day_zhi": day_zhi,
            "hour_gan": hour_gan,
            "hour_zhi": hour_zhi,
            "gongli_input": gongli_input,
            "sizhubazi_input": sizhubazi_input,
            "leap_month": leap_month
        }

    else:
        # 未知格式，不处理
        return None


def make_reply(infos):
    from plugins.bazi_plugin.bazi_plugin import process_bazi_data, 显示命主关键信息
    # 调用process_bazi_data执行分析(此函数是你自己写的入口函数)
    process_bazi_data(
        sizhubazi_input=infos["sizhubazi_input"],
        gongli_input=infos["gongli_input"],
        leap_month=infos["leap_month"],
        gender=infos["gender"],
        year=infos.get("year"),
        month=infos.get("month"),
        day=infos.get("day"),
        hour=infos.get("hour"),
        year_gan=infos.get("year_gan"),
        year_zhi=infos.get("year_zhi"),
        month_gan=infos.get("month_gan"),
        month_zhi=infos.get("month_zhi"),
        day_gan=infos.get("day_gan"),
        day_zhi=infos.get("day_zhi"),
        hour_gan=infos.get("hour_gan"),
        hour_zhi=infos.get("hour_zhi")
    )

    # 然后调用显示命主关键信息获取最终结果字符串
    result = 显示命主关键信息()
    return result



class BaziPlugin(Plugin):
    def __init__(self):
        super().__init__()
        print("[BaziPlugin] inited")

    def on_message(self, context: Context):
        """
        当接收到一条微信群内的消息且@到本机器人时，会执行此函数。
        我们从消息中提取出用户输入的内容，判断输入类型，分析八字，然后返回结果给微信群。
        """
        if context.type == ContextType.GROUP and context.is_at:
            text = context.content.strip()
            # 文本格式一般是"@机器人 ...",我们取出@机器人后面的内容  🚨🚨🚨🚨🚨
            parts = text.split(" ", 1)
            if len(parts) < 2:
                return
            user_input = parts[1].strip()  # 获取实际的指令部分（去掉@机器人）

            infos = judge_input_type_and_extract_info(user_input)
            if infos is None:
                # 如果无法解析输入，就不回应
                return

            # 调用make_reply生成回复文本
            reply_text = make_reply(infos)

            # 使用框架提供的Reply对象返回消息
            reply = Reply(ReplyType.TEXT, reply_text)
            return reply

# 注册插件
plugin = BaziPlugin()
