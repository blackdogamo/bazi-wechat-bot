# plugins/bazi_plugin/__init__.py

import re
from bridge.reply import Reply, ReplyType
from bridge.context import Context, ContextType

# 从 bazi_plugin.py 中导入你的两个关键函数
# 假设 bazi_plugin.py 中有 process_bazi_data(riqi, typetype) 和 显示命主关键信息(data) 函数。
from .bazi_plugin import process_bazi_data, 显示命主关键信息

__plugin_name__ = "BaziPlugin"
__plugin_usage__ = """
插件名称：BaziPlugin
用法：
在群聊中 @机器人 后输入：
1. 公历生日输入法：
   "@机器人 男 1990 12 06 22"
   （格式：性别 年 月 日 时）
2. 四柱八字输入法：
   "@机器人 女 甲 子 丙 寅 丁 丑 戌 亥"
   （格式：性别 年干 年支 月干 月支 日干 日支 时干 时支）
插件将根据以上输入调用八字计算逻辑并回复分析结果。
"""

def on_handle_message(context: Context):
    """
    当收到消息时，插件会调用此函数。
    如果消息符合八字格式则直接用 process_bazi_data() 和 显示命主关键信息() 返回结果。
    如果不符合，则返回None让消息进入后续环节（例如ChatGPT回答）。
    """

    # 只处理文本消息
    if context.type != ContextType.TEXT:
        return None

    msg = context.content.strip()
    # 根据你的实际机器人昵称进行调整，这里假设你的机器人昵称是"@机器人"
    # 如果群聊中发信息会自动附上"@机器人", 我们需要把开头的这段给去掉
    msg = re.sub(r'^@机器人\s+', '', msg)

    typetype = None
    riqi = None

    # 公历输入法匹配规则：性别(男|女) 年(4位) 月(1-2位) 日(1-2位) 时(1-2位)
    gl_pattern = r'^(男|女)\s+(\d{4})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})$'

    # 四柱八字输入法匹配（大致匹配，不同干支可根据具体情况微调）
    # 假设干支都是中文汉字（天干地支为一字，如“甲”、“子”、“丙”、“寅”...）
    # 格式：性别 后接8个汉字（每两个字组合为一个干支）
    # 例如：女 甲 子 丙 寅 丁 丑 戌 亥
    # 为简单起见，用中文字符范围匹配：
    sz_pattern = r'^(男|女)\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+\s+([\u4e00-\u9fa5])+$'

    gl_match = re.match(gl_pattern, msg)
    sz_match = re.match(sz_pattern, msg)

    if gl_match:
        # 公历输入法
        typetype = 1
        gender = gl_match.group(1)
        year = gl_match.group(2)
        month = gl_match.group(3)
        day = gl_match.group(4)
        hour = gl_match.group(5)
        riqi = {
            "gender": gender,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour
        }

    elif sz_match:
        # 四柱八字输入法
        typetype = 2
        parts = msg.split()
        gender = parts[0]
        # 余下8个字符即为干支信息
        ganzhi = parts[1:]
        riqi = {
            "gender": gender,
            "ganzhi": ganzhi
        }

    # 如果既不匹配公历也不匹配四柱八字，则不处理
    if typetype is None:
        return None

    # 调用你的八字处理逻辑
    # process_bazi_data会处理riqi和typetype，并返回一个数据结构供显示命主关键信息函数使用
    processed_data = process_bazi_data(riqi, typetype)

    # 调用 显示命主关键信息 函数得到最终输出文本（假设这个函数返回字符串）
    final_result = 显示命主关键信息(processed_data)

    # 返回Reply，让程序直接发送该文本给用户
    return Reply(ReplyType.TEXT, final_result)
