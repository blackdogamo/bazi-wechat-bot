import os
import sys
import re

# 添加项目根目录到系统路径
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 添加插件目录到系统路径
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

# 现在导入所需的模块
from common.log import logger
from bridge.context import Context, ContextType
from bridge.reply import Reply, ReplyType
from plugins import Plugin, plugins
from . import bazi_core

def handle_bazi_request(content, gender):
    """处理八字请求"""
    import argparse
    
    # 创建参数对象
    class Args:
        def __init__(self):
            self.n = (gender == "女")  # 性别
            self.g = True  # 默认使用公历
            self.r = False  # 非闰月
            self.b = False  # 非直接八字输入
            self.start = 1850
            self.end = '2030'
    
    # 捕获print输出
    import io
    import sys
    old_stdout = sys.stdout
    result = io.StringIO()
    sys.stdout = result
    
    try:
        # 解析输入内容
        parts = content.strip().split()
        if len(parts) == 5:  # 公历输入: 男 1990 12 06 22
            args = Args()
            args.year = parts[1]
            args.month = parts[2]
            args.day = parts[3]
            args.time = parts[4]
        elif len(parts) == 9:  # 八字输入: 女 甲 子 丙 寅 丁 丑 戌 亥
            args = Args()
            args.b = True
            args.year = parts[1] + parts[2]    # 年干支
            args.month = parts[3] + parts[4]   # 月干支
            args.day = parts[5] + parts[6]     # 日干支
            args.time = parts[7] + parts[8]    # 时干支
        else:
            return "输入格式错误"
            
        # 调用原有函数处理
        global options
        options = args
        命盘分析界面(None, 本命盘四个天干名字列表, 本命盘四个地支名字列表, 四个天干十神列表, 四个地支十神列表, gender).显示命主关键信息()
        
    except Exception as e:
        return f"处理失败: {str(e)}"
    finally:
        # 恢复标准输出
        sys.stdout = old_stdout
        
    return result.getvalue()

@plugins.register(name="BaZiPlugin", desc="八字分析插件", version="1.0", author="YourName")
class BaZiPlugin(Plugin):
    def __init__(self):
        logger.info("[BaZiPlugin] 插件初始化完成")

    def on_handle_context(self, context: Context):
        # 只处理群聊消息
        if context.type != ContextType.GROUP_MSG:
            return

        # 获取收到的消息内容
        content = context.content.strip()
        # 获取机器人在群聊中的名字
        bot_name = context["msg"].to_user_nickname

        # 检测消息是否以 @机器人 开头
        if not content.startswith(f"@{bot_name}"):
            return

        # 去掉 @机器人 的前缀
        content = content[len(f"@{bot_name}"):].strip()

        # 匹配输入格式
        # 公历生日输入法
        match = re.match(r"(男|女)\s+(\d{4})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})", content)
        if match:
            gender = match.group(1)
            year = int(match.group(2))
            month = int(match.group(3))
            day = int(match.group(4))
            hour = int(match.group(5))

            # 调用八字分析函数
            result = bazi_core.calculate_bazi(
                year=year,
                month=month,
                day=day,
                hour=hour,
                gender=gender
            )

            # 发送结果
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = result
            return reply

        # 四柱八字输入法
        match = re.match(r"(男|女)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)", content)
        if match:
            gender = match.group(1)
            bazi = match.groups()[1:]  # 获取后面的八个汉字

            # year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, hour_gan, hour_zhi
            bazi_list = list(bazi)

            # 调用八字分析函数
            result = bazi_core.calculate_bazi(
                year=bazi_list[0],
                month=bazi_list[1],
                day=bazi_list[2],
                hour=bazi_list[3],
                gender=gender
            )

            # 发送结果
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = result
            return reply

        # 如果不符合格式，则不处理
        return 