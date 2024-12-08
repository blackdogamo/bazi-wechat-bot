import argparse
import collections
import pprint
import datetime

from lunar_python import Lunar, Solar
from colorama import init
from ganzhi import *
from datas import *
from sizi import summarys
from common import *
from yue import months
import sys
import tkinter as tk
from tkinter import ttk

global_ba = None
八字信息主字典 = {}
  
# 导入Tkinter库，它是 GUI (图形用户界面) 库，它让你可以轻松创建窗口、按钮、文本框等界面元素。
from tkinter import messagebox
#导入argparse库，它能帮你轻松处理命令行输入的参数，进行参数的类型检查和转。
import argparse
from argparse import Namespace

# 这是一个【GUI界面并获取用户输入】的"获取用户在界面里输入的信息"函数
def 获取用户在界面里输入的信息():
    # 创建主窗口
    输入窗口 = tk.Tk()
    输入窗口.title("八字排盘输入")
    输入窗口.geometry("400x500")  # 稍微增加了窗口高度
    输入窗口.configure(bg='#F5F5F5')  # 设置背景色为浅灰色
    
    # 设置字体
    标题字体设置 = ("Arial", 18, "bold")
    标签字体设置 = ("Arial", 14)
    条目字体设置 = ("Arial", 14)
    按钮字体设置 = ("Arial", 14, "bold")
    
    # 创建标题
    标题_标签 = tk.Label(输入窗口, text="请输入您的出生信息", font=标题字体设置, bg='#F5F5F5')
    标题_标签.pack(pady=20)
    
    # 创建输入框框架
    input_frame = tk.Frame(输入窗口, bg='#F5F5F5')
    input_frame.pack(pady=10)
    
    # 年、月、日、时的标签和输入框
    labels = ["年：", "月：", "日：", "时："]
    text_vars = [tk.StringVar() for _ in range(4)]        #StringVar()创建了四个装年、月、日、时信息的"盒子"。StringVar()是一种特殊的变量，可以和输入框（Entry）连接起来
    for i in range(4):                         #for循环创建实际输入框，把每个输入框和对应的年、月、日时的四个"盒子"连接起来。"年"会被存到text_vars[0]这个"盒子"里。"月"会被存到text_vars[1]这个"盒子"里。
        label = tk.Label(input_frame, text=labels[i], font=标签字体设置, bg='#F5F5F5', fg='#333333')
        label.grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(input_frame, textvariable=text_vars[i], font=条目字体设置, width=10, bg='#FFFFFF', fg='#333333', bd=1, relief='solid')
        entry.grid(row=i, column=1, padx=10, pady=5)
    
    # 性别选择框
    global 性别变量
    gender_frame = tk.Frame(输入窗口, bg='#F5F5F5')
    gender_frame.pack(pady=10)
    
    gender_标签 = tk.Label(gender_frame, text="性别：", font=标签字体设置, bg='#F5F5F5', fg='#333333')
    gender_标签.pack(side=tk.LEFT, padx=5)
    性别变量 = tk.StringVar(value="男")             #创建了性别变量对象，用于存储用户选择的【性别】
    radio_male = tk.Radiobutton(gender_frame, text="男", variable=性别变量, value="男", font=标签字体设置, bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_male.pack(side=tk.LEFT, padx=10)
    radio_female = tk.Radiobutton(gender_frame, text="女", variable=性别变量, value="女", font=标签字体设置, bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_female.pack(side=tk.LEFT, padx=10)
    
    # 历法选择框
    历法_frame = tk.Frame(输入窗口, bg='#F5F5F5')
    历法_frame.pack(pady=10)
    
    历法_标签 = tk.Label(历法_frame, text="历法：", font=标签字体设置, bg='#F5F5F5', fg='#333333')
    历法_标签.pack(side=tk.LEFT, padx=5)
    历法_var = tk.StringVar(value="公历")         #创建了历法_var对象，用于存储用户选择的【历法】
    radio_solar = tk.Radiobutton(历法_frame, text="公历", variable=历法_var, value="公历", font=标签字体设置, bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_solar.pack(side=tk.LEFT, padx=10)
    radio_lunar = tk.Radiobutton(历法_frame, text="农历", variable=历法_var, value="农历", font=标签字体设置, bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_lunar.pack(side=tk.LEFT, padx=10)
    
    # 定义一个变量，判断是否直接输入八字
    direct_input = tk.BooleanVar(value=False)
    
    # 定义一个函数，用于切换到直接输入八字的界面
    def switch_to_direct_input():
        # 将direct_input设置为True
        direct_input.set(True)
        # 关闭当前窗口
        输入窗口.destroy()
    
    # 创建"我要直接输入八字！"按钮
    direct_input_button = tk.Button(输入窗口, text="我要直接输入八字！", command=switch_to_direct_input,
                                    font=按钮字体设置, bg='#eeeeee', fg='#a2a2a2',
                                    activebackground='#d0d0d0', activeforeground='#FFFFFF',
                                    bd=0, padx=10, pady=5, relief='flat')
    direct_input_button.pack(pady=10)
    
    # 定义提交按钮的函数
    def submit():
        # 获取用户输入的值
        year = text_vars[0].get()
        month = text_vars[1].get()
        day = text_vars[2].get()
        time = text_vars[3].get()
        gender = 性别变量.get()
        历法 = 历法_var.get()
    
        # 创建一个Namespace对象来存储这些值，将输入的值存储到options中（这个options对象就是最终传递给脚本的数据）
        options = Namespace()
        options.year = year
        options.month = month
        options.day = day
        options.time = time
        options.n = (gender == "女")
        options.g = (历法 == "公历")  # 是否采用公历
        options.r = False  # 闰月，默认为False
        options.b = False  # 是否直接输入八字
        options.start = 1850  # 默认值
        options.end = '2030'  # 默认值
    
        # 关闭窗口并返回options
        输入窗口.destroy()
        输入窗口.options = options
    

    # 创建"提交"按钮
    submit_button = tk.Button(输入窗口, text="提交", command=submit,
                              font=按钮字体设置, bg='#eeeeee', fg='#a2a2a2',
                              activebackground='#d0d0d0', activeforeground='#FFFFFF',
                              bd=0, padx=20, pady=10, relief='flat')
    submit_button.pack(pady=10)
    
    # 进入主循环，显示窗口
    输入窗口.mainloop()
    
    # 如果direct_input为True，跳转到直接输入八字的界面
    if direct_input.get():
        # 调用直接输入八字的函数
        options = 获取用户在界面里输入的信息_直接输入八字()
        return options
    else:
        try:
            return 输入窗口.options
        except AttributeError:
            print("没有输入任何内容，程序退出")
            sys.exit(0)


# 【直接输入八字】的函数
def 获取用户在界面里输入的信息_直接输入八字():
    import sxtwl
    # 创建新窗口
    输入窗口 = tk.Tk()
    输入窗口.title("直接输入八字")
    输入窗口.geometry("1100x400")

    # 定义天干和地支的选项
    十天干的名字列表 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    十二地支的名字列表 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 定义变量，用于存储选择的天干和地支
    天干_vars = [tk.StringVar() for _ in range(4)]
    地支_vars = [tk.StringVar() for _ in range(4)]

    # 创建四柱选择框
    columns = ["年柱", "月柱", "日柱", "时柱"]
    for i in range(4):
        frame = tk.Frame(输入窗口)
        frame.pack(side=tk.LEFT, padx=5, pady=5)

        label = tk.Label(frame, text=columns[i])
        label.pack()

        # 天干选择框
        天干_combo = ttk.Combobox(frame, values=十天干的名字列表, textvariable=天干_vars[i])
        天干_combo.pack()
        天干_combo.current(0)  # 默认为第一个选项

        # 地支选择框
        地支_combo = ttk.Combobox(frame, values=十二地支的名字列表, textvariable=地支_vars[i])
        地支_combo.pack()
        地支_combo.current(0)
    # 性别选择框
    global 性别变量
    gender_frame = tk.Frame(输入窗口, bg='#F5F5F5')
    gender_frame.pack(pady=10)
    gender_标签 = tk.Label(gender_frame, text="性别：", bg='#F5F5F5', fg='#333333')
    gender_标签.pack(side=tk.LEFT, padx=5)
    性别变量 = tk.StringVar(value="男")  # 创建了性别变量对象，用于存储用户选择的【性别】
    radio_male = tk.Radiobutton(gender_frame, text="男", variable=性别变量, value="男", bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_male.pack(side=tk.LEFT, padx=10)
    radio_female = tk.Radiobutton(gender_frame, text="女", variable=性别变量, value="女", bg='#F5F5F5', fg='#333333', selectcolor='#F5F5F5')
    radio_female.pack(side=tk.LEFT, padx=10)
    
    # 添加默认生日选项
    use_default_date = tk.BooleanVar(value=True)
    # 创建"默认生日"复选框
    default_date_checkbutton = tk.Checkbutton(输入窗口,text="默认生日",variable=use_default_date,font=("Arial", 10),bg='#F5F5F5')
    default_date_checkbutton.pack(pady=5)


    # 定义显示可能生日选择窗口函数
    def 显示可能生日选择窗口(possible_dates):
        选择窗口 = tk.Toplevel()
        选择窗口.title("选择可能的生日")
        选择窗口.geometry("400x300")
        
        # 创建滚动条和列表框
        scrollbar = tk.Scrollbar(选择窗口)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(选择窗口, yscrollcommand=scrollbar.set, font=("Arial", 12))
        listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=listbox.yview)
        # 添加日期到列表
        for date in possible_dates:
            listbox.insert(tk.END, f"公历：{date.strftime('%Y - %m - %d - %H:%M:%S')}")
        
        # 选择日期的处理函数
        def on_select(event):
            selection = listbox.get(listbox.curselection())
            date_str = selection.split("：")[1].strip()
            year, month, day, time = date_str.split(" - ")
            hour = time.split(":")[0]
            
            # 更新options
            输入窗口.selected_date = {'year': year,'month': month,'day': day,'time': hour}
            选择窗口.destroy()
        
        listbox.bind('<<ListboxSelect>>', on_select)



    # 定义提交函数
    def 提交直接输入的八字信息():
        # 获取用户输入的值
        year = 天干_vars[0].get() + 地支_vars[0].get()
        month = 天干_vars[1].get() + 地支_vars[1].get()
        day = 天干_vars[2].get() + 地支_vars[2].get()
        time = 天干_vars[3].get() + 地支_vars[3].get()
        gender = 性别变量.get()

        # 创建options对象
        options = Namespace()
        options.year = year
        options.month = month
        options.day = day
        options.time = time
        options.n = (gender == "女")
        options.g = False
        options.r = False
        options.b = True
        options.start = 1801
        options.end = '2040'

        if use_default_date.get():
            # 使用默认生日
            try:
                jds = sxtwl.siZhu2Year(getGZ(year), getGZ(month), getGZ(day), getGZ(time), options.start, int(options.end))
            except Exception as e:
                print(f"计算生日时出错：{e}")
                messagebox.showerror("错误", f"计算生日时出错：{e}")
                return

            possible_dates = []
            for jd in jds:
                t = sxtwl.JD2DD(jd)
                possible_dates.append(datetime.datetime(int(t.Y), int(t.M), int(t.D), int(t.h), 0, 0))

            if possible_dates:
                current_year = datetime.datetime.now().year
                chosen_date = min(
                    (date for date in possible_dates if date.year <= current_year),
                    key=lambda x: abs(x.year - current_year)
                )
                options.selected_datetime = chosen_date

                print(f"已选择默认生日：{chosen_date.strftime('%Y年%m月%d日 %H时')}")
            else:
                messagebox.showwarning("警告", "未找到可能的生日")
                return
        else:
            # 显示可能生日选择窗口
            try:
                jds = sxtwl.siZhu2Year(getGZ(year), getGZ(month), getGZ(day), getGZ(time), options.start, int(options.end))
            except Exception as e:
                print(f"计算生日时出错：{e}")
                messagebox.showerror("错误", f"计算生日时出错：{e}")
                return

            possible_dates = []
            for jd in jds:
                t = sxtwl.JD2DD(jd)
                possible_dates.append(datetime.datetime(int(t.Y), int(t.M), int(t.D), int(t.h), 0, 0))

            if possible_dates:
                显示可能生日选择窗口(possible_dates)
                输入窗口.wait_window()  # 等待窗口关闭
                if hasattr(输入窗口, 'selected_date'):
                    options.year = 输入窗口.selected_date['year']
                    options.month = 输入窗口.selected_date['month']
                    options.day = 输入窗口.selected_date['day']
                    options.time = 输入窗口.selected_date['time']
                else:
                    return
            else:
                messagebox.showwarning("警告", "未找到可能的生日")
                return

        if 输入窗口.winfo_exists():  
            输入窗口.destroy()
        
        # 更新输入窗口的options属性
        输入窗口.options = options

    # 创建"确定"按钮
    submit_button = tk.Button(输入窗口, text="确定", command=提交直接输入的八字信息)
    submit_button.pack(pady=10)

    # 进入主循环
    输入窗口.mainloop()

    # 返回options
    return 输入窗口.options



"""
这是【输出】的GUI界面
"""
# 初始化受制次数字典，存储主体名字信息和受制次数
受制次数统计字典 = {'月支': 0, '日支': 0, '月干': 0, '时干': 0}

# 定义一个函数，用于在GUI中显示四柱八字和十神标签
def 显示四柱八字命盘结果的界面(本命盘四个天干名字列表, 本命盘四个地支名字列表, 四个天干十神列表, 四个地支十神列表):
    #在GUI界面中显示四柱八字和十神标签，并提供两个按钮，供用户自行选择，是否继续显示其他乱七八糟信息。
    #参数：1.十天干的名字列表: 天干列表    2.十二地支的名字列表: 地支列表    3.四个天干十神列表: 天干对应的十神标签    4.四个地支十神列表: 地支对应的十神标签
    #返回：show_remaining (bool): 用户是否选择继续显示其他信息
    # 创建主窗口
    result_window = tk.Tk()
    result_window.title("四柱八字排盘结果")
    result_window.configure(bg='#F5F5F5')

    # 设置字体
    标题字体设置 = ("Arial", 20, "bold")
    标签字体设置 = ("Arial", 18)
    small_font = ("Arial", 14)
    shen_font = ("Arial", 12)  # 用于十神标签

    # 创建标题
    标题_标签 = tk.Label(result_window, text="八字排盘结果", font=标题字体设置, bg='#F5F5F5')
    标题_标签.pack(pady=10)

    # 创建四柱展示框架
    四柱们的框架 = tk.Frame(result_window, bg='#F5F5F5')
    四柱们的框架.pack(pady=30)

    # 定义柱名
    pillars = ["年柱", "月柱", "日柱", "时柱"]

    for i in range(4):
        # 创建每一柱的框架
        柱_框架 = tk.Frame(四柱们的框架, bg='#F5F5F5', bd=0)
        柱_框架.grid(row=0, column=i, padx=30)

        # 显示柱名
        pillar_标签 = tk.Label(柱_框架, text=pillars[i], font=small_font, bg='#F5F5F5', fg='#A0A0A0')
        pillar_标签.pack(pady=5)

        # 显示天干的十神标签
        天干_shen_标签 = tk.Label(柱_框架, text=四个天干十神列表[i], font=shen_font, bg='#F5F5F5', fg='#C0C0C0')
        天干_shen_标签.pack()

        # 显示天干
        天干_标签 = tk.Label(柱_框架, text=本命盘四个天干名字列表[i], font=标签字体设置, bg='#F5F5F5')
        天干_标签.pack()

        # 显示地支
        地支_标签 = tk.Label(柱_框架, text=本命盘四个地支名字列表[i], font=标签字体设置, bg='#F5F5F5')
        地支_标签.pack()

        # 显示地支的十神标签
        地支_shen_标签 = tk.Label(柱_框架, text=四个地支十神列表[i], font=shen_font, bg='#F5F5F5', fg='#C0C0C0', bd=0)
        地支_shen_标签.pack()

    # 定义回调函数
    def quit_without_print():
        result_window.quit()
        result_window.destroy()
    
    def quit_with_print():
        # 这里可以添加显示其他信息的逻辑
        result_window.quit()
        result_window.destroy()
        
        # 进入新的界面
        result_window.quit()
        result_window.destroy()
        
        # 调用新的函数显示分析结果
        命盘分析界面(本命盘四个天干名字列表, 本命盘四个地支名字列表)

    # 创建按钮框架
    buttons_frame = tk.Frame(result_window, bg='#F5F5F5')
    buttons_frame.pack(pady=20)

    # 定义按钮样式
    style = ttk.Style()
    style.theme_use('default')  # 使用默认主题以确保自定义样式生效
    style.configure('TButton',
                    font=("Arial", 14),
                    padding=10,
                    relief="flat",
                    foreground="#333333",  # 改为深灰色文字
                    background="#eeeeee",
                    borderwidth=0)
    style.map('TButton',
              background=[('active', '#d5d5d5')],
              foreground=[('active', '#FFFFFF')])  # 鼠标悬停时文字变白

    import time


    # 定义"断旺衰，找用神"按钮的事件函数，在同一位置添加：
    def 出现分析命盘界面窗口():
        # 发光特效（持续 0.1 秒）
        for _ in range(1):
            result_window.configure(bg='#FFFFE0')  # 发光颜色
            result_window.update()
            time.sleep(0.1)
            result_window.configure(bg='#F5F5F5')  # 恢复原始背景色
            result_window.update()
            time.sleep(0.1)
        
        # 调用新的函数显示分析结果
        命盘分析界面(result_window,本命盘四个天干名字列表, 本命盘四个地支名字列表, 四个天干十神列表, 四个地支十神列表, 性别变量)

    # 创建"断旺衰，找用神"按钮
    btn_analyze = ttk.Button(buttons_frame, text="断旺衰，找用神", command=出现分析命盘界面窗口)
    btn_analyze.pack(side=tk.LEFT, padx=10)

    # 创建其他按钮
    btn_quit_no = ttk.Button(buttons_frame, text="不显示其他信息", command=quit_without_print)
    btn_quit_no.pack(side=tk.LEFT, padx=10)
 
    # 创建"显示其他信息"按钮
    btn_quit_yes = ttk.Button(buttons_frame, text="除了四柱八字，再告诉我其他信息", command=quit_with_print)
    btn_quit_yes.pack(side=tk.LEFT, padx=10)

    # 运行主循环
    result_window.mainloop()
    return 本命盘四个天干名字列表, 本命盘四个地支名字列表, 四个天干十神列表, 四个地支十神列表



# 使用GUI获取用户输入的options
options = 获取用户在界面里输入的信息()
Gans = collections.namedtuple("Gans", "year month day time")  #创建一个名为 Gans 的 namedtuple，它有四个字段：year、month、day、time
Zhis = collections.namedtuple("Zhis", "year month day time")

#如果用户选择直接输入八字（options.b为True），使用sxtwl库（一个中国历法库）来处理输入的八字，将输入的天干地支转换为可能的出生时间。
#如果用户输入的是生辰（options.b为False），代码会：根据是否使用公历（options.g）来选择处理方法。如果是公历，先转换为农历；如果是农历，直接使用。使用lunar_python库来计算八字（这反映了传统八字排盘中，需要先确定农历日期的步骤）
#代码使用ba.getYearGan()等方法获取年、月、日、时的天干。使用ba.getYearZhi()等方法获取年、月、日、时的地支。（代码中的options.r用于处理闰月情况）
#【输入处理】
from ganzhi import 十神关系表,地支藏干字典,地支合会破刑害字典
from datas import 地支空亡字典,year_shens,month_shens,day_shens,g_shens
from common import 计算阴阳属性,天干间合冲关系判断

if options.b:
    if hasattr(options, 'selected_datetime'):
        # 用户选择了默认生日，使用公历日期计算八字
        from lunar_python import Solar, Lunar

        # 创建 Solar 对象
        solar = Solar.fromYmdHms(
            options.selected_datetime.year,
            options.selected_datetime.month,
            options.selected_datetime.day,
            options.selected_datetime.hour,
            0,
            0
        )
        # 获取 Lunar 对象
        lunar = solar.getLunar()
        # 获取八字对象
        ba = lunar.getEightChar()

        # 获取天干和地支列表
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

    else:
        # 用户未选择默认生日，使用自定义的 BaZi 类
        ba = BaZi(options.year, options.month, options.day, options.time)
        本命盘四个天干名字列表 = Gans(
            year=options.year[0],
            month=options.month[0],
            day=options.day[0],
            time=options.time[0]
        )
        本命盘四个地支名字列表 = Zhis(
            year=options.year[1],
            month=options.month[1],
            day=options.day[1],
            time=options.time[1]
        )
else:
    # 原有的处理生辰的代码
    if options.g:
        solar = Solar.fromYmdHms(int(options.year), int(options.month), int(options.day), int(options.time), 0, 0)
        lunar = solar.getLunar()
    else:
        month_ = int(options.month)*-1 if options.r else int(options.month)
        lunar = Lunar.fromYmdHms(int(options.year), month_, int(options.day),int(options.time), 0, 0)
        solar = lunar.getSolar()
    #如果用户输入生辰
    day = lunar
    ba = lunar.getEightChar() 
    本命盘四个天干名字列表 = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
    本命盘四个地支名字列表 = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())
    
    global_ba = ba

所有断语 = []  # 用来存储所有断语
当前选中流年列表 = []
当前选中大运 = None
def 收集断语(断语内容):   # 收集断语，并打印出来
    global 所有断语
    所有断语.append(断语内容)


# 先计算大运信息
def 计算大运信息():
    from lunar_python import Solar, Lunar
    global 大运天干字典, 大运地支字典, global_ba
    # 关键的《大运字典》的创建
    大运天干字典 = {}
    大运地支字典 = {}
    
    if options.b:
        if hasattr(options, 'selected_datetime'):
            # 如果有选定的公历日期，使用公历日期创建lunar对象
            lunar = Lunar.fromSolar(Solar.fromYmdHms(
                options.selected_datetime.year,
                options.selected_datetime.month,
                options.selected_datetime.day,
                options.selected_datetime.hour,
                0,
                0
            ))
            lunar = solar.getLunar()
            global_ba = lunar.getEightChar()  # 重要：更新global_ba
        else:
            lunar = Lunar.fromYmdHms(int(options.year), int(options.month), int(options.day),int(options.time), 0, 0)    # 使用推算出的出生时间创建lunar对象
            global_ba = lunar.getEightChar() 
    
    else:  # 正常输入生日的情况
        lunar = Lunar.fromYmdHms(int(options.year), int(options.month), int(options.day),int(options.time), 0, 0)    # 使用推算出的出生时间创建lunar对象
        global_ba = lunar.getEightChar()   # 使用lunar对象获取八字和大运信息
        
    yun = global_ba.getYun(not options.n)
    for dayun in yun.getDaYun()[1:]:
        ganzhi = dayun.getGanZhi()
        大运天干 = ganzhi[0]
        大运地支 = ganzhi[1]
        zhus = [item for item in zip(本命盘四个天干名字列表, 本命盘四个地支名字列表)]
        # 填充“大运天干字典”和“大运地支字典”的一级键和二级键的值
        大运天干字典[大运天干] = {"阴阳属性": 计算阴阳属性(大运天干),"旺弱状态": "","是否实神": ""}
        大运地支字典[大运地支] = {"阴阳属性": 计算阴阳属性(大运地支),"旺弱状态": "","是否实神": "","是否空亡": "空亡" if 大运地支 in 地支空亡字典[zhus[2]] else "不空亡"}
    # 打印调试信息
    print("\n=== 🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️大运天干字典 ===")
    for 天干, 属性 in 大运天干字典.items():
        print(f"{天干}: {属性}")
    print("\n=== 🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️大运地支字典 ===")
    for 地支, 属性 in 大运地支字典.items():
        print(f"{地支}: {属性}")
    return 大运天干字典, 大运地支字典
计算大运信息()



def 命盘分析界面(parent, 本命盘四个天干名字列表, 本命盘四个地支名字列表,四个天干十神列表, 四个地支十神列表, 性别):
    # 导入必要的库
    import tkinter as tk
    from tkinter import ttk
    import time  # 用于可能的动画效果
    from datas import 地支空亡字典  # 导入空亡地支的数据
    global 性别变量, 所有断语,所有断语,大运天干字典,大运地支字典
    所有断语.clear()
    性别变量 = 性别

    bazi_strength_analysis = {}   # 初始化八字力量分析字典，存储主体名字信息、属性、力量数值
    地支_标签_列表 = []   # 初始化列表，用于存储地支标签

    # 🖥️🖥️🖥️创建新窗口，指定父窗口为parent
    分析命盘界面窗口 = tk.Toplevel(parent)
    分析命盘界面窗口.title("断旺衰找用神（新派王易成算法）")
    分析命盘界面窗口.configure(bg='#f5f5f1')  # 设置"断旺衰找用神（新派王易成算法）"子输出界面的背景颜色
    分析命盘界面窗口.geometry("1550x850")  # 设置窗口长宽
    # 设置字体和样式，与显示界面保持一致
    标题字体设置 = ("Arial", 20, "bold")  # 标题字体
    标签字体设置 = ("Arial", 18)          # 标签字体
    small_font = ("Arial", 14)          # 小号字体
    shen_font = ("Arial", 10)           # 十神标签字体
    # 创建标题
    标题_标签 = tk.Label(分析命盘界面窗口, text="八字排盘结果", font=标题字体设置, bg='#f5f5f1')
    标题_标签.pack(pady=20)
    # 创建四柱展示框架并使其居中
    四柱们的框架 = tk.Frame(分析命盘界面窗口, bg='#f5f5f1', width=900, height=300)   # width、heiht设置框架的宽度和高度为固定值
    四柱们的框架.pack(expand=False)
    # 定义柱名
    天干_shen_标签_列表 = []
    地支_标签_列表 = []
    pillars = ["年柱", "月柱", "日柱", "时柱"]
    柱_框架_列表 = []  # 定义一个列表，用于存储每一柱的框架
    for i in range(4):
        # 创建每一柱的框架并使其在父框架中居中
        柱_框架 = tk.Frame(四柱们的框架, bg='#f5f5f1', bd=0, width=300, height=200)  # width、heiht设置框架的宽度和高度为固定值
        柱_框架.grid(row=1, column=i, padx=50, pady=(20, 20))
        柱_框架_列表.append(柱_框架)    # 将柱_框架添加到列表中，方便后续定位
        # 显示柱名
        pillar_标签 = tk.Label(柱_框架, text=pillars[i], font=small_font, bg='#f5f5f1', fg='#A0A0A0')
        pillar_标签.pack(pady=5)
        # 显示天干的十神标签（暂时只显示十神，忌用神归属稍后更新）
        天干_shen_标签 = tk.Label(柱_框架, text=四个天干十神列表[i], font=shen_font, bg='#f5f5f1', fg='#C0C0C0')
        天干_shen_标签.pack()
        天干_shen_标签_列表.append(天干_shen_标签)  # 将天干十神标签存储到列表中
        # 显示天干
        天干_标签 = tk.Label(柱_框架, text=本命盘四个天干名字列表[i], font=标签字体设置, bg='#f5f5f1')
        天干_标签.pack()
        # 显示地支
        地支_标签 = tk.Label(柱_框架, text=本命盘四个地支名字列表[i], font=标签字体设置, bg='#f5f5f1', bd=0, padx=8, pady=8)
        地支_标签.pack()
        # 将地支标签添加到列表中
        地支_标签_列表.append(地支_标签)
        # 显示地支的十神标签
        地支_shen_标签 = tk.Label(柱_框架, text=四个地支十神列表[i], font=shen_font, bg='#f5f5f1', fg='#d9d9d9', bd=0,padx=8, pady=2)
        地支_shen_标签.pack()






    from ganzhi import  十天干五行对照表, 十二地支五行对照表, 五行作用关系字典, 晦脆冲特殊关系字典, 十天干的名字列表, 十二地支的名字列表, 十神关系表, 有根字典
    # 初始化八字信息主字典字典
    八字信息主字典 = {'年干': {}, '年支': {}, '月干': {}, '月支': {}, '日干': {}, '日支': {}, '时干': {}, '时支': {}}

    # 定义所有的一级键和二级键
    一级键列表 = ['年干', '年支', '月干', '月支', '日干', '日支', '时干', '时支']
    二级键列表 = ['十神', '名字', '五行属性', '是否空亡', '正负属性', '力量数值', '忌用神归属', '外环境', '内环境', '阴阳属性','旺弱状态']

    # 使用循环为每个一级键添加所有二级键
    for 一级键 in 一级键列表:
        for 二级键 in 二级键列表:
            八字信息主字典[一级键][二级键] = None              # 初始化所有值为 None

    # 添加十神信息
    for i, 键 in enumerate(['年干', '月干', '日干', '时干']):
        八字信息主字典[键]['十神'] = 四个天干十神列表[i]
    for i, 键 in enumerate(['年支', '月支', '日支', '时支']):
        八字信息主字典[键]['十神'] = 四个地支十神列表[i]

    # 添加名字和五行属性
    for i, (干键, 支键) in enumerate(zip(['年干', '月干', '日干', '时干'], ['年支', '月支', '日支', '时支'])):
        八字信息主字典[干键]['名字'] = 本命盘四个天干名字列表[i]
        八字信息主字典[干键]['五行属性'] = 十天干五行对照表[本命盘四个天干名字列表[i]]
        八字信息主字典[支键]['名字'] = 本命盘四个地支名字列表[i]
        八字信息主字典[支键]['五行属性'] = 十二地支五行对照表[本命盘四个地支名字列表[i]]

    # 设置特定的正负属性
    for 键 in ['年干', '月干', '时干', '日支']:
        八字信息主字典[键]['正负属性'] = '零'

    # 设置空亡初始值
    for 键 in ['年支','月支','日支','时支']:
        八字信息主字典[键]['是否空亡'] = '否'

    # 设置力量数值
    for 一级键 in 一级键列表:
        八字信息主字典[一级键]['力量数值'] = 0  # 设置为数字 0

    #判断并设置阴阳属性
    for 一级键 in 一级键列表:
        名字 = 八字信息主字典[一级键]['名字']
        if 一级键.endswith('干'):
            if 名字 in 阳属性天干列表:
                八字信息主字典[一级键]['阴阳属性'] = '阳'
            elif 名字 in 阴属性天干列表:
                八字信息主字典[一级键]['阴阳属性'] = '阴'
        elif 一级键.endswith('支'):
            if 名字 in 阳属性地支列表:
                八字信息主字典[一级键]['阴阳属性'] = '阳'
            elif 名字 in 阴属性地支列表:
                八字信息主字典[一级键]['阴阳属性'] = '阴'



#1. 看空亡
    # 🖥️🖥️🖥️ 创建一个空白的标签，用于在右上角显示空亡的地支    # 使主窗口中的所有组件居中
    分析命盘界面窗口.grid_columnconfigure(0, weight=1)
    分析命盘界面窗口.grid_rowconfigure(0, weight=1)
    四柱们的框架.grid_columnconfigure(0, weight=1)
    四柱们的框架.grid_rowconfigure(0, weight=1)
    # 获取空亡的地支列表，使用日柱的天干和地支作为键
    空亡_地支_列表 = 地支空亡字典.get((本命盘四个天干名字列表[2], 本命盘四个地支名字列表[2]), ())
    空亡_地支_text = "空亡的地支：" + '、'.join(空亡_地支_列表)
    空亡_标签 = tk.Label(分析命盘界面窗口, text=空亡_地支_text, font=small_font, fg='#A9A9A9', bg='#f5f5f1')
    空亡_标签.place(relx=0.95, rely=0.05, anchor='ne')
    分析命盘界面窗口.update_idletasks()         # 更新窗口，以确保可以获取正确的坐标
    
    # 新增代码：更新"八字信息主字典"中的空亡信息
    地支一级键列表 = ['年支', '月支', '日支', '时支']
    for i, 地支 in enumerate(本命盘四个地支名字列表):
        if 地支 in 空亡_地支_列表:
            八字信息主字典[地支一级键列表[i]]['是否空亡'] = '空亡'
    
    # 🖥️🖥️🖥️ 在合适的位置创建[空亡]标签
    for i in range(4):
        if 本命盘四个地支名字列表[i] in 空亡_地支_列表:
            地支_标签 = 地支_标签_列表[i]  # 获取对应的地支标签
            # 创建 '[空亡]' 标签
            空亡_地支_标签 = tk.Label(地支_标签.master, text='[空亡]', font=("Arial", 7), fg='#9d8383', bg='#f7e5e5', padx=0, pady=1, bd=0, highlightthickness=0)
            # 获取 地支_标签 在父容器中的位置
            x = 地支_标签.winfo_x() + 24
            y = 地支_标签.winfo_y() + 地支_标签.winfo_height() - 8
            # 将 空亡_地支_标签 放置在指定位置
            空亡_地支_标签.place(x=x, y=y)





    #先把"未现正偏十神主字典"完善起来，自成一派。代码块实现了"未现正偏十神主字典"里所有一级键的填充，也完成赋值了'十神'、'名字'、'五行属性'三个二级键
    十天干的名字列表 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    五个正十神列表大全 = ['正印', '正官', '正财', '劫财', '伤官'] 
    五个偏十神列表大全 = ['偏印(枭)', '七杀', '偏财', '比肩', '食神']
    年干十神 = 四个天干十神列表[0]  # 获取年干十神
    月干十神 = 四个天干十神列表[1]  # 获取月干十神
    时干十神 = 四个天干十神列表[3]  # 获取时干十神
    me = 八字信息主字典['日干']['名字']      # 获取日干（第三个天干）
    global 未现正偏十神主字典   # 声明全局变量，存储未现正偏十神信息
    未现正偏十神主字典 = {}
    global 实神虚神作用关系字典
    实神虚神作用关系字典 = {} 

    月干和时干的十神信息列表 = [四个天干十神列表[1], 四个天干十神列表[3]]                                  # 获取月干🌕和时干⏰的十神，组成一个列表  （即使在没有匹配项时（命盘上面没有"已现正十神"或者没有"已现偏十神"）也会安全地返回空列表）
                                    
    已现正十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个正十神列表大全]                   # 找出已现正十神（在月干和时干中）
    未现正十神 = [shen for shen in 五个正十神列表大全 if shen not in 已现正十神 and shen != 年干十神]    # 找出未现正十神（排除年干的十神）
    已现偏十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个偏十神列表大全]                   # 已现偏十神
    未现偏十神 = [shen for shen in 五个偏十神列表大全 if shen not in 已现偏十神 and shen != 年干十神]   # 未现偏十神

    未现十神们及其天干名的字典 = {}      # 创建未现正十神及其对应的天干名的字典
    for 天干名 in 十天干的名字列表:
        shen = 十神关系表[me][天干名]      # 获取查询日主与当前天干的关系，推导出"未现正十神"的"十神"
        if shen in 未现正十神:
            未现十神们及其天干名的字典[shen] = 天干名     # 记录十神和对应的天干名
        if shen in 未现偏十神:
            未现十神们及其天干名的字典[shen] = 天干名     # 记录十神和对应的天干名

    for shen, 天干名 in 未现十神们及其天干名的字典.items():         # 遍历未现正十神，填充未现正偏十神主字典
        未现正偏十神主字典[天干名] = {'十神': shen,  '名字': 天干名,  '五行属性': 十天干五行对照表[天干名]}            #未现正偏十神主字典正式赋值完成







    def 元素间关系分析(一级键1, 一级键2):
        from ganzhi import 十二地支五行对照表
        global 未现正偏十神主字典
        global 实神虚神作用关系字典

        if 一级键1 in 大运地支字典:   # 先检查是否在“大运地支字典”里
            一级键1的子字典 = {'名字': 一级键1, '五行属性': 十二地支五行对照表[一级键1], '阴阳属性': 大运地支字典[一级键1]['阴阳属性']}
        else:
            try:
                一级键1的子字典 = 八字信息主字典[一级键1]
            except KeyError:
                一级键1的子字典 = 未现正偏十神主字典.get(一级键1, None)  # 如果在八字信息主字典中找不到，则尝试从未现正偏十神主字典中获取

        if 一级键2 in 大运地支字典:  
            一级键2的子字典 = {'名字': 一级键2, '五行属性': 十二地支五行对照表[一级键2], '阴阳属性': 大运地支字典[一级键2]['阴阳属性']}
        else:
            try:
                一级键2的子字典 = 八字信息主字典[一级键2]
            except KeyError:
                一级键2的子字典 = 未现正偏十神主字典.get(一级键2, None)  # 如果在八字信息主字典中找不到，则尝试从未现正偏十神主字典中获取   

        def 查找二级键对应的一级键(键):
            for 柱, 信息 in 八字信息主字典.items():
                if 信息.get('名字') == 键:
                    return 八字信息主字典[柱]
            return None

        if 一级键1的子字典 is None:
            一级键1的子字典 = 查找二级键对应的一级键(一级键1)
            if 一级键1的子字典 is None:
                print(f"{一级键1}的值为空，无法分析关系。")
                return None

        if 一级键2的子字典 is None:
            一级键2的子字典 = 查找二级键对应的一级键(一级键2)
            if 一级键2的子字典 is None:
                print(f"{一级键2}的值为空，无法分析关系。")
                return

        # 创建用于查找关系的元组
        临时元组 = (一级键1的子字典['名字'], 一级键2的子字典['名字'])

        # 查询特殊关系字典
        if 临时元组 in 晦脆冲特殊关系字典:
            两者关系 = 晦脆冲特殊关系字典[临时元组]   # 如果存在特殊关系，获取关系的值
        else:
            五行关系分析_临时元组 = (一级键1的子字典['五行属性'], 一级键2的子字典['五行属性'])
            两者关系 = 五行作用关系字典.get(五行关系分析_临时元组, '零')  # 默认关系为 '零'

        生扶受制关系概括 = '不旺不弱关系'

        if 两者关系 in ('同', '生', '旺'):
            生扶受制关系概括 = '生扶关系'
            正负属性 = '正'
            力量数值 = 51
        elif 两者关系 in ('克', '泄', '耗', '刑', '冲', '晦', '脆', '弱'):
            生扶受制关系概括 = '受制关系'
            正负属性 = '正'
            力量数值 = 51
        elif 两者关系 == '零':
            生扶受制关系概括 = '不旺不弱关系'
            正负属性 = '零'
            力量数值 = 0
            print(f"{一级键1的子字典['名字']} 是 {一级键2的子字典['名字']} 的墓库")

        else:
            print(f"警告：发现未处理的关系类型：{两者关系}")   # 如果出现了预期之外的关系值，打印出来以便调试

        # 判断一级键1和一级键2是否在八字信息主字典中
        一级键1是实神 = 一级键1的子字典 is not None
        一级键2是实神 = 一级键2的子字典 is not None

        if ('干' in 一级键1 and '干' in 一级键2) or ('支' in 一级键1 and '支' in 一级键2):
            if (一级键1是实神 and not 一级键2是实神) or (not 一级键1是实神 and 一级键2是实神):    # 一个实神一个虚神，存储到实神虚神作用关系字典
                实神虚神作用关系字典[f'{一级键1}_{一级键2}_关系'] = {'关系': 两者关系, '概括': 生扶受制关系概括, '外环境': '', '内环境': ''}
            elif 一级键1是实神 and 一级键2是实神:    # 两个都是实神，存储到八字信息主字典
                八字信息主字典[f'{一级键1}_{一级键2}_关系'] = {'关系': 两者关系, '概括': 生扶受制关系概括, '正负属性': 正负属性, '力量数值': 力量数值}
            else:
                print("一级键1和一级键2无法作用")

        return 两者关系, 生扶受制关系概括, 正负属性, 力量数值
    




#1. 看月支🌙
    #1.2 两干一支的分析

    # 调用 元素间关系分析 函数并获取返回值
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('月支', '日干')    # 1、获得"月支"🌙与【日干】👧🏻的关系

    八字信息主字典['月支']['力量数值'] = 力量数值     
    八字信息主字典['月支']['正负属性'] = 正负属性

    print(f"{'月支'} 和 {'日干'} 的关系为：{两者关系}，概括为：{生扶受制关系概括}")   
    print(f"月支🌙的力量值：属性 = {八字信息主字典['月支']['正负属性']}，力量数值 = {八字信息主字典['月支']['力量数值']}")    

    新的力量值 = 八字信息主字典['月支']['力量数值']    # 初始化 新的力量值，默认值为当前的力量数值
    受制次数统计字典.setdefault('月支', 0)   # 如果 '月支' 不存在，则初始化为 0

    # 调用函数并获取返回值
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('年支', '月支')    # 2、获得"年支"🧨与"月支"🌙的关系。，查看"月支"是否受制了一次，如果受制一次，'力量数值'就更新为原先数值减去17（等于34）（特殊情况：如果元素间关系分析是'耗'，就不用减去17，'力量数值'继承之前的数值不变）。

    if 生扶受制关系概括 == '受制关系':
        受制次数统计字典['月支'] += 1                                # 无论关系为何，都增加受制次数
        if 两者关系 != '耗':                                       # 如果关系不是 '耗'
            旧的力量值 = 八字信息主字典['月支']['力量数值']
            新的力量值 = 旧的力量值 - 17                             # 原力量值减去 17
            八字信息主字典['月支']['力量数值'] = 新的力量值
            print(f"年支🧨与月支🌙关系分析：月支🌙受制{受制次数统计字典['月支']}次，力量数值减17，现在是：{新的力量值}")
        else:
            当前_力量数值 = 八字信息主字典['月支']['力量数值']    # 力量值不变，直接引用当前值
            print(f"年支🧨与月支🌙关系分析：月支🌙受制{受制次数统计字典['月支']}次，关系为'耗'，力量数值不变：{当前_力量数值}")
    else:
        print("年支🧨与月支🌙关系分析：月支🌙未受制，力量值不变。")


    受制次数统计字典.setdefault('月支', 0)          # 如果 '月支' 不存在于受制次数统计字典，则'月支'的受制次数初始化为 0
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('日支', '月支')    # 3、获得"日支"📅与"月支"🌙的关系。，查看"月支"是否受制了一次，如果又受制一次，'力量数值'就更新为原先数值再减去17（特殊情况：是'耗'，就不用减去17，'力量数值'不变）。

    if 生扶受制关系概括 == '受制关系':
        受制次数统计字典['月支'] += 1                        # 无论关系为何，都增加受制次数
        if 两者关系 != '耗':                                  # 如果关系不是 '耗'
            旧的力量值 = 八字信息主字典['月支']['力量数值']
            新的力量值 = 旧的力量值 - 17                 # 原力量值减去 17
            八字信息主字典['月支']['力量数值'] = 新的力量值
            print(f"日支📅与月支🌙关系分析：月支🌙受制{受制次数统计字典['月支']}次，力量数值减去17，现在是：{新的力量值}")
        else:
            当前_力量数值 = 八字信息主字典['月支']['力量数值']    # 力量值不变，直接引用当前值
            print(f"日支📅与月支🌙关系分析：月支🌙受制{受制次数统计字典['月支']}次，因为关系为'耗'(主克者不减力)，所以月支🌙力量数值现在是：{新的力量值}")
    else:
        print(f"纵观月支左右分析：月支🌙总共受制{受制次数统计字典['月支']}次，所以月支🌙力量数值现在是：{新的力量值}")

    

#2. 看日支📅
 
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('日支', '日干')         # 第一步，分析日支📅和日干👧🏻的关系
    if 生扶受制关系概括 == '生扶关系':     # 根据关系更新日支的属性和力量数值
        八字信息主字典['日支']['正负属性'] = '正'
        八字信息主字典['日支']['力量数值'] = 15
    elif 生扶受制关系概括 == '受制关系':
        八字信息主字典['日支']['正负属性'] = '负'
        八字信息主字典['日支']['力量数值'] = 15
    elif 生扶受制关系概括 == '不旺不弱关系':
        八字信息主字典['日支']['正负属性'] = '零'
        八字信息主字典['日支']['力量数值'] = 0

    
    受制次数统计字典['日支'] = 0      # 第二步，初始化日支的受制次数为0
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('月支', '日支')       # 分析月支🌙和日支📅的关系
    if 生扶受制关系概括 == '受制关系':
        if 两者关系 != '耗':
            受制次数统计字典['日支'] += 1     
            八字信息主字典['日支']['力量数值'] -= 8        
        elif 两者关系 == '耗':
            受制次数统计字典['日支'] += 1

    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('时支', '日支')       # 分析时支⌚️和日支📅的关系
    if 生扶受制关系概括 == '受制关系':
        if 两者关系 != '耗':
            受制次数统计字典['日支'] += 1    
            八字信息主字典['日支']['力量数值'] -= 8 
        elif 两者关系 == '耗':
            受制次数统计字典['日支'] += 1

    # 特殊情况，检查月支和日支的受制次数
    if 受制次数统计字典['月支'] == 2 and 受制次数统计字典['日支'] == 2:
        受制次数统计字典['月支'] = 1      # 月支受制次数更新为1次
        八字信息主字典['月支']['力量数值'] += 17       # 月支力量数值加回17
        print(f"月支🌙在步骤三时受制次数为：{受制次数统计字典['月支']}。力量数值为：{八字信息主字典['月支']['力量数值']}")

    #print(f"日支📅在步骤三时受制次数为：{受制次数统计字典['日支']}。属性为：{八字信息主字典['日支']['正负属性']}，力量数值为：{八字信息主字典['日支']['力量数值']}")



# 3. 看月干🌕

    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('月干', '日干')  # 分析月干🌕对日干👧🏻的关系
    print(f"月干与日干的关系: {两者关系}，概括为: {生扶受制关系概括}")       
    if 生扶受制关系概括 == '生扶关系':                # 根据关系更新月干的属性和力量数值
        八字信息主字典['月干']['正负属性'] = '正'
        八字信息主字典['月干']['力量数值'] = 15
    elif 生扶受制关系概括 == '受制关系':
        八字信息主字典['月干']['正负属性'] = '负'
        八字信息主字典['月干']['力量数值'] = 15
    elif 生扶受制关系概括 == '不旺不弱关系':
        八字信息主字典['月干']['正负属性'] = '零'
        八字信息主字典['月干']['力量数值'] = 15

    受制次数统计字典['月干'] = 0                # 初始化月干🌕的受制次数为0

    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('月支', '月干')       # 分析月支🌙和月干🌕的关系

    if 生扶受制关系概括 == '受制关系':
        受制次数统计字典['月干'] += 1

    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('年干', '月干')        # 分析年干🧨和月干🌕的关系

    if 生扶受制关系概括 == '受制关系':
        受制次数统计字典['月干'] += 1        

    #print(f"月干🌕在步骤四时受制次数为：{受制次数统计字典['月干']}。属性为：{八字信息主字典['月干']['正负属性']}，力量数值为：{八字信息主字典['月干']['力量数值']}")


# 4. 看时干⏰

    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('时干', '日干')         # 分析时干⏰对日干👧🏻的关系
    if 生扶受制关系概括 == '生扶关系':
        八字信息主字典['时干']['正负属性'] = '正'
        八字信息主字典['时干']['力量数值'] = 10
    elif 生扶受制关系概括 == '受制关系' and 两者关系 != '耗':
        八字信息主字典['时干']['正负属性'] = '负'
        八字信息主字典['时干']['力量数值'] = 10
    elif 生扶受制关系概括 == '不旺不弱关系':
        八字信息主字典['时干']['正负属性'] = '零'
        八字信息主字典['时干']['力量数值'] = 0

    受制次数统计字典['时干'] = 0                # 初始化时干⏰的受制次数为0
    两者关系, 生扶受制关系概括, 正负属性, 力量数值 = 元素间关系分析('时支', '时干')       # 分析时支⌚️和时干⏰的关系
    if 生扶受制关系概括 == '生扶关系':
        受制次数统计字典['时干'] += 1        # 受制次数加1
        八字信息主字典['时干']['力量数值'] += 10          # 力量数值加10

    #print(f"时干⏰在步骤五时受制次数为：{受制次数统计字典['时干']}。属性为：{八字信息主字典['时干']['正负属性']}，力量数值为：{八字信息主字典['时干']['力量数值']}")


# 5. 同党查找
    # 获取元素的属性和力量数值，存入同党查找字典
    两干一支遍历列表 = ['月干', '日支', '时干']
    同党查找字典 = {}
    for 遍历列表的变量 in 两干一支遍历列表:
        正负属性 = 八字信息主字典[遍历列表的变量]['正负属性']
        力量数值 = 八字信息主字典[遍历列表的变量]['力量数值']
        if 力量数值 != 0:
            if 正负属性 not in 同党查找字典:
                同党查找字典[正负属性] = []
            同党查找字典[正负属性].append(遍历列表的变量)

    # 处理月干🌙
    正负属性 = 八字信息主字典['月干']['正负属性']
    if 正负属性 in 同党查找字典 and len(同党查找字典[正负属性]) > 1:
        八字信息主字典['月干']['力量数值'] += 10

    # 处理时干⏰
    正负属性 = 八字信息主字典['时干']['正负属性']
    if 正负属性 in 同党查找字典 and len(同党查找字典[正负属性]) > 1:
        八字信息主字典['时干']['力量数值'] += 10

    # 处理日支📅
    正负属性 = 八字信息主字典['日支']['正负属性']
    if 正负属性 in 同党查找字典 and len(同党查找字典[正负属性]) > 1:
        八字信息主字典['日支']['力量数值'] += 10

    # 确保力量数值在0到10之间
    for 遍历处理目标 in ['月干', '时干', '日支']:
        力量数值 = 八字信息主字典[遍历处理目标]['力量数值']
        if 力量数值 > 10:
            八字信息主字典[遍历处理目标]['力量数值'] = 10
        elif 力量数值 < 0:
            八字信息主字典[遍历处理目标]['力量数值'] = 0

    # 分别打出最终的受制次数、属性和力量数值
    print(f"月干🌙最终受制次数：{受制次数统计字典['月干']},  属性：{八字信息主字典['月干']['正负属性']},  力量数值：{八字信息主字典['月干']['力量数值']}")
    print(f"时干⏰最终受制次数：{受制次数统计字典['时干']},  属性：{八字信息主字典['时干']['正负属性']},  力量数值：{八字信息主字典['时干']['力量数值']}")
    print(f"日支📅最终受制次数：{受制次数统计字典['日支']},  属性：{八字信息主字典['日支']['正负属性']},  力量数值：{八字信息主字典['日支']['力量数值']}")




# 6. 本命盘的【格局判定】
    def 本命盘的格局判定():
        生扶力量总值 = sum(八字信息主字典[遍历列表的变量]['力量数值'] for 遍历列表的变量 in 同党查找字典.get('正', []))
        受制力量总值 = sum(八字信息主字典[遍历列表的变量]['力量数值'] for 遍历列表的变量 in 同党查找字典.get('负', []))
        if 生扶力量总值 > 受制力量总值:
            if 受制力量总值 == 0:
                格局 = '从旺格局'
                print("☯️本命局格局为：从旺格局")
            else:
                格局 = '身旺格局'
                print("☯️本命局格局为：身旺格局")
        elif 生扶力量总值 < 受制力量总值:
            if 生扶力量总值 == 0:
                格局 = '从弱格局'
                print("☯️本命局格局为：从弱格局")
            else:
                格局 = '身弱格局'
                print("☯️本命局格局为：身弱格局")
        return 格局
    格局 = 本命盘的格局判定()




# 7. 日支🌳、月干🌕、时干⏰ 定用神/忌神

    def 判定用忌神(一级键1, 一级键2, 格局):
        # 调用元素间关系分析函数，获取生扶受制关系概括
        _, 生扶受制关系概括, _, _ = 元素间关系分析(一级键1, 一级键2)
        
        # 初始化忌用神归属
        忌用神归属 = None
        
        # 根据格局和关系概括，判定忌用神归属
        if 格局 in ['从弱格局', '身旺格局']:
            if 生扶受制关系概括 == '生扶关系':
                忌用神归属 = '忌神'
            elif 生扶受制关系概括 == '受制关系':
                忌用神归属 = '用神'
        elif 格局 in ['从旺格局', '身弱格局']:
            if 生扶受制关系概括 == '生扶关系':
                忌用神归属 = '用神'
            elif 生扶受制关系概括 == '受制关系':
                忌用神归属 = '忌神'
        
        # 各回各家 各找各妈，更新相应字典—— 实神更新在"八字信息主字典"，虚神更新在"未现正偏十神主字典"。彻底避免了KeyError问题.
        if 忌用神归属:
            if 一级键1 in 八字信息主字典:
                八字信息主字典[一级键1]['忌用神归属'] = 忌用神归属
            elif 一级键1 in 未现正偏十神主字典:
                未现正偏十神主字典[一级键1]['忌用神归属'] = 忌用神归属
        
        # 返回忌用神归属
        return 忌用神归属

    # 调用判定用忌神函数，分别处理日支、月干、时干
    判定用忌神('日支', '日干', 格局)
    判定用忌神('月干', '日干', 格局)
    判定用忌神('时干', '日干', 格局)


    # 处理年干对月干的关系
    def 年干作用于月干():
        _, 生扶受制关系概括_年干对月干, _, _ = 元素间关系分析('年干', '月干')     # 年干对月干的关系
        月干忌用神归属 = 八字信息主字典['月干'].get('忌用神归属')        # 获取月干的归属

        if 月干忌用神归属 == '用神':
            if 生扶受制关系概括_年干对月干 == '受制关系':
                八字信息主字典['年干']['忌用神归属'] = '忌神'
            elif 生扶受制关系概括_年干对月干 == '生扶关系':
                八字信息主字典['年干']['忌用神归属'] = '用神'
        elif 月干忌用神归属 == '忌神':
            if 生扶受制关系概括_年干对月干 == '受制关系':
                八字信息主字典['年干']['忌用神归属'] = '用神'
            elif 生扶受制关系概括_年干对月干 == '生扶关系':
                八字信息主字典['年干']['忌用神归属'] = '忌神'

        # 打印 八字信息主字典 字典中各个位置的十神和忌用神归属
        print("八字信息字典：")
        for 四干支遍历列表 in ['年干', '月干', '日支', '时干']:
            信息 = 八字信息主字典.get(四干支遍历列表)
            名字 = 信息.get('名字')
            十神 = 信息.get('十神')
            忌用神归属 = 信息.get('忌用神归属')
            收集断语(f"{四干支遍历列表}: 名字 - 【{名字}】, 十神 - 【{十神}】, 忌用神归属 - 【{忌用神归属}】")



        # 创建一个列表，用于对应四干的名称
        四干列表 = ['年干', '月干', '日干', '时干']

        # 遍历四个天干十神标签，更新它们的显示内容和样式
        for i in range(4):
            天干_shen_标签 = 天干_shen_标签_列表[i]  # 获取对应的天干十神标签
            四干名称 = 四干列表[i]  # 对应的干名称

            信息 = 八字信息主字典.get(四干名称, {})
            十神 = 信息.get('十神', '')
            忌用神归属 = 信息.get('忌用神归属', '')

            # 设置忌用神归属的颜色
            if 忌用神归属 == '用神':
                color = '#da61cd'  # 用神颜色
            elif 忌用神归属 == '忌神':
                color = '#52577d'  # 忌神颜色
            else:
                color = '#C0C0C0'  # 默认颜色

            # 组合十神和忌用神归属的文本
            if 忌用神归属:
                十神文本 = f"{十神}（{忌用神归属}）"
            else:
                十神文本 = 十神

            # 更新标签的文本和颜色
            天干_shen_标签.config(text=十神文本, fg=color)
        return 八字信息主字典
    八字信息主字典 = 年干作用于月干()

    
    def 创建六亲对应字典(日干, 性别):
        关系 = 十神关系表[日干]   # 获取日干的十神关系
        if 性别 == "男":        # 根据性别判断六亲
            六亲字典 = {
                '正印': {'六亲': '母亲', '天干名字': 关系.inverse['正印']},
                '偏财': {'六亲': '父亲', '天干名字': 关系.inverse['偏财']},
                '正财': {'六亲': '妻子', '天干名字': 关系.inverse['正财']},
                '七杀': {'六亲': '儿子', '天干名字': 关系.inverse['七杀']},
                '正官': {'六亲': '女儿', '天干名字': 关系.inverse['正官']},
            }
        else:  # 性别为女
            六亲字典 = {
                '偏印(枭)': {'六亲': '母亲', '天干名字': 关系.inverse['偏印(枭)']},
                '正财': {'六亲': '父亲', '天干名字': 关系.inverse['正财']},
                '正官': {'六亲': '丈夫', '天干名字': 关系.inverse['正官']},
                '七杀': {'六亲': '男朋友', '天干名字': 关系.inverse['七杀']},
                '食神': {'六亲': '女儿', '天干名字': 关系.inverse['食神']},
                '伤官': {'六亲': '儿子', '天干名字': 关系.inverse['伤官']},
            }
        return 六亲字典
    
    日干 = 八字信息主字典['日干']['名字']
    性别 = 性别变量.get()
    六亲字典 = 创建六亲对应字典(日干, 性别)




    # 8. 列出所有未现正十神和偏十神

    # 判断月干和时干是否为正十神或偏十神
    月干是正十神 = 月干十神 in 五个正十神列表大全
    时干是正十神 = 时干十神 in 五个正十神列表大全
    月干是偏十神 = 月干十神 in 五个偏十神列表大全
    时干是偏十神 = 时干十神 in 五个偏十神列表大全

    if (月干是正十神 and 时干是偏十神) or (月干是偏十神 and 时干是正十神):                 # 如果是“一正一偏”的情况  #8.1 处理偏正定位情况：当命盘里的月柱和时柱一个是正十神一个是偏十神
        def 处理偏正定位情况():
            global 未现正偏十神主字典     # 大声宣告我要在函数内用这个全局字典了
            已现正十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个正十神列表大全]          
            未现正十神 = [shen for shen in 五个正十神列表大全 if shen not in 已现正十神 and shen != 年干十神]  
            已现偏十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个偏十神列表大全]                
            未现偏十神 = [shen for shen in 五个偏十神列表大全 if shen not in 已现偏十神 and shen != 年干十神]  
            已现年干十神 = 八字信息主字典['年干']['十神']
            未现正十神 = [shen for shen in 五个正十神列表大全 if shen not in 已现正十神 + [已现年干十神]] 

            for 天干名 in 十天干的名字列表:
                shen = 十神关系表[me][天干名]
                if shen in 未现正十神 or shen in 未现偏十神:
                    if 天干名 not in 未现正偏十神主字典:
                        未现正偏十神主字典[天干名] = {}
                    未现正偏十神主字典[天干名].update({
                        '名字': 天干名,
                        '十神': shen,
                        '五行属性': 十天干五行对照表[天干名],
                        '阴阳属性': '阳' if 天干名 in 阳属性天干列表 else '阴',
                        '窗口名字': '',
                        '窗口位置': '',
                        '窗口十神': '',
                        '忌用神归属': '',
                        '外环境': '',
                        '内环境': '',
                        '是否有镜像': ''
                    })
    

            for 天干名, 值 in 未现正偏十神主字典.items():
                for 新加的二级键 in ['窗口名字', '窗口十神', '窗口位置', '忌用神归属', '外环境', '内环境']:       # 为未现正偏十神主字典添加新的二级键
                    if 新加的二级键 not in 值:
                        值[新加的二级键] = None

            #在函数内重新生成未现正十神们及其天干名的字典
            未现正十神们及其天干名的字典 = {}     
            for 天干名 in 十天干的名字列表:
                shen = 十神关系表[me][天干名]     
                if shen in 未现正十神:
                    未现正十神们及其天干名的字典[shen] = 天干名     # 记录十神和对应的天干名

            # 9.1.1 找到未现正十神
            已现正十神索引 = [i for i in [1, 3] if 四个天干十神列表[i] in 已现正十神]               # 查找已现正十神在[月干🌕]或[时干⏰]中的索引  （之所以用索引这样的设计，是为了想让每一个已现正十神的天干名字和十神名字 一一对应起来）
            if 已现正十神索引:               # 如果存在已现正十神，更新"未现正十神"的值    #翻译：“如果 已现正十神索引 不为空则：”
                for 索引_正 in 已现正十神索引:
                    四柱列表 = ['年干', '月干', '日干', '时干']
                    已现正十神天干 = 八字信息主字典[四柱列表[索引_正]]['名字']
                    函数内已现正十神 = 四个天干十神列表[索引_正]          #翻译：已现正十神 的名字是这两个（如： '正印','正官'）
                    for 天干名, 值 in 未现正偏十神主字典.items():
                        if 值['十神'] in 未现正十神:
                            值['窗口名字'] = 已现正十神天干
                            值['窗口十神'] = 函数内已现正十神
                            值['忌用神归属'] = 判定用忌神(天干名, '日干', 格局)
                            for 位置 in ['年干', '月干', '日干', '时干']:   # 通过十神和天干名双重匹配来定位窗口位置
                                if 八字信息主字典[位置]['名字'] == 已现正十神天干 and 八字信息主字典[位置]['十神'] == 函数内已现正十神:
                                    值['窗口位置'] = 位置
                                    break

                print("未在命盘上显示的【正十神】：" + ', '.join(f"{属性字典['十神']}→{天干名}" for 天干名, 属性字典 in 未现正偏十神主字典.items() if 属性字典['十神'] in 未现正十神))

                # 🖥️🖥️🖥️【GUI界面打印】在对应的柱子上方创建一个新的框架，显示未现正十神
                未现正十神的框架 = tk.Frame(四柱们的框架, bg='#f5f5f1')
                未现正十神的框架.grid(row=0, column=索引_正, pady=(0, 6))
                # 🖥️🖥️🖥️GUI界面显示未现正十神信息
                未现正十神信息的描述标签 = tk.Label(未现正十神的框架, text="未在命盘上显示的【正十神】：",font=("Arial", 10), fg="#a4a4a4", bg='#f5f5f1')
                未现正十神信息的描述标签.pack(anchor='center')
                未现正十神十神天干显示的容器 = tk.Frame(未现正十神的框架, bg='#f5f5f1')
                未现正十神十神天干显示的容器.pack(anchor='center')
                for shen in 未现正十神:       # 遍历未现正十神
                    天干名 = 未现正十神们及其天干名的字典.get(shen, '')
                    忌用神归属 = 未现正偏十神主字典[天干名]['忌用神归属']
                    color = '#d189c9' if 忌用神归属 == '用神' else '#74789c'
                    未现正十神十神天干的框架 = tk.Frame(未现正十神十神天干显示的容器, bg='#f5f5f1')    # 创建一个小框架包含十神和天干
                    未现正十神十神天干的框架.pack(side=tk.LEFT, padx=6)
                    tk.Label(未现正十神十神天干的框架, text=f"{shen}({忌用神归属})", font=("Arial", 8), fg=color, bg='#f5f5f1').pack(pady=2, padx=2)
                    tk.Label(未现正十神十神天干的框架, text=天干名, font=("Arial", 18), fg="#7e7e7e", bg='#f5f5f1').pack(pady=3, padx=3)    # 显示对应的天干名

            else:   # 如果不存在已现正十神，提示信息
                print("这个命局里，不是“一正一偏”的情况，本命局适用于“处理非偏正定位情况”的推导方式🧐")



            # 9.1.2 找到未现偏十神
            未现偏十神们及其天干名的字典 = {}     
            for 天干名 in 十天干的名字列表:
                shen = 十神关系表[me][天干名]     
                if shen in 未现偏十神:
                    未现偏十神们及其天干名的字典[shen] = 天干名    
            已现偏十神索引 = [i for i in [1, 3] if 四个天干十神列表[i] in 已现偏十神]               # 查找已现偏十神在[月干🌕]或[时干⏰]中的索引  （之所以用索引这样的设计，是为了想让每一个已现偏十神的天干名字和十神名字 一一对应起来）

            if 已现偏十神索引:               # 如果存在已现偏十神，更新"未现偏十神"的值    #翻译：“如果 已现偏十神索引 不为空则：”
                for 索引_偏 in 已现偏十神索引:
                    四柱列表 = ['年干', '月干', '日干', '时干'] 
                    已现偏十神天干 = 八字信息主字典[四柱列表[索引_偏]]['名字']     
                    函数内已现偏十神 = 四个天干十神列表[索引_偏]          #翻译：已现偏十神 的名字是这两个（如： '偏印','七杀'）

                    for 天干名, 值 in 未现正偏十神主字典.items():
                        if 值['十神'] in 未现偏十神:
                            值['窗口名字'] = 已现偏十神天干
                            值['窗口十神'] = 函数内已现偏十神
                            值['忌用神归属'] = 判定用忌神(天干名, '日干', 格局)
                            for 位置 in ['年干', '月干', '日干', '时干']:   # 通过十神和天干名双重匹配来定位窗口位置
                                if 八字信息主字典[位置]['名字'] == 已现偏十神天干 and 八字信息主字典[位置]['十神'] == 函数内已现偏十神:
                                    值['窗口位置'] = 位置
                                    break
                
                print("未在命盘上显示的【偏十神】：" + ', '.join(f"{属性字典['十神']}→{天干名}" for 天干名, 属性字典 in 未现正偏十神主字典.items() if 属性字典['十神'] in 未现偏十神))

                # 🖥️🖥️🖥️【GUI界面打印】在对应的柱子上方创建一个新的框架，显示未现偏十神
                未现偏十神的框架 = tk.Frame(四柱们的框架, bg='#f5f5f1')
                未现偏十神的框架.grid(row=0, column=索引_偏, pady=(0, 6))
                # 🖥️🖥️🖥️GUI界面显示未现偏十神信息
                未现偏十神信息的描述标签 = tk.Label(未现偏十神的框架, text="未在命盘上显示的【偏十神】：",font=("Arial", 10), fg="#a4a4a4", bg='#f5f5f1')
                未现偏十神信息的描述标签.pack(anchor='center')
                未现偏十神十神天干显示的容器 = tk.Frame(未现偏十神的框架, bg='#f5f5f1')
                未现偏十神十神天干显示的容器.pack(anchor='center')
                for shen in 未现偏十神:       # 遍历未现偏十神
                    天干名 = 未现偏十神们及其天干名的字典.get(shen, '')
                    忌用神归属 = 未现正偏十神主字典[天干名]['忌用神归属']
                    color = '#d189c9' if 忌用神归属 == '用神' else '#74789c'
                    未现偏十神十神天干的框架 = tk.Frame(未现偏十神十神天干显示的容器, bg='#f5f5f1')    # 创建一个小框架包含十神和天干
                    未现偏十神十神天干的框架.pack(side=tk.LEFT, padx=6)
                    tk.Label(未现偏十神十神天干的框架, text=f"{shen}({忌用神归属})", font=("Arial", 8), fg=color, bg='#f5f5f1').pack(pady=2, padx=2)   # 显示十神名称
                    tk.Label(未现偏十神十神天干的框架, text=天干名, font=("Arial", 18), fg="#7e7e7e",bg='#f5f5f1').pack(pady=3, padx=3)  # 显示对应的天干名
                    
            else:   # 如果不存在已现偏十神，提示信息
                print("这个命局里，不是“一正一偏”的情况，本命局适用于“处理非偏正定位情况”的推导方式🧐")
            pass
        处理偏正定位情况()

    elif (月干是正十神 and 时干是正十神) or (月干是偏十神 and 时干是偏十神):             #双正或双偏的情况   #8.2 处理非偏正定位情况：当命盘里的月柱和时柱两个都是正十神 or 两个都是偏十神（即：两都正or两都偏）
        def 双正或双偏的情况下找未现正偏十神的办法(找正十神的窗口, 找偏十神的窗口):
                global 未现正偏十神主字典
                # 获取已现的正十神和偏十神
                已现正十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个正十神列表大全]          
                未现正十神 = [shen for shen in 五个正十神列表大全 if shen not in 已现正十神 and shen != 年干十神]  
                已现偏十神 = [shen for shen in 月干和时干的十神信息列表 if shen in 五个偏十神列表大全]                
                未现偏十神 = [shen for shen in 五个偏十神列表大全 if shen not in 已现偏十神 and shen != 年干十神] 
                已现年干十神 = 八字信息主字典['年干']['十神']
                # 寻找未现的正十神
                未现正十神 = [shen for shen in 五个正十神列表大全 if shen not in 已现正十神 + [已现年干十神]]     # 找到未现的正十神
                十神与天干的对应关系字典 = {}
                for 天干名 in 十天干的名字列表:
                    当前十神 = 十神关系表[me][天干名]  # 获取日主与当前天干的十神关系
                    if 当前十神 in 未现正十神:
                        十神与天干的对应关系字典[当前十神] = 天干名  # 记录十神和对应的天干

                if 未现正十神:         # 在未现正偏十神主字典中添加信息
                    for 未现十神 in 未现正十神:
                        天干 = 十神与天干的对应关系字典.get(未现十神, "")
                        未现正偏十神主字典[天干] = {'十神': 未现十神,'名字': 天干,'五行属性': 十天干五行对照表[天干],'阴阳属性': '阳' if 天干 in 阳属性天干列表 else '阴','忌用神归属': 判定用忌神(天干, '日干', 格局),'窗口名字': '','窗口位置': '','窗口十神': '','外环境': '','内环境': '','是否有镜像': ''}
                        已现正十神的天干 = 八字信息主字典[找正十神的窗口]['名字']            # 获取已现正十神的天干和十神
                        已现正十神的十神 = 八字信息主字典[找正十神的窗口]['十神']
                        未现正偏十神主字典[天干]['窗口名字'] = 已现正十神的天干
                        未现正偏十神主字典[天干]['窗口十神'] = 已现正十神的十神
                        未现正偏十神主字典[天干]['窗口位置'] = 找正十神的窗口
                        if ((性别 == "男" and 找正十神的窗口 == '时干') or (性别 == "女" and 找正十神的窗口 == '时干')):
                            未现正偏十神主字典[天干]['是否有镜像'] = '有镜像'

                    # 🖥️🖥️🖥️ 创建未现正十神的框架并显示于GUI界面
                    idx_找正十神 = {'年干': 0, '月干': 1, '日干': 2, '时干': 3}[找正十神的窗口]
                    未现正十神的框架 = tk.Frame(四柱们的框架, bg='#f5f5f1')
                    未现正十神的框架.grid(row=0, column=idx_找正十神, pady=(0, 6))
                    描述标签 = tk.Label(未现正十神的框架,text="未在命盘上显示的【正十神】：",font=("Arial", 10),fg="#a4a4a4",bg='#f5f5f1')
                    描述标签.pack(anchor='center')
                    容器 = tk.Frame(未现正十神的框架, bg='#f5f5f1')
                    容器.pack(anchor='center')
                    for 未现十神 in 未现正十神:
                        天干 = 十神与天干的对应关系字典.get(未现十神, '')
                        忌用神归属 = 未现正偏十神主字典[天干]['忌用神归属']
                        color = '#d189c9' if 忌用神归属 == '用神' else '#74789c'
                        框架 = tk.Frame(容器, bg='#f5f5f1')
                        框架.pack(side=tk.LEFT, padx=6)
                        tk.Label(框架,text=f"{未现十神}({忌用神归属})",font=("Arial", 8),fg=color, bg='#f5f5f1').pack(pady=2, padx=2)
                        tk.Label(框架,text=天干,font=("Arial", 18),fg="#7e7e7e",bg='#f5f5f1').pack(pady=3, padx=3)

                # 寻找未现的偏十神
                未现偏十神 = [未现十神 for 未现十神 in 五个偏十神列表大全 if 未现十神 not in 已现偏十神 + [已现年干十神]]     # 找到未现的偏十神
                偏十神与天干的对应关系字典 = {}
                for 天干名 in 十天干的名字列表:
                    当前十神 = 十神关系表[me][天干名]
                    if 当前十神 in 未现偏十神:
                        偏十神与天干的对应关系字典[当前十神] = 天干名

                if 未现偏十神:    # 在未现正偏十神主字典中添加信息
                    for 未现十神 in 未现偏十神:
                        天干 = 偏十神与天干的对应关系字典.get(未现十神, "")
                        未现正偏十神主字典[天干] = {'十神': 未现十神,'名字': 天干,'五行属性': 十天干五行对照表[天干],'忌用神归属': 判定用忌神(天干, '日干', 格局),'窗口名字': '','窗口位置': '','窗口十神': '','外环境': '','内环境': '','是否有镜像': ''}
                        已现偏十神的天干 = 八字信息主字典[找偏十神的窗口]['名字']             # 获取已现偏十神的天干和十神
                        已现偏十神的十神 = 八字信息主字典[找偏十神的窗口]['十神']
                        未现正偏十神主字典[天干]['窗口名字'] = 已现偏十神的天干     # 更新未现偏十神的窗口信息
                        未现正偏十神主字典[天干]['窗口十神'] = 已现偏十神的十神
                        未现正偏十神主字典[天干]['窗口位置'] = 找偏十神的窗口
                        if ((性别 == "男" and 找偏十神的窗口 == '时干') or (性别 == "女" and 找偏十神的窗口 == '月干')):
                            未现正偏十神主字典[天干]['是否有镜像'] = '有镜像'

                    # 🖥️🖥️🖥️ 创建未现偏十神的框架并显示于GUI界面
                    idx_找偏十神 = {'年干': 0, '月干': 1, '日干': 2, '时干': 3}[找偏十神的窗口]
                    未现偏十神的框架 = tk.Frame(四柱们的框架, bg='#f5f5f1')
                    未现偏十神的框架.grid(row=0, column=idx_找偏十神, pady=(0, 6))
                    描述标签 = tk.Label(未现偏十神的框架,text="未在命盘上显示的【偏十神】（镜像十神）：",font=("Arial", 10),fg="#a4a4a4",bg='#f5f5f1')
                    描述标签.pack(anchor='center')
                    容器 = tk.Frame(未现偏十神的框架, bg='#f5f5f1')
                    容器.pack(anchor='center')
                    for 未现十神 in 未现偏十神:
                        天干 = 偏十神与天干的对应关系字典.get(未现十神, '')
                        忌用神归属 = 未现正偏十神主字典[天干]['忌用神归属']
                        color = '#d189c9' if 忌用神归属 == '用神' else '#74789c'
                        框架 = tk.Frame(容器, bg='#f5f5f1')
                        框架.pack(side=tk.LEFT, padx=6)
                        tk.Label(框架,text=f"{未现十神}({忌用神归属})",font=("Arial", 8), fg=color, bg='#f5f5f1').pack(pady=2, padx=2)
                        tk.Label(框架,text=天干,font=("Arial", 18),fg="#7e7e7e",bg='#f5f5f1').pack(pady=3, padx=3)

                return 未现正偏十神主字典
        def 处理非偏正定位情况():   
            if 性别 == "男":
                双正或双偏的情况下找未现正偏十神的办法('月干', '时干')      # 男：月干🌕为未出现正十神的窗口，时干⏰为未出现偏十神的窗口
            elif 性别 == "女":
                双正或双偏的情况下找未现正偏十神的办法('时干', '月干')      # 女：月干🌕为未出现偏十神的窗口，时干⏰为未出现正十神的窗口
            else:
                print("这个命局，不是双正或双偏的情况，本命局适用于其他推导方式🧐")
        处理非偏正定位情况()  # 调用处理非偏正定位情况的函数







    #9. 天干十神的外环境吉凶和内环境定吉凶（加上大运流年关系）
    from ganzhi import 十天干五行对照表, 十二地支五行对照表, 晦脆冲特殊关系字典, 五行作用关系字典
    生扶列表 = ['同', '生']
    受制列表 = ['克', '泄', '耗', '刑', '冲', '晦', '脆', '零']



    def 判断两者是否生扶受制(作用者, 被作用者):
        # 判断两个元素之间是否为生扶关系
        _, 生扶受制关系概括, _, _ = 元素间关系分析(作用者, 被作用者)
        return 生扶受制关系概括

    # 9.1 分析天干十神的外环境吉凶
    def 分析天干十神的外环境吉凶():
        外环境结论 = {}
        # 分析时干⏰ 和 月干🌕 的外环境吉凶
        for 位置, 索引 in [('时干', 3), ('月干', 1)]:
            十神 = 四个天干十神列表[索引]
            忌用神归属 = 八字信息主字典[位置].get('忌用神归属')
            天干名 = 八字信息主字典[位置]['名字']

            if 忌用神归属 == '用神':
                八字信息主字典[位置]['外环境'] = '吉'
            elif 忌用神归属 == '忌神':
                八字信息主字典[位置]['外环境'] = '凶'
            
            作用链路过程 = f"🔍「已现十神の外环境」推导过程：∵【{位置}】【{天干名}】【{十神}】为【{忌用神归属}】，∴ 【{位置}】【{天干名}】【{十神}】【{忌用神归属}】外环境为【{八字信息主字典[位置]['外环境']}】"
            收集断语(作用链路过程)
            print(作用链路过程)

            # 在循环内部就保存结论
            外环境结论[位置] = {'外环境': 八字信息主字典[位置]['外环境'],
                '作用路径': f"∵【{位置}】【{天干名}】【{十神}】为【{忌用神归属}】，∴ 【{位置}】【{天干名}】【{十神}】【{忌用神归属}】外环境为【{八字信息主字典[位置]['外环境']}】"}


        # 分析年干🧨 的外环境吉凶
        月干忌用神归属 = 八字信息主字典['月干'].get('忌用神归属')
        # 判断月干对年干🧨是否生扶
        年干对月干的生扶受制关系 = 判断两者是否生扶受制('年干', '月干')
        if 月干忌用神归属: 
            if 月干忌用神归属 == '用神':
                if 年干对月干的生扶受制关系 == '生扶关系':
                    八字信息主字典['年干']['忌用神归属'] = '用神'
                    八字信息主字典['年干']['外环境'] = '吉'
                elif 年干对月干的生扶受制关系 == '受制关系'or 年干对月干的生扶受制关系 == '不旺不弱关系':
                    八字信息主字典['年干']['忌用神归属'] = '忌神'
                    八字信息主字典['年干']['外环境'] = '凶'
                else:
                    八字信息主字典['年干']['外环境'] = '不旺不弱，既不吉也不凶'
            elif 月干忌用神归属 == '忌神':
                if 年干对月干的生扶受制关系 == '生扶关系':
                    八字信息主字典['年干']['忌用神归属'] = '忌神'
                    八字信息主字典['年干']['外环境'] = '凶'
                elif 年干对月干的生扶受制关系 == '受制关系'or 年干对月干的生扶受制关系 == '不旺不弱关系':
                    八字信息主字典['年干']['忌用神归属'] = '用神'
                    八字信息主字典['年干']['外环境'] = '吉'
                else:
                    八字信息主字典['年干']['外环境'] = '不旺不弱，既不吉也不凶'
            else:
                八字信息主字典['年干']['外环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'
    
        年干忌用神归属 = 八字信息主字典['年干'].get('忌用神归属')
        月干忌用神归属 = 八字信息主字典['月干'].get('忌用神归属')
        月干名 = 八字信息主字典['月干']['名字']
        年干名 = 八字信息主字典['年干']['名字']
        月干十神 = 四个天干十神列表[1]

        作用链路过程 = f"🔍「已现十神の外环境」推导过程：∵【年干】【{年干对月干的生扶受制关系}】【月干】【{月干十神}】， ∵【{月干名}】【{月干十神}】为【{年干忌用神归属}】。 ∴ 【年干】【{年干名}】【{十神}】外环境为【{八字信息主字典['年干']['外环境']}】"
        收集断语(作用链路过程)
        print(作用链路过程)
        

        外环境结论['年干'] = {
            '外环境': 八字信息主字典['年干']['外环境'],
            '作用路径': f"∵【年干】【{年干对月干的生扶受制关系}】【月干】【{月干十神}】， ∵【{月干名}】【{月干十神}】为【{年干忌用神归属}】。 ∴ 【年干】【{年干名}】【{十神}】外环境为【{八字信息主字典['年干']['外环境']}】"}
    
        return 外环境结论
    分析天干十神的外环境吉凶()

    # 9.2 分析天干十神的内环境吉凶
    def 分析天干十神的内环境吉凶():
        for idx, 干名, 十神 in zip([3, 1, 0], ['时干', '月干', '年干'], [时干十神, 月干十神, 年干十神]):
            天干名字 = 本命盘四个天干名字列表[idx]
            地支名字 = 本命盘四个地支名字列表[idx]

            # 判断是否有根
            if (地支名字, 天干名字) in 有根字典 and 有根字典[(地支名字, 天干名字)] == '有根':
                有根 = True
            else:
                天干五行 = 十天干五行对照表.get(天干名字)
                地支五行 = 十二地支五行对照表.get(地支名字)
                if 天干五行 and 地支五行:
                    if (地支名字, 天干名字) in 晦脆冲特殊关系字典:
                        两者关系 = 晦脆冲特殊关系字典[(地支名字, 天干名字)]
                    else:
                        两者关系 = 五行作用关系字典.get((天干五行, 地支五行), '')
                    有根 = 两者关系 in 生扶列表
                else:
                    有根 = False

            if 有根:
                八字信息主字典[干名]['是否有根'] = '有根'

            # 根据有根与忌用神归属，确定内环境吉凶
            忌用神归属 = 八字信息主字典[干名].get('忌用神归属')
            if 忌用神归属 == '用神':
                if 有根:
                    八字信息主字典[干名]['内环境'] = '吉'
                else:
                    八字信息主字典[干名]['内环境'] = '凶'
            elif 忌用神归属 == '忌神':
                if 有根:
                    八字信息主字典[干名]['内环境'] = '凶'
                else:
                    八字信息主字典[干名]['内环境'] = '吉'
            else:
                八字信息主字典[干名]['内环境'] = '既不吉也不凶'

            作用链路过程 = f"🔍「已现十神の内环境」推导过程： ∵【{干名}】【{八字信息主字典[干名]['名字']}】【{'有根' if 八字信息主字典[干名].get('是否有根') == '有根' else '无根'}】且为【{忌用神归属}】，∴【{干名}】【{十神}】【{忌用神归属}】的内环境为【{八字信息主字典[干名]['内环境']}】"
            收集断语(作用链路过程)
            print(作用链路过程)

        内环境结论 = {'时干': {
            '内环境': 八字信息主字典['时干']['内环境'],
            '作用路径': f"【时干】【{八字信息主字典['时干']['名字']}】【{'有根' if 八字信息主字典['时干'].get('是否有根') == '有根' else '无根'}】且为【{八字信息主字典['时干'].get('忌用神归属')}】"},
        '月干': {
            '内环境': 八字信息主字典['月干']['内环境'],
            '作用路径': f"【月干】【{八字信息主字典['月干']['名字']}】【{'有根' if 八字信息主字典['月干'].get('是否有根') == '有根' else '无根'}】且为【{八字信息主字典['月干'].get('忌用神归属')}】"},
        '年干': {
            '内环境': 八字信息主字典['年干']['内环境'],
            '作用路径': f"【年干】【{八字信息主字典['年干']['名字']}】【{'有根' if 八字信息主字典['年干'].get('是否有根') == '有根' else '无根'}】且为【{八字信息主字典['年干'].get('忌用神归属')}】"}}
        
        for 干名 in ['时干', '月干', '年干']:
            八字信息主字典[干名].update({'内环境': 内环境结论[干名]['内环境']})   # 更新到八字信息主字典中
        return 内环境结论
    分析天干十神的内环境吉凶()

    #9.3 分析天干十神的左环境吉凶
    def 分析天干十神的左环境吉凶():
        # 分析时干 🕰️ 的左环境吉凶
        时干忌用神归属 = 八字信息主字典['时干'].get('忌用神归属')
        生扶受制关系 = 判断两者是否生扶受制('日干', '时干')
        if 时干忌用神归属 == '用神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['时干']['左环境'] = '吉'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['时干']['左环境'] = '凶'
            else:  # 不旺不弱关系
                八字信息主字典['时干']['左环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'
        elif 时干忌用神归属 == '忌神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['时干']['左环境'] = '凶'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['时干']['左环境'] = '吉'
            else:  # 不旺不弱关系
                八字信息主字典['时干']['左环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'


        # 分析月干🌕 的左环境吉凶
        月干忌用神归属 = 八字信息主字典['月干'].get('忌用神归属')
        生扶受制关系 = 判断两者是否生扶受制('年干', '月干')
        if 月干忌用神归属 == '用神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['月干']['左环境'] = '吉'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['月干']['左环境'] = '凶'
            else:  # 不旺不弱关系
                八字信息主字典['月干']['左环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'
        elif 月干忌用神归属 == '忌神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['月干']['左环境'] = '凶'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['月干']['左环境'] = '吉'
            else:  # 不旺不弱关系
                八字信息主字典['月干']['左环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'


        # 分析年干 🧨 的左环境吉凶
        年干忌用神归属 = 八字信息主字典['年干'].get('忌用神归属')
        if 年干忌用神归属:
            月干生扶年干 = 判断两者是否生扶受制('月干', '年干') == '生扶关系'
            日干生扶月干 = 判断两者是否生扶受制('日干', '月干') == '生扶关系'
            月干制年干 = 判断两者是否生扶受制('月干', '年干') in ['受制关系', '不旺不弱关系']
            日干制月干 = 判断两者是否生扶受制('日干', '月干') in ['受制关系', '不旺不弱关系']

            if 年干忌用神归属 == '用神':
                if 月干生扶年干 and 日干生扶月干:
                    八字信息主字典['年干']['左环境'] = '吉'
                elif (月干生扶年干 and 日干制月干) or (月干制年干 and 日干生扶月干):
                    八字信息主字典['年干']['左环境'] = '凶'
                else:
                    八字信息主字典['年干']['左环境'] = '吉'
            elif 年干忌用神归属 == '忌神':
                if 月干生扶年干 and 日干生扶月干:
                    八字信息主字典['年干']['左环境'] = '凶'
                elif (月干生扶年干 and 日干制月干) or (月干制年干 and 日干生扶月干):
                    八字信息主字典['年干']['左环境'] = '吉'
                else:
                    八字信息主字典['年干']['左环境'] = '凶'
        else:
            八字信息主字典['年干']['左环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'

        # 打印结果
        global 性别变量
        环境类型字典 = {}
        for 天干 in ['时干', '月干', '年干']:
            十神 = 八字信息主字典.get(天干).get('十神')
            忌用神归属 = 八字信息主字典.get(天干).get('忌用神归属')
            左环境 = 八字信息主字典.get(天干).get('左环境')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别 == '男' and 是正十神) or (性别 == '女' and not 是正十神):
                环境类型字典[天干] = "社会环境"
            else:
                环境类型字典[天干] = "内心环境"
            
            作用链路过程 =f"🔍{天干}: {十神} - {忌用神归属} - 左环境：{左环境} - {环境类型字典[天干]}:{左环境}"
            收集断语(作用链路过程)
            print(作用链路过程)
        
            # 添加推导过程的打印
            时干名字 = 八字信息主字典['时干']['名字']
            时干十神 = 八字信息主字典['时干']['十神']
            月干名字 = 八字信息主字典['月干']['名字']
            月干十神 = 八字信息主字典['月干']['十神']
            年干名字 = 八字信息主字典['年干']['名字']
            年干十神 = 八字信息主字典['年干']['十神']

            日时关系 = "生" if 判断两者是否生扶受制('日干', '时干') == '生扶关系' else "制"
            年月关系 = "生" if 判断两者是否生扶受制('年干', '月干') == '生扶关系' else "制"
            日干月干关系 = "生" if 日干生扶月干 else "制"
            月干年干关系 = "生" if 月干生扶年干 else "制"
            if 天干 == '时干':
                作用链路过程 =f"🔍「已现十神の左环境」推导过程：【日干】【{八字信息主字典['日干']['名字']}】【{日时关系}】【时干】【{时干名字}】【{时干十神}】，∴【{时干名字}】【{时干十神}】的左环境（{环境类型字典[天干]}）【{八字信息主字典['时干']['左环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            elif 天干 == '月干':
                作用链路过程 =f"🔍「已现十神の左环境」推导过程：【年干】【{年干名字}】【{年干十神}】【{年月关系}】【月干】【{月干名字}】【{月干十神}】，∴【{月干名字}】【{月干十神}】的左环境（{环境类型字典[天干]}）【{八字信息主字典['月干']['左环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            elif 天干 == '年干':
                作用链路过程 =f"🔍「已现十神の左环境」推导过程：【日干】【{八字信息主字典['日干']['名字']}】【{日干月干关系}】【月干】【{月干名字}】【{月干十神}】，【月干】【{月干名字}】【{月干十神}】【{月干年干关系}】【年干】【{年干名字}】【{年干十神}】，∴【{年干名字}】【{年干十神}】的左环境（{环境类型字典[天干]}）【{八字信息主字典['年干']['左环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)


        # 在函数末尾添加“左环境结论”字典
        左环境结论 = {
            '时干': {
                '作用路径': f"【日干】【{八字信息主字典['日干']['名字']}】【{日时关系}】【时干】【{时干名字}】【{时干十神}】",
                '环境类型': 环境类型字典['时干'],
                '环境结果': 八字信息主字典['时干']['左环境']},
            '月干': {
                '作用路径': f"【年干】【{年干名字}】【{年干十神}】【{年月关系}】【月干】【{月干名字}】【{月干十神}】",
                '环境类型': 环境类型字典['月干'],
                '环境结果': 八字信息主字典['月干']['左环境']},
            '年干': {
                '作用路径': f"【日干】【{八字信息主字典['日干']['名字']}】【{日干月干关系}】【月干】【{月干名字}】【{月干十神}】，【月干】【{月干名字}】【{月干十神}】【{月干年干关系}】【年干】【{年干名字}】【{年干十神}】",
                '环境类型': 环境类型字典['年干'],
                '环境结果': 八字信息主字典['年干']['左环境']}}
        return 左环境结论
    分析天干十神的左环境吉凶()

    #9.4 分析天干十神的右环境吉凶
    def 分析天干十神的右环境吉凶():
        # 分析年干🧨 的右环境吉凶
        年干忌用神归属 = 八字信息主字典['年干'].get('忌用神归属')
        生扶受制关系 = 判断两者是否生扶受制('月干', '年干')
        if 年干忌用神归属 == '用神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['年干']['右环境'] = '吉'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['年干']['右环境'] = '凶'
            else:
                八字信息主字典['年干']['右环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'
        elif 年干忌用神归属 == '忌神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['年干']['右环境'] = '凶'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['年干']['右环境'] = '吉'
            else: 
                八字信息主字典['年干']['右环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'

        # 分析月干🌕 的右环境吉凶
        月干忌用神归属 = 八字信息主字典['月干'].get('忌用神归属')
        生扶受制关系 = 判断两者是否生扶受制('日干', '月干')
        if 月干忌用神归属 == '用神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['月干']['右环境'] = '吉'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['月干']['右环境'] = '凶'
            else:  # 不旺不弱关系
                八字信息主字典['月干']['右环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'
        elif 月干忌用神归属 == '忌神':
            if 生扶受制关系 == '生扶关系':
                八字信息主字典['月干']['右环境'] = '凶'
            elif 生扶受制关系 == '受制关系'or 生扶受制关系 == '不旺不弱关系':
                八字信息主字典['月干']['右环境'] = '吉'
            else:  # 不旺不弱关系
                八字信息主字典['月干']['右环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'

        # 分析时干⏰ 的右环境吉凶
        时干忌用神归属 = 八字信息主字典['时干'].get('忌用神归属')
        if 时干忌用神归属:
            月干生扶日干 = 判断两者是否生扶受制('月干', '年干') == '生扶关系'
            日干生扶时干 = 判断两者是否生扶受制('日干', '月干') == '生扶关系'
            日干制时干 = 判断两者是否生扶受制('月干', '年干') in ['受制关系', '不旺不弱关系']   #是不是等于'受制关系'or'不旺不弱关系'
            月干制日干 = 判断两者是否生扶受制('日干', '月干') in ['受制关系', '不旺不弱关系']

            if 时干忌用神归属 == '用神':
                if 日干生扶时干 and 月干生扶日干:
                    八字信息主字典['时干']['右环境'] = '吉'
                elif (日干生扶时干 and 月干制日干) or (日干制时干 and 月干生扶日干):
                    八字信息主字典['时干']['右环境'] = '凶'
                else:
                    八字信息主字典['时干']['右环境'] = '吉'
            elif 时干忌用神归属 == '忌神':
                if 日干生扶时干 and 月干生扶日干:
                    八字信息主字典['时干']['右环境'] = '凶'
                elif (日干生扶时干 and 月干制日干) or (日干制时干 and 月干生扶日干):
                    八字信息主字典['时干']['右环境'] = '吉'
                else:
                    八字信息主字典['时干']['右环境'] = '凶'
        else:
            八字信息主字典['时干']['右环境'] = '外环境被作用关系不旺不弱关系，既不吉也不凶'

        # 打印结果
        global 性别变量
        环境类型字典 = {}
        for 天干 in ['年干', '月干', '时干']:
            十神 = 八字信息主字典.get(天干).get('十神')
            忌用神归属 = 八字信息主字典.get(天干).get('忌用神归属')
            右环境 = 八字信息主字典.get(天干).get('右环境')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型字典[天干] = "内心环境"
            else:
                环境类型字典[天干] = "社会环境"
            作用链路过程 =f"{天干}: {十神} - {忌用神归属} - 右环境：{右环境} - {环境类型字典[天干]}:{右环境}"
            收集断语(作用链路过程)
            print(作用链路过程)
            
            # 添加推导过程的打印
            时干名字 = 八字信息主字典['时干']['名字']
            时干十神 = 八字信息主字典['时干']['十神']
            月干名字 = 八字信息主字典['月干']['名字']
            月干十神 = 八字信息主字典['月干']['十神']
            年干名字 = 八字信息主字典['年干']['名字']
            年干十神 = 八字信息主字典['年干']['十神']

            月年关系 = "生" if 判断两者是否生扶受制('月干', '年干') == '生扶关系' else "制"
            日月关系 = "生" if 判断两者是否生扶受制('日干', '月干') == '生扶关系' else "制"
            月干日干关系 = "生" if 月干生扶日干 else "制"
            日干时干关系 = "生" if 日干生扶时干 else "制"

            if 天干 == '年干':
                作用链路过程 =f"🔍「已现十神の右环境」推导过程：【月干】【{月干名字}】【{月干十神}】【{月年关系}】【年干】【{年干名字}】【{年干十神}】，∴【{年干名字}】【{年干十神}】的右环境（{环境类型字典[天干]}）【{八字信息主字典['年干']['右环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            elif 天干 == '月干':
                作用链路过程 =f"🔍「已现十神の右环境」推导过程：【日干】【{八字信息主字典['日干']['名字']}】【{日月关系}】【月干】【{月干名字}】【{月干十神}】，∴【{月干名字}】【{月干十神}】的右环境（{环境类型字典[天干]}）【{八字信息主字典['月干']['右环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            elif 天干 == '时干':
                作用链路过程 =f"🔍「已现十神の右环境」推导过程：【月干】【{月干名字}】【{月干十神}】【{月干日干关系}】【日干】【{八字信息主字典['日干']['名字']}】，【日干】【{八字信息主字典['日干']['名字']}】【{日干时干关系}】【时干】【{时干名字}】【{时干十神}】，∴【{时干名字}】【{时干十神}】的右环境（{环境类型字典[天干]}）【{八字信息主字典['时干']['右环境']}】"
                收集断语(作用链路过程)
                print(作用链路过程)
        # 在函数末尾添加结论字典
        右环境结论 = {
            '年干': {
                '作用路径': f"【月干】【{月干名字}】【{月干十神}】【{月年关系}】【年干】【{年干名字}】【{年干十神}】",
                '环境类型': 环境类型字典['年干'],
                '环境结果': 八字信息主字典['年干']['右环境']},
            '月干': {
                '作用路径': f"【日干】【{八字信息主字典['日干']['名字']}】【{日月关系}】【月干】【{月干名字}】【{月干十神}】",
                '环境类型': 环境类型字典['月干'],
                '环境结果': 八字信息主字典['月干']['右环境']},
            '时干': {
                '作用路径': f"【月干】【{月干名字}】【{月干十神}】【{月干日干关系}】【日干】【{八字信息主字典['日干']['名字']}】，【日干】【{八字信息主字典['日干']['名字']}】【{日干时干关系}】【时干】【{时干名字}】【{时干十神}】",
                '环境类型': 环境类型字典['时干'],
                '环境结果': 八字信息主字典['时干']['右环境']}}
        return 右环境结论
    分析天干十神的右环境吉凶()

    #9.5 分析天干十神的内环境的左环境吉凶
    def 分析天干十神的内环境的左环境吉凶():
        # 分析时干⏰月干🌕的内环境左环境吉凶
        for 天干, 地支索引, 左侧地支索引 in [('时干', 3, 2), ('月干', 1, 0)]:     #第一次赋值:天干 = '时干'、地支索引 = 3、左侧地支索引 = 2
            内环境吉凶 = 八字信息主字典[天干]['内环境']        # 获取该天干的内环境吉凶状态
            同柱地支 = ['年支', '月支', '日支', '时支'][地支索引]         # 获取同柱的地支和左侧的地支
            左侧地支 = ['年支', '月支', '日支', '时支'][左侧地支索引]      # 判断左侧地支对同柱地支的生扶受制关系
            生扶受制关系 = 判断两者是否生扶受制(左侧地支, 同柱地支)
            if 内环境吉凶 == '吉':                             # 根据内环境吉凶和生扶受制关系，确定左环境的吉凶
                if 生扶受制关系 == '生扶关系':
                    八字信息主字典[天干]['内环境左环境'] = '吉'
                else:
                    八字信息主字典[天干]['内环境左环境'] = '凶'
            elif 内环境吉凶 == '凶':
                if 生扶受制关系 == '生扶关系':
                    八字信息主字典[天干]['内环境左环境'] = '凶'
                else:
                    八字信息主字典[天干]['内环境左环境'] = '吉'
            else:
                八字信息主字典[天干]['内环境左环境'] = '既不吉也不凶，肯定是代码哪里出错了'

        # 分析年干🧨的内环境左环境吉凶（特殊情况） （年干没有左侧地支，需要通过月支和日支间接判断）
        年干内环境吉凶 = 八字信息主字典['年干']['内环境']
        月支与年地支作用关系 = 判断两者是否生扶受制('月支', '年支')    # 判断月支对年支的生扶受制关系
        日支与月地支作用关系 = 判断两者是否生扶受制('日支', '月支')    # 判断日支对月支的生扶受制关系
        # 根据内环境吉凶和生扶受制关系，确定年干左环境的吉凶
        if 年干内环境吉凶 == '吉':
            if 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                if 日支与月地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['年干']['内环境左环境'] = '吉'
                elif 日支与月地支作用关系 == '生扶关系':
                    八字信息主字典['年干']['内环境左环境'] = '凶'
            elif 月支与年地支作用关系 == '生扶关系':
                if 日支与月地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['年干']['内环境左环境'] = '凶'
                elif 日支与月地支作用关系 == '生扶关系':
                    八字信息主字典['年干']['内环境左环境'] = '吉'
        elif 年干内环境吉凶 == '凶':
            if 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                if 日支与月地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['年干']['内环境左环境'] = '凶'
                elif 日支与月地支作用关系 == '生扶关系':
                    八字信息主字典['年干']['内环境左环境'] = '吉'
            elif 月支与年地支作用关系 == '生扶关系':
                if 日支与月地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['年干']['内环境左环境'] = '吉'
                elif 日支与月地支作用关系 == '生扶关系':
                    八字信息主字典['年干']['内环境左环境'] = '凶'
        else:
            八字信息主字典['年干']['内环境左环境'] = '既不吉也不凶，肯定是代码哪里出错了'

        # 打印结果
        global 性别变量
        环境类型字典 = {}
        for 天干 in ['时干', '月干', '年干']:
            内环境左环境 = 八字信息主字典.get('年干').get('内环境左环境')
            十神 = 八字信息主字典.get(天干).get('十神')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型字典[天干] = "社会环境的内环境"
            else:
                环境类型字典[天干] = "内心环境的内环境"
            作用链路过程 = f"{天干}的内环境的左环境:{内环境左环境} - {环境类型字典[天干]}:{内环境左环境}"
            收集断语(作用链路过程)
            print(作用链路过程)

            #添加推导过程的打印
            天干名字 = 八字信息主字典[天干]['名字']
            内环境 = 八字信息主字典[天干]['内环境']
            
            if 天干 in ['时干', '月干']:
                左侧地支索引 = 2 if 天干 == '时干' else 0
                左侧地支 = ['年支', '月支', '日支', '时支'][左侧地支索引]
                同柱地支 = ['年支', '月支', '日支', '时支'][['年干', '月干', '日干', '时干'].index(天干)]
                左侧地支名字 = 本命盘四个地支名字列表[左侧地支索引]
                同柱地支名字 = 本命盘四个地支名字列表[['年干', '月干', '日干', '时干'].index(天干)]
                生扶受制关系 = 判断两者是否生扶受制(左侧地支, 同柱地支)
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                
                作用链路过程 = f"🔍「已现十神の内环境的左环境」推导过程：∵【{左侧地支}】【{左侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{天干}】【{天干名字}】【{十神}】的内环境【{内环境}】，∴【{天干}】【{天干名字}】【{十神}】的内环境左环境（{环境类型字典[天干]}）【{内环境左环境}】"
                收集断语(作用链路过程)
                print(作用链路过程)

            elif 天干 == '年干':
                月支名字 = 本命盘四个地支名字列表[1]
                日支名字 = 本命盘四个地支名字列表[2]
                年支名字 = 本命盘四个地支名字列表[0]
                月支与年地支作用关系 = "生" if 判断两者是否生扶受制('月支', '年支') == '生扶关系' else "制"
                日支与月地支作用关系 = "生" if 判断两者是否生扶受制('日支', '月支') == '生扶关系' else "制"
                
                作用链路过程 = f"🔍「已现十神の内环境的左环境」推导过程：∵【日支】【{日支名字}】【{日支与月地支作用关系}】【月支】【{月支名字}】，【月支】【{月支名字}】【{月支与年地支作用关系}】【年支】【{年支名字}】，∴【年干】【{天干名字}】【{十神}】的内环境【{内环境}】，∴【年干】【{天干名字}】【{十神}】的内环境左环境（{环境类型字典[天干]}）【{内环境左环境}】"
                收集断语(作用链路过程)
                print(作用链路过程)

        # 在函数末尾，添加结论字典
        内环境左环境结论 = {
            '时干': {
                '作用路径': f"∵【{左侧地支}】【{左侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，∴【时干】【{八字信息主字典['时干']['名字']}】【{八字信息主字典['时干']['十神']}】的内环境【{八字信息主字典['时干']['内环境']}】",
                '环境类型': 环境类型字典['时干'],
                '环境结果': 八字信息主字典['时干']['内环境左环境']},
            '月干': {
                '作用路径': f"∵【{左侧地支}】【{左侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，∴【月干】【{八字信息主字典['月干']['名字']}】【{八字信息主字典['月干']['十神']}】的内环境【{八字信息主字典['月干']['内环境']}】",
                '环境类型': 环境类型字典['月干'],
                '环境结果': 八字信息主字典['月干']['内环境左环境']},
            '年干': {
                '作用路径': f"∵【日支】【{日支名字}】【{日支与月地支作用关系}】【月支】【{月支名字}】，【月支】【{月支名字}】【{月支与年地支作用关系}】【年支】【{年支名字}】，∴【年干】【{八字信息主字典['年干']['名字']}】【{八字信息主字典['年干']['十神']}】的内环境【{八字信息主字典['年干']['内环境']}】",
                '环境类型': 环境类型字典['年干'],
                '环境结果': 八字信息主字典['年干']['内环境左环境']}}
        
        return 内环境左环境结论 
    分析天干十神的内环境的左环境吉凶()

    #9.6 分析天干十神的内环境的右环境吉凶
    def 分析天干十神的内环境右环境吉凶():
        # 分析月干和年干的内环境右环境吉凶
        for 天干, 地支索引, 右侧地支索引 in [('月干', 1, 2), ('年干', 0, 1)]:
            内环境吉凶 = 八字信息主字典[天干]['内环境']
            同柱地支 = ['年支', '月支', '日支', '时支'][地支索引] 
            右侧地支 = ['年支', '月支', '日支', '时支'][右侧地支索引] 
            生扶受制关系 = 判断两者是否生扶受制(右侧地支, 同柱地支)
            # 根据内环境吉凶和生扶受制关系，确定右环境的吉凶
            if 内环境吉凶 == '吉':
                if 生扶受制关系 == '生扶关系':
                    八字信息主字典[天干]['内环境右环境'] = '吉'
                else:
                    八字信息主字典[天干]['内环境右环境'] = '凶'
            elif 内环境吉凶 == '凶':
                if 生扶受制关系 == '生扶关系':
                    八字信息主字典[天干]['内环境右环境'] = '凶'
                else:
                    八字信息主字典[天干]['内环境右环境'] = '吉'
            else:
                八字信息主字典[天干]['内环境右环境'] = '既不吉也不凶，肯定是代码哪里出错了'

        # 分析时干的内环境右环境吉凶（特殊情况）
        时干内环境吉凶 = 八字信息主字典['时干']['内环境']
        日支与时地支作用关系 = 判断两者是否生扶受制('日支', '时支')    # 判断日支对时支的生扶受制关系
        月支与日地支作用关系 = 判断两者是否生扶受制('月支', '日支')    # 判断月支对日支的生扶受制关系
        if 时干内环境吉凶 == '吉':                         # 根据内环境吉凶和生扶受制关系，确定时干右环境的吉凶
            if 日支与时地支作用关系 in ['受制关系', '不旺不弱关系']:
                if 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['时干']['内环境右环境'] = '吉'
                elif 月支与日地支作用关系 == '生扶关系':
                    八字信息主字典['时干']['内环境右环境'] = '凶'
            elif 日支与时地支作用关系 == '生扶关系':
                if 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['时干']['内环境右环境'] = '凶'
                elif 月支与日地支作用关系 == '生扶关系':
                    八字信息主字典['时干']['内环境右环境'] = '吉'
        elif 时干内环境吉凶 == '凶':
            if 日支与时地支作用关系 in ['受制关系', '不旺不弱关系']:
                if 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['时干']['内环境右环境'] = '凶'
                elif 月支与日地支作用关系 == '生扶关系':
                    八字信息主字典['时干']['内环境右环境'] = '吉'
            elif 日支与时地支作用关系 == '生扶关系':
                if 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                    八字信息主字典['时干']['内环境右环境'] = '吉'
                elif 月支与日地支作用关系 == '生扶关系':
                    八字信息主字典['时干']['内环境右环境'] = '凶'
        else:
            八字信息主字典['时干']['内环境右环境'] = '既不吉也不凶，肯定是代码哪里出错了'
        
        # 打印结果
        global 性别变量
        环境类型字典 = {}
        临时变量字典 = {'年干': {}, '月干': {}, '时干': {}}
        for 天干 in ['年干', '月干', '时干']:
            内环境右环境 = 八字信息主字典.get(天干).get('内环境右环境')
            十神 = 八字信息主字典.get(天干).get('十神')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型字典[天干] = "内心环境的内环境"
            else:
                环境类型字典[天干] = "社会环境的内环境"
            作用链路过程= f"{天干}的内环境的右环境：{内环境右环境} - {环境类型字典[天干]}:{内环境右环境}"
            收集断语(作用链路过程)
            print(作用链路过程)

            # 添加推导过程的打印
            天干名字 = 八字信息主字典[天干]['名字']
            内环境 = 八字信息主字典[天干]['内环境']

            if 天干 in ['年干', '月干']:
                右侧地支索引 = ['年干', '月干', '日干', '时干'].index(天干) + 1
                右侧地支 = ['年支', '月支', '日支', '时支'][右侧地支索引]
                同柱地支 = ['年支', '月支', '日支', '时支'][['年干', '月干', '日干', '时干'].index(天干)]
                右侧地支名字 = 本命盘四个地支名字列表[右侧地支索引]
                同柱地支名字 = 本命盘四个地支名字列表[['年干', '月干', '日干', '时干'].index(天干)]
                生扶受制关系 = 判断两者是否生扶受制(右侧地支, 同柱地支)
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                临时变量字典[天干].update({'右侧地支': 右侧地支,'右侧地支名字': 右侧地支名字,'生制关系': 生制关系,'同柱地支': 同柱地支,'同柱地支名字': 同柱地支名字,'天干名字': 天干名字,'十神': 十神,'内环境': 内环境})
                作用链路过程= f"🔍「已现十神の内环境的右环境」推导过程：∵【{右侧地支}】【{右侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{天干}】【{天干名字}】【{十神}】的内环境【{内环境}】，∴【{天干}】【{天干名字}】【{十神}】的内环境右环境（{环境类型字典[天干]}）【{内环境右环境}】"
                收集断语(作用链路过程)
                print(作用链路过程)

            elif 天干 == '时干':
                日支名字 = 本命盘四个地支名字列表[2]
                月支名字 = 本命盘四个地支名字列表[1]
                时支名字 = 本命盘四个地支名字列表[3]
                日支与时地支作用关系 = "生" if 判断两者是否生扶受制('日支', '时支') == '生扶关系' else "制"
                月支与日地支作用关系 = "生" if 判断两者是否生扶受制('月支', '日支') == '生扶关系' else "制"
                作用链路过程= f"🔍「已现十神の内环境的右环境」推导过程：∵【月支】【{月支名字}】【{月支与日地支作用关系}】【日支】【{日支名字}】，【日支】【{日支名字}】【{日支与时地支作用关系}】【时支】【{时支名字}】，【时干】【{天干名字}】【{十神}】的内环境【{内环境}】，∴【时干】【{天干名字}】【{十神}】的内环境右环境（{环境类型字典[天干]}）【{内环境右环境}】"
                收集断语(作用链路过程)
                print(作用链路过程)
        
        内环境右环境结论 = {
        '年干': {
            '作用路径': f"∵【{临时变量字典['年干']['右侧地支']}】【{临时变量字典['年干']['右侧地支名字']}】【{临时变量字典['年干']['生制关系']}】【{临时变量字典['年干']['同柱地支']}】【{临时变量字典['年干']['同柱地支名字']}】，【年干】【{临时变量字典['年干']['天干名字']}】【{临时变量字典['年干']['十神']}】的内环境【{临时变量字典['年干']['内环境']}】",
            '环境类型': 环境类型字典['年干'],
            '环境结果': 八字信息主字典['年干']['内环境右环境']},
        '月干': {
            '作用路径': f"∵【{临时变量字典['月干']['右侧地支']}】【{临时变量字典['月干']['右侧地支名字']}】【{临时变量字典['月干']['生制关系']}】【{临时变量字典['月干']['同柱地支']}】【{临时变量字典['月干']['同柱地支名字']}】，【月干】【{临时变量字典['月干']['天干名字']}】【{临时变量字典['月干']['十神']}】的内环境【{临时变量字典['月干']['内环境']}】",
            '环境类型': 环境类型字典['月干'],
            '环境结果': 八字信息主字典['月干']['内环境右环境']},
        '时干': {
            '作用路径': f"∵【月支】【{月支名字}】【{月支与日地支作用关系}】【日支】【{日支名字}】，【日支】【{日支名字}】【{日支与时地支作用关系}】【时支】【{时支名字}】，【时干】【{天干名字}】【{十神}】的内环境【{内环境}】",
            '环境类型': 环境类型字典['时干'],
            '环境结果': 八字信息主字典['时干']['内环境右环境']}}
        return 内环境右环境结论
    分析天干十神的内环境右环境吉凶()

    #特别版：分析天干十神的国外环境吉凶
    def 分析天干十神的国外环境吉凶():
        def 反转作用结果(作用结果):
            if 作用结果 == '生扶关系':
                return '受制关系'
            elif 作用结果 == '受制关系':
                return '生扶关系'
            return 作用结果
        
        天干顺序 = ['年干', '月干', '日干', '时干']
        for 天干 in ['年干', '月干', '时干']:
            # 根据性别确定方向
            if 性别 == '男':
                环境方向 = -1  # 男命左侧为社会环境
                国外环境方向 = -2  # 男命左侧的左侧为国外环境
            else:
                环境方向 = 1   # 女命右侧为社会环境
                国外环境方向 = 2   # 女命右侧的右侧为国外环境

            当前索引 = 天干顺序.index(天干)
            国外环境索引 = 当前索引 + 国外环境方向

            # 处理特殊情况
            if 国外环境索引 < 0 or 国外环境索引 >= len(天干顺序):

                # 男命特殊情况处理
                if 性别 == '男':
                    if 天干 == '年干':
                        # 男命年干的国外环境：日干作用月干，再作用于年干
                        月干旺弱 = 八字信息主字典['月干']['旺弱状态']
                        日干作用月干结果 = 判断两者是否生扶受制('日干', '月干')
                        if 月干旺弱 == '弱':
                            日干作用月干结果 = 反转作用结果(日干作用月干结果)
                        月干作用年干结果 = 判断两者是否生扶受制('月干', '年干')
                        if 日干作用月干结果 == '生扶':
                            八字信息主字典[天干]['国外环境'] = '吉'
                        else:
                            八字信息主字典[天干]['国外环境'] = '凶'
                        continue
                    elif 天干 == '月干':
                        # 男命月干的国外环境：日干作用月干，再作用于年干
                        # 与年干的国外环境相同
                        月干旺弱 = 八字信息主字典['月干']['旺弱状态']
                        日干作用月干结果 = 判断两者是否生扶受制('日干', '月干')
                        if 月干旺弱 == '弱':
                            日干作用月干结果 = 反转作用结果(日干作用月干结果)
                        月干作用年干结果 = 判断两者是否生扶受制('月干', '年干')
                        if 日干作用月干结果 == '生扶':
                            八字信息主字典[天干]['国外环境'] = '吉'
                        else:
                            八字信息主字典[天干]['国外环境'] = '凶'
                        continue

                # 女命特殊情况处理
                else:
                    if 天干 == '时干':
                        # 女命时干的国外环境：月干作用日干，再作用于时干
                        日干旺弱 = 八字信息主字典['日干']['旺弱状态']
                        月干作用日干结果 = 判断两者是否生扶受制('月干', '日干')
                        if 日干旺弱 == '弱':
                            月干作用日干结果 = 反转作用结果(月干作用日干结果)
                        日干作用时干结果 = 判断两者是否生扶受制('日干', '时干')
                        if 月干作用日干结果 == '生扶':
                            八字信息主字典[天干]['国外环境'] = '吉'
                        else:
                            八字信息主字典[天干]['国外环境'] = '凶'
                        continue
                    elif 天干 == '日干':
                        # 女命日干的国外环境：月干作用日干，再作用于时干
                        # 与时干的国外环境相同
                        日干旺弱 = 八字信息主字典['日干']['旺弱状态']
                        月干作用日干结果 = 判断两者是否生扶受制('月干', '日干')
                        if 日干旺弱 == '弱':
                            月干作用日干结果 = 反转作用结果(月干作用日干结果)
                        日干作用时干结果 = 判断两者是否生扶受制('日干', '时干')
                        if 月干作用日干结果 == '生扶':
                            八字信息主字典[天干]['国外环境'] = '吉'
                        else:
                            八字信息主字典[天干]['国外环境'] = '凶'
            else:
                # 正常情况处理
                国外环境天干 = 天干顺序[国外环境索引]
                作用方 = 国外环境天干
                被作用方 = 天干
                被作用方旺弱 = 八字信息主字典[被作用方]['旺弱状态']
                作用结果 = 判断两者是否生扶受制(作用方, 被作用方)
                if 被作用方旺弱 == '弱':
                    作用结果 = 反转作用结果(作用结果)
                if 作用结果 == '生扶':
                    八字信息主字典[天干]['国外环境'] = '吉'
                else:
                    八字信息主字典[天干]['国外环境'] = '凶'
    分析天干十神的国外环境吉凶()



    #9.7 分析未现天干十神的的外环境吉凶
    def 分析未现天干十神的外环境吉凶():
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            名字 = 属性子字典.get('名字', '')
            十神 = 属性子字典.get('十神', '')
            忌用神归属 = 属性子字典.get('忌用神归属', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')
            
            if not 窗口名字:    #缺少窗口十神时的处理逻辑
                print(f"未现十神：{天干名}，缺少窗口十神信息，无法判断外环境")
                属性子字典['外环境'] = '未知'
                continue  # 跳过本次循环，处理下一个未现十神

            生扶受制关系 = 判断两者是否生扶受制(窗口名字, 名字)
            
            # 根据忌用神归属和生扶受制关系，初步确定外环境结论
            if 忌用神归属 == '忌神':
                if 生扶受制关系 == '受制关系':
                    外环境结论 = '吉'
                elif 生扶受制关系 == '生扶关系':
                    外环境结论 = '凶'
                else:
                    外环境结论 = '未知'
            elif 忌用神归属 == '用神':
                if 生扶受制关系 == '受制关系':
                    外环境结论 = '凶'
                elif 生扶受制关系 == '生扶关系':
                    外环境结论 = '吉'
                else:
                    外环境结论 = '未知'
            else:
                外环境结论 = '未知'
            
            # 检查是否有镜像，如果有，则反转外环境结论
            if 是否有镜像 == '有镜像':
                if 外环境结论 == '吉':
                    外环境结论 = '凶'
                elif 外环境结论 == '凶':
                    外环境结论 = '吉'
            
            # 将最终的外环境结论存入属性子字典
            属性子字典['外环境'] = 外环境结论
            未现正偏十神主字典[天干名]['外环境'] = 外环境结论

            作用链路过程 =f"未现十神：{十神} - {名字} - 外环境结论：{外环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)
            #新增打印推导过程
            窗口位置 = next(位置 for 位置, 信息 in 八字信息主字典.items() if 信息['名字'] == 属性子字典['窗口名字'])
            生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
            作用链路过程 =f"🔍「未现十神の外环境」推导过程：∵【{窗口位置}】【{八字信息主字典[窗口位置]['名字']}】【{八字信息主字典[窗口位置]['十神']}】【{生制关系}】未现十神的【{名字}】【{十神}】，∴未现天干十神【{名字}】【{十神}】的外环境【{外环境结论}】"
            收集断语(作用链路过程)
            print(作用链路过程)

        外环境结论 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 属性子字典['窗口名字']), None)
            if 窗口位置:
                外环境结论[天干名] = {
                    '外环境': 属性子字典['外环境'],  # 使用未现正偏十神主字典中的外环境
                    '作用路径': f"🔍「未现十神の外环境」推导过程：∵【{窗口位置}】的【{八字信息主字典[窗口位置]['名字']}】【{八字信息主字典[窗口位置]['十神']}】【{生制关系}】未现十神的【{属性子字典['名字']}】【{属性子字典['十神']}】，∴未现天干十神【{属性子字典['名字']}】【{属性子字典['十神']}】的外环境【{属性子字典['外环境']}】"
                }
        return 外环境结论
    分析未现天干十神的外环境吉凶()

    #9.8 分析未现天干十神的的内环境吉凶
    def 分析未现天干十神的内环境吉凶():
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            名字 = 属性子字典.get('名字', '')
            十神 = 属性子字典.get('十神', '')
            外环境 = 属性子字典.get('外环境', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')

            if not 窗口名字:     # 如果缺少窗口十神的信息，无法判断内环境
                属性子字典['内环境'] = '未知'
                continue

            # 获取窗口十神的“是否有根”信息。  窗口十神是已现十神，可以从八字信息主字典中获取
            窗口是否有根 = ''
            for 键, 值 in 八字信息主字典.items():
                if 值.get('名字') == 窗口名字:
                    窗口是否有根 = 值.get('是否有根', '')
                    break
            else:     # 如果在八字信息主字典中找不到窗口十神的信息，无法判断内环境
                属性子字典['内环境'] = '果在八字信息主字典中找不到其窗口十神的信息'
                continue

            # 根据外环境和窗口十神的有根情况，确定内环境结论
            if 外环境 == '吉':
                if 窗口是否有根 == '有根':
                    内环境结论 = '吉'
                else:
                    内环境结论 = '凶'
            elif 外环境 == '凶':
                if 窗口是否有根 == '有根':
                    内环境结论 = '凶'
                else:
                    内环境结论 = '吉'
            else:
                内环境结论 = '未知'

            # 检查是否有镜像，如果有，则反转内环境结论
            if 是否有镜像 == '有镜像':
                if 内环境结论 == '吉':
                    内环境结论 = '凶'
                elif 内环境结论 == '凶':
                    内环境结论 = '吉'

            # 将最终的内环境结论存入属性子字典
            属性子字典['内环境'] = 内环境结论
            未现正偏十神主字典[天干名]['内环境'] = 内环境结论

            作用链路过程 = f"未现十神：{十神} - {名字} - 内环境结论：{内环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)
            
            #推导过程print代码
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), "未知位置")
            窗口十神 = next((信息.get('十神', '') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 窗口名字), "")
            窗口是否有根 = next((信息.get('是否有根', '无根') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 窗口名字), "无根")
            
            作用链路过程 = f"🔍「未现十神の内环境」推导过程：因为【{窗口位置}】【{窗口十神}】【{窗口名字}】【{窗口是否有根}】，∴未现天干十神【{名字}】【{十神}】的内环境【{内环境结论}】。"
            收集断语(作用链路过程)
            print(作用链路过程)
        内环境结论 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口名字 = 属性子字典.get('窗口名字')
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 属性子字典['窗口名字']), None)
            if 窗口位置:
                窗口十神 = next((信息.get('十神', '') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 窗口名字), "")
                窗口是否有根 = next((信息.get('是否有根', '无根') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 窗口名字), "无根")
                内环境结论[天干名] = {
                '内环境': 属性子字典['内环境'],
                '作用路径': f"🔍「未现十神の内环境」推导过程：∵【{窗口位置}】【{窗口十神}】【{窗口名字}】【{窗口是否有根}】，∴未现天干十神【{属性子字典['名字']}】【{属性子字典['十神']}】的内环境【{属性子字典['内环境']}】。"
            }
        return 内环境结论
    分析未现天干十神的内环境吉凶()

    #9.9 分析未现天干十神的左环境吉凶
    def 分析未现天干十神的左环境吉凶():
        天干顺序 = ['年干', '月干', '日干', '时干']
        
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            十神 = 属性子字典.get('十神', '')
            外环境 = 属性子字典.get('外环境', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')

            if not 窗口名字:
                属性子字典['左环境'] = '未知'
                continue  # 缺少窗口名字信息，无法判断

            # 找出窗口名字对应的干支位置
            窗口位置 = None
            for 位置, 干名 in zip(天干顺序, 本命盘四个天干名字列表):
                if 干名 == 窗口名字:
                    窗口位置 = 位置
                    break

            if 窗口位置:
                窗口索引 = 天干顺序.index(窗口位置)
                if 窗口索引 > 0:
                    左侧位置 = 天干顺序[窗口索引 - 1]
                    左侧名字 = 本命盘四个天干名字列表[窗口索引 - 1]
                else:
                    左侧名字 = None  # 窗口名字已是最左边，无左侧

                if 左侧名字:
                    生扶受制关系 = 判断两者是否生扶受制(左侧名字, 窗口名字)
                    
                    if 外环境 == '吉':
                        if 生扶受制关系 == '生扶关系':
                            左环境结论 = '吉'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            左环境结论 = '凶'
                        else:
                            左环境结论 = '未知'
                    elif 外环境 == '凶':
                        if 生扶受制关系 == '生扶关系':
                            左环境结论 = '凶'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            左环境结论 = '吉'
                        else:
                            左环境结论 = '未知'
                    else:
                        左环境结论 = '未知'
                else:
                    左环境结论 = '未知'  # 无左侧名字，无法判断
            else:
                左环境结论 = '未知'  # 窗口名字不在天干顺序中，可能是特殊情况

            # 特殊情况：窗口十神在年干
            if 窗口位置 == '年干':
                日干生扶月干 = 判断两者是否生扶受制(本命盘四个天干名字列表[2], 本命盘四个天干名字列表[1]) == '生扶关系'
                月干生扶年干 = 判断两者是否生扶受制(本命盘四个天干名字列表[1], 本命盘四个天干名字列表[0]) == '生扶关系'
                日干受制月干 = 判断两者是否生扶受制(本命盘四个天干名字列表[2], 本命盘四个天干名字列表[1]) in ['受制关系', '不旺不弱关系']
                月干受制年干 = 判断两者是否生扶受制(本命盘四个天干名字列表[1], 本命盘四个天干名字列表[0]) in ['受制关系', '不旺不弱关系']

                生扶受制关系 = 判断两者是否生扶受制(窗口名字, 天干名)

                if 外环境 == '吉':
                    if 月干生扶年干 and 日干生扶月干:
                        左环境结论 = '吉'
                    elif 月干生扶年干 and 日干受制月干:
                        左环境结论 = '凶'
                    elif 月干受制年干 and 日干生扶月干:
                        左环境结论 = '凶'
                    elif 月干受制年干 and 日干受制月干:
                        左环境结论 = '吉'
                    else:
                        左环境结论 = '未知'
                elif 外环境 == '凶':
                    if 月干生扶年干 and 日干生扶月干:
                        左环境结论 = '凶'
                    elif 月干生扶年干 and 日干受制月干:
                        左环境结论 = '吉'
                    elif 月干受制年干 and 日干生扶月干:
                        左环境结论 = '吉'
                    elif 月干受制年干 and 日干受制月干:
                        左环境结论 = '凶'
                    else:
                        左环境结论 = '未知'

            # 检查是否有镜像，需要反转结论
            if 是否有镜像 == '有镜像':
                if 左环境结论 == '吉':
                    左环境结论 = '凶'
                elif 左环境结论 == '凶':
                    左环境结论 = '吉'

            # 判断左环境代表的含义
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别 == '男' and 是正十神) or (性别 == '女' and not 是正十神):
                环境类型 = "社会环境"
            else:
                环境类型 = "内心环境"

            # 将左环境结论记录到属性子字典
            属性子字典['左环境'] = 左环境结论
            属性子字典['环境类型'] = 环境类型

            作用链路过程 = f"未现十神：{十神} - {天干名} - 左环境：{左环境结论} - {环境类型}:{左环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)

            # 添加推导过程的打印
            左侧位置 = 天干顺序[窗口索引 - 1] if 窗口索引 > 0 else "无"
            左侧名字 = 本命盘四个天干名字列表[窗口索引 - 1] if 窗口索引 > 0 else "无"
            左侧十神 = next((信息.get('十神', '') for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 左侧名字), "")
            窗口十神 = next((信息.get('十神', '') for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), "")

            if 窗口位置 == '年干':
                日干月干关系 = "生" if 日干生扶月干 else "制"
                月干年干关系 = "生" if 月干生扶年干 else "制"
                作用链路过程 = f"「未现十神の左环境」推导过程：∵【日干】【{本命盘四个天干名字列表[2]}】【{八字信息主字典['日干']['十神']}】【{日干月干关系}】【月干】【{本命盘四个天干名字列表[1]}】【{八字信息主字典['月干']['十神']}】，【月干】【{本命盘四个天干名字列表[1]}】【{八字信息主字典['月干']['十神']}】【{月干年干关系}】【年干】【{窗口名字}】【{窗口十神}】【{生扶受制关系}】未现天干十神【{天干名}】【{十神}】∴未现十神【{天干名}】【{十神}】的左环境（{环境类型}）【{左环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            else:
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                作用链路过程 = f"「未现十神の左环境」推导过程：∵【{左侧位置}】【{左侧名字}】【{左侧十神}】【{生制关系}】【{窗口位置}】【{窗口十神}】【{窗口名字}】，【{窗口位置}】【{窗口十神}】【{窗口名字}】【{生制关系}】未现天干十神【{天干名}】【{十神}】∴未现十神【{天干名}】【{十神}】的左环境（{环境类型}）【{左环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
        
        左环境结论 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口名字 = 属性子字典.get('窗口名字')
            十神 = 属性子字典.get('十神')
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), None)
            
            if 窗口位置 == '年干':
                # 特殊情况：窗口十神在年干
                日干月干关系 = "生" if 日干生扶月干 else "制"
                月干年干关系 = "生" if 月干生扶年干 else "制"
                左环境结论[天干名] = {
                    '左环境': 属性子字典['左环境'],
                    '作用路径': f"「未现十神の左环境」推导过程：∵【日干】【{本命盘四个天干名字列表[2]}】【{八字信息主字典['日干']['十神']}】【{日干月干关系}】【月干】【{本命盘四个天干名字列表[1]}】【{八字信息主字典['月干']['十神']}】，【月干】【{本命盘四个天干名字列表[1]}】【{八字信息主字典['月干']['十神']}】【{月干年干关系}】【年干】【{窗口名字}】【{窗口十神}】，∴未现十神【{天干名}】【{十神}】的左环境为【{属性子字典['左环境']}】"
                }
            else:
                # 普通情况
                左侧位置 = 天干顺序[天干顺序.index(窗口位置) - 1] if 天干顺序.index(窗口位置) > 0 else None
                if 左侧位置:
                    左侧名字 = 八字信息主字典[左侧位置]['名字']
                    左侧十神 = 八字信息主字典[左侧位置]['十神']
                    生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                    左环境结论[天干名] = {
                        '左环境': 属性子字典['左环境'],
                        '作用路径': f"「未现十神の左环境」推导过程：∵【{左侧位置}】【{左侧名字}】【{左侧十神}】【{生制关系}】【{窗口位置}】【{窗口十神}】【{窗口名字}】，∴未现十神【{天干名}】【{十神}】的左环境为【{属性子字典['左环境']}】"
                    }
        return 左环境结论
    分析未现天干十神的左环境吉凶()

    # 9.10 分析未现天干十神的右环境吉凶
    def 分析未现天干十神的右环境吉凶():
        天干顺序 = ['年干', '月干', '日干', '时干']
        右环境结论字典 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            十神 = 属性子字典.get('十神', '')
            外环境 = 属性子字典.get('外环境', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')

            if not 窗口名字:
                属性子字典['右环境'] = '未知'
                continue  # 缺少窗口名字信息，无法判断

            # 找出窗口名字对应的干支位置
            窗口位置 = None
            for 位置, 干名 in zip(天干顺序, 本命盘四个天干名字列表):
                if 干名 == 窗口名字:
                    窗口位置 = 位置
                    break

            if 窗口位置:
                窗口索引 = 天干顺序.index(窗口位置)
                if 窗口索引 < len(天干顺序) - 1:
                    右侧位置 = 天干顺序[窗口索引 + 1]
                    右侧名字 = 本命盘四个天干名字列表[窗口索引 + 1]
                else:
                    右侧名字 = None  # 窗口名字已是最右边，无右侧

                if 右侧名字:
                    生扶受制关系 = 判断两者是否生扶受制(右侧名字, 窗口名字)
                    
                    if 外环境 == '吉':
                        if 生扶受制关系 == '生扶关系':
                            右环境结论 = '吉'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            右环境结论 = '凶'
                        else:
                            右环境结论 = '未知'
                    elif 外环境 == '凶':
                        if 生扶受制关系 == '生扶关系':
                            右环境结论 = '凶'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            右环境结论 = '吉'
                        else:
                            右环境结论 = '未知'
                    else:
                        右环境结论 = '未知'
                else:
                    右环境结论 = '未知'  # 无右侧名字，无法判断
            else:
                右环境结论 = '未知'  # 窗口名字不在天干顺序中，可能是特殊情况

            # 特殊情况：窗口十神在时干
            if 窗口位置 == '时干':
                月干生扶日干 = 判断两者是否生扶受制(本命盘四个天干名字列表[1], 本命盘四个天干名字列表[2]) == '生扶关系'
                日干生扶时干 = 判断两者是否生扶受制(本命盘四个天干名字列表[2], 本命盘四个天干名字列表[3]) == '生扶关系'
                月干受制日干 = 判断两者是否生扶受制(本命盘四个天干名字列表[1], 本命盘四个天干名字列表[2]) in ['受制关系', '不旺不弱关系']
                日干受制时干 = 判断两者是否生扶受制(本命盘四个天干名字列表[2], 本命盘四个天干名字列表[3]) in ['受制关系', '不旺不弱关系']

                if 外环境 == '吉':
                    if 日干生扶时干 and 月干生扶日干:
                        右环境结论 = '吉'
                    elif 日干生扶时干 and 月干受制日干:
                        右环境结论 = '凶'
                    elif 日干受制时干 and 月干生扶日干:
                        右环境结论 = '凶'
                    elif 日干受制时干 and 月干受制日干:
                        右环境结论 = '吉'
                    else:
                        右环境结论 = '未知'
                elif 外环境 == '凶':
                    if 日干生扶时干 and 月干生扶日干:
                        右环境结论 = '凶'
                    elif 日干生扶时干 and 月干受制日干:
                        右环境结论 = '吉'
                    elif 日干受制时干 and 月干生扶日干:
                        右环境结论 = '吉'
                    elif 日干受制时干 and 月干受制日干:
                        右环境结论 = '凶'
                    else:
                        右环境结论 = '未知'

            # 检查是否有镜像，需要反转结论
            if 是否有镜像 == '有镜像':
                if 右环境结论 == '吉':
                    右环境结论 = '凶'
                elif 右环境结论 == '凶':
                    右环境结论 = '吉'

            # 判断右环境代表的含义
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型 = "内心环境"
            else:
                环境类型 = "社会环境"

            # 将右环境结论记录到属性子字典
            属性子字典['右环境'] = 右环境结论
            属性子字典['环境类型'] = 环境类型

            作用链路过程 = f"未现十神：{十神} - {天干名} - 右环境：{右环境结论} - {环境类型}:{右环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)

            # 添加推导过程的打印
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), "未知位置")
            窗口十神 = next((信息.get('十神', '') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 窗口名字), "")
            
            if 窗口位置 != '时干':
                右侧位置 = 天干顺序[天干顺序.index(窗口位置) + 1] if 天干顺序.index(窗口位置) < 3 else "无"
                右侧名字 = 本命盘四个天干名字列表[天干顺序.index(窗口位置) + 1] if 天干顺序.index(窗口位置) < 3 else "无"
                右侧十神 = next((信息.get('十神', '') for 信息 in 八字信息主字典.values() if 信息.get('名字') == 右侧名字), "")
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                作用链路过程 = f"🔍「未现十神の右环境」推导过程：∵【{右侧位置}】【{右侧名字}】【{右侧十神}】【{生制关系}】【{窗口位置}】【{窗口名字}】【{窗口十神}】，∴未现天干十神【{天干名}】【{十神}】的右环境（{环境类型}）【{右环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            else:
                月干名字 = 本命盘四个天干名字列表[1]
                月干十神 = 八字信息主字典['月干']['十神']
                日干名字 = 本命盘四个天干名字列表[2]
                日干十神 = 八字信息主字典['日干']['十神']
                
                月日关系 = "生" if 月干生扶日干 else "制"
                日时关系 = "生" if 日干生扶时干 else "制"
                作用链路过程 = f"🔍「未现十神の右环境」推导过程：∵【月干】【{月干名字}】【{月干十神}】【{月日关系}】【日干】【{日干名字}】【{日干十神}】，【日干】【{日干名字}】【{日干十神}】【{日时关系}】【时干】【{窗口名字}】【{窗口十神}】，∴未现天干十神【{天干名}】【{十神}】的右环境（{环境类型}）【{右环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)

            if 窗口位置 == '时干':
                右环境结论字典[天干名] = {'右环境': 右环境结论,
                    '作用路径': f"🔍「未现十神の右环境」推导过程：∵【月干】【{月干名字}】【{月干十神}】【{月日关系}】【日干】【{日干名字}】【{日干十神}】，【日干】【{日干名字}】【{日干十神}】【{日时关系}】【时干】【{窗口名字}】【{窗口十神}】，∴未现天干十神【{天干名}】【{十神}】的右环境（{环境类型}）【{右环境结论}】"
                }
            else:
                右环境结论字典[天干名] = {'右环境': 右环境结论,
                    '作用路径': f"🔍「未现十神の右环境」推导过程：∵【{右侧位置}】【{右侧名字}】【{右侧十神}】【{生制关系}】【{窗口位置}】【{窗口名字}】【{窗口十神}】，∴未现天干十神【{天干名}】【{十神}】的右环境（{环境类型}）【{右环境结论}】"
                }

        return 右环境结论字典
    分析未现天干十神的右环境吉凶()

    # 9.11 分析未现天干十神的内环境的左环境
    def 分析未现天干十神的内环境的左环境():
        天干顺序 = ['年干', '月干', '日干', '时干']
        地支顺序 = ['年支', '月支', '日支', '时支']

        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            十神 = 属性子字典.get('十神', '')
            内环境 = 属性子字典.get('内环境', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')

            if not 窗口名字 or not 内环境:
                属性子字典['内环境左环境'] = '未知'
                continue

            # 找出窗口名字对应的干支位置
            窗口位置 = None
            for 位置, 干名 in zip(天干顺序, 本命盘四个天干名字列表):
                if 干名 == 窗口名字:
                    窗口位置 = 位置
                    break

            if 窗口位置:
                窗口索引 = 天干顺序.index(窗口位置)
                同柱地支 = 地支顺序[窗口索引]

                if 窗口位置 != '年干':
                    左侧地支 = 地支顺序[窗口索引 - 1]
                    生扶受制关系 = 判断两者是否生扶受制(左侧地支, 同柱地支)

                    if 内环境 == '吉':
                        if 生扶受制关系 == '生扶关系':
                            内环境左环境结论 = '吉'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '凶'
                    elif 内环境 == '凶':
                        if 生扶受制关系 == '生扶关系':
                            内环境左环境结论 = '凶'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '吉'
                else:
                    # 特殊情况：窗口十神在年干
                    日支与月地支作用关系 = 判断两者是否生扶受制('日支', '月支')
                    月支与年地支作用关系 = 判断两者是否生扶受制('月支', '年支')

                    if 内环境 == '吉':
                        if 日支与月地支作用关系 == '生扶关系' and 月支与年地支作用关系 == '生扶关系':
                            内环境左环境结论 = '吉'
                        elif 日支与月地支作用关系 == '生扶关系' and 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '凶'
                        elif 日支与月地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与年地支作用关系 == '生扶关系':
                            内环境左环境结论 = '凶'
                        elif 日支与月地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '吉'
                    elif 内环境 == '凶':
                        if 日支与月地支作用关系 == '生扶关系' and 月支与年地支作用关系 == '生扶关系':
                            内环境左环境结论 = '凶'
                        elif 日支与月地支作用关系 == '生扶关系' and 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '吉'
                        elif 日支与月地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与年地支作用关系 == '生扶关系':
                            内环境左环境结论 = '吉'
                        elif 日支与月地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与年地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境左环境结论 = '凶'

                # 检查是否有镜像，需要反转结论
                if 是否有镜像 == '有镜像':
                    if 内环境左环境结论 == '吉':
                        内环境左环境结论 = '凶'
                    elif 内环境左环境结论 == '凶':
                        内环境左环境结论 = '吉'

                # 将内环境左环境结论记录到属性子字典
                属性子字典['内环境左环境'] = 内环境左环境结论

            内环境左环境结论 = 属性子字典.get('内环境左环境', '')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型 = "社会环境的内环境"
            else:
                环境类型 = "内心环境的内环境"
            作用链路过程 = f"未现十神：{十神} - {天干名} - 内环境左环境：{内环境左环境结论} - {环境类型}:{内环境左环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)

            # 添加推导过程的打印
            if 窗口位置 != '年干':
                左侧地支名字 = 本命盘四个地支名字列表[窗口索引 - 1]
                同柱地支名字 = 本命盘四个地支名字列表[窗口索引]
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                作用链路过程 = f"🔍「未现十神の内环境的左环境」推导过程：【{左侧地支}】【{左侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的左环境（{环境类型}）【{内环境左环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            else:
                日支名字 = 本命盘四个地支名字列表[2]
                月支名字 = 本命盘四个地支名字列表[1]
                年支名字 = 本命盘四个地支名字列表[0]
                日月关系 = "生" if 日支与月地支作用关系 == '生扶关系' else "制"
                月年关系 = "生" if 月支与年地支作用关系 == '生扶关系' else "制"
                作用链路过程 = f"🔍「未现十神の内环境的左环境」推导过程：∵【日支】【{日支名字}】【{日月关系}】【月支】【{月支名字}】，【月支】【{月支名字}】【{月年关系}】【年支】【{年支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的左环境（{环境类型}）【{内环境左环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)

        内环境左环境结论字典 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口名字 = 属性子字典.get('窗口名字')
            十神 = 属性子字典.get('十神', '')
            内环境 = 属性子字典.get('内环境', '')
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), None)
            
            if 窗口位置 == '年干':
                # 特殊情况：窗口在年干
                内环境左环境结论字典[天干名] = {
                    '内环境左环境': 属性子字典['内环境左环境'],
                    '作用路径': f"🔍「未现十神の内环境の左环境」推导过程：∵【日支】【{日支名字}】【{日月关系}】【月支】【{月支名字}】，【月支】【{月支名字}】【{月年关系}】【年支】【{年支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的左环境（{环境类型}）【{内环境左环境结论}】"
                }
            else:
                # 普通情况
                内环境左环境结论字典[天干名] = {
                    '内环境左环境': 属性子字典['内环境左环境'],
                    '作用路径': f"🔍「未现十神の内环境の左环境」推导过程：【{左侧地支}】【{左侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的左环境（{环境类型}）【{内环境左环境结论}】"
                }
        return 内环境左环境结论字典
    分析未现天干十神的内环境的左环境()

    # 9.12 分析未现天干十神的内环境的右环境
    def 分析未现天干十神的内环境的右环境():
        天干顺序 = ['年干', '月干', '日干', '时干']
        地支顺序 = ['年支', '月支', '日支', '时支']

        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            十神 = 属性子字典.get('十神', '')
            内环境 = 属性子字典.get('内环境', '')
            窗口名字 = 属性子字典.get('窗口名字', '')
            是否有镜像 = 属性子字典.get('是否有镜像', '')

            if not 窗口名字 or not 内环境:
                属性子字典['内环境右环境'] = '未知'
                continue

            # 找出窗口名字对应的干支位置
            窗口位置 = None
            for 位置, 干名 in zip(天干顺序, 本命盘四个天干名字列表):
                if 干名 == 窗口名字:
                    窗口位置 = 位置
                    break

            if 窗口位置:
                窗口索引 = 天干顺序.index(窗口位置)
                同柱地支 = 地支顺序[窗口索引]

                if 窗口位置 != '时干':
                    右侧地支 = 地支顺序[窗口索引 + 1]
                    生扶受制关系 = 判断两者是否生扶受制(右侧地支, 同柱地支)

                    if 内环境 == '吉':
                        if 生扶受制关系 == '生扶关系':
                            内环境右环境结论 = '吉'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '凶'
                    elif 内环境 == '凶':
                        if 生扶受制关系 == '生扶关系':
                            内环境右环境结论 = '凶'
                        elif 生扶受制关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '吉'
                else:
                    # 特殊情况：窗口十神在时干
                    日支与时地支作用关系 = 判断两者是否生扶受制('日支', '时支')
                    月支与日地支作用关系 = 判断两者是否生扶受制('月支', '日支')

                    if 内环境 == '吉':
                        if 日支与时地支作用关系 == '生扶关系' and 月支与日地支作用关系 == '生扶关系':
                            内环境右环境结论 = '吉'
                        elif 日支与时地支作用关系 == '生扶关系' and 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '凶'
                        elif 日支与时地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与日地支作用关系 == '生扶关系':
                            内环境右环境结论 = '凶'
                        elif 日支与时地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '吉'
                    elif 内环境 == '凶':
                        if 日支与时地支作用关系 == '生扶关系' and 月支与日地支作用关系 == '生扶关系':
                            内环境右环境结论 = '凶'
                        elif 日支与时地支作用关系 == '生扶关系' and 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '吉'
                        elif 日支与时地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与日地支作用关系 == '生扶关系':
                            内环境右环境结论 = '吉'
                        elif 日支与时地支作用关系 in ['受制关系', '不旺不弱关系'] and 月支与日地支作用关系 in ['受制关系', '不旺不弱关系']:
                            内环境右环境结论 = '凶'

                # 检查是否有镜像，需要反转结论
                if 是否有镜像 == '有镜像':
                    if 内环境右环境结论 == '吉':
                        内环境右环境结论 = '凶'
                    elif 内环境右环境结论 == '凶':
                        内环境右环境结论 = '吉'

                # 将内环境右环境结论记录到属性子字典
                属性子字典['内环境右环境'] = 内环境右环境结论

            内环境右环境结论 = 属性子字典.get('内环境右环境', '')
            是正十神 = 十神 in ['正官', '正印', '正财', '伤官', '劫财']
            if (性别变量 == '男' and 是正十神) or (性别变量 == '女' and not 是正十神):
                环境类型 = "内心环境的内环境"
            else:
                环境类型 = "社会环境的内环境"
            作用链路过程 = f"未现十神：{十神} - {天干名} - 内环境右环境：{内环境右环境结论} - {环境类型}:{内环境右环境结论}"
            收集断语(作用链路过程)
            print(作用链路过程)
            
            # 添加推导过程的打印
            if 窗口位置 != '时干':
                右侧地支名字 = 本命盘四个地支名字列表[窗口索引 + 1]
                同柱地支名字 = 本命盘四个地支名字列表[窗口索引]
                生制关系 = "生" if 生扶受制关系 == '生扶关系' else "制"
                作用链路过程 = f"🔍「未现十神の内环境的右环境」推导过程：∵【{右侧地支}】【{右侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的右环境（{环境类型}）【{内环境右环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
            else:
                日支名字 = 本命盘四个地支名字列表[2]
                月支名字 = 本命盘四个地支名字列表[1]
                时支名字 = 本命盘四个地支名字列表[3]
                日时关系 = "生" if 日支与时地支作用关系 == '生扶关系' else "制"
                月日关系 = "生" if 月支与日地支作用关系 == '生扶关系' else "制"
                作用链路过程 = f"🔍「未现十神の内环境的右环境」推导过程：∵【月支】【{月支名字}】【{月日关系}】【日支】【{日支名字}】，【日支】【{日支名字}】【{日时关系}】【时支】【{时支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的右环境（{环境类型}）【{内环境右环境结论}】"
                收集断语(作用链路过程)
                print(作用链路过程)
    
        内环境右环境结论字典 = {}
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口名字 = 属性子字典.get('窗口名字')
            十神 = 属性子字典.get('十神', '')
            内环境 = 属性子字典.get('内环境', '')
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), None)
            
            if 窗口位置 == '时干':
                # 特殊情况：窗口在时干
                内环境右环境结论字典[天干名] = {'内环境右环境': 属性子字典['内环境右环境'],
                    '作用路径': f"🔍「未现十神の内环境の右环境」推导过程：∵【月支】【{月支名字}】【{月日关系}】【日支】【{日支名字}】，【日支】【{日支名字}】【{日时关系}】【时支】【{时支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的右环境（{环境类型}）【{内环境右环境结论}】"}
            else:
                # 普通情况
                内环境右环境结论字典[天干名] = {'内环境右环境': 属性子字典['内环境右环境'],
                    '作用路径': f"🔍「未现十神の内环境の右环境」推导过程：∵【{右侧地支}】【{右侧地支名字}】【{生制关系}】【{同柱地支}】【{同柱地支名字}】，【{窗口位置}】【{窗口名字}】【{十神}】的内环境【{内环境}】，∴未现十神【{天干名}】【{十神}】的内环境的右环境（{环境类型}）【{内环境右环境结论}】"}
        return 内环境右环境结论字典
    分析未现天干十神的内环境的右环境()






     # 打印未现十神信息
    for 名字, 属性 in 未现正偏十神主字典.items():
        收集断语(f"未现十神的忌用神信息:【{名字}】- 【{属性['十神']}】 - 【{属性['忌用神归属']}】")

    def 判断日主自身状态():   #根据格局判断日主是用神还是忌神，并更新GUI显示
        import contextlib
        日干标签索引 = 2
        # 根据格局判断日主状态
        if 格局 in ['从强格局', '身弱格局']:
            八字信息主字典['日干']['忌用神归属'] = '用神'
            天干_shen_标签 = 天干_shen_标签_列表[日干标签索引]
            十神 = 八字信息主字典['日干']['十神']
            天干_shen_标签.config(text=f"{十神}（用神）", fg='#da61cd')
        elif 格局 in ['从弱格局', '身强格局']:
            八字信息主字典['日干']['忌用神归属'] = '忌神'
            天干_shen_标签 = 天干_shen_标签_列表[日干标签索引]
            十神 = 八字信息主字典['日干']['十神']
            天干_shen_标签.config(text=f"{十神}（忌神）", fg='#52577d')
        # 判断日干的左右环境
        月干生扶受制 = 判断两者是否生扶受制('月干', '日干')
        时干生扶受制 = 判断两者是否生扶受制('时干', '日干')
        日支生扶受制 = 判断两者是否生扶受制('日支', '日干')
        月支生扶受制 = 判断两者是否生扶受制('月支', '日支')
        时支生扶受制 = 判断两者是否生扶受制('时支', '日支')
        # 判断日干左右环境
        日干忌用神归属 = 八字信息主字典['日干']['忌用神归属']
        # 左环境判断
        if (日干忌用神归属 == '用神' and 月干生扶受制 == '生扶关系') or \
           (日干忌用神归属 == '忌神' and 月干生扶受制 == '受制关系'):
            日干左环境 = '吉'
        else:
            日干左环境 = '凶'
            
        # 右环境判断
        if (日干忌用神归属 == '用神' and 时干生扶受制 == '生扶关系') or \
           (日干忌用神归属 == '忌神' and 时干生扶受制 == '受制关系'):
            日干右环境 = '吉'
        else:
            日干右环境 = '凶'

        # 内环境判断
        if (日干忌用神归属 == '用神' and 日支生扶受制 == '生扶关系') or \
           (日干忌用神归属 == '忌神' and 日支生扶受制 == '受制关系'):
            日干内环境 = '吉'
        else:
            日干内环境 = '凶'

        # 内环境的左右环境判断
        if (日干内环境 == '吉' and 月支生扶受制 == '生扶关系') or \
           (日干内环境 == '凶' and 月支生扶受制 == '受制关系'):
            内环境左环境 = '吉'
        else:
            内环境左环境 = '凶'

        if (日干内环境 == '吉' and 时支生扶受制 == '生扶关系') or \
           (日干内环境 == '凶' and 时支生扶受制 == '受制关系'):
            内环境右环境 = '吉'
        else:
            内环境右环境 = '凶'
        
        with contextlib.redirect_stdout(None):
            # 打印结论
            月干关系 = "生" if 月干生扶受制 == '生扶关系' else "制"
            时干关系 = "生" if 时干生扶受制 == '生扶关系' else "制"
            日支关系 = "生" if 日支生扶受制 == '生扶关系' else "制"
            月支关系 = "生" if 月支生扶受制 == '生扶关系' else "制"
            时支关系 = "生" if 时支生扶受制 == '生扶关系' else "制"
            # 在函数末尾添加，存储环境信息到八字信息主字典
            八字信息主字典['日干'].update({'左环境': 日干左环境,'右环境': 日干右环境,'内环境': 日干内环境,'内环境左环境': 内环境左环境,'内环境右环境': 内环境右环境})

            作用链路过程 =f"∵日干为{日干忌用神归属}，月干【{月干关系}】日干，时干【{时干关系}】日干，∴日干的左环境为【{日干左环境}】，日干的右环境为【{日干右环境}】"
            收集断语(作用链路过程)
            print(作用链路过程)

            作用链路过程 =f"∵日干为{日干忌用神归属}，日支【{日支关系}】日干，∴日干的内环境为【{日干内环境}】。∵月支【{月支关系}】日支，时支【{时支关系}】日支，∴日干内环境的左环境为【{内环境左环境}】，日干内环境的右环境为【{内环境右环境}】。"
            收集断语(作用链路过程)
            print(作用链路过程)
        
        # 在函数末尾，构建并返回结论字典
        结论信息 = {'环境信息': {'左环境': 日干左环境,'右环境': 日干右环境,'内环境': 日干内环境,'内环境左环境': 内环境左环境,'内环境右环境': 内环境右环境},
            '作用路径说明': {'外环境说明': f"∵日干为{日干忌用神归属}，月干【{月干关系}】日干，时干【{时干关系}】日干，∴日干的左环境为【{日干左环境}】，日干的右环境为【{日干右环境}】",'内环境说明': f"∵日干为{日干忌用神归属}，日支【{日支关系}】日干，∴日干的内环境为【{日干内环境}】",'内环境扩展说明': f"∵月支【{月支关系}】日支，时支【{时支关系}】日支，∴日干内环境的左环境为【{内环境左环境}】，日干内环境的右环境为【{内环境右环境}】"}}
        
        八字信息主字典['日干'].update(结论信息['环境信息'])
        return 结论信息
    判断日主自身状态()




    # 🖥️🖥️🖥️ GUI窗口里创建一个新的Frame来容纳十神分析结果
    十神分析结果框架 = tk.Frame(分析命盘界面窗口, bg='#f5f5f1')
    十神分析结果框架.pack(pady=(0, 0))  # 设置与上方命局的间距为20像素
    #🖥️已现十神展示区
    已现十神吉凶界面展示文本 = "【已现十神】😐\n"
    for 三天干遍历列表 in ['时干', '月干', '年干']:
        十神 = 八字信息主字典.get(三天干遍历列表).get('十神')
        忌用神归属 = 八字信息主字典.get(三天干遍历列表).get('忌用神归属')
        外环境 = 八字信息主字典.get(三天干遍历列表).get('外环境')
        内环境 = 八字信息主字典.get(三天干遍历列表).get('内环境')
        左环境 = 八字信息主字典.get(三天干遍历列表).get('左环境')
        右环境 = 八字信息主字典.get(三天干遍历列表).get('右环境')
        内环境左环境 = 八字信息主字典.get(三天干遍历列表).get('内环境左环境')
        内环境右环境 = 八字信息主字典.get(三天干遍历列表).get('内环境右环境')

        已现十神吉凶界面展示文本 += f"{三天干遍历列表}👉 {十神}({忌用神归属})。 外环境：{外环境}。 内环境：{内环境}。 左环境：{左环境}。 右环境：{右环境}。 内环境左环境:{内环境左环境}。  内环境右环境:{内环境右环境}\n"
    # 创建已现十神标签并添加到框架中
    已现十神标签 = tk.Label(十神分析结果框架, text=已现十神吉凶界面展示文本, font=("Arial", 9), fg="#7e7e7e", bg='#f5f5f1', justify=tk.LEFT, anchor='w') #"justify=tk.LEFT"代表文本左对齐。"anchor='w'"代表标签内容左对齐
    已现十神标签.pack(padx=50, pady=(0, 10), anchor='w')  # 向左对齐，上下间距10像素         
     #🖥️未现十神展示区
    未现十神吉凶界面展示文本 = "【未现十神】🫥\n"
    for 天干名,子字典 in 未现正偏十神主字典.items():
        十神 = 子字典.get('十神', '')
        忌用神归属 = 子字典.get('忌用神归属', '')
        外环境 = 子字典.get('外环境', '')
        内环境 = 子字典.get('内环境', '')
        左环境 = 子字典.get('左环境')
        右环境 = 子字典.get('右环境')
        内环境左环境 = 子字典.get('内环境左环境')
        内环境右环境 = 子字典.get('内环境右环境')
        未现十神吉凶界面展示文本 += f"{天干名}👉 {十神}({忌用神归属})。 外环境：{外环境}。 内环境：{内环境}。 左环境：{左环境}。 右环境：{右环境}。 内环境左环境:{内环境左环境}。 内环境右环境:{内环境右环境}\n"
    # 创建未现十神标签并添加到框架中
    未现十神标签 = tk.Label(十神分析结果框架, text=未现十神吉凶界面展示文本, font=("Arial", 9), fg="#7e7e7e", bg='#f5f5f1', justify=tk.LEFT, anchor='w')
    未现十神标签.pack(padx=50, pady=(0, 10), anchor='w')  # 向左对齐，上下间距10像素





    # 🖥️🖥️🖥️ 创建一个容器框架来放置所有分析结果和操作区域
    底部操作区域框架 = tk.Frame(分析命盘界面窗口, bg='#f5f5f1')
    底部操作区域框架.pack(fill=tk.BOTH, padx=50, pady=(10, 20))
    # 创建左右分栏框架
    左侧框架 = tk.Frame(底部操作区域框架, bg='#f5f5f1')
    左侧框架.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    右侧框架 = tk.Frame(底部操作区域框架, bg='#f5f5f1')
    右侧框架.pack(side=tk.RIGHT, fill=tk.BOTH)

    # 1.🖥️🖥️🖥️ 创建右侧大运流年选择框架
    选择区域框架 = tk.Frame(右侧框架, bg='#f5f5f1')
    选择区域框架.pack(anchor='e', pady=(10, 0))
    # 2.创建大运选择部分
    大运容器 = tk.Frame(选择区域框架, bg='#f5f5f1')
    大运容器.pack(side=tk.LEFT, padx=(0, 20))
    # 《大运》选择部分
    大运容器 = tk.Frame(选择区域框架, bg='#f5f5f1')
    大运容器.pack(side=tk.LEFT, padx=(0, 20))
    大运按钮 = tk.Button(大运容器, text="大运▼", width=20, bg='white', relief='solid', borderwidth=1)
    大运按钮.pack()
    大运列表框 = tk.Listbox(大运容器, selectmode=tk.MULTIPLE, height=0, width=20)
    已选大运标签 = tk.Label(大运容器, text="", bg='#f5f5f1', width=20)
    已选大运标签.pack()


    # 3.获取大运信息并添加到列表框
    大运信息列表 = []
    global 流年天干字典, 流年地支字典
    流年天干字典 = {}# 更新流年列表函数
    流年地支字典 = {}
    yun = ba.getYun(not options.n)
    for dayun in yun.getDaYun()[1:]:
        age = dayun.getStartAge()
        ganzhi = dayun.getGanZhi()
        year_str = '📒大运'
        大运信息 = f"{age}岁  {year_str}  {ganzhi}"
        大运列表框.insert(tk.END, 大运信息)
        大运信息列表.append(大运信息)
        # 在处理每个大运信息时
        大运天干 = ganzhi[0]  # 取第一个字符作为天干
        大运地支 = ganzhi[1]  # 取第二个字符作为地支
        # 更新大运天干字典
        if 大运天干 not in 大运天干字典:
            大运天干字典[大运天干] = {"阴阳属性": 计算阴阳属性(大运天干), "旺弱状态": "","是否实神": ""}
        # 更新大运地支字典
        if 大运地支 not in 大运地支字典:
            大运地支字典[大运地支] = {"阴阳属性": 计算阴阳属性(大运地支), "旺弱状态": "","是否实神": "","是否空亡": "空亡" if 大运地支 in 地支空亡字典[zhus[2]] else "不空亡"}
            if 大运地支字典[大运地支]["是否空亡"] == "空亡":  # 如果地支空亡，更新旺弱状态
                大运地支字典[大运地支]["旺弱状态"] = "不弱不旺"


    # 4.🖥️🖥️🖥️ 创建流年容器和组件
    流年容器 = tk.Frame(选择区域框架, bg='#f5f5f1')
    流年容器.pack(side=tk.LEFT)
    流年按钮 = tk.Button(流年容器, text="流年▼", width=20, bg='white', relief='solid', borderwidth=1)
    流年按钮.pack()
    流年列表框 = tk.Listbox(流年容器, selectmode=tk.MULTIPLE, height=0, width=20)
    已选流年标签 = tk.Label(流年容器, text="", bg='#f5f5f1', width=20)
    已选流年标签.pack()
    # 流年提示标签放在流年容器下方
    流年提示标签 = tk.Label(流年容器, text="请先选择大运，才能显示对应的流年", font=("Arial", 9), fg="#7e7e7e", bg='#f5f5f1')
    流年提示标签.pack(pady=(5, 0))

    # 定义所有事件处理函数
    def 切换大运列表显示状态(event=None):
        当前高度 = 大运列表框.cget('height')   #控制大运列表的显示和隐藏
        if 当前高度 == 0:
            大运列表框.configure(height=7)  # 显示列表
            大运按钮.configure(text="大运▲")
            大运列表框.pack()  # 显示列表框
        else:
            大运列表框.configure(height=0)  # 隐藏列表
            大运按钮.configure(text="大运▼")


    def 查看大运作用按钮点击():
        global 当前选中大运
        print("🧐🧐🧐🧐🧐🧐🧐测试：查看大运作用按钮被点击了！") 
        if not 当前选中大运:
            print("请先选择一个大运！")
            return

        处理大运作用()
        更新大运作用后的环境结论()

    def 处理大运选择(event):
        global 当前选中大运
        点击索引 = 大运列表框.nearest(event.y)     #处理大运的选择和取消选择
        if 点击索引 in 大运列表框.curselection():
            大运列表框.selection_clear(点击索引)
            当前选中大运 = None  # 清除全局变量中的选择
        else:
            大运列表框.selection_clear(0, tk.END)
            大运列表框.selection_set(点击索引)
            当前选中大运 = 大运列表框.get(点击索引)  
        更新已选大运显示()
    
    def 更新流年列表(event=None):
        global 当前选中大运, 流年天干字典, 流年地支字典
        流年列表框.delete(0, tk.END)
        流年天干字典.clear()
        流年地支字典.clear()
        if 当前选中大运: 
            流年提示标签.pack_forget()
            age = int(当前选中大运.split('岁')[0])

            # 获取原局元素名字列表（用于判断实神）
            原局元素名字列表 = []
            for 位置, 信息 in 八字信息主字典.items():
                # 跳过空亡的地支
                if '支' in 位置 and 信息.get('是否空亡') == '空亡':
                    continue
                名字 = 信息.get('名字')
                if 名字:
                    原局元素名字列表.append(名字)

            for dayun in yun.getDaYun()[1:]:
                if dayun.getStartAge() == age:
                    for liunian in dayun.getLiuNian():
                        current_age = liunian.getAge()
                        if age <= current_age < age + 10:
                            year = str(liunian.getYear())
                            流年天干 = liunian.getGanZhi()[0]
                            流年地支 = liunian.getGanZhi()[1]
                            ganzhi = 流年天干 + 流年地支
                            流年信息 = f"{current_age}岁  {year}  {ganzhi}"
                            流年列表框.insert(tk.END, 流年信息)

                            # 更新流年天干字典
                            if 流年天干 not in 流年天干字典:
                                流年天干字典[流年天干] = {"阴阳属性": 计算阴阳属性(流年天干),
                                    "旺弱状态": "",
                                    "是否实神": "实神" if 流年天干 in 原局元素名字列表 else "虚神"}

                            # 更新流年地支字典
                            if 流年地支 not in 流年地支字典:
                                流年地支字典[流年地支] = {"阴阳属性": 计算阴阳属性(流年地支),
                                    "旺弱状态": "",
                                    "是否实神": "实神" if 流年地支 in 原局元素名字列表 else "虚神",
                                    "是否空亡": "空亡" if 流年地支 in 地支空亡字典[zhus[2]] else "不空亡"}
                                # 如果地支空亡，更新旺弱状态
                                if 流年地支字典[流年地支]["是否空亡"] == "空亡":
                                    流年地支字典[流年地支]["旺弱状态"] = "不弱不旺"

            # 打印调试信息
            #print("\n=== 🌟🌟🌟流年天干字典 ===")
            #for 天干, 属性 in 流年天干字典.items():
                #print(f"{天干}: {属性}")
            #print("\n=== 🌟🌟🌟流年地支字典 ===")
            #for 地支, 属性 in 流年地支字典.items():
                #print(f"{地支}: {属性}")
        else:
            流年提示标签.pack()
            流年列表框.pack_forget()
            流年按钮.configure(text="流年▼")

    # 流年相关函数
    def 切换流年列表显示状态(event=None):      #控制流年列表的显示和隐藏
        当前高度 = 流年列表框.cget('height')        
        if 当前高度 == 0:
            流年列表框.configure(height=5)
            流年按钮.configure(text="流年▲")
            流年列表框.pack()
        else:
            流年列表框.configure(height=0)
            流年按钮.configure(text="流年▼")
            流年列表框.pack_forget()
            更新已选流年显示()

    def 更新已选流年显示():    #更新已选流年标签的显示内容
        global 当前选中流年列表
        选中项 = [流年列表框.get(idx) for idx in 流年列表框.curselection()]
        当前选中流年列表 = 选中项  # 保存选中的流年
        已选流年标签.configure(text=", ".join(选中项) if 选中项 else "")

    def 处理流年选择(event):   #处理流年的选择和取消选择
        点击索引 = 流年列表框.nearest(event.y)
        if 点击索引 in 流年列表框.curselection():
            流年列表框.selection_clear(点击索引)
        else:
            流年列表框.selection_set(点击索引)
        更新已选流年显示()

    # 7.绑定事件
    大运按钮.bind('<Button-1>', 切换大运列表显示状态)
    大运列表框.bind('<Button-1>', 处理大运选择)
    流年按钮.bind('<Button-1>', 切换流年列表显示状态)
    流年列表框.bind('<Button-1>', 处理流年选择)



    # 添加查看大运作用按钮和查看大运流年作用按钮
    查看大运作用按钮 = tk.Button(选择区域框架, text="查看大运作用",command=查看大运作用按钮点击, font=("Arial", 9), bg='white', relief='solid', borderwidth=1)
    查看大运作用按钮.pack(side=tk.LEFT, padx=(20, 0))


     
    def 更新已选大运显示():
        选中项 = [大运列表框.get(idx) for idx in 大运列表框.curselection()]    #获取用户展示最终选择结果选的大运
        已选大运标签.configure(text=", ".join(选中项) if 选中项 else "")   #在界面上显示选的大运
        更新流年列表()       #更新流年的显示

    def 处理空亡特殊情况():
        # 处理大运地支空亡的情况
        for 大运地支, 属性字典 in 大运地支字典.items():
            if 属性字典['是否空亡'] == '空亡':
                # 空亡地支状态设为不弱不旺
                属性字典['旺弱状态'] = '不弱不旺'
                大运地支阴阳 = 属性字典['阴阳属性']
                # 遍历原局地支，处理大运空亡地支对原局地支的作用
                for 原局地支键 in ['年支', '月支', '日支', '时支']:
                    原局地支阴阳 = 八字信息主字典[原局地支键]['阴阳属性']
                    生扶受制关系 = 判断两者是否生扶受制(大运地支, 原局地支键)
                    # 如果原局地支是空亡的，直接设为不弱不旺并跳过
                    if 八字信息主字典[原局地支键]['是否空亡'] == '空亡':
                        八字信息主字典[原局地支键]['旺弱状态'] = '不弱不旺'
                        continue
                    # 处理大运空亡地支对原局地支的作用
                    if 生扶受制关系 == '受制关系':
                        八字信息主字典[原局地支键]['旺弱状态'] = '旺'
                    elif 生扶受制关系 == '生扶关系':
                        八字信息主字典[原局地支键]['旺弱状态'] = '弱'
        # 处理原局空亡地支的特殊情况
        for 地支键, 地支信息 in 八字信息主字典.items():
            if 地支信息.get('是否空亡') == '空亡':
                # 设置空亡地支状态为不弱不旺
                地支信息['旺弱状态'] = '不弱不旺'
                # 找到与空亡地支同柱的天干
                天干键 = 地支键.replace('支', '干')
                # 更新同柱天干的环境状态
                八字信息主字典[天干键]['内环境'] = '不吉不凶'
                八字信息主字典[天干键]['内环境左环境'] = '不吉不凶'
                八字信息主字典[天干键]['内环境右环境'] = '不吉不凶'
                # 更新以该天干为窗口的未现十神的环境状态
                天干名字 = 八字信息主字典[天干键]['名字']
                for 未现十神, 属性 in 未现正偏十神主字典.items():
                    if 属性.get('窗口名字') == 天干名字:
                        属性['内环境'] = '不吉不凶'
                        属性['内环境左环境'] = '不吉不凶'
                        属性['内环境右环境'] = '不吉不凶'
    def 处理实神情况():
        原局元素名字列表 = []
        for 位置, 信息 in 八字信息主字典.items():
            # 跳过空亡的地支
            if '支' in 位置 and 信息.get('是否空亡') == '空亡':
                continue
            # 使用.get()方法，如果没有'名字'键就跳过
            名字 = 信息.get('名字')
            if 名字:  # 只有当名字存在时才添加
                原局元素名字列表.append(名字)
        # 检查大运天干是否为实神
        for 天干, 属性 in 大运天干字典.items():
            if 天干 in 原局元素名字列表:
                属性['是否实神'] = '实神'
            else:
                属性['是否实神'] = '虚神'
        # 检查大运地支是否为实神
        for 地支, 属性 in 大运地支字典.items():
            if 地支 in 原局元素名字列表:
                属性['是否实神'] = '实神'
            else:
                属性['是否实神'] = '虚神'
    def 更新环境吉凶结论():
    # 处理已现十神的各种环境
        for 天干键, 天干信息 in 八字信息主字典.items():
            if '干' not in 天干键:  # 跳过地支
                continue
                
            # 获取相关状态
            外环境 = 天干信息.get('外环境', '')
            内环境 = 天干信息.get('内环境', '')
            左环境 = 天干信息.get('左环境', '')
            右环境 = 天干信息.get('右环境', '')
            内环境左环境 = 天干信息.get('内环境左环境', '')
            内环境右环境 = 天干信息.get('内环境右环境', '')

            # 处理已现十神的外环境
            if 外环境 in ['吉', '凶']:
                旺弱状态 = 天干信息.get('旺弱状态', '')
                if '弱' in 旺弱状态:  # 包括 "弱" 和 "弱+"
                    新环境 = '凶' if 外环境 == '吉' else '吉'
                    天干信息['外环境'] = 新环境 + "+" if "+" in 旺弱状态 else 新环境

            # 处理已现十神的内环境
            if 内环境 in ['吉', '凶']:
                同柱地支键 = 天干键.replace('干', '支')
                地支旺弱状态 = 八字信息主字典[同柱地支键].get('旺弱状态', '')
                if '弱' in 地支旺弱状态:
                    新环境 = '凶' if 内环境 == '吉' else '吉'
                    天干信息['内环境'] = 新环境 + "+" if "+" in 地支旺弱状态 else 新环境

            # 处理已现十神的左环境
            if 左环境 in ['吉', '凶']:
                if 天干键 == '年干':
                    参考天干 = '日干'
                else:
                    天干顺序 = ['年干', '月干', '日干', '时干']
                    当前索引 = 天干顺序.index(天干键)
                    参考天干 = 天干顺序[当前索引 - 1] if 当前索引 > 0 else ''
                
                if 参考天干:
                    参考旺弱状态 = 八字信息主字典[参考天干].get('旺弱状态', '')
                    if '弱' in 参考旺弱状态:
                        新环境 = '凶' if 左环境 == '吉' else '吉'
                        天干信息['左环境'] = 新环境 + "+" if "+" in 参考旺弱状态 else 新环境

            # 处理已现十神的右环境
            if 右环境 in ['吉', '凶']:
                if 天干键 == '时干':
                    参考天干 = '月干'
                else:
                    天干顺序 = ['年干', '月干', '日干', '时干']
                    当前索引 = 天干顺序.index(天干键)
                    参考天干 = 天干顺序[当前索引 + 1] if 当前索引 < 3 else ''
                if 参考天干:
                    参考旺弱状态 = 八字信息主字典[参考天干].get('旺弱状态', '')
                    if '弱' in 参考旺弱状态:
                        新环境 = '凶' if 右环境 == '吉' else '吉'
                        天干信息['右环境'] = 新环境 + "+" if "+" in 参考旺弱状态 else 新环境

            # 处理已现十神的内环境的左环境和右环境
            for 环境键, 环境值 in [('内环境左环境', 内环境左环境), ('内环境右环境', 内环境右环境)]:
                if 环境值 in ['吉', '凶']:
                    同柱地支键 = 天干键.replace('干', '支')
                    地支旺弱状态 = 八字信息主字典[同柱地支键].get('旺弱状态', '')
                    if '弱' in 地支旺弱状态:
                        新环境 = '凶' if 环境值 == '吉' else '吉'
                        天干信息[环境键] = 新环境 + "+" if "+" in 地支旺弱状态 else 新环境

            #处理日干环境吉凶结论
            if 天干键 == '日干': 
                月干旺弱状态 = 八字信息主字典['月干'].get('旺弱状态', '') 
                if '弱' in 月干旺弱状态:     # 处理日干左环境（受月干影响）
                    新环境 = '凶' if 天干信息['左环境'] == '吉' else '吉'
                    天干信息['左环境'] = 新环境 + "+" if "+" in 月干旺弱状态 else 新环境

                时干旺弱状态 = 八字信息主字典['时干'].get('旺弱状态', '')   # 处理日干右环境（受时干影响）
                if '弱' in 时干旺弱状态:
                    新环境 = '凶' if 天干信息['右环境'] == '吉' else '吉'
                    天干信息['右环境'] = 新环境 + "+" if "+" in 时干旺弱状态 else 新环境

                日支旺弱状态 = 八字信息主字典['日支'].get('旺弱状态', '')   # 处理日干内环境（受日支影响）
                if '弱' in 日支旺弱状态:
                    新环境 = '凶' if 天干信息['内环境'] == '吉' else '吉'
                    天干信息['内环境'] = 新环境 + "+" if "+" in 日支旺弱状态 else 新环境

                if '弱' in 日支旺弱状态:
                    for 环境键 in ['内环境左环境', '内环境右环境']:    # 处理内环境的左右环境（仍然受日支状态影响）
                        新环境 = '凶' if 天干信息[环境键] == '吉' else '吉'
                        天干信息[环境键] = 新环境 + "+" if "+" in 日支旺弱状态 else 新环境
            
        # 处理未现十神的各种环境
        for 天干名, 属性子字典 in 未现正偏十神主字典.items():
            窗口名字 = 属性子字典.get('窗口名字', '')
            if not 窗口名字:
                continue
            # 获取窗口十神所在位置和相关信息
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息['名字'] == 窗口名字), None)
            if not 窗口位置:
                continue
            # 处理未现十神的外环境
            外环境 = 属性子字典.get('外环境', '')
            if 外环境 in ['吉', '凶']:
                窗口旺弱状态 = 八字信息主字典[窗口位置].get('旺弱状态', '')
                if '弱' in 窗口旺弱状态:
                    新环境 = '凶' if 外环境 == '吉' else '吉'
                    属性子字典['外环境'] = 新环境 + "+" if "+" in 窗口旺弱状态 else 新环境
            # 处理未现十神的内环境
            内环境 = 属性子字典.get('内环境', '')
            if 内环境 in ['吉', '凶']:
                窗口地支键 = 窗口位置.replace('干', '支')
                地支旺弱状态 = 八字信息主字典[窗口地支键].get('旺弱状态', '')
                if '弱' in 地支旺弱状态:
                    新环境 = '凶' if 内环境 == '吉' else '吉'
                    属性子字典['内环境'] = 新环境 + "+" if "+" in 地支旺弱状态 else 新环境
            # 处理未现十神的左环境
            左环境 = 属性子字典.get('左环境', '')
            if 左环境 in ['吉', '凶']:
                if 窗口位置 == '年干':
                    参考旺弱状态 = 八字信息主字典['日干'].get('旺弱状态', '')
                else:
                    天干顺序 = ['年干', '月干', '日干', '时干']
                    窗口索引 = 天干顺序.index(窗口位置)
                    左边位置 = 天干顺序[窗口索引 - 1] if 窗口索引 > 0 else None
                    参考旺弱状态 = 八字信息主字典[左边位置].get('旺弱状态', '') if 左边位置 else ''

                if '弱' in 参考旺弱状态:
                    新环境 = '凶' if 左环境 == '吉' else '吉'
                    属性子字典['左环境'] = 新环境 + "+" if "+" in 参考旺弱状态 else 新环境
            # 处理未现十神的右环境
            右环境 = 属性子字典.get('右环境', '')
            if 右环境 in ['吉', '凶']:
                if 窗口位置 == '时干':
                    参考旺弱状态 = 八字信息主字典['月干'].get('旺弱状态', '')
                else:
                    天干顺序 = ['年干', '月干', '日干', '时干']
                    窗口索引 = 天干顺序.index(窗口位置)
                    右边位置 = 天干顺序[窗口索引 + 1] if 窗口索引 < 3 else None
                    参考旺弱状态 = 八字信息主字典[右边位置].get('旺弱状态', '') if 右边位置 else ''

                if '弱' in 参考旺弱状态:
                    新环境 = '凶' if 右环境 == '吉' else '吉'
                    属性子字典['右环境'] = 新环境 + "+" if "+" in 参考旺弱状态 else 新环境
            # 处理未现十神的内环境的左右环境
            for 环境键, 特殊位置 in [('内环境左环境', '年干'), ('内环境右环境', '时干')]:
                环境值 = 属性子字典.get(环境键, '')
                if 环境值 in ['吉', '凶']:
                    窗口地支键 = 窗口位置.replace('干', '支')
                    if 窗口位置 == 特殊位置:
                        参考地支键 = '日支'
                    else:
                        地支顺序 = ['年支', '月支', '日支', '时支']
                        窗口索引 = 地支顺序.index(窗口地支键)
                        参考索引 = 窗口索引 - 1 if '左' in 环境键 else 窗口索引 + 1
                        参考地支键 = 地支顺序[参考索引] if 0 <= 参考索引 < 4 else None
                    if 参考地支键:
                        参考旺弱状态 = 八字信息主字典[参考地支键].get('旺弱状态', '')
                        if '弱' in 参考旺弱状态:
                            新环境 = '凶' if 环境值 == '吉' else '吉'
                            属性子字典[环境键] = 新环境 + "+" if "+" in 参考旺弱状态 else 新环境
    def 更新干支旺弱状态(大运干支, 原局干支, 大运阴阳, 原局阴阳):
        生扶受制关系 = 判断两者是否生扶受制(大运干支, 原局干支)
        是同性作用 = (大运阴阳 == 原局阴阳)
        
        # 判断是否为实神
        是实神 = False
        if 大运干支 in 大运天干字典:
            是实神 = 大运天干字典[大运干支]['是否实神'] == '实神'
        elif 大运干支 in 大运地支字典:
            是实神 = 大运地支字典[大运干支]['是否实神'] == '实神'
        
        # 确定基础旺弱状态
        if 生扶受制关系 == '生扶关系':
            基础状态 = "旺" if 是同性作用 else "弱"
        elif 生扶受制关系 == '受制关系':
            基础状态 = "弱" if 是同性作用 else "旺"
        
        # 如果是实神，添加"+"标记
        最终状态 = 基础状态 + "+" if 是实神 else 基础状态
        八字信息主字典[原局干支]['旺弱状态'] = 最终状态 
    def 处理大运作用():     # 更新原局干支的旺弱状态
        global 当前选中大运
        if 当前选中大运:
            print(f"🥔🥔🥔选中大运: {当前选中大运}")
            print("🥔🥔🥔开始处理大运作用……")
            处理空亡特殊情况()
            处理实神情况() 
            大运干支 = 大运信息.split()[-1]
            大运天干 = 大运干支[0]
            大运地支 = 大运干支[1]
            # 添加安全检查
            if 大运天干 not in 大运天干字典:
                print(f"警告：{大运天干}不在大运天干字典中")
            if 大运地支 not in 大运地支字典:
                print(f"警告：{大运地支}不在大运地支字典中")
            大运天干阴阳 = 大运天干字典[大运天干]['阴阳属性']
            大运地支阴阳 = 大运地支字典[大运地支]['阴阳属性']
            for 原局天干 in ['年干', '月干', '日干', '时干']:
                原局天干阴阳 = 八字信息主字典[原局天干]['阴阳属性']
                更新干支旺弱状态(大运天干, 原局天干, 大运天干阴阳, 原局天干阴阳)
            for 原局地支 in ['年支', '月支', '日支', '时支']:
                原局地支阴阳 = 八字信息主字典[原局地支]['阴阳属性']
                更新干支旺弱状态(大运地支, 原局地支, 大运地支阴阳, 原局地支阴阳)
        else:
            print("🥔🥔🥔没有选中任何大运！")  # 调试语句
        更新环境吉凶结论()

    def 更新大运作用后的环境结论():
        import contextlib
        global 当前选中大运
        if not 当前选中大运:
            print("🥔🥔🥔请先选择一个大运！")  # 调试语句
            return
        大运干支 = 当前选中大运.split()[-1]
        大运天干 = 大运干支[0]
        大运地支 = 大运干支[1]
        
        print(f"👼👼👼\n{大运干支}大运作用到原局后，原局各种环境的结论如下：")
        
        print("\n=== 😐 已现十神的环境 ===")
        with contextlib.redirect_stdout(None):
            外环境结论 = 分析天干十神的外环境吉凶()
            内环境结论 = 分析天干十神的内环境吉凶()
            左环境结论 = 分析天干十神的左环境吉凶()
            右环境结论 = 分析天干十神的右环境吉凶()
            内环境左环境结论 = 分析天干十神的内环境的左环境吉凶()
            内环境右环境结论 = 分析天干十神的内环境右环境吉凶()
        for 天干 in ['时干', '月干', '年干']:
            天干名字 = 八字信息主字典[天干]['名字']
            十神 = 八字信息主字典[天干]['十神']
            旺弱状态 = 八字信息主字典[天干].get('旺弱状态', '')
            外环境 = 八字信息主字典[天干].get('外环境', '')
            内环境 = 八字信息主字典[天干].get('内环境', '')
            左环境 = 八字信息主字典[天干].get('左环境', '')
            右环境 = 八字信息主字典[天干].get('右环境', '')
            内环境左环境 = 八字信息主字典[天干].get('内环境左环境', '')
            内环境右环境 = 八字信息主字典[天干].get('内环境右环境', '')
            同柱地支键 = 天干.replace('干', '支')
            地支旺弱状态 = 八字信息主字典[同柱地支键].get('旺弱状态', '')
            
            # 处理外环境
            if 旺弱状态:
                if '弱' in 旺弱状态:
                    新环境 = '凶' if 外环境 == '吉' else '吉'
                    if '+' in 旺弱状态:
                        新环境 += '+'
                else:
                    新环境 = 外环境
                    if '+' in 旺弱状态:
                        新环境 += '+'
            else:
                新环境 = 外环境
            
            # 处理内环境
            if 地支旺弱状态:
                if '弱' in 地支旺弱状态:
                    新内环境 = '凶' if 内环境 == '吉' else '吉'
                    if '+' in 地支旺弱状态:
                        新内环境 += '+'
                else:
                    新内环境 = 内环境
                    if '+' in 地支旺弱状态:
                        新内环境 += '+'
            else:
                新内环境 = 内环境
            
            # 处理左环境
            if 旺弱状态:
                if '弱' in 旺弱状态:
                    新左环境 = '凶' if 左环境 == '吉' else '吉'
                    if '+' in 旺弱状态:
                        新左环境 += '+'
                else:
                    新左环境 = 左环境
                    if '+' in 旺弱状态:
                        新左环境 += '+'
            else:
                新左环境 = 左环境
            
            # 处理右环境
            if 旺弱状态:
                if '弱' in 旺弱状态:
                    新右环境 = '凶' if 右环境 == '吉' else '吉'
                    if '+' in 旺弱状态:
                        新右环境 += '+'
                else:
                    新右环境 = 右环境
                    if '+' in 旺弱状态:
                        新右环境 += '+'
            else:
                新右环境 = 右环境
            
            # 处理内环境左环境
            if 地支旺弱状态:
                if '弱' in 地支旺弱状态:
                    新内环境左环境 = '凶' if 内环境左环境 == '吉' else '吉'
                    if '+' in 地支旺弱状态:
                        新内环境左环境 += '+'
                else:
                    新内环境左环境 = 内环境左环境
                    if '+' in 地支旺弱状态:
                        新内环境左环境 += '+'
            else:
                新内环境左环境 = 内环境左环境
                
            # 处理内环境右环境
            if 地支旺弱状态:
                if '弱' in 地支旺弱状态:
                    新内环境右环境 = '凶' if 内环境右环境 == '吉' else '吉'
                    if '+' in 地支旺弱状态:
                        新内环境右环境 += '+'
                else:
                    新内环境右环境 = 内环境右环境
                    if '+' in 地支旺弱状态:
                        新内环境右环境 += '+'
            else:
                新内环境右环境 = 内环境右环境

            print(f"\n《原局已现十神外环境作用路径》：{外环境结论[天干]['作用路径']}")
            print(f"\n《原局已现十神内环境作用路径》：{内环境结论[天干]['作用路径']}")
            print(f"\n《原局已现十神左环境作用路径》：{左环境结论[天干]['作用路径']}")
            print(f"\n《原局已现十神右环境作用路径》：{右环境结论[天干]['作用路径']}")
            print(f"\n《原局已现十神内环境左环境作用路径》：{内环境左环境结论[天干]['作用路径']}")
            print(f"\n《原局已现十神内环境右环境作用路径》：{内环境右环境结论[天干]['作用路径']}")

                
            # 判断是否为实神
            是实神 = False
            if 大运干支[0] in 大运天干字典:
                是实神 = 大运天干字典[大运干支[0]]['是否实神'] == '实神'
            
            print(f"\n《大运作用后的外环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{天干}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】外环境为【{新环境}】")
            
            print(f"\n《大运作用后的内环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】内环境为【{新内环境}】")
            
            print(f"\n《大运作用后的左环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{天干}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】左环境为【{新左环境}】")

            print(f"\n《大运作用后的右环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{天干}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】右环境为【{新右环境}】")

            print(f"\n《大运作用后的内环境的左环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】内环境左环境为【{新内环境左环境}】")
            
            print(f"\n《大运作用后的内环境的右环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴【{天干}】【{天干名字}】【{十神}】内环境右环境为【{新内环境右环境}】")
            
        else:
            print(f" ∴【{天干}】【{天干名字}】【{十神}】外环境为【{外环境}】")
            print(f" ∴【{天干}】【{天干名字}】【{十神}】内环境为【{内环境}】")
            print(f" ∴【{天干}】【{天干名字}】【{十神}】左环境为【{左环境}】")
            print(f" ∴【{天干}】【{天干名字}】【{十神}】右环境为【{右环境}】")
            print(f" ∴【{天干}】【{天干名字}】【{十神}】内环境左环境为【{内环境左环境}】")
            print(f" ∴【{天干}】【{天干名字}】【{十神}】内环境右环境为【{内环境右环境}】")




        print("\n=== 🫥 未现十神的环境 ===")
        with contextlib.redirect_stdout(None):
            未现外环境结论 = 分析未现天干十神的外环境吉凶()
            未现内环境结论 = 分析未现天干十神的内环境吉凶()
            未现左环境结论 = 分析未现天干十神的左环境吉凶()
            未现右环境结论 = 分析未现天干十神的右环境吉凶()
            未现内环境左环境结论 = 分析未现天干十神的内环境的左环境()
            未现内环境右环境结论 = 分析未现天干十神的内环境的右环境()

        # 获取所有未现十神的列表
        未现十神列表 = list(未现正偏十神主字典.keys())

        # 处理地支旺弱状态对未现十神内环境的影响
        for 天干名 in 未现十神列表:
            属性子字典 = 未现正偏十神主字典[天干名]
            窗口名字 = 属性子字典.get('窗口名字')
            十神 = 属性子字典.get('十神') 
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), None)  # 找到窗口十神对应的位置
            同柱地支键 = 窗口位置.replace('干', '支') if 窗口位置 else ''
            地支旺弱状态 = 八字信息主字典[同柱地支键].get('旺弱状态') if 同柱地支键 else ''
            天干旺弱状态 = 八字信息主字典[窗口位置].get('旺弱状态') if 窗口位置 else ''
            if 窗口位置:
                地支位置 = 窗口位置.replace('干', '支')   # 获取同柱地支的位置
                地支旺弱状态 = 八字信息主字典[地支位置].get('旺弱状态')  # 获取地支的旺弱状态
                天干旺弱状态 = 八字信息主字典[窗口位置].get('旺弱状态') 
                

                # 如果窗口十神的天干是弱，则反转外环境吉凶
                if '弱' in 天干旺弱状态:
                    原外环境 = 属性子字典.get('外环境', '')
                    if 原外环境 == '吉':
                        属性子字典['外环境'] = '凶'
                    elif 原外环境 == '凶':
                        属性子字典['外环境'] = '吉'
                    # 如果天干旺弱状态带有'+'，则在新内环境后也加上'+'
                    if '+' in 地支旺弱状态:
                        属性子字典['外环境'] += '+'

                # 如果地支是弱，则反转内环境吉凶
                if '弱' in 地支旺弱状态:
                    原内环境 = 属性子字典.get('内环境', '')
                    if 原内环境 == '吉':
                        属性子字典['内环境'] = '凶'
                    elif 原内环境 == '凶':
                        属性子字典['内环境'] = '吉'
                    # 如果地支旺弱状态带有'+'，则在新内环境后也加上'+'
                    if '+' in 地支旺弱状态:
                        属性子字典['内环境'] += '+'

                # 处理未现十神左环境
                天干顺序 = ['年干', '月干', '日干', '时干']
                窗口位置 = next((位置 for 位置, 干名 in zip(天干顺序, 本命盘四个天干名字列表) if 干名 == 窗口名字), None)
                if 窗口位置 == '年干':
                    # 特殊情况：窗口十神在年干
                    月干旺弱状态 = 八字信息主字典['月干'].get('旺弱状态', '')
                    日干旺弱状态 = 八字信息主字典['日干'].get('旺弱状态', '')
                    
                    # 根据日干和月干的旺弱状态调整左环境
                    if ('弱' in 日干旺弱状态 and '弱' in 月干旺弱状态):
                        原左环境 = 属性子字典.get('左环境', '')
                        if 原左环境 == '吉':
                            属性子字典['左环境'] = '凶'
                        elif 原左环境 == '凶':
                            属性子字典['左环境'] = '吉'
                        # 如果两个旺弱状态都带有'+'，则在新左环境后也加上'+'
                        if '+' in 日干旺弱状态 and '+' in 月干旺弱状态:
                            属性子字典['左环境'] += '+'
                else:
                    # 普通情况：找到左侧位置的旺弱状态
                    窗口索引 = 天干顺序.index(窗口位置) if 窗口位置 else -1
                    if 窗口索引 > 0:
                        左侧位置 = 天干顺序[窗口索引 - 1]
                        左侧旺弱状态 = 八字信息主字典[左侧位置].get('旺弱状态')
                        
                        # 如果左侧位置的旺弱状态是'弱'或'弱+'，反转左环境结论
                        if '弱' in 左侧旺弱状态:
                            原左环境 = 属性子字典.get('左环境')
                            if 原左环境 == '吉':
                                属性子字典['左环境'] = '凶'
                            elif 原左环境 == '凶':
                                属性子字典['左环境'] = '吉'
                            # 如果旺弱状态带有'+'，则在新左环境后也加上'+'
                            if '+' in 左侧旺弱状态:
                                属性子字典['左环境'] += '+'

                # 处理未现十神右环境
                if 窗口位置 == '时干':
                    # 特殊情况：窗口十神在时干
                    月干旺弱状态 = 八字信息主字典['月干'].get('旺弱状态')
                    日干旺弱状态 = 八字信息主字典['日干'].get('旺弱状态')
                    
                    # 根据月干和日干的旺弱状态调整右环境
                    if ('弱' in 月干旺弱状态 and '弱' in 日干旺弱状态):
                        原右环境 = 属性子字典.get('右环境')
                        if 原右环境 == '吉':
                            属性子字典['右环境'] = '凶'
                        elif 原右环境 == '凶':
                            属性子字典['右环境'] = '吉'
                        # 如果两个旺弱状态都带有'+'，则在新右环境后也加上'+'
                        if '+' in 月干旺弱状态 and '+' in 日干旺弱状态:
                            属性子字典['右环境'] += '+'
                else:
                    # 普通情况：找到右侧位置的旺弱状态
                    窗口索引 = 天干顺序.index(窗口位置) if 窗口位置 else -1
                    if 窗口索引 < len(天干顺序) - 1:
                        右侧位置 = 天干顺序[窗口索引 + 1]
                        右侧旺弱状态 = 八字信息主字典[右侧位置].get('旺弱状态', '')             
                        # 如果右侧位置的旺弱状态是'弱'或'弱+'，反转右环境结论
                        if '弱' in 右侧旺弱状态:
                            原右环境 = 属性子字典.get('右环境', '')
                            if 原右环境 == '吉':
                                属性子字典['右环境'] = '凶'
                            elif 原右环境 == '凶':
                                属性子字典['右环境'] = '吉'
                            # 如果旺弱状态带有'+'，则在新右环境后也加上'+'
                            if '+' in 右侧旺弱状态:
                                属性子字典['右环境'] += '+'  

                # 处理未现十神的内环境的左环境
                if 窗口位置 == '年干':
                    # 特殊情况：窗口在年干
                    日支旺弱状态 = 八字信息主字典['日支'].get('旺弱状态', '')
                    月支旺弱状态 = 八字信息主字典['月支'].get('旺弱状态', '')
                    
                    if ('弱' in 日支旺弱状态 and '弱' in 月支旺弱状态):
                        原内环境左环境 = 属性子字典.get('内环境左环境', '')
                        if 原内环境左环境 == '吉':
                            属性子字典['内环境左环境'] = '凶'
                        elif 原内环境左环境 == '凶':
                            属性子字典['内环境左环境'] = '吉'
                        if '+' in 日支旺弱状态 and '+' in 月支旺弱状态:
                            属性子字典['内环境左环境'] += '+'
                else:
                    # 普通情况
                    地支顺序 = ['年支', '月支', '日支', '时支']
                    同柱地支 = 窗口位置.replace('干', '支')
                    地支索引 = 地支顺序.index(同柱地支)
                    if 地支索引 > 0:
                        左侧地支位置 = 地支顺序[地支索引 - 1]
                        左侧地支旺弱状态 = 八字信息主字典[左侧地支位置].get('旺弱状态', '')
                        if '弱' in 左侧地支旺弱状态:
                            原内环境左环境 = 属性子字典.get('内环境左环境', '')
                            if 原内环境左环境 == '吉':
                                属性子字典['内环境左环境'] = '凶'
                            elif 原内环境左环境 == '凶':
                                属性子字典['内环境左环境'] = '吉'
                            if '+' in 左侧地支旺弱状态:
                                属性子字典['内环境左环境'] += '+'

            # 处理未现十神的内环境的右环境
            if 窗口位置 == '时干':
                # 特殊情况：窗口在时干
                月支旺弱状态 = 八字信息主字典['月支'].get('旺弱状态', '')
                日支旺弱状态 = 八字信息主字典['日支'].get('旺弱状态', '')
                
                if ('弱' in 月支旺弱状态 and '弱' in 日支旺弱状态):
                    原内环境右环境 = 属性子字典.get('内环境右环境', '')
                    if 原内环境右环境 == '吉':
                        属性子字典['内环境右环境'] = '凶'
                    elif 原内环境右环境 == '凶':
                        属性子字典['内环境右环境'] = '吉'
                    if '+' in 月支旺弱状态 and '+' in 日支旺弱状态:
                        属性子字典['内环境右环境'] += '+'
            else:
                # 普通情况
                地支顺序 = ['年支', '月支', '日支', '时支']
                同柱地支 = 窗口位置.replace('干', '支')
                地支索引 = 地支顺序.index(同柱地支)
                
                if 地支索引 < len(地支顺序) - 1:
                    右侧地支位置 = 地支顺序[地支索引 + 1]
                    右侧地支旺弱状态 = 八字信息主字典[右侧地支位置].get('旺弱状态', '')
                    
                    if '弱' in 右侧地支旺弱状态:
                        原内环境右环境 = 属性子字典.get('内环境右环境', '')
                        if 原内环境右环境 == '吉':
                            属性子字典['内环境右环境'] = '凶'
                        elif 原内环境右环境 == '凶':
                            属性子字典['内环境右环境'] = '吉'
                        if '+' in 右侧地支旺弱状态:
                            属性子字典['内环境右环境'] += '+'


            print(f"\n《原局未现十神外环境作用路径》：{未现外环境结论[天干名]['作用路径']}")
            print(f"\n《原局未现十神内环境作用路径》：{未现内环境结论[天干名]['作用路径']}")
            print(f"\n《原局未现十神左环境作用路径》：{未现左环境结论[天干名]['作用路径']}")
            print(f"\n《原局未现十神右环境作用路径》：{未现右环境结论[天干名]['作用路径']}")
            print(f"\n《原局未现十神内环境左环境作用路径》：{未现内环境左环境结论[天干名]['作用路径']}")
            print(f"\n《原局未现十神内环境右环境作用路径》：{未现内环境右环境结论[天干名]['作用路径']}")



            # 判断是否为实神
            是实神 = False
            if 大运干支[0] in 大运天干字典:
                是实神 = 大运天干字典[大运干支[0]]['是否实神'] == '实神'
            
            print(f"\n《大运作用后未现十神的外环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{天干名}】【{十神}】状态为【{天干旺弱状态}】")
            print(f" ∴【{天干名}】【{十神}】外环境为【{属性子字典.get('外环境')}】")
            
            print(f"\n《大运作用后未现十神的内环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，使【{窗口名字}】同柱地支【{同柱地支键}】状态为【{地支旺弱状态}】")
            print(f" ∴【{天干名}】【{十神}】内环境为【{属性子字典.get('内环境')}】")

            print(f"\n《大运作用后未现十神的左环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，" + (f"使【日干】状态为【{日干旺弱状态}】，【月干】状态为【{月干旺弱状态}】" if 窗口位置 == '年干' else f"使左侧【{天干顺序[窗口索引 - 1] if 窗口索引 > 0 else '无'}】状态为【{左侧旺弱状态 if 窗口索引 > 0 else '无'}】"))
            print(f" ∴【{天干名}】【{十神}】左环境为【{属性子字典.get('左环境')}】")

            print(f"\n《大运作用后未现十神的右环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，" + (f"使【月干】状态为【{月干旺弱状态}】，【日干】状态为【{日干旺弱状态}】" if 窗口位置 == '时干' else f"使右侧【{天干顺序[窗口索引 + 1] if 窗口索引 < len(天干顺序) - 1 else '无'}】状态为【{右侧旺弱状态 if 窗口索引 < len(天干顺序) - 1 else '无'}】"))
            print(f" ∴【{天干名}】【{十神}】右环境为【{属性子字典.get('右环境')}】")

            print(f"\n《大运作用后未现十神的内环境左环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，" + (f"使【日支】状态为【{日支旺弱状态}】，【月支】状态为【{月支旺弱状态}】" if 窗口位置 == '年干' else f"使左侧地支【{左侧地支位置 if 地支索引 > 0 else '无'}】状态为【{左侧地支旺弱状态 if 地支索引 > 0 else '无'}】"))
            print(f" ∴【{天干名}】【{十神}】内环境左环境为【{属性子字典.get('内环境左环境')}】")

            print(f"\n《大运作用后未现十神的内环境右环境结果》：∵【{大运干支}】大运{'(实神)' if 是实神 else ''}作用于原局后，" + (f"使【月支】状态为【{月支旺弱状态}】，【日支】状态为【{日支旺弱状态}】" if 窗口位置 == '时干' else f"使右侧地支【{右侧地支位置 if 地支索引 < len(地支顺序) - 1 else '无'}】状态为【{右侧地支旺弱状态 if 地支索引 < len(地支顺序) - 1 else '无'}】"))
            print(f" ∴【{天干名}】【{十神}】内环境右环境为【{属性子字典.get('内环境右环境')}】")




        print("\n===🤠日干的环境 ===")
        日干信息 = 八字信息主字典['日干']
        原始结论 = 判断日主自身状态()['作用路径说明']
        大运天干 = 大运干支[0]
        大运地支 = 大运干支[1]

        print(f"日干【{日干信息['名字']}】在【{大运干支}】作用后的环境：")

        # 外环境部分
        月干关系 = '生' if 判断两者是否生扶受制(大运天干, '月干') == '生扶关系' else '制'
        时干关系 = '生' if 判断两者是否生扶受制(大运天干, '时干') == '生扶关系' else '制'
        print(f"《原局日主外环境作用路径》：{原始结论['外环境说明']} \n《大运作用后 日主外环境的结果》： ∵【{大运干支}】大运作用于原局后，【{月干关系}】月干，【{时干关系}】时干， ∴日干的左环境为【{日干信息['左环境']}】，日干的右环境为【{日干信息['右环境']}】")

        # 内环境部分
        日支关系 = '生' if 判断两者是否生扶受制(大运天干, '日支') == '生扶关系' else '制'
        print(f"《原局日主内环境作用路径》：{原始结论['内环境说明']} \n《大运作用后 日主内环境的结果》：∵【{大运干支}】大运作用于原局后，【{日支关系}】日支， ∴日干的内环境为【{日干信息['内环境']}】")

        # 内环境扩展部分
        月支关系 = '生' if 判断两者是否生扶受制(大运地支, '月支') == '生扶关系' else '制'
        时支关系 = '生' if 判断两者是否生扶受制(大运地支, '时支') == '生扶关系' else '制'
        print(f"《原局日主内环境的左环境/右环境作用路径》：{原始结论['内环境扩展说明']} \n《大运作用后 日主内环境的左环境/右环境的结果》：∵【{大运干支}】大运作用于原局后，【{月支关系}】月支，【{时支关系}】时支， ∴日干内环境的左环境为【{日干信息['内环境左环境']}】，日干内环境的右环境为【{日干信息['内环境右环境']}】")



    def 处理大运流年共同作用():
        if not 当前选中流年列表:  # 使用保存的流年列表
            print("请先选择流年！")
            return

        # 获取当前选中的大运信息
        大运干支 = 当前选中大运.split()[-1]
        大运天干 = 大运干支[0]
        大运地支 = 大运干支[1]
        大运天干属性 = 大运天干字典[大运天干]
        大运天干属性['名字'] = 大运天干
        大运地支属性 = 大运地支字典[大运地支]
        大运地支属性['名字'] = 大运地支

        for 位置 in ['年支', '月支', '日支', '时支']:   # 先处理原局空亡地支
            地支属性 = 八字信息主字典[位置]
            if 地支属性.get('是否空亡') == '空亡':
                地支属性['旺弱状态'] = '不旺不弱'

        # 获取原局天干的阴阳属性列表
        原局天干阴阳列表 = [八字信息主字典[位置]['阴阳属性'] for 位置 in ['年干', '月干', '日干', '时干']]
        if 原局天干阴阳列表.count('阴') == 4:
            原局属性 = '全阴'
        elif 原局天干阴阳列表.count('阳') == 4:
            原局属性 = '全阳'
        else:
            原局属性 = '有阴有阳'

        # 遍历选中的流年
        for 流年信息 in 当前选中流年列表:
            流年干支 = 流年信息.split()[-1]
            流年天干 = 流年干支[0]
            流年地支 = 流年干支[1]
            流年天干属性 = 流年天干字典[流年天干]
            流年天干属性['名字'] = 流年天干
            流年地支属性 = 流年地支字典[流年地支]
            流年地支属性['名字'] = 流年地支

            # 判断大运和流年天干、地支的实虚神属性和阴阳属性
            大运天干实虚 = 大运天干属性['是否实神']
            流年天干实虚 = 流年天干属性['是否实神']
            大运地支实虚 = 大运地支属性['是否实神']
            流年地支实虚 = 流年地支属性['是否实神']
            大运地支空亡 = 大运地支属性.get('是否空亡', '不空亡')
            流年地支空亡 = 流年地支属性.get('是否空亡', '不空亡')

            # 处理天干部分
            if 大运天干实虚 == '实神' or 流年天干实虚 == '实神':
                # 优先处理实神
                处理实神天干(大运天干属性, 流年天干属性)
            else:
                # 按照阴阳属性处理
                处理天干阴阳(原局属性, 大运天干属性, 流年天干属性)

            # 处理地支部分
            if 大运地支实虚 == '实神' or 流年地支实虚 == '实神':
                # 优先处理实神
                处理实神地支(大运地支属性, 流年地支属性)
            elif 大运地支空亡 == '空亡' or 流年地支空亡 == '空亡':
                # 处理空亡情况
                处理地支空亡(大运地支属性, 流年地支属性)
            else:
                # 按照阴阳属性处理
                处理地支阴阳(原局属性, 大运地支属性, 流年地支属性)

        # 处理天干作用原局
        天干作用原局(大运天干属性)
        天干作用原局(流年天干属性)

        for 位置 in ['年支', '月支', '日支', '时支']:   # 处理地支作用原局
            原局地支属性 = 八字信息主字典[位置]
            if 原局地支属性.get('是否空亡') != '空亡':     # 空亡地支不参与作用
                判断地支作用(大运地支属性, 流年地支属性, 原局地支属性)

        更新大运流年共同作用后的环境吉凶结论()
        print(f"处理完毕：{流年信息}的环境吉凶已更新。")
    def 更新大运流年共同作用后的环境吉凶结论():
        import contextlib
        global 当前选中流年列表
        if not 当前选中流年列表:
            print("请先选择流年！")
            return
        大运干支 = 当前选中大运.split()[-1]
        流年信息 = 当前选中流年列表[-1]
        流年干支 = 流年信息.split()[-1]  # 获取干支部分
        print(f"👼👼👼\n【大运:{大运干支} +流年:{流年干支}】大运作用到原局后，原局各种环境的结论如下：")
        with contextlib.redirect_stdout(None):
            外环境结论 = 分析天干十神的外环境吉凶()
            内环境结论 = 分析天干十神的内环境吉凶()
            左环境结论 = 分析天干十神的左环境吉凶()
            右环境结论 = 分析天干十神的右环境吉凶()
            内环境左环境结论 = 分析天干十神的内环境的左环境吉凶()
            内环境右环境结论 = 分析天干十神的内环境右环境吉凶()
    
        for 位置 in ['时干', '月干', '年干']:  # 不包含日干
            天干信息 = 八字信息主字典[位置]
            if '干' not in 位置:
                continue

        print("\n=== 😐 已现十神的环境 ===")
        with contextlib.redirect_stdout(None):   # 1. 先获取环境结论
            外环境结论 = 分析天干十神的外环境吉凶()
            内环境结论 = 分析天干十神的内环境吉凶()
            左环境结论 = 分析天干十神的左环境吉凶()
            右环境结论 = 分析天干十神的右环境吉凶()
            内环境左环境结论 = 分析天干十神的内环境的左环境吉凶()
            内环境右环境结论 = 分析天干十神的内环境右环境吉凶()
        
        天干顺序 = ['年干', '月干', '时干']      # 2. 处理各个位置的环境
        for 位置 in 天干顺序:
            天干信息 = 八字信息主字典[位置]
            同柱地支键 = 位置.replace('干', '支')
            地支旺弱状态 = 八字信息主字典[同柱地支键].get('旺弱状态', '')
            旺弱状态 = 天干信息.get('旺弱状态', '')

            # 打印环境结论
            print(f"\n《原局已现十神外环境作用路径》：{外环境结论[位置]['作用路径']}")
            print(f"\n《原局已现十神内环境作用路径》：{内环境结论[位置]['作用路径']}")
            print(f"\n《原局已现十神左环境作用路径》：{左环境结论[位置]['作用路径']}")
            print(f"\n《原局已现十神右环境作用路径》：{右环境结论[位置]['作用路径']}")
            print(f"\n《原局已现十神内环境左环境作用路径》：{内环境左环境结论[位置]['作用路径']}")
            print(f"\n《原局已现十神内环境右环境作用路径》：{内环境右环境结论[位置]['作用路径']}")
            
            # 处理外环境
            if '弱' in 旺弱状态:
                原外环境 = 天干信息.get('外环境')
                if 原外环境 in ['吉', '凶']:
                    新环境 = '凶' if 原外环境 == '吉' else '吉'
                    天干信息['外环境'] = 新环境 + '+' if '+' in 旺弱状态 else 新环境
                    
            # 处理内环境
            if 地支旺弱状态 and '弱' in 地支旺弱状态:
                原内环境 = 天干信息.get('内环境')
                if 原内环境 in ['吉', '凶']:
                    新环境 = '凶' if 原内环境 == '吉' else '吉'
                    天干信息['内环境'] = 新环境 + '+' if '+' in 地支旺弱状态 else 新环境

            # 处理左环境
            if 地支旺弱状态 and '弱' in 旺弱状态:
                原左环境 = 天干信息.get('左环境')
                if 原左环境 in ['吉', '凶']:
                    新环境 = '凶' if 原左环境 == '吉' else '吉'
                    天干信息['左环境'] = 新环境 + '+' if '+' in 旺弱状态 else 新环境
            
            # 处理右环境
            if 地支旺弱状态 and '弱' in 旺弱状态:
                原右环境 = 天干信息.get('右环境')
                if 原右环境 in ['吉', '凶']:
                    新环境 = '凶' if 原右环境 == '吉' else '吉'
                    天干信息['右环境'] = 新环境 + '+' if '+' in 旺弱状态 else 新环境
            
            # 处理内环境左环境
            if 地支旺弱状态 and '弱' in 地支旺弱状态:
                原内环境左环境 = 天干信息.get('内环境左环境')
                if 原内环境左环境 in ['吉', '凶']:
                    新环境 = '凶' if 原内环境左环境 == '吉' else '吉'
                    天干信息['内环境左环境'] = 新环境 + '+' if '+' in 地支旺弱状态 else 新环境
                
            # 处理内环境右环境
            if 地支旺弱状态 and '弱' in 地支旺弱状态:
                原内环境右环境 = 天干信息.get('内环境右环境')
                if 原内环境右环境 in ['吉', '凶']:
                    新环境 = '凶' if 原内环境右环境 == '吉' else '吉'
                    天干信息['内环境右环境'] = 新环境 + '+' if '+' in 地支旺弱状态 else 新环境


            # 4. 处理环境变化
            天干名字 = 天干信息['名字']
            十神 = 天干信息['十神']
            
            print(f"\n《大运流年作用后的外环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{位置}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴外环境为【{天干信息['外环境']}】")
            print(f"\n《大运流年作用后的内环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴内环境为【{天干信息['内环境']}】")
            print(f"\n《大运流年作用后的左环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{位置}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴左环境为【{天干信息['左环境']}】")
            print(f"\n《大运流年作用后的右环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{位置}】【{天干名字}】【{十神}】状态为【{旺弱状态}】，∴右环境为【{天干信息['右环境']}】")
            print(f"\n《大运流年作用后的内环境左环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴内环境左环境为【{天干信息['内环境左环境']}】")
            print(f"\n《大运流年作用后的内环境右环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{同柱地支键}】状态为【{地支旺弱状态}】，∴内环境右环境为【{天干信息['内环境右环境']}】")



        print("\n=== 🫥 未现十神的环境 ===")
        with contextlib.redirect_stdout(None):
            未现外环境结论 = 分析未现天干十神的外环境吉凶()
            未现内环境结论 = 分析未现天干十神的内环境吉凶()
            未现左环境结论 = 分析未现天干十神的左环境吉凶()
            未现右环境结论 = 分析未现天干十神的右环境吉凶()
            未现内环境左环境结论 = 分析未现天干十神的内环境的左环境()
            未现内环境右环境结论 = 分析未现天干十神的内环境的右环境()
        # 获取所有未现十神的列表
        未现十神列表 = list(未现正偏十神主字典.keys())

        for 天干名 in 未现十神列表:
            属性子字典 = 未现正偏十神主字典[天干名]
            窗口名字 = 属性子字典.get('窗口名字')
            十神 = 属性子字典.get('十神')
            窗口位置 = next((位置 for 位置, 信息 in 八字信息主字典.items() if 信息.get('名字') == 窗口名字), None)
            
            if not 窗口位置:
                continue

            # 获取天干和地支的旺弱状态
            天干旺弱状态 = 八字信息主字典[窗口位置].get('旺弱状态', '')
            地支位置 = 窗口位置.replace('干', '支')
            地支旺弱状态 = 八字信息主字典[地支位置].get('旺弱状态', '')

            # 处理外环境和内环境
            for 环境类型, 参考状态 in [('外环境', 天干旺弱状态), ('内环境', 地支旺弱状态)]:
                if '弱' in 参考状态 and 属性子字典.get(环境类型) in ['吉', '凶']:
                    属性子字典[环境类型] = '凶' if 属性子字典[环境类型] == '吉' else '吉'
                    if '+' in 参考状态:
                        属性子字典[环境类型] += '+'

            # 处理左右环境
            天干顺序 = ['年干', '月干', '日干', '时干']
            窗口索引 = 天干顺序.index(窗口位置)

            # 特殊位置处理（年干和时干）
            特殊位置处理 = {
                '年干': ('左环境', ['月干', '日干']),
                '时干': ('右环境', ['月干', '日干'])
            }

            if 窗口位置 in 特殊位置处理:
                环境类型, 参考位置列表 = 特殊位置处理[窗口位置]
                if all('弱' in 八字信息主字典[位置].get('旺弱状态', '') for 位置 in 参考位置列表):
                    原环境 = 属性子字典.get(环境类型, '')
                    if 原环境 in ['吉', '凶']:
                        属性子字典[环境类型] = '凶' if 原环境 == '吉' else '吉'
                        if all('+' in 八字信息主字典[位置].get('旺弱状态', '') for 位置 in 参考位置列表):
                            属性子字典[环境类型] += '+'
            else:
                # 普通位置处理
                for 环境类型, 偏移 in [('左环境', -1), ('右环境', 1)]:
                    相邻索引 = 窗口索引 + 偏移
                    if 0 <= 相邻索引 < len(天干顺序):
                        相邻位置 = 天干顺序[相邻索引]
                        相邻旺弱状态 = 八字信息主字典[相邻位置].get('旺弱状态', '')
                        if '弱' in 相邻旺弱状态 and 属性子字典.get(环境类型) in ['吉', '凶']:
                            属性子字典[环境类型] = '凶' if 属性子字典[环境类型] == '吉' else '吉'
                            if '+' in 相邻旺弱状态:
                                属性子字典[环境类型] += '+'

            # 处理内环境的左右环境
            地支顺序 = ['年支', '月支', '日支', '时支']
            地支索引 = 地支顺序.index(地支位置)

            # 特殊位置处理（年支和时支的内环境左右环境）
            特殊地支处理 = {'年支': ('内环境左环境', ['月支', '日支']),
                '时支': ('内环境右环境', ['月支', '日支'])}

            if 地支位置 in 特殊地支处理:
                环境类型, 参考位置列表 = 特殊地支处理[地支位置]
                if all('弱' in 八字信息主字典[位置].get('旺弱状态', '') for 位置 in 参考位置列表):
                    原环境 = 属性子字典.get(环境类型, '')
                    if 原环境 in ['吉', '凶']:
                        属性子字典[环境类型] = '凶' if 原环境 == '吉' else '吉'
                        if all('+' in 八字信息主字典[位置].get('旺弱状态', '') for 位置 in 参考位置列表):
                            属性子字典[环境类型] += '+'
            else:
                # 普通位置处理
                for 环境类型, 偏移 in [('内环境左环境', -1), ('内环境右环境', 1)]:
                    相邻索引 = 地支索引 + 偏移
                    if 0 <= 相邻索引 < len(地支顺序):
                        相邻位置 = 地支顺序[相邻索引]
                        相邻旺弱状态 = 八字信息主字典[相邻位置].get('旺弱状态', '')
                        if '弱' in 相邻旺弱状态 and 属性子字典.get(环境类型) in ['吉', '凶']:
                            属性子字典[环境类型] = '凶' if 属性子字典[环境类型] == '吉' else '吉'
                            if '+' in 相邻旺弱状态:
                                属性子字典[环境类型] += '+'

            # 打印结果
            print(f"\n《大运流年作用后未现十神的外环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{窗口位置}】状态为【{天干旺弱状态}】，∴【{天干名}】【{十神}】外环境为【{属性子字典.get('外环境')}】")
            print(f"\n《大运流年作用后未现十神的内环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，使【{地支位置}】状态为【{地支旺弱状态}】，∴【{天干名}】【{十神}】内环境为【{属性子字典.get('内环境')}】")
            
            左环境信息 = "使【月干】状态为【{}】，【日干】状态为【{}】".format(八字信息主字典['月干'].get('旺弱状态', ''), 八字信息主字典['日干'].get('旺弱状态', '')
            ) if 窗口位置 == '年干' else "使左侧【{}】状态为【{}】".format(
                天干顺序[窗口索引 - 1] if 窗口索引 > 0 else '无',
                八字信息主字典.get(天干顺序[窗口索引 - 1], {}).get('旺弱状态', '无') if 窗口索引 > 0 else '无'
            )
            print(f"\n《大运流年作用后未现十神的左环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，{左环境信息}，∴【{天干名}】【{十神}】左环境为【{属性子字典.get('左环境')}】")

            右环境信息 = "使【月干】状态为【{}】，【日干】状态为【{}】".format(
                八字信息主字典['月干'].get('旺弱状态', ''),
                八字信息主字典['日干'].get('旺弱状态', '')
            ) if 窗口位置 == '时干' else "使右侧【{}】状态为【{}】".format(
                天干顺序[窗口索引 + 1] if 窗口索引 < len(天干顺序) - 1 else '无',
                八字信息主字典.get(天干顺序[窗口索引 + 1], {}).get('旺弱状态', '无') if 窗口索引 < len(天干顺序) - 1 else '无'
            )
            print(f"\n《大运流年作用后未现十神的右环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，{右环境信息}，∴【{天干名}】【{十神}】右环境为【{属性子字典.get('右环境')}】")

            内环境左环境信息 = "使【日支】状态为【{}】，【月支】状态为【{}】".format(
                八字信息主字典['日支'].get('旺弱状态', ''),
                八字信息主字典['月支'].get('旺弱状态', '')
            ) if 地支位置 == '年支' else "使左侧地支【{}】状态为【{}】".format(
                地支顺序[地支索引 - 1] if 地支索引 > 0 else '无',
                八字信息主字典.get(地支顺序[地支索引 - 1], {}).get('旺弱状态', '无') if 地支索引 > 0 else '无'
            )
            print(f"\n《大运流年作用后未现十神的内环境左环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，{内环境左环境信息}，∴【{天干名}】【{十神}】内环境左环境为【{属性子字典.get('内环境左环境')}】")

            内环境右环境信息 = "使【月支】状态为【{}】，【日支】状态为【{}】".format(
                八字信息主字典['月支'].get('旺弱状态', ''),
                八字信息主字典['日支'].get('旺弱状态', '')
            ) if 地支位置 == '时支' else "使右侧地支【{}】状态为【{}】".format(
                地支顺序[地支索引 + 1] if 地支索引 < len(地支顺序) - 1 else '无',
                八字信息主字典.get(地支顺序[地支索引 + 1], {}).get('旺弱状态', '无') if 地支索引 < len(地支顺序) - 1 else '无'
            )
            print(f"\n《大运流年作用后未现十神的内环境右环境结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，{内环境右环境信息}，∴【{天干名}】【{十神}】内环境右环境为【{属性子字典.get('内环境右环境')}】")

        print("\n===🤠日干的环境 ===")
        日干信息 = 八字信息主字典['日干']
        原始结论 = 判断日主自身状态()['作用路径说明']
        
        # 获取大运和流年的干支
        大运天干, 大运地支 = 大运干支[0], 大运干支[1]
        流年天干, 流年地支 = 流年干支[0], 流年干支[1]
        
        # 定义生制关系获取函数
        def 获取生制关系(作用干支, 被作用位置):
            return '生' if 判断两者是否生扶受制(作用干支, 被作用位置) == '生扶关系' else '制'
        
        # 获取各个位置的关系
        关系信息 = {
            '月干': (获取生制关系(大运天干, '月干'), 获取生制关系(流年天干, '月干')),
            '时干': (获取生制关系(大运天干, '时干'), 获取生制关系(流年天干, '时干')),
            '日支': (获取生制关系(大运天干, '日支'), 获取生制关系(流年天干, '日支')),
            '月支': (获取生制关系(大运地支, '月支'), 获取生制关系(流年地支, '月支')),
            '时支': (获取生制关系(大运地支, '时支'), 获取生制关系(流年地支, '时支'))
        }
        
        # 打印环境信息
        print(f"\n《原局日主外环境作用路径》：{原始结论['外环境说明']} \n\n《大运流年作用后日主外环境的结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，大运【{关系信息['月干'][0]}】月干，【{关系信息['时干'][0]}】时干，流年【{关系信息['月干'][1]}】月干，【{关系信息['时干'][1]}】时干，∴日干的左环境为【{日干信息['左环境']}】，日干的右环境为【{日干信息['右环境']}】")
        
        print(f"\n《原局日主内环境作用路径》：{原始结论['内环境说明']} \n\n《大运流年作用后日主内环境的结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，大运【{关系信息['日支'][0]}】日支，流年【{关系信息['日支'][1]}】日支，∴日干的内环境为【{日干信息['内环境']}】")
        
        print(f"\n《原局日主内环境的左环境/右环境作用路径》：{原始结论['内环境扩展说明']} \n\n《大运流年作用后日主内环境的左环境/右环境的结果》：∵【{大运干支}】大运和【{流年干支}】流年作用于原局后，大运【{关系信息['月支'][0]}】月支，【{关系信息['时支'][0]}】时支，流年【{关系信息['月支'][1]}】月支，【{关系信息['时支'][1]}】时支，∴日干内环境的左环境为【{日干信息['内环境左环境']}】，日干内环境的右环境为【{日干信息['内环境右环境']}】")

    def 处理实神天干(大运天干属性, 流年天干属性):
        if 大运天干属性['是否实神'] == '实神' and 流年天干属性['是否实神'] == '实神':
            # 情况8：实神和实神
            流年天干属性['旺弱状态'] = '旺+'
            天干作用原局(流年天干属性)
        else:
            # 情况7：一个实神，一个虚神
            if 大运天干属性['是否实神'] == '实神':
                更新旺弱状态(流年天干属性, 大运天干属性)
                天干作用原局(大运天干属性)
            else:
                更新旺弱状态(大运天干属性, 流年天干属性)
                天干作用原局(流年天干属性)

    def 处理实神地支(大运地支属性, 流年地支属性):
        if 大运地支属性['是否实神'] == '实神' and 流年地支属性['是否实神'] == '实神':
            流年地支属性['旺弱状态'] = '旺+'
            地支作用原局(流年地支属性)
        else:
            if 大运地支属性['是否实神'] == '实神':
                更新旺弱状态(流年地支属性, 大运地支属性)
                大运地支属性['旺弱状态'] += '+'
                地支作用原局(大运地支属性)
            else:
                更新旺弱状态(大运地支属性, 流年地支属性)
                流年地支属性['旺弱状态'] += '+'
                地支作用原局(流年地支属性)

    def 处理天干阴阳(原局属性, 大运天干属性, 流年天干属性):
        大运对流年关系 = 判断两者是否生扶受制(大运天干属性['名字'], 流年天干属性['名字'])
        流年对大运关系 = 判断两者是否生扶受制(流年天干属性['名字'], 大运天干属性['名字'])
        
        # 设置大运天干的旺弱状态
        if 流年对大运关系 == '生扶关系':
            大运天干属性['旺弱状态'] = '旺'
        elif 流年对大运关系 == '受制关系':
            大运天干属性['旺弱状态'] = '弱'
        else:
            大运天干属性['旺弱状态'] = '不旺不弱'
            
        # 设置流年天干的旺弱状态
        if 大运对流年关系 == '生扶关系':
            流年天干属性['旺弱状态'] = '旺'
        elif 大运对流年关系 == '受制关系':
            流年天干属性['旺弱状态'] = '弱'
        else:
            流年天干属性['旺弱状态'] = '不旺不弱'

        if 原局属性 == '全阴':
            if 大运天干属性['阴阳属性'] != 流年天干属性['阴阳属性']:
                if 大运天干属性['阴阳属性'] == '阳':
                    更新旺弱状态(大运天干属性, 流年天干属性)
                    天干作用原局(流年天干属性)
                else:
                    更新旺弱状态(流年天干属性, 大运天干属性)
                    天干作用原局(大运天干属性)
        elif 原局属性 == '全阳':
            if 大运天干属性['阴阳属性'] != 流年天干属性['阴阳属性']:
                if 大运天干属性['阴阳属性'] == '阴':
                    更新旺弱状态(大运天干属性, 流年天干属性)
                    天干作用原局(流年天干属性)
                else:
                    更新旺弱状态(流年天干属性, 大运天干属性)
                    天干作用原局(大运天干属性)
        else:
            # 原局有阴有阳
            for 位置 in ['年干', '月干', '日干', '时干']:
                原局天干属性 = 八字信息主字典[位置]
                原局阴阳 = 原局天干属性['阴阳属性']
                for 天干属性 in [大运天干属性, 流年天干属性]:
                    if 天干属性['阴阳属性'] == 原局阴阳:
                        更新旺弱状态(天干属性, 原局天干属性)

    def 处理地支阴阳(原局属性, 大运地支属性, 流年地支属性):
        大运对流年关系 = 判断两者是否生扶受制(大运地支属性['名字'], 流年地支属性['名字'])    # 先判断大运地支和流年地支的关系
        流年对大运关系 = 判断两者是否生扶受制(流年地支属性['名字'], 大运地支属性['名字'])
        # 设置大运地支的旺弱状态
        if 流年对大运关系 == '生扶关系':
            大运地支属性['旺弱状态'] = '旺'
        elif 流年对大运关系 == '受制关系':
            大运地支属性['旺弱状态'] = '弱'
        else:
            大运地支属性['旺弱状态'] = '不旺不弱'
        # 设置流年地支的旺弱状态
        if 大运对流年关系 == '生扶关系':
            流年地支属性['旺弱状态'] = '旺'
        elif 大运对流年关系 == '受制关系':
            流年地支属性['旺弱状态'] = '弱'
        else:
            流年地支属性['旺弱状态'] = '不旺不弱'

        if 原局属性 == '全阴':
            if 大运地支属性['阴阳属性'] != 流年地支属性['阴阳属性']:
                if 大运地支属性['阴阳属性'] == '阳':
                    更新旺弱状态(大运地支属性, 流年地支属性)
                    地支作用原局(流年地支属性)
                else:
                    更新旺弱状态(流年地支属性, 大运地支属性)
                    地支作用原局(大运地支属性)
        elif 原局属性 == '全阳':
            if 大运地支属性['阴阳属性'] != 流年地支属性['阴阳属性']:
                if 大运地支属性['阴阳属性'] == '阴':
                    更新旺弱状态(大运地支属性, 流年地支属性)
                    地支作用原局(流年地支属性)
                else:
                    更新旺弱状态(流年地支属性, 大运地支属性)
                    地支作用原局(大运地支属性)
        else:
            # 原局有阴有阳
            for 地支属性 in [大运地支属性, 流年地支属性]:
                for 位置 in ['年支', '月支', '日支', '时支']:
                    原局地支属性 = 八字信息主字典[位置]
                    if 原局地支属性.get('是否空亡') == '空亡':
                        原局地支属性['旺弱状态'] = '不旺不弱'
                        continue
                    if 地支属性['阴阳属性'] == 原局地支属性['阴阳属性']:
                        更新旺弱状态(地支属性, 原局地支属性)

    def 处理地支空亡(大运地支属性, 流年地支属性):
        if 大运地支属性.get('是否空亡') == '空亡':
            大运地支属性['旺弱状态'] = '不旺不弱'
            if 流年地支属性.get('是否空亡') != '空亡':
                反转结论(流年地支属性)
        elif 流年地支属性.get('是否空亡') == '空亡':
            流年地支属性['旺弱状态'] = '不旺不弱'
            反转结论(大运地支属性)

    def 判断地支作用(大运地支属性, 流年地支属性, 原局地支属性):
        if 原局地支属性.get('是否空亡') == '空亡':   # 如果原局地支是空亡，直接返回不旺不弱
            原局地支属性['旺弱状态'] = '不旺不弱'
            return
        大运对原局关系 = 判断两者是否生扶受制(大运地支属性['名字'], 原局地支属性['名字'])    # 获取作用关系
        流年对原局关系 = 判断两者是否生扶受制(流年地支属性['名字'], 原局地支属性['名字'])
        
        需要反转 = (大运地支属性.get('是否空亡') == '空亡' or 流年地支属性.get('是否空亡') == '空亡')  # 判断是否需要反转结果（当大运或流年地支是空亡时）
        
        if 大运对原局关系 == '生扶关系' or 流年对原局关系 == '生扶关系':   # 确定基础状态
            基础状态 = '旺' if not 需要反转 else '弱'
        elif 大运对原局关系 == '受制关系' or 流年对原局关系 == '受制关系':
            基础状态 = '弱' if not 需要反转 else '旺'
        else:
            基础状态 = '不旺不弱'

        原局地支属性['旺弱状态'] = 基础状态

        if 基础状态 == '弱':     # 反转结论如果状态是弱
            反转结论(原局地支属性)

    def 反转结论(属性字典):
        原结论 = 属性字典.get('环境结论', '')
        if 原结论 == '吉':
            属性字典['环境结论'] = '凶'
        elif 原结论 == '凶':
            属性字典['环境结论'] = '吉'

    def 更新旺弱状态(作用者属性, 被作用者属性):
        关系 = 判断两者是否生扶受制(作用者属性['名字'], 被作用者属性['名字'])
        是同性 = 作用者属性['阴阳属性'] == 被作用者属性['阴阳属性']
        if 关系 == '生扶关系':
            基础状态 = '旺' if 是同性 else '弱'
        elif 关系 == '受制关系':
            基础状态 = '弱' if 是同性 else '旺'
        else:
            基础状态 = '不旺不弱'
        if 作用者属性['是否实神'] == '实神':
            基础状态 += '+'
        被作用者属性['旺弱状态'] = 基础状态
  
        if 基础状态.startswith('弱'):   # 反转结论如果状态是弱
            反转结论(被作用者属性)

    def 天干作用原局(天干属性):
        for 位置 in ['年干', '月干', '日干', '时干']:
            原局天干属性 = 八字信息主字典[位置]
            更新旺弱状态(天干属性, 原局天干属性)

    def 地支作用原局(地支属性):
        for 位置 in ['年支', '月支', '日支', '时支']:
            原局地支属性 = 八字信息主字典[位置]
            if 原局地支属性.get('是否空亡') == '空亡':
                原局地支属性['旺弱状态'] = '不旺不弱'
                continue
            更新旺弱状态(地支属性, 原局地支属性)
   
   
    # 在右侧框架中添加按钮，绑定函数
    查看大运流年作用按钮 = tk.Button(右侧框架, text="查看大运流年作用", command=处理大运流年共同作用)
    查看大运流年作用按钮.pack(pady=10)




    def 发送到Coze的API(文本):
        import requests
        import json
        import time
        session = requests.Session() # 创建新的会话
        # Coze的API配置信息
        bot_id = "7430070428481470472"  # 你的机器人ID
        api_token = "pat_N0P8ThAsnNn7RhlWQXKHJamRR1fqmE6jZRgGzPdxTwpudzbUsjm0gL7SV1j5ksvK"  # 你的API令牌
        api_url = "https://api.coze.com/v3/chat"  # 官方提供的API地址
        # 设置请求头
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        # 设置请求体，按照官方文档示例
        message = {"bot_id": bot_id, "user_id": f"user_{int(time.time())}", "stream": True, "auto_save_history": False,
            "additional_messages": [{"role": "user","content": 文本, "content_type": "text"}]}
        try:  # 发送POST请求，启用流式响应
            response = session.post(api_url, headers=headers, json=message, stream=True)
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                print("⌛ 正在等待bot生成完整回复...")
                time.sleep(20)  # 先等待20秒,让bot充分思考和生成
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data:"):
                            try:
                                json_str = line.replace("data:", "").strip()
                                data = json.loads(json_str)
                                if isinstance(data, dict):
                                    if data.get("type") == "answer":
                                        content = data.get("content", "")
                                        if content:
                                            full_response = content  # 直接替换而不是追加
                            except json.JSONDecodeError:
                                continue             
                return full_response.strip() if full_response else None
            else:
                print(f"请求失败, 错误代码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None  # 添加返回
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {str(e)}")
            return None  # 添加返回
        except Exception as e:
            print(f"其他错误: {str(e)}")
            return None  # 添加返回
        finally:
            session.close()   # 确保会话被关闭


    # 在最后创建一个新的Frame用于容纳"断语句子定向筛选"区域
    底部容器 = tk.Frame(分析命盘界面窗口, bg='#f5f5f1')
    底部容器.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
    # 创建分隔线
    tk.Frame(底部容器, height=2, bg='#e0e0e0').pack(fill=tk.X, pady=10)

    def 筛选断语():
        选中主题 = 筛选选项.get()
        if 选中主题 == "投资":
            关键词 = ["【偏财】"]
            筛选结果 = [句子 for 句子 in 所有断语 if any(关键词 in 句子 for 关键词 in 关键词)]
            print("\n" + "="*50)  # 添加分隔线
            print(f"📄📄📄📄📄📄本轮“投资”主题的逻辑链句子有以下：")
            for 句子 in 筛选结果:
                print(句子)
            print("="*50 + "\n")  # 添加分隔线

            # 提取核心逻辑并直接添加到筛选结果中
            for 句子 in 筛选结果.copy():  # 使用copy()避免在遍历时修改列表
                if "推导过程：" in 句子:
                    if "【日干】" in 句子 or "【日支】" in 句子:
                        主体 = "【日干】" if "【日干】" in 句子 else "【日支】"
                        结果 = "【吉】" if "【吉】" in 句子 else "【凶】"
                        日干支作用的简化句子 = f"{主体}让{关键词[0]}{结果}"
                        筛选结果.append(日干支作用的简化句子)  # 直接添加到筛选结果中
            # 合并所有句子
            所有筛选句子 = "\n".join(筛选结果)
            print("\n 正在连接Coze机器人 请稍候...⌛")
            coze回复 = 发送到Coze的API(f"根据命主八字生成的关于【投资】主体作用链路的句子如下，请对核心内容进行筛选与精简，针对【投资】给出断语：\n{所有筛选句子}")
            if coze回复:
                print("\n🤖🤖🤖🤖🤖 Coze分析结果:")
                print(coze回复)
            else:
                print("❌ 获取分析结果失败，请稍后重试")




    # 🖥️🖥️🖥️ 1. 断语句子定向筛选区域 - 放在左侧
    筛选区域框架 = tk.Frame(左侧框架, bg='#f5f5f1')
    筛选区域框架.pack(anchor='w', pady=(10, 0))  # anchor='w' 确保左对齐
    水平框架 = tk.Frame(筛选区域框架, bg='#f5f5f1')
    水平框架.pack(fill='x')
    筛选选项 = ttk.Combobox(水平框架, values=["投资"], font=("Arial", 8), width=15, state="readonly")
    筛选选项.set("请选择筛选主题")
    筛选选项.pack(side=tk.LEFT, padx=(0, 5))
    筛选选项.bind('<<ComboboxSelected>>', lambda e: 提示文本.config(text="将筛选所有带【偏财】相关的句子" if 筛选选项.get() == "投资" else ""))   # 添加事件绑定
    # 创建确定按钮
    确定按钮 = tk.Button(水平框架, text="确定", command=筛选断语, font=("Arial", 7), width=3, height=1, relief="solid", bd=0.5) 
    确定按钮.pack(side=tk.LEFT)
    # 创建提示文本
    提示文本 = tk.Label(筛选区域框架, text="", font=("Arial", 8), fg="gray", bg='#f5f5f1') 
    提示文本.pack(pady=5)  






    # 🖥️🖥️🖥️在左侧框架添加新按钮（放在筛选区域框架下方）
    作用关系按钮 = tk.Button(左侧框架, text="查看任意两个元素的作用吉凶", font=("Arial", 10),
        command=lambda: 显示作用关系窗口(分析命盘界面窗口,性别,本命盘四个天干名字列表,本命盘四个地支名字列表,
            四个天干十神列表,空亡_地支_列表,八字信息主字典,未现正偏十神主字典,元素间关系分析,判断两者是否生扶受制),
        relief="solid",bd=0.5)
    作用关系按钮.pack(anchor='w', pady=(10, 0))



    return 本命盘四个天干名字列表,本命盘四个地支名字列表,空亡_地支_列表



def 显示作用关系窗口(parent, 性别, 本命盘四个天干名字列表, 本命盘四个地支名字列表, 四个天干十神列表, 空亡_地支_列表, 八字信息主字典, 未现正偏十神主字典, 元素间关系分析, 判断两者是否生扶受制):
    global 选中值
    # 创建新窗口和左右区域框架
    作用关系窗口 = tk.Toplevel(parent)
    作用关系窗口.title("元素作用关系分析")
    作用关系窗口.geometry("1000x800")
    作用关系窗口.configure(bg='#f5f5f1')
    左区域 = tk.Frame(作用关系窗口, bg='#f5f5f1')
    左区域.pack(side=tk.LEFT, padx=20, pady=20, expand=True)
    右区域 = tk.Frame(作用关系窗口, bg='#f5f5f1')
    右区域.pack(side=tk.RIGHT, padx=20, pady=20, expand=True)

    # 区域标题
    tk.Label(左区域, text="作用方", font=("Arial", 12), bg='#f5f5f1').pack()
    tk.Label(右区域, text="被作用方", font=("Arial", 12), bg='#f5f5f1').pack()

    # 创建选项值
    已现天干选项 = [f"【{天干}】【{位置}】【{八字信息主字典[位置]['十神']}】"
                for 天干, 位置 in zip(本命盘四个天干名字列表, ['年干', '月干', '日干', '时干'])]

    未现天干选项 = [f"【{属性['名字']}】【{属性['十神']}】"
                for 属性 in 未现正偏十神主字典.values()]

    地支选项 = [f"【{地支}】【{位置}】"
             for 地支, 位置 in zip(本命盘四个地支名字列表, ['年支', '月支', '日支', '时支'])]

    # 创建下拉框
    tk.Label(左区域, text="已现天干", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    作用方天干_已现 = ttk.Combobox(左区域, values=[''] + 已现天干选项, width=30, state='readonly', name='作用方天干_已现')
    作用方天干_已现.pack()

    tk.Label(左区域, text="未现天干", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    作用方天干_未现 = ttk.Combobox(左区域, values=[''] + 未现天干选项, width=30, state='readonly', name='作用方天干_未现')
    作用方天干_未现.pack()

    tk.Label(左区域, text="已现地支", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    作用方地支 = ttk.Combobox(左区域, values=[''] + 地支选项, width=30, state='readonly', name='作用方地支')
    作用方地支.pack()

    tk.Label(右区域, text="已现天干", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    被作用方天干_已现 = ttk.Combobox(右区域, values=[''] + 已现天干选项, width=30, state='readonly', name='被作用方天干_已现')
    被作用方天干_已现.pack()

    tk.Label(右区域, text="未现天干", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    被作用方天干_未现 = ttk.Combobox(右区域, values=[''] + 未现天干选项, width=30, state='readonly', name='被作用方天干_未现')
    被作用方天干_未现.pack()

    tk.Label(右区域, text="已现地支", font=("Arial", 9), bg='#f5f5f1').pack(pady=(10, 0))
    被作用方地支 = ttk.Combobox(右区域, values=[''] + 地支选项, width=30, state='readonly', name='被作用方地支')
    被作用方地支.pack()

    选中值 = {'作用方天干': '', '作用方地支': '', '被作用方天干': '', '被作用方地支': ''}


    def 从选项提取信息(选项文本, 类型=''):
        if not 选项文本:
            return {}
        
        parts = 选项文本.strip('【】').split('】【')
        天干名 = parts[0]
        结果 = {
            '元素': parts[0],
            '类型': 类型
        }
        
        if 类型 == '已现天干':
            结果.update({
                '位置': parts[1],
                '十神': parts[2] if len(parts) > 2 else ''
            })
        elif 类型 == '未现天干':
            结果.update({
                '十神': parts[1] if len(parts) > 1 else ''
            })
        elif 类型 == '已现地支':
            结果.update({
                '位置': parts[1]
            })
        
        return 结果


    def 更新选中值(event, 键名):
        选中项 = event.widget.get()
        if not 选中项:
            选中值[键名] = ''
            return
        组件名称 = event.widget.winfo_name()
        # 清除其他相关选项
        if '天干' in 键名:
            if '作用方' in 键名:
                if '未现' in 组件名称:
                    作用方天干_已现.set('')
                    选中值['作用方来源'] = '未现天干'
                else:
                    作用方天干_未现.set('')
                    选中值['作用方来源'] = '已现天干'
            else:
                if '未现' in 组件名称:
                    被作用方天干_已现.set('')
                    选中值['被作用方来源'] = '未现天干'
                else:
                    被作用方天干_未现.set('')
                    选中值['被作用方来源'] = '已现天干'
        
        # 根据不同类型的下拉框，设置不同的类型标记
        if '天干' in 键名:
            if '未现' in event.widget._name:
                选中值[键名] = 从选项提取信息(选中项, 类型='未现天干')
            else:
                选中值[键名] = 从选项提取信息(选中项, 类型='已现天干')
        else:  # 地支
            选中值[键名] = 从选项提取信息(选中项, 类型='已现地支')


    # 绑定事件
    作用方天干_已现.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '作用方天干'))
    作用方天干_未现.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '作用方天干'))
    作用方地支.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '作用方地支'))
    被作用方天干_已现.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '被作用方天干'))
    被作用方天干_未现.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '被作用方天干'))
    被作用方地支.bind('<<ComboboxSelected>>', lambda e: 更新选中值(e, '被作用方地支'))

    def 获取作用路径(起始信息, 目标信息, 类型='天干'):
        if 类型 == '天干':
            位置顺序 = ['年干', '月干', '日干', '时干']
        else:
            位置顺序 = ['年支', '月支', '日支', '时支']
        
        # 1. 处理被作用方是"未现天干"的特殊情况
        if isinstance(目标信息, dict) and 目标信息.get('类型') == '未现天干':
            窗口位置 = 未现正偏十神主字典[目标信息['元素']]['窗口位置']
            起始位置 = 起始信息['位置']
            
            # 获取从起始位置到窗口位置的路径
            起始索引 = 位置顺序.index(起始位置)
            结束索引 = 位置顺序.index(窗口位置)
            
            if 起始索引 <= 结束索引:
                路径 = 位置顺序[起始索引:结束索引+1]
            else:
                路径 = 位置顺序[起始索引:结束索引-1:-1]
            return 路径
        
        # 2. 处理作用方是"未现天干"的特殊情况
        elif 起始信息.get('类型') == '未现天干' and 目标信息.get('类型') != '未现天干':
            作用方窗口位置 = 未现正偏十神主字典[起始信息['元素']]['窗口位置']
            路径 = [f"未现天干({起始信息['元素']})", 作用方窗口位置]
            
            # 从窗口位置到目标位置的路径
            起始索引 = 位置顺序.index(作用方窗口位置)
            结束索引 = 位置顺序.index(目标信息['位置'])
            if 起始索引 <= 结束索引:
                路径.extend(位置顺序[起始索引+1:结束索引+1])
            else:
                路径.extend(位置顺序[起始索引-1:结束索引-1:-1])
            return 路径
        
        # 3. 处理作用方和被作用方都是未现天干的特殊情况
        elif 起始信息.get('类型') == '未现天干' and 目标信息.get('类型') == '未现天干':
            作用方窗口位置 = 未现正偏十神主字典[起始信息['元素']]['窗口位置']
            被作用方窗口位置 = 未现正偏十神主字典[目标信息['元素']]['窗口位置']
            
            # 如果是同一个窗口
            if 作用方窗口位置 == 被作用方窗口位置:
                return [
                    f"未现天干({起始信息['元素']})",
                    作用方窗口位置,
                    f"未现天干({目标信息['元素']})"]
            
            # 如果是不同窗口
            路径 = [f"未现天干({起始信息['元素']})", 作用方窗口位置]
            起始索引 = 位置顺序.index(作用方窗口位置)
            结束索引 = 位置顺序.index(被作用方窗口位置)
            
            if 起始索引 <= 结束索引:
                路径.extend(位置顺序[起始索引+1:结束索引+1])
            else:
                路径.extend(位置顺序[起始索引-1:结束索引-1:-1])
            
            路径.append(f"未现天干({目标信息['元素']})")
            return 路径
        
        # 4. 处理普通情况（已现天干/地支之间的作用）
        if isinstance(起始信息, dict):
            起始位置 = 起始信息['位置']
        else:
            起始位置 = 起始信息
        if isinstance(目标信息, dict):
            目标位置 = 目标信息['位置']
        else:
            目标位置 = 目标信息

        if 类型 == '天干':
            位置顺序 = ['年干', '月干', '日干', '时干']
        else:
            位置顺序 = ['年支', '月支', '日支', '时支']

        起始索引 = 位置顺序.index(起始位置)
        结束索引 = 位置顺序.index(目标位置)

        if 起始索引 == 结束索引:
            # 起始位置和目标位置相同
            路径 = [起始位置]
        elif 起始索引 < 结束索引:
            # 顺序前进
            路径 = 位置顺序[起始索引:结束索引+1]
        else:
            # 逆序前进
            路径 = 位置顺序[起始索引:结束索引-1:-1]
        return 路径


    def 判断正偏关系(十神):
        五个正十神列表大全 = ['正印', '正官', '正财', '劫财', '伤官'] 
        return '正十神' if 十神 in 五个正十神列表大全 else '偏十神'


    def 检查作用关系(显示过程=True):
        global 选中值
        nonlocal 八字信息主字典
        def 打印信息(信息):
            if 显示过程:
                print(信息)
            

        作用路径 = []
        被作用方信息 = {}
        被作用方属性 = {}

        五个正十神列表大全 = ['正印', '正官', '正财', '劫财', '伤官']
        作用方_天干 = 选中值.get('作用方天干')
        作用方_地支 = 选中值.get('作用方地支')
        被作用方_天干 = 选中值.get('被作用方天干')
        被作用方_地支 = 选中值.get('被作用方地支')
        

        # 如果是天干作用
        if 作用方_天干 and 被作用方_天干:
            if 作用方_天干.get('类型') == '已现天干' and 被作用方_天干.get('类型') == '已现天干':
                作用路径.append(作用方_天干['位置'])
                被作用方信息 = {'位置': 被作用方_天干['位置']}
            作用方 = 作用方_天干['位置']
            被作用方 = 被作用方_天干['位置']
        # 如果是地支作用
        elif 作用方_地支 and 被作用方_地支:
            if 作用方_地支.get('类型') == '已现地支' and 被作用方_地支.get('类型') == '已现地支':
                作用路径.append(作用方_地支['位置'])
                被作用方信息 = {'位置': 被作用方_地支['位置']}
                作用方 = 作用方_地支['位置']
                被作用方 = 被作用方_地支['位置']



        if 作用方_天干:
            打印信息(f"作用方天干类型={作用方_天干.get('类型')}")
        if 被作用方_天干:
            打印信息(f"被作用方天干类型={被作用方_天干.get('类型')}")

        # 情况1：作用方"已现天干" + 被作用方"已现天干"🌟
        if (作用方_天干 and 被作用方_天干 and 作用方_天干.get('类型') == '已现天干' and 被作用方_天干.get('类型') == '已现天干'):
            打印信息("\n进入情况1：作用方“已现天干” + 被作用方“已现天干”")
            
            # 获取作用路径
            作用路径 = 获取作用路径(作用方_天干, 被作用方_天干, 类型='天干')
            if not 作用路径:  # 如果正向路径为空，尝试逆向路径
                作用路径 = 获取作用路径(被作用方_天干, 作用方_天干, 类型='天干')
                if 作用路径:  # 如果找到逆向路径，将其反转
                    作用路径 = 作用路径[::-1]

            打印信息("\n作用路径：" + "→".join(作用路径))
            
            最终作用结果 = None
            
            # 遍历作用路径，逐步处理每一步的作用
            for i in range(len(作用路径) - 1):
                当前位置 = 作用路径[i]
                下一个位置 = 作用路径[i + 1]
                当前元素 = 八字信息主字典[当前位置]
                下一个元素 = 八字信息主字典[下一个位置]
                当前元素名字 = 当前元素['名字']
                下一个元素名字 = 下一个元素['名字']
                关系 = 判断两者是否生扶受制(当前元素名字, 下一个元素名字)
                最终关系 = 关系
                if 八字信息主字典[当前位置].get('旺弱状态') == '弱':
                    最终关系 = '受制关系' if 关系[1] == '生扶关系' else '生扶关系'
                
                打印信息(f"\n【{当前位置}】【{当前元素名字}】作用于【{下一个位置}】【{下一个元素名字}】")
                打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{八字信息主字典[当前位置].get('旺弱状态')}】，∴两者作用关系为：{最终关系}")
                if 最终关系 == '受制关系':
                    八字信息主字典[下一个位置]['旺弱状态'] = '弱'
                打印信息(f"本次被作用者【{下一个位置}】【{下一个元素名字}】的旺弱状态为：【{八字信息主字典[下一个位置].get('旺弱状态')}】")

                最终作用结果 = 最终关系               # 记录最后一次的作用关系，用于最终结论
            
                if i == len(作用路径) - 2:          # -2是因为我们是在看当前位置到下一个位置的关系
                    最终被作用方 = 下一个位置
                    最终关系结果 = 最终关系

            # 获取最终被作用方的信息
            最终被作用方位置 = 作用路径[-1]
            最终被作用方信息 = 八字信息主字典[最终被作用方位置]
            最终被作用方忌用神 = 最终被作用方信息.get('忌用神归属')
            
            # 判断被作用环境结论
            if 最终被作用方信息.get('是否空亡') == '空亡':
                被作用环境结论 = '不吉不凶'
            else:
                if 最终被作用方忌用神 == '用神':
                    被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                elif 最终被作用方忌用神 == '忌神':
                    被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                else:
                    被作用环境结论 = '未知'
            
            # 输出最终结论
            打印信息(f"\n🔍最终被作用方：【{最终被作用方位置}】【{最终被作用方信息['名字']}】被前一元素【{最终作用结果}】，∵被作用方为【{最终被作用方忌用神}】，∴最终【{最终被作用方位置}】【{最终被作用方信息['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[最终被作用方位置]['十神']}】作用结论为：【{被作用环境结论}】")
            
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}



        # 情况2：作用方"已现天干" + 被作用方"未现天干"🌟
        elif (作用方_天干 and 被作用方_天干 and 作用方_天干.get('类型') == '已现天干' and 被作用方_天干.get('类型') == '未现天干'):
            打印信息("\n进入情况2：作用方“已现天干” + 被作用方“未现天干”")
            # 第一步：获取作用方信息
            作用方信息 = 作用方_天干
            被作用方信息 = 被作用方_天干
            被作用方天干名 = 被作用方信息['元素']
            被作用方属性 = 未现正偏十神主字典[被作用方天干名]
            作用方属性 = 八字信息主字典[作用方信息['位置']]
            窗口位置 = 被作用方属性['窗口位置']

            # 第二步：获取作用路径（从作用方位置到窗口位置）
            if 作用方信息['窗口位置'] == 窗口位置:
                作用路径 = [作用方信息['窗口位置']]
            else:
                作用路径 = 获取作用路径(作用方信息, 窗口位置, 类型='天干')
            作用路径.append(f"未现天干({被作用方天干名})")
            打印信息("作用路径：" + "→".join(作用路径))
            最终作用结果 = None
            # 第三步：依次作用到窗口
            for i in range(len(作用路径)-2):  # 不包括最后的未现天干
                当前位置 = 作用路径[i]
                下一个位置 = 作用路径[i+1]
                当前元素 = 八字信息主字典[当前位置]
                下一个元素 = 八字信息主字典[下一个位置]
                当前元素名字 = 当前元素['名字']
                下一个元素名字 = 下一个元素['名字']
                关系 = 判断两者是否生扶受制(当前元素['名字'], 下一个元素['名字'])
                最终关系 = 关系
                if 八字信息主字典[当前位置].get('旺弱状态') == '弱':
                    最终关系 = '受制关系' if 关系[1] == '生扶关系' else '生扶关系'
                打印信息(f"\n【{当前位置}】【{当前元素名字}】作用于【{下一个位置}】【{下一个元素名字}】")
                打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{八字信息主字典[当前位置].get('旺弱状态')}】，∴两者作用关系为：{最终关系}")
                if 最终关系 == '受制关系':
                    八字信息主字典[下一个位置]['旺弱状态'] = '弱'
                打印信息(f"本次被作用者【{下一个位置}】【{下一个元素名字}】的旺弱状态为：【{八字信息主字典[下一个位置].get('旺弱状态')}】")

            # 第四步：窗口天干作用未现天干（考虑镜像反转）
            窗口天干 = 八字信息主字典[窗口位置]
            窗口十神 = 被作用方属性['窗口十神']
            被作用方十神 = 被作用方信息.get('十神') 
            窗口十神 = 被作用方属性.get('窗口十神')
            最终关系 = 判断两者是否生扶受制(窗口天干['名字'], 被作用方天干名)[1]

            # 判断是否需要镜像反转（正偏性不同）
            被作用方正偏 = '正十神' if str(被作用方十神) in 五个正十神列表大全 else '偏十神'
            窗口正偏 = '正十神' if str(窗口十神) in 五个正十神列表大全 else '偏十神'
            
            if 被作用方正偏 != 窗口正偏:
                最终关系 = '受制关系' if 最终关系 == '生扶关系' else '生扶关系'
                打印信息(f"\n∵未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{窗口天干['名字']}】的十神【{窗口十神}】正偏性不同，∴发生镜像反转，变成{最终关系}")
            else:
                打印信息(f"\n∵未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{窗口天干['名字']}】的十神【{窗口十神}】正偏相同，∴它们是作用关系“{最终关系}”不用变")
            # 判断是否需要镜像反转（窗口天干为弱）
            if 窗口天干.get('旺弱状态') == '弱':
                最终关系 = '受制关系' if 最终关系 == '生扶关系' else '生扶关系'
                打印信息(f"\n∵窗口天干为弱，∴发生镜像反转，变成{最终关系}")
            
            最终作用结果 = 最终关系

            # 判断被作用环境结论
            if 被作用方属性.get('是否空亡') == '空亡':
                被作用环境结论 = '不吉不凶'
            else:
                if 被作用方属性['忌用神归属'] == '用神':
                    被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                elif 被作用方属性['忌用神归属'] == '忌神':
                    被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                else:
                    被作用环境结论 = '未知'

            # 输出最终结论
            打印信息(f"\n🔍最终被作用方：【未现天干】【{被作用方天干名}】被窗口【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【未现天干】【{被作用方天干名}】【{被作用方十神}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}


        # 情况3：作用方"未现天干" + 被作用方"已现天干"🌟
        elif (作用方_天干 and 被作用方_天干 and 作用方_天干.get('类型') == '未现天干' and 被作用方_天干.get('类型') == '已现天干'):
            打印信息("\n进入情况3：作用方“未现天干” + 被作用方“已现天干”")
            # 第一步：获取作用方信息
            作用方信息 = 作用方_天干
            被作用方信息 = 被作用方_天干
            作用方天干名 = 作用方信息['元素']
            被作用方天干名 = 被作用方信息['元素']
            作用方属性 = 未现正偏十神主字典[作用方天干名]
            被作用方属性 = 八字信息主字典[被作用方天干名]
            窗口位置 = 作用方属性['窗口位置']
            窗口天干 = 八字信息主字典[窗口位置]

            # 第二步：打印作用路径
            窗口信息 = {'类型': '已现天干', '窗口位置': 窗口位置, '名字': 八字信息主字典[窗口位置]['名字']}

            if 被作用方信息['窗口位置'] == 窗口位置:    # 处理特殊情况：被作用方就是窗口
                作用路径 = [窗口位置]
            else:
                作用路径 = 获取作用路径(窗口信息, 被作用方信息, 类型='天干')     # 获取从窗口到被作用方的路径
                if not 作用路径:
                    作用路径 = 获取作用路径(被作用方信息, 窗口信息, 类型='天干')
                    if 作用路径: 
                        作用路径 = 作用路径[::-1]
            打印信息("\n作用路径：" + "→".join([f"未现天干({作用方天干名})"] + 作用路径))

            # 第三步：作用方未现天干作用到窗口（考虑镜像反转 and 受制后要变‘弱’）
            关系 = 判断两者是否生扶受制(作用方天干名, 窗口天干['名字'])
            最终关系 = 关系
            # 判断是否需要镜像反转（正偏性不同）
            作用方十神 = 作用方属性['十神']
            窗口十神 = 作用方属性['窗口十神']
            作用方正偏 = '正十神' if str(作用方十神) in 五个正十神列表大全 else '偏十神'
            窗口正偏 = '正十神' if str(窗口十神) in 五个正十神列表大全 else '偏十神'
            if 作用方正偏 != 窗口正偏:
                最终关系 = '受制关系' if 最终关系 == '生扶关系' else '生扶关系'
                打印信息(f"\n∵未现天干【{作用方天干名}】的十神【{作用方十神}】与窗口天干【{窗口天干['名字']}】的十神【{窗口十神}】正偏性不同，∴发生镜像反转，变成{最终关系}")
            else:
                打印信息(f"\n∵未现天干【{作用方天干名}】的十神【{作用方十神}】与窗口天干【{窗口天干['名字']}】的十神【{窗口十神}】正偏相同，∴它们是作用关系【{最终关系}】不用变")
            # 判断窗口作用于下一个元素时关系结论是否需要镜像反转（窗口天干为弱）
            if 最终关系 == '受制关系':
                窗口天干['旺弱状态'] = '弱'

            for i in range(len(作用路径)-1):
                当前位置 = 作用路径[i]
                下一个位置 = 作用路径[i+1]
                当前元素 = 八字信息主字典[当前位置]
                下一个元素 = 八字信息主字典[下一个位置]
                当前元素名字 = 当前元素['名字']
                下一个元素名字 = 下一个元素['名字']
                关系 = 判断两者是否生扶受制(当前元素名字, 下一个元素名字)
                最终关系 = 关系
                打印信息(f"\n【{当前位置}】【{当前元素名字}】作用于【{下一个位置}】【{下一个元素名字}】")
                if 八字信息主字典[当前位置].get('旺弱状态') == '弱':
                    最终关系 = '受制关系' if 关系[1] == '生扶关系' else '生扶关系'
                    
                    打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{八字信息主字典[当前位置].get('旺弱状态')}】，∴两者作用关系为：{最终关系}")
                if 最终关系 == '受制关系':
                    八字信息主字典[下一个位置]['旺弱状态'] = '弱'
                打印信息(f"本次被作用者【{下一个位置}】【{下一个元素名字}】的旺弱状态为：【{八字信息主字典[下一个位置].get('旺弱状态')}】")
                
                最终作用结果 = 最终关系
                
                if i == len(作用路径) - 2:  # 记录最后一次作用关系
                    最终被作用方 = 下一个位置
                    最终关系结果 = 最终关系
            
            # 获取最终被作用方的信息
            最终被作用方位置 = 作用路径[-1]
            最终被作用方信息 = 八字信息主字典[最终被作用方位置]
            最终被作用方忌用神 = 最终被作用方信息.get('忌用神归属')
            最终作用结果 = 最终关系
            # 第四步：判断最终结果
            if 最终被作用方信息.get('是否空亡')  == '空亡':
                被作用环境结论 = '不吉不凶'
            else:
                if 最终被作用方忌用神 == '用神':
                    被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                elif 最终被作用方忌用神 == '忌神':
                    被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                else:
                    被作用环境结论 = '未知'


            # 最后的输出
            打印信息(f"\n🔍最终被作用方：【{最终被作用方位置}】【{最终被作用方信息['名字']}】被前一元素【{最终作用结果}】，∵被作用方为【{最终被作用方忌用神}】，∴最终【{最终被作用方位置}】【{最终被作用方信息['名字']}】【{被作用方属性['十神']}】被“未现天干”【{作用方天干名}】【{作用方属性['十神']}】作用结论为：【{被作用环境结论}】")
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}



        # 情况4：作用方"未现天干" + 被作用方"未现天干"⭐️
        elif (作用方_天干 and 被作用方_天干 and 作用方_天干.get('类型') == '未现天干' and 被作用方_天干.get('类型') == '未现天干'):
            打印信息("\n进入情况4：作用方“未现天干” + 被作用方“未现天干”")
            # 第一步：获取双方信息
            作用方信息 = 作用方_天干
            被作用方信息 = 被作用方_天干
            作用方天干名 = 作用方信息['元素']
            被作用方天干名 = 被作用方信息['元素']
            作用方属性 = 未现正偏十神主字典[作用方天干名]
            被作用方属性 = 未现正偏十神主字典[被作用方天干名]
            作用方窗口位置 = 作用方属性['窗口位置']
            被作用方窗口位置 = 被作用方属性['窗口位置']
            作用方十神 = 作用方属性['十神']
            被作用方十神 = 被作用方属性['十神']

            # 第二步：获取作用路径
            if 作用方窗口位置 == 被作用方窗口位置:
                # 特殊情况：同一个窗口
                作用路径 = [作用方窗口位置]
                完整作用路径 = [f"未现天干({作用方天干名})", 作用方窗口位置, f"未现天干({被作用方天干名})"]
                打印信息("作用路径：" + "→".join(完整作用路径))
                
                # 处理 作用方未现天干 到 窗口 的作用
                作用方窗口天干 = 八字信息主字典[作用方窗口位置]
                关系1 = 判断两者是否生扶受制(作用方天干名, 作用方窗口天干['名字'])
                
                # 判断作用方是否需要镜像反转
                作用方十神 = 作用方属性['十神']
                作用方窗口十神 = 作用方属性['窗口十神']
                作用方正偏 = '正十神' if str(作用方十神) in 五个正十神列表大全 else '偏十神'
                窗口正偏 = '正十神' if str(作用方窗口十神) in 五个正十神列表大全 else '偏十神'
                
                if 作用方正偏 != 窗口正偏:
                    关系1 = '受制关系' if 关系1 == '生扶关系' else '生扶关系'
                    打印信息(f"\n∵作用方未现天干【{作用方天干名}】的十神【{作用方十神}】与窗口天干【{作用方窗口天干['名字']}】的十神【{作用方窗口十神}】正偏性不同，∴发生镜像反转，变成【{关系1}】")
                else:
                    打印信息(f"\n作用方未现天干【{作用方天干名}】的十神【{作用方十神}】与窗口天干【{作用方窗口天干['名字']}】的十神【{作用方窗口十神}】正偏相同，∴它们是作用关系【{关系1}】不用变")

                if 关系1 == '受制关系':
                    作用方窗口天干['旺弱状态'] = '弱'
                    打印信息(f"∵关系为受制关系，∴窗口天干【{作用方窗口天干['名字']}】的旺弱状态变为【弱】")
                else:
                    打印信息(f"∵关系为生扶关系，∴窗口天干【{作用方窗口天干['名字']}】的旺弱状态不变")
                # 处理窗口 到 被作用方未现天干 的作用
                被作用方窗口天干 = 八字信息主字典[被作用方窗口位置]
                关系2 = 判断两者是否生扶受制(作用方窗口天干['名字'], 被作用方天干名)
                
                # 判断被作用方是否需要镜像反转
                被作用方十神 = 被作用方属性['十神']
                被作用方窗口十神 = 被作用方属性['窗口十神']
                被作用方正偏 = '正十神' if str(被作用方十神) in 五个正十神列表大全 else '偏十神'
                
                if 被作用方正偏 != 窗口正偏:
                    关系2 = '受制关系' if 关系2 == '生扶关系' else '生扶关系'
                    打印信息(f"\n∵被作用方未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{被作用方窗口天干['名字']}】的十神【{被作用方窗口十神}】正偏性不同，∴发生镜像反转，变成{关系2}")
                else:
                    打印信息(f"\n作用方未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{被作用方窗口天干['名字']}】的十神【{被作用方窗口十神}】正偏相同，∴它们是作用关系【{关系2}】不用变")
                if 被作用方窗口天干.get('旺弱状态') == '弱':
                    关系2 = '受制关系' if 关系2 == '生扶关系' else '生扶关系'
                    打印信息(f"∵窗口天干【{被作用方窗口天干['名字']}】的旺弱状态为【弱】，∴作用关系发生反转，变成【{关系2}】")
                
                最终关系 = 关系2  # 用于后续判断吉凶结论
                


            else:
                # 非特殊情况：不同窗口。 原有的非特殊情况代码保持不变
                作用方窗口信息 = {'类型': '已现天干', '位置': 作用方窗口位置, '名字': 八字信息主字典[作用方窗口位置]['名字']}
                被作用方窗口信息 = {'类型': '已现天干', '位置': 被作用方窗口位置, '名字': 八字信息主字典[被作用方窗口位置]['名字']}
                作用路径 = 获取作用路径(作用方窗口信息, 被作用方窗口信息, 类型='天干')
                完整作用路径 = [f"未现天干({作用方天干名})"] + 作用路径 + [f"未现天干({被作用方天干名})"]
                打印信息("作用路径：" + "→".join(完整作用路径))

                # 第三步：作用方未现天干作用到其窗口（考虑镜像反转）
                作用方窗口天干 = 八字信息主字典[作用方窗口位置]
                关系 = 判断两者是否生扶受制(作用方天干名, 作用方窗口天干['名字'])
                打印信息(f"\n【未现天干】【{作用方天干名}】作用于【{作用方窗口位置}】【{作用方窗口天干['名字']}】，两者作用关系为：{关系}")

                # 判断是否需要镜像反转（正偏性不同）
                作用方十神 = 作用方属性['十神']
                作用方窗口十神 = 作用方属性['窗口十神']
                作用方正偏 = '正十神' if str(作用方十神) in 五个正十神列表大全 else '偏十神'
                窗口正偏 = '正十神' if str(作用方窗口十神) in 五个正十神列表大全 else '偏十神'
                
                if 作用方正偏 != 窗口正偏:
                    关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                    打印信息(f"\n∵未现天干【{作用方天干名}】的十神【{作用方十神}】与窗口天干【{作用方窗口天干['名字']}】的十神【{作用方窗口十神}】正偏性不同，∴发生镜像反转，变成{关系}")

                if 关系 == '受制关系':
                    作用方窗口天干['旺弱状态'] = '弱'

                # 第四步：窗口间的逐步作用
                for i in range(len(作用路径)-1):
                    当前位置 = 作用路径[i]
                    下一位置 = 作用路径[i+1]
                    当前元素 = 八字信息主字典[当前位置]
                    下一元素 = 八字信息主字典[下一位置]
                    关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                    
                    打印信息(f"\n【{当前位置}】【{当前元素['名字']}】作用于【{下一位置}】【{下一元素['名字']}】")
                    if 当前元素.get('旺弱状态') == '弱':
                        关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                        打印信息(f"∵本次作用者【{当前位置}】【{当前元素['名字']}】的旺弱状态为【弱】，∴两者作用关系为：{关系}")
                    
                    if 关系 == '受制关系':
                        下一元素['旺弱状态'] = '弱'
                    打印信息(f"本次被作用者【{下一位置}】【{下一元素['名字']}】因为“{关系}”，所以旺弱状态为【{下一元素.get('旺弱状态', '正常')}】")

                # 第五步：最后窗口作用到被作用方未现天干
                被作用方窗口天干 = 八字信息主字典[被作用方窗口位置]
                最终关系 = 判断两者是否生扶受制(被作用方窗口天干['名字'], 被作用方天干名)
                
                # 判断是否需要镜像反转（正偏性不同）
                被作用方十神 = 被作用方属性['十神']
                被作用方窗口十神 = 被作用方属性['窗口十神']
                被作用方正偏 = '正十神' if str(被作用方十神) in 五个正十神列表大全 else '偏十神'
                窗口正偏 = '正十神' if str(被作用方窗口十神) in 五个正十神列表大全 else '偏十神'
                
                if 被作用方正偏 != 窗口正偏:
                    最终关系 = '受制关系' if 最终关系 == '生扶关系' else '生扶关系'
                    打印信息(f"\n∵未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{被作用方窗口天干['名字']}】的十神【{被作用方窗口十神}】正偏性不同，∴发生镜像反转，变成{最终关系}")
                else:
                    打印信息(f"\n∵未现天干【{被作用方天干名}】的十神【{被作用方十神}】与窗口天干【{被作用方窗口天干['名字']}】的十神【{被作用方窗口十神}】正偏相同，∴它们是作用关系“{最终关系}”不用变")
                if 被作用方窗口天干.get('旺弱状态') == '弱':
                    最终关系 = '受制关系' if 最终关系 == '生扶关系' else '生扶关系'
                    打印信息(f"\n∵窗口天干为弱，∴发生镜像反转，变成{最终关系}")

            # 第六步：判断最终结论
            if 被作用方属性.get('是否空亡') == '空亡':
                被作用环境结论 = '不吉不凶'
            else:
                if 被作用方属性['忌用神归属'] == '用神':
                    被作用环境结论 = '吉' if 最终关系 == '生扶关系' else '凶'
                elif 被作用方属性['忌用神归属'] == '忌神':
                    被作用环境结论 = '吉' if 最终关系 == '受制关系' else '凶'
                else:
                    被作用环境结论 = '不吉不凶'

            # 最后输出结论
            打印信息(f"\n🔍最终被作用方：【未现天干】【{被作用方天干名}】被窗口【{最终关系}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【未现天干】【{被作用方天干名}】【{被作用方十神}】被【未现天干】【{作用方天干名}】【{作用方十神}】作用结论为：【{被作用环境结论}】")
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}



        #情况5、作用方“已现地支”+被作用方“已现天干”     情况6、作用方“已现地支”+被作用方“未现天干”
        elif 作用方_地支 and 被作用方_天干:
            if 八字信息主字典[作用方_地支['位置']].get('是否空亡') == '空亡':
                打印信息("作用方地支为空亡，无法作用！")
                return
            # 第一步：获取基本信息
            作用方信息 = 作用方_地支
            被作用方信息 = 被作用方_天干

            # 先判断是情况5还是情况6
            if 被作用方信息.get('类型') == '已现天干':
                打印信息("\n进入情况5：作用方“已现地支”+被作用方“已现天干”")
            else:
                打印信息("\n进入情况6：作用方“已现地支”+被作用方“未现天干”")
                被作用方天干名 = 被作用方信息['元素']
                被作用方属性 = 未现正偏十神主字典[被作用方天干名]

            
            # 创建选择窗口
            选择窗口 = tk.Toplevel(作用关系窗口)
            选择窗口.title("选择作用方案")
            选择窗口.geometry("400x150")
            tk.Label(选择窗口, text="你要看哪一个结论？").pack(pady=10)
            

            def 选择方案(方案):
                选择窗口.destroy()
                
                if 方案 == 1:  # 方案一《外在明面上的作用路径》
                    if 被作用方信息.get('类型') == '已现天干':
                        # 情况5：作用方"已现地支"+被作用方"已现天干"⭐️
                        # 第一步：获取作用方地支的同柱天干
                        地支位置 = 作用方信息['位置']
                        同柱天干位置 = 地支位置.replace('支', '干')
                        
                        # 第二步：地支作用同柱天干
                        作用路径 = [地支位置, 同柱天干位置]
                        打印信息("作用路径第一段：" + "→".join(作用路径))
                        
                        当前元素 = 八字信息主字典[地支位置]
                        下一元素 = 八字信息主字典[同柱天干位置]
                        当前元素名字 = 当前元素['名字']
                        下一元素名字 = 下一元素['名字']
                        关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                        需要反转 = False

                        # 检查旺弱状态
                        if 当前元素.get('旺弱状态') == '弱':
                            需要反转 = not 需要反转
                            打印信息(f"\n∵作用者【{地支位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                            
                        # 检查空亡状态
                        if '支' in 地支位置 and 当前元素.get('是否空亡') == '空亡':
                            需要反转 = not 需要反转
                            打印信息(f"\n∵作用者【{地支位置}】【{当前元素名字}】为空亡 ∴该空亡地支作用相邻地支时 要发生作用反转")
                            
                        最终关系 = 关系
                        if 需要反转:
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            
                        打印信息(f"【{地支位置}】【{当前元素名字}】作用于【{同柱天干位置}】【{下一元素名字}】。∵本次作用者【{地支位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为【{最终关系}】")
                        
                        if 最终关系 == '受制关系':
                            下一元素['旺弱状态'] = '弱'
                        打印信息(f"本次被作用者【{同柱天干位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")
                        
                        # 第三步：同柱天干作用到被作用方天干
                        起始位置信息 = {'位置': 同柱天干位置, '类型': '已现天干'}
                        目标位置信息 = {'位置': 被作用方信息['位置'], '类型': '已现天干'}
                        后续路径 = 获取作用路径(起始位置信息, 目标位置信息, 类型='天干')
                        作用路径.extend(后续路径[1:])
                        打印信息("完整作用路径：" + "→".join(作用路径))
                        
                        # 第四步：依次作用
                        最终作用结果 = None
                        for i in range(1, len(作用路径)-1):
                            当前位置 = 作用路径[i]
                            下一位置 = 作用路径[i+1]
                            当前元素 = 八字信息主字典[当前位置]
                            下一元素 = 八字信息主字典[下一位置]
                            当前元素名字 = 当前元素['名字']
                            下一元素名字 = 下一元素['名字']
                            关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                            需要反转 = False
                            
                            if 当前元素.get('旺弱状态') == '弱':
                                需要反转 = not 需要反转
                                打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为【弱】 ∴作用发生反转")
                                
                            最终关系 = 关系
                            if 需要反转:
                                最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                                
                            打印信息(f"【{当前位置}】【{当前元素名字}】作用于【{下一位置}】【{下一元素名字}】")
                            打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为【{最终关系}】")
                            
                            if 最终关系 == '受制关系':
                                下一元素['旺弱状态'] = '弱'
                            打印信息(f"本次被作用者【{下一位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")
                            
                            最终作用结果 = 最终关系

                        # 判断被作用环境结论
                        被作用方属性 = 八字信息主字典[被作用方信息['位置']]
                        if 被作用方属性.get('是否空亡') == '空亡':
                            被作用环境结论 = '不吉不凶'
                        else:
                            if 被作用方属性['忌用神归属'] == '用神':
                                被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                            elif 被作用方属性['忌用神归属'] == '忌神':
                                被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                            else:
                                被作用环境结论 = '不吉不凶'

                        # 输出最终结论
                        打印信息(f"\n🔍最终被作用方：【{被作用方信息['位置']}】【{被作用方属性['名字']}】被前一元素【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【{被作用方信息['位置']}】【{被作用方属性['名字']}】【{被作用方属性['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")
                        

                    else:  # 情况6：作用方"已现地支"+被作用方"未现天干"⭐️
                        # 第一步：获取基本信息
                        被作用方天干名 = 被作用方信息['元素']
                        被作用方属性 = 未现正偏十神主字典[被作用方天干名]
                        窗口位置 = 被作用方属性['窗口位置']
                        
                        # 第二步：地支作用同柱天干
                        地支位置 = 作用方信息['位置']
                        同柱天干位置 = 地支位置.replace('支', '干')
                        作用路径 = [地支位置, 同柱天干位置]
                        打印信息("作用路径第一段：" + "→".join(作用路径))
                        
                        当前元素 = 八字信息主字典[地支位置]
                        下一元素 = 八字信息主字典[同柱天干位置]
                        当前元素名字 = 当前元素['名字']
                        下一元素名字 = 下一元素['名字']
                        关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                        需要反转 = False
                        
                        # 检查旺弱状态
                        if 当前元素.get('旺弱状态') == '弱':
                            需要反转 = not 需要反转
                            打印信息(f"\n∵作用者【{地支位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                            
                        # 检查空亡状态
                        if '支' in 地支位置 and 当前元素.get('是否空亡') == '空亡':
                            需要反转 = not 需要反转
                            打印信息(f"\n∵作用者【{地支位置}】【{当前元素名字}】为空亡 ∴作用发生反转")
                            
                        最终关系 = 关系
                        if 需要反转:
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            
                        打印信息(f"【{地支位置}】【{当前元素名字}】作用于【{同柱天干位置}】【{下一元素名字}】")
                        打印信息(f"∵本次作用者【{地支位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为：{最终关系}")
                        
                        if 最终关系 == '受制关系':
                            下一元素['旺弱状态'] = '弱'
                        打印信息(f"本次被作用者【{同柱天干位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")
                        
                        # 第三步：同柱天干作用到窗口位置
                        起始位置信息 = {'位置': 同柱天干位置, '类型': '已现天干'}
                        目标位置信息 = {'位置': 窗口位置, '类型': '已现天干'}
                        中间路径 = 获取作用路径(起始位置信息, 目标位置信息, 类型='天干')
                        作用路径.extend(中间路径[1:])
                        
                        # 第四步：依次作用
                        最终作用结果 = None
                        for i in range(1, len(作用路径)-1):
                            当前位置 = 作用路径[i]
                            下一位置 = 作用路径[i+1]
                            当前元素 = 八字信息主字典[当前位置]
                            下一元素 = 八字信息主字典[下一位置]
                            当前元素名字 = 当前元素['名字']
                            下一元素名字 = 下一元素['名字']
                            关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                            需要反转 = False
                            
                            if 当前元素.get('旺弱状态') == '弱':
                                需要反转 = not 需要反转
                                打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                                
                            最终关系 = 关系
                            if 需要反转:
                                最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                                
                            打印信息(f"【{当前位置}】【{当前元素名字}】作用于【{下一位置}】【{下一元素名字}】")
                            打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为【{最终关系}】")
                            
                            if 最终关系 == '受制关系':
                                下一元素['旺弱状态'] = '弱'
                            打印信息(f"本次被作用者【{下一位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")
                            最终作用结果 = 最终关系
                        # 第五步：窗口天干作用未现天干（考虑镜像反转）
                        作用路径.append(f"未现天干({被作用方天干名})")
                        打印信息("完整作用路径：" + "→".join(作用路径))
                        
                        窗口天干 = 八字信息主字典[窗口位置]
                        需要反转 = 判断正偏关系(被作用方属性['十神']) != 判断正偏关系(窗口天干['十神'])
                        关系 = 判断两者是否生扶受制(窗口天干['名字'], 被作用方天干名)
                        最终关系 = 关系
                        
                        if 窗口天干.get('旺弱状态') == '弱' or 需要反转:
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            if 窗口天干.get('旺弱状态') == '弱':
                                打印信息(f"∵窗口天干【{窗口天干['名字']}】为【弱】，∴作用【未现天干】【{被作用方天干名}】时发生镜像反转")
                            if 需要反转:
                                打印信息(f"∵窗口天干与未现天干的十神 正偏性不同，∴发生镜像反转")
                        else:
                            打印信息(f"∵窗口天干【{窗口天干['名字']}】为【旺】且与未现天干的十神 正偏性相同，∴保持正常作用【{最终关系}】")
                        
                        最终作用结果 = 最终关系

                        # 判断被作用环境结论
                        if 被作用方属性.get('是否空亡') == '空亡':
                            被作用环境结论 = '不吉不凶'
                        else:
                            if 被作用方属性['忌用神归属'] == '用神':
                                被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                            elif 被作用方属性['忌用神归属'] == '忌神':
                                被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                            else:
                                被作用环境结论 = '不吉不凶'

                        # 输出最终结论
                        打印信息(f"\n🔍最终被作用方：【未现天干】【{被作用方天干名}】被前一元素【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【未现天干】【{被作用方天干名}】【{被作用方属性['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")
                    



                else:  # 方案二《人物内心想法/内在健康的作用路径》
                    if 被作用方信息.get('类型') == '已现天干':
                        
                        # 情况5：作用方“已现地支”+被作用方“已现天干”⭐️
                        # 第一步：获取被作用方天干的同柱地支
                        天干位置 = 被作用方信息['位置']
                        目标地支位置 = 天干位置.replace('干', '支')
                        
                        # 第二步：作用方地支作用到目标地支
                        起始信息 = {'位置': 作用方信息['位置'], '类型': '已现地支'}
                        目标信息 = {'位置': 目标地支位置, '类型': '已现地支'}
                        作用路径 = 获取作用路径(起始信息, 目标信息, 类型='地支')
                        打印信息("作用路径第一段：" + "→".join(作用路径))
                        
                        # 第三步：依次作用
                        最终作用结果 = None
                        for i in range(len(作用路径)-1):
                            当前位置 = 作用路径[i]
                            下一位置 = 作用路径[i+1]
                            当前元素 = 八字信息主字典[当前位置]
                            下一元素 = 八字信息主字典[下一位置]
                            当前元素名字 = 当前元素['名字']
                            下一元素名字 = 下一元素['名字']
                            关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                            需要反转 = False     
                            if 当前元素.get('旺弱状态') == '弱':
                                需要反转 = not 需要反转
                                打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                            # 检查空亡状态
                            if '支' in 当前位置 and 八字信息主字典[当前位置].get('是否空亡') == '空亡':
                                需要反转 = not 需要反转
                                打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为空亡 ∴该空亡地支作用相邻地支时 要发生作用反转")
                            if '支' in 下一位置 and 八字信息主字典[下一位置].get('是否空亡') == '空亡':
                                需要反转 = not 需要反转
                                打印信息(f"\n∵被作用者【{下一位置}】【{下一元素名字}】为空亡 ∴该空亡地支作用同柱天干时 要发生作用反转")
                            最终关系 = 关系
                            if 需要反转:
                                最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            打印信息(f"【{当前位置}】【{当前元素名字}】作用于【{下一位置}】【{下一元素名字}】")
                            打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为：{最终关系}")

                            if 最终关系 == '受制关系':
                                下一元素['旺弱状态'] = '弱'
                            打印信息(f"本次被作用者【{下一位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")

                        # 第四步：目标地支 作用于 其同柱天干
                        作用路径.append(天干位置)
                        打印信息("完整作用路径：" + "→".join(作用路径))
                        目标地支 = 八字信息主字典[目标地支位置]
                        被作用方天干 = 八字信息主字典[天干位置]
                        关系 = 判断两者是否生扶受制(目标地支['名字'], 被作用方天干['名字'])
                        最终关系 = 关系
                        if 目标地支.get('旺弱状态') == '弱':
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            打印信息(f"∵目标天干的同柱地支为弱，∴发生镜像反转，变成【{最终关系}】") 
                        else:
                            打印信息(f"∵目标天干的同柱地支不为弱，∴保持原关系【{最终关系}】") 
                        if 最终关系 == '受制关系':
                            被作用方天干['旺弱状态'] = '弱'
                        最终作用结果 = 最终关系

                        
                        # 判断被作用环境结论
                        被作用方属性 = 八字信息主字典[被作用方信息['位置']]
                        if 被作用方属性.get('是否空亡') == '空亡':
                            被作用环境结论 = '不吉不凶'
                        else:
                            if 被作用方属性['忌用神归属'] == '用神':
                                被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                            elif 被作用方属性['忌用神归属'] == '忌神':
                                被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                            else:
                                被作用环境结论 = '不吉不凶'

                        # 输出最终结论
                        打印信息(f"\n🔍最终被作用方：【{天干位置}】【{被作用方天干['名字']}】被前一元素【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【{天干位置}】【{被作用方天干['名字']}】【{被作用方属性['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")


                        
                    else:  
                        # 情况6：作用方"已现地支"+被作用方"未现天干"⭐️
                        # 第一步：获取基本信息
                        被作用方天干名 = 被作用方信息['元素']
                        被作用方属性 = 未现正偏十神主字典[被作用方天干名]
                        窗口位置 = 被作用方属性['窗口位置']
                        窗口地支位置 = 窗口位置.replace('干', '支')
                        
                        # 第二步：作用方地支作用到窗口地支
                        起始信息 = {'位置': 作用方信息['位置'], '类型': '已现地支'}
                        目标信息 = {'位置': 窗口地支位置, '类型': '已现地支'}
                        作用路径 = 获取作用路径(起始信息, 目标信息, 类型='地支')
                        打印信息("作用路径第一段：" + "→".join(作用路径))
                        
                        # 第三步：依次作用
                        最终作用结果 = None
                        for i in range(len(作用路径)-1):
                            当前位置 = 作用路径[i]
                            下一位置 = 作用路径[i+1]
                            当前元素 = 八字信息主字典[当前位置]
                            下一元素 = 八字信息主字典[下一位置]
                            当前元素名字 = 当前元素['名字']
                            下一元素名字 = 下一元素['名字']
                            关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                            需要反转 = False     
                            最终关系 = 关系
                            打印信息(f"【{当前位置}】【{当前元素名字}】作用于【{下一位置}】【{下一元素名字}】")

                            if 当前元素.get('旺弱状态') == '弱':
                                需要反转 = not 需要反转
                                打印信息(f"∵作用者【{当前位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                            # 检查空亡状态
                            if '支' in 当前位置 and 八字信息主字典[当前位置].get('是否空亡') == '空亡':
                                需要反转 = not 需要反转
                                打印信息(f"∵作用者【{当前位置}】【{当前元素名字}】为空亡 ∴作用发生反转")
                            if '支' in 下一位置 and 八字信息主字典[下一位置].get('是否空亡') == '空亡':
                                需要反转 = not 需要反转
                                打印信息(f"∵被作用者【{下一位置}】【{下一元素名字}】为空亡 ∴作用发生反转")
                            
                            if 需要反转:
                                最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            
                            打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为：{最终关系}")

                            if 最终关系 == '受制关系':
                                下一元素['旺弱状态'] = '弱'
                            打印信息(f"本次被作用者【{下一位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")

                        # 第四步：窗口地支作用窗口天干
                        作用路径.extend([窗口位置, f"未现天干({被作用方天干名})"])
                        打印信息("完整作用路径：" + "→".join(作用路径))
                        
                        窗口地支 = 八字信息主字典[窗口地支位置]
                        窗口天干 = 八字信息主字典[窗口位置]
                        关系 = 判断两者是否生扶受制(窗口地支['名字'], 窗口天干['名字'])
                        最终关系 = 关系
                        if 窗口地支.get('旺弱状态') == '弱':
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            打印信息(f"∵窗口天干的同柱地支【{窗口地支位置}】【{窗口地支['名字']}】为弱，∴它俩发生镜像反转，变成【{最终关系}】")
                        else:
                            打印信息(f"∵窗口天干的同柱地支【{窗口地支位置}】【{窗口地支['名字']}】不为弱，∴它俩保持原关系【{最终关系}】")
                        if 最终关系 == '受制关系':
                            窗口天干['旺弱状态'] = '弱'
                        
                        # 第五步：窗口天干作用未现天干（考虑镜像反转）
                        需要反转 = 判断正偏关系(被作用方属性['十神']) != 判断正偏关系(窗口天干['十神'])
                        关系 = 判断两者是否生扶受制(窗口天干['名字'], 被作用方天干名)
                        最终关系 = 关系
                        if 窗口天干.get('旺弱状态') == '弱' or 需要反转:
                            最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                            if 窗口天干.get('旺弱状态') == '弱':
                                打印信息(f"∵窗口天干【{窗口天干['名字']}】被同柱地支作用后为【弱】，∴【{窗口天干['名字']}】作用【未现天干】【{被作用方天干名}】时发生镜像反转")
                            else:
                                打印信息(f"∵窗口天干【{窗口天干['名字']}】被同柱地支作用后为【旺】，∴【{窗口天干['名字']}】作用【未现天干】【{被作用方天干名}】时保持正常作用")

                            if 需要反转:
                                打印信息(f"∵窗口天干与未现天干的十神 正偏性不同，∴发生镜像反转")
                            else:
                                打印信息(f"∵窗口天干与未现天干的十神 正偏性相同，∴保持正常作用")
                        最终作用结果 = 最终关系

                        # 判断被作用环境结论
                        if 被作用方属性.get('是否空亡') == '空亡':
                            被作用环境结论 = '不吉不凶'
                        else:
                            if 被作用方属性['忌用神归属'] == '用神':
                                被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                            elif 被作用方属性['忌用神归属'] == '忌神':
                                被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                            else:
                                被作用环境结论 = '不吉不凶'

                        # 输出最终结论
                        打印信息(f"\n🔍最终被作用方：【未现天干】【{被作用方天干名}】被前一元素【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【未现天干】【{被作用方天干名}】【{被作用方属性['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")
                

        
            # 添加选择按钮
            tk.Button(选择窗口, text="方案一《外在明面上的作用路径》", command=lambda: 选择方案(1)).pack(pady=5)
            tk.Button(选择窗口, text="方案二《人物内心想法/内在健康的作用路径》", command=lambda: 选择方案(2)).pack(pady=5)
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}


        # 情况7：作用方"已现地支" + 被作用方"已现地支"⭐️
        elif 作用方_地支 and 被作用方_地支:
            打印信息("\n进入情况7：作用方“已现地支” + 被作用方“已现地支”")
            def 判断地支忌用神归属(地支位置):
                nonlocal 八字信息主字典
                天干位置 = 地支位置.replace('支', '干')

                天干 = 八字信息主字典[天干位置]
                if 天干['忌用神归属'] == '忌神':
                    if 天干.get('是否有根') == '有根':
                        八字信息主字典[地支位置]['忌用神归属'] = '忌神'
                    else:
                        八字信息主字典[地支位置]['忌用神归属'] = '用神'
                elif 天干['忌用神归属'] == '用神':
                    if 天干.get('是否有根') == '有根':
                        八字信息主字典[地支位置]['忌用神归属'] = '用神'
                    else:
                        八字信息主字典[地支位置]['忌用神归属'] = '忌神'
            # 为所有地支设置忌用神归属
            for 地支位置 in ['年支', '月支', '日支', '时支']:
                判断地支忌用神归属(地支位置)

            # 第一步：获取双方信息
            作用方信息 = {'位置': 作用方_地支['位置'], '类型': '已现地支'}
            被作用方信息 = {'位置': 被作用方_地支['位置'], '类型': '已现地支'}

            # 第二步：获取作用路径
            作用路径 = 获取作用路径(作用方信息, 被作用方信息, 类型='地支')
            if not 作用路径:  # 如果正向路径为空，尝试逆向路径
                作用路径 = 获取作用路径(被作用方信息, 作用方信息, 类型='地支')
                if 作用路径:  # 如果找到逆向路径，将其反转
                    作用路径 = 作用路径[::-1]
            打印信息("作用路径：" + "→".join(作用路径))

            # 第三步：依次作用
            最终作用结果 = None
            for i in range(len(作用路径)-1):
                当前位置 = 作用路径[i]
                下一位置 = 作用路径[i+1]
                当前元素 = 八字信息主字典[当前位置]
                下一元素 = 八字信息主字典[下一位置]
                当前元素名字 = 当前元素['名字']
                下一元素名字 = 下一元素['名字']
                关系 = 判断两者是否生扶受制(当前元素['名字'], 下一元素['名字'])
                需要反转 = False

                # 检查旺弱状态
                if 当前元素.get('旺弱状态') == '弱':
                    需要反转 = not 需要反转
                    打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为弱 ∴作用发生反转")
                
                # 检查空亡状态
                if '支' in 当前位置 and 当前元素.get('是否空亡') == '空亡':
                    需要反转 = not 需要反转
                    打印信息(f"\n∵作用者【{当前位置}】【{当前元素名字}】为空亡 ∴该空亡地支作用相邻地支时 要发生作用反转")
                
                最终关系 = 关系
                if 需要反转:
                    最终关系 = '受制关系' if 关系 == '生扶关系' else '生扶关系'
                
                打印信息(f"【{当前位置}】【{当前元素名字}】作用于【{下一位置}】【{下一元素名字}】")
                打印信息(f"∵本次作用者【{当前位置}】【{当前元素名字}】的旺弱状态为【{当前元素.get('旺弱状态')}】，∴两者作用关系为：{最终关系}")
                
                if 最终关系 == '受制关系':
                    下一元素['旺弱状态'] = '弱'
                打印信息(f"本次被作用者【{下一位置}】【{下一元素名字}】的旺弱状态为【{下一元素.get('旺弱状态')}】")
                
                最终作用结果 = 最终关系

            # 第四步：判断被作用环境结论
            被作用方属性 = 八字信息主字典[被作用方信息['位置']]
            if 被作用方属性.get('是否空亡') == '空亡':
                被作用环境结论 = '不吉不凶'
            # 检查作用方是否空亡
            elif 八字信息主字典[作用路径[0]].get('是否空亡') == '空亡':
                被作用环境结论 = '不吉不凶'
            # 检查作用路径中是否有空亡元素
            elif any(八字信息主字典[位置].get('是否空亡') == '空亡' for 位置 in 作用路径[1:-1]):
                被作用环境结论 = '不吉不凶'

            else:
                if 被作用方属性['忌用神归属'] == '用神':
                    被作用环境结论 = '吉' if 最终作用结果 == '生扶关系' else '凶'
                elif 被作用方属性['忌用神归属'] == '忌神':
                    被作用环境结论 = '吉' if 最终作用结果 == '受制关系' else '凶'
                else:
                    被作用环境结论 = '不吉不凶'

            # 第五步：输出最终结论
            打印信息(f"\n最终被作用方：【{被作用方信息['位置']}】【{被作用方属性['名字']}】被前一元素【{最终作用结果}】，∵被作用方为【{被作用方属性['忌用神归属']}】，∴最终【{被作用方信息['位置']}】【{被作用方属性['名字']}】【{被作用方属性['十神']}】被【{作用路径[0]}】【{八字信息主字典[作用路径[0]]['名字']}】【{八字信息主字典[作用路径[0]]['十神']}】作用结论为：【{被作用环境结论}】")
            return {'作用方': 作用方,'被作用方': 被作用方,'作用结论': 被作用环境结论}
        
        else:
            打印信息("无法得出结论，因为天干只能作用天干，天干绝对不能作用地支")
            return {'作用方': None,'被作用方': None,'作用结论': "天干只能作用天干，天干绝对不能作用地支，无法得出结论"}






    def 自动获取作用结论(作用方, 被作用方):

        global 选中值
        选中值 = {'作用方天干': '', '作用方地支': '', '被作用方天干': '', '被作用方地支': ''}

        # 设置作用方信息
        if '干' in 作用方:
            选中值['作用方天干'] = {
                '元素': 八字信息主字典[作用方]['名字'],
                '位置': 作用方,
                '十神': 八字信息主字典[作用方]['十神'],
                '类型': '已现天干'
            }
            选中值['作用方来源'] = '已现天干'

        elif '支' in 作用方:
            选中值['作用方地支'] = {
                '元素': 八字信息主字典[作用方]['名字'],
                '位置': 作用方,
                '类型': '已现地支'
            }
            选中值['作用方来源'] = '已现地支'

        # 设置被作用方信息
        if '干' in 被作用方:
            选中值['被作用方天干'] = {
                '元素': 八字信息主字典[被作用方]['名字'],
                '位置': 被作用方,
                '十神': 八字信息主字典[被作用方]['十神'],
                '类型': '已现天干'
            }
            选中值['被作用方来源'] = '已现天干'

        elif '支' in 被作用方:
            选中值['被作用方地支'] = {
                '元素': 八字信息主字典[被作用方]['名字'],
                '位置': 被作用方,
                '类型': '已现地支'
            }
            选中值['被作用方来源'] = '已现地支'

        
        for key in 八字信息主字典:
            八字信息主字典[key]['旺弱状态'] = 'None'


        结果 = 检查作用关系(显示过程=False)
        print(f"检查作用关系返回结果：{结果}")
        return 结果



    # 创建命主关键信息按钮
    def 显示命主关键信息():

        print("\n命主关键信息罗列如下：") 
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
        print(f"\n·{'男命' if 性别 == '男' else '女命'}，出生地[未知]")

        # 输出命局透出十神
        print("\n·命局透出十神：")
        for 位置 in ['年干', '月干', '时干']:
            天干 = 八字信息主字典[位置]
            print(f"{位置}-{天干['名字']}-{天干['十神']}-{天干['忌用神归属']}", end="  ")
        for 位置 in ['年支', '月支', '时支']:
            地支 = 八字信息主字典[位置]
            print(f"{位置}-{地支['名字']}-{地支['忌用神归属']}", end="  ")

        # 输出所有未现十神
        print("\n·所有未现十神：")
        for 天干, 信息 in 未现正偏十神主字典.items():
            print(f"{天干}-{信息['十神']}-{信息['忌用神归属']}", end="  ")

        # 输出命局透出十神的环境吉凶
        print("\n·命局透出十神的环境的吉凶：")
        for 位置 in ['年干', '月干', '时干']:
            天干 = 八字信息主字典[位置]
            print(f"{位置}-{天干['名字']}-{天干['十神']}-{天干['忌用神归属']}：", end="")
            print(f"外环境【{天干['外环境']}】、内环境【{天干['内环境']}】、社会环境【{天干['左环境']}】、内心环境【{天干['右环境']}】、内环境的左环境【{天干['内环境左环境']}】、内环境的右环境【{天干['内环境右环境']}】、国外环境【{天干['国外环境']}】")


        # 输出未现十神的环境吉凶
        print("\n·未现十神的环境的吉凶：")
        for 天干, 信息 in 未现正偏十神主字典.items():
            print(f"{天干}-{信息['十神']}-{信息['忌用神归属']}：", end="")
            print(f"外环境【{信息['外环境']}】、内环境【{信息['内环境']}】、社会环境【{信息['左环境']}】、内心环境【{信息['右环境']}】、内环境的左环境【{信息['内环境左环境']}】、内环境的右环境【{信息['内环境右环境']}】")

        # 输出日干作用结论
        print("\n·【日干】作用所有命局透出十神后的吉凶：")
        for 位置, 结论 in 日干作用结论字典.items():
            print(f"【日干】让【{八字信息主字典[位置]['十神']}】【{结论}】")

        # 输出被日干作用结论
        print("\n·每个透出十神让【日干】应吉凶：")
        for 位置, 结论 in 被日干作用结论字典.items():
            print(f"【{八字信息主字典[位置]['十神']}】让【日干】【{结论}】")

        # 输出日支作用结论
        print("\n·【日支】让每个透出十神的根应吉凶：")
        for 位置, 结论 in 日支作用结论字典.items():
            相应天干位置 = 位置.replace('支', '干')
            print(f"【日支】让【{八字信息主字典[相应天干位置]['十神']}】的根【{结论}】")

        # 输出被日支作用结论
        print("\n·每个透出十神的根让【日支】应吉凶：")
        for 位置, 结论 in 被日支作用结论字典.items():
            相应天干位置 = 位置.replace('支', '干')
            print(f"【{八字信息主字典[相应天干位置]['十神']}】的根让【日支】【{结论}】")

        # 输出所有未现十神的窗口十神
        print("\n·所有未现十神的'窗口十神'：")
        for 天干, 信息 in 未现正偏十神主字典.items():
            print(f"{天干}的窗口十神是【{信息['窗口十神']}】(位于{信息['窗口位置']}的{信息['窗口名字']})")





    命主关键信息按钮 = tk.Button(作用关系窗口,text="命主关键信息自动获取",font=("Arial", 10),
    command=显示命主关键信息,relief="solid",bd=0.5)
    命主关键信息按钮.pack(anchor='w', pady=(10, 0))



    # 添加确认按钮
    确认按钮 = tk.Button(
        作用关系窗口,
        text="查询作用关系",
        font=("Arial", 10),
        command=检查作用关系,
        relief="solid",
        bd=0.5
    )
    确认按钮.pack(side=tk.BOTTOM, pady=(0, 20))









#【基本信息提取】提取日主（me）和月支（month），并整理天干地支信息
me = 本命盘四个天干名字列表.day
month = 本命盘四个地支名字列表.month
alls = list(本命盘四个天干名字列表) + list(本命盘四个地支名字列表)

#【天干十神计算】
四个天干十神列表 = []
for seq, item in enumerate(本命盘四个天干名字列表):   #这行代码遍历四柱的天干（年、月、日、时）
    if seq == 2:
        四个天干十神列表.append('--')  # 如果是第三个天干（seq == 2，因为索引从0开始），也就是日柱天干，直接添加'--'。这是因为日主与自己没有十神关系。
    else:
        四个天干十神列表.append(十神关系表[me][item]) # 其他天干，使用 十神关系表[me][item] 来确定十神
print("本命局里四个天干十神列表：", 四个天干十神列表)

#【地支十神计算】
四个地支十神列表 = [] 
for item in 本命盘四个地支名字列表:
    d = 地支藏干字典[item]
    四个地支十神列表.append(十神关系表[me][max(d, key=d.get)])
print("本命局里四个地支十神列表：", 四个地支十神列表)

shens = 四个天干十神列表 + 四个地支十神列表


四个地支十神列表2 = [] # 地支的所有神，包含余气和尾气, 混合在一起
地支_shen3 = [] 
for item in 本命盘四个地支名字列表:
    d = 地支藏干字典[item]
    tmp = ''
    for item2 in d:
        四个地支十神列表2.append(十神关系表[me][item2])
        tmp += 十神关系表[me][item2]
    地支_shen3.append(tmp)
shens2 = 四个天干十神列表 + 四个地支十神列表2



# 计算大运的方向
# 定义完整的十天干和十二地支列表，用于计算大运
阳属性天干列表 = ["甲","丙","戊","庚","壬"]
阴属性天干列表 = ["乙","丁","己","辛","癸"]
阳属性地支列表 = ["子", "寅","辰","午","申","戌"]
阴属性地支列表 = ["丑", "卯","巳","未","酉","亥"]
天干列表 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支列表 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 获取年干在天干列表中的索引
年干索引 = 天干列表.index(本命盘四个天干名字列表.year)
# 判断大运的顺逆方向，根据年干的阴阳属性和性别确定
if options.n:  # 男性
    if 年干索引 % 2 == 0:
        direction = -1  # 阳年男逆排
    else:
        direction = 1   # 阴年男顺排
else:          # 女性
    if 年干索引 % 2 == 0:
        direction = 1   # 阳年女顺排
    else:
        direction = -1  # 阴年女逆排

# 计算大运的具体内容
# 获取月干和月支在天干列表和地支列表中的索引
天干_序列 = 天干列表.index(本命盘四个天干名字列表.month)        #原文：gan_seq = Gan.index(gans.month)
地支_序列 = 地支列表.index(本命盘四个地支名字列表.month)        #原文：zhi_seq = Zhi.index(zhis.month)
zhus = [item for item in zip(本命盘四个天干名字列表, 本命盘四个地支名字列表)]
for i in range(12):
    # 按照方向更新索引，并使用取模实现循环
    天干_序列 = (天干_序列 + direction) % 10
    地支_序列 = (地支_序列 + direction) % 12
    # 获取对应的大运天干和大运地支
    大运天干 = 天干列表[天干_序列]
    大运地支 = 地支列表[地支_序列]


yun = ba.getYun(not options.n) 
for dayun in yun.getDaYun()[1:]:   
    gan_ = dayun.getGanZhi()[0]     
    zhi_ = dayun.getGanZhi()[1]
    fu = '*' if (gan_, zhi_) in zhus else " "
    地支藏干字典_ = ''                 #计算初始化一个空字符串地支藏干字典_，用于存储大运地支的藏干信息
    for gan in 地支藏干字典[zhi_]:     #遍历当前大运的地支藏干,地支藏干字典是《地支藏干字典》
        地支藏干字典_ = 地支藏干字典_ + "{}{}　".format(gan, 十神关系表[me][gan])   #为每个藏干添加其与日主的十神关系
    
    zhi__ = set()             #创建一个空集合zhi__，用于存储大运地支与本命盘地支的关系
    
    for item in 本命盘四个地支名字列表:        #遍历 本命盘四个地支名字列表，也就是本命盘的四柱地支（年支、月支、日支、时支）
    
        for type_ in 地支合会破刑害字典[zhi_]:      #遍历当前大运地支 zhi_ 在 地支合会破刑害字典 字典《地支刑冲合害字典》中的关系
            if item in 地支合会破刑害字典[zhi_][type_]:   #检查本命盘中的地支 item 是否与当前大运地支 zhi_ 存在《地支刑冲合害字典》中的关系
                zhi__.add(type_ + ":" + item)  #如果存在关系，就将这个关系信息添加到 zhi__ 集合中。格式为 "关系类型:地支"
    zhi__ = '  '.join(zhi__)   #最后zhi__ 包含了当前大运地支与本命盘四柱地支之间所有的特殊关系（如刑、冲、合、害）的字符串大全（它可能看起来像这样："刑:寅  冲:申  合:酉  害:未"）
    
    empty = chr(12288)
    if zhi_ in 地支空亡字典[zhus[2]]:  
        empty = '地支空亡'        
    


    #《打印大运》
    jia = ""
    if gan_ in 本命盘四个天干名字列表:
        for i in range(4):
            if gan_ == 本命盘四个天干名字列表[i]:
                if abs(地支列表.index(zhi_) - 地支列表.index(本命盘四个地支名字列表[i])) == 2:
                    jia = jia + "  --夹：" +  地支列表[( 地支列表.index(zhi_) + 地支列表.index(本命盘四个地支名字列表[i]) )//2]
                if abs(地支列表.index(zhi_) - 地支列表.index(本命盘四个地支名字列表[i]) ) == 10:
                    jia = jia + "  --夹：" +  地支列表[(地支列表.index(zhi_) + 地支列表.index(本命盘四个地支名字列表[i]))%12]
    age = dayun.getStartAge()
    year_str = '📒大运'  
    ganzhi = dayun.getGanZhi()
    out = "{age:<3d}岁    {year:<7s}{ganzhi:<5s}   {shi_shen}    {empty} {fu}     {gan}:{十神关系}{yinyang}      {zhi}:{地支_十神关系}{yinyang}          {zhi_info}".format(         
        # 原作者写的是：{gan}:{十神关系}{yinyang}{天干间合冲关系判断:{fill}<6s}{zhi_info}{zhi}{yinyang}{地支_十神关系}
        #- {zhi_canggan:{fill}<10s} {other}".format(
        shi_shen=十神关系表[me][gan_], empty=empty, fu=fu, age=age, year=year_str, ganzhi=ganzhi,
        gan=gan_, 十神关系=十神关系表[me][gan_],fill=chr(12288),
        yinyang=计算阴阳属性(zhi_), 天干间合冲关系判断=天干间合冲关系判断(gan_, 本命盘四个天干名字列表), zhi=zhi_, 地支_十神关系=十神关系表[me][zhi_], zhi_info=zhi__, other='')    #zhi__ 是用于存储大运地支与本命盘地支刑冲合害关系的关系
        #zhi_canggan=地支藏干字典_,
    print(out)



    gan_index = 天干列表.index(gan_)
    zhi_index = 地支列表.index(zhi_)
    def get_shens(本命盘四个天干名字列表, 本命盘四个地支名字列表, gan_, zhi_):         
        all_shens = []
        for item in year_shens:
            if zhi_ in year_shens[item][本命盘四个地支名字列表.year]:    
                all_shens.append(item)
                    
        for item in month_shens:
            if gan_ in month_shens[item][本命盘四个地支名字列表.month] or zhi_ in month_shens[item][本命盘四个地支名字列表.month]:     
                all_shens.append(item)
                    
        for item in day_shens:
            if zhi_ in day_shens[item][本命盘四个地支名字列表.day]:     
                all_shens.append(item)
                    
        for item in g_shens:
            if zhi_ in g_shens[item][me]:    
                all_shens.append(item) 
        if all_shens:  
            return "  神:" + ' '.join(all_shens)
        else:
            return ""
    out = out + jia + get_shens(本命盘四个天干名字列表, 本命盘四个地支名字列表, gan_, zhi_)
    #print(out)


    zhis2 = list(本命盘四个地支名字列表) + [zhi_]      #计算每个大运中的流年
    gans2 = list(本命盘四个天干名字列表) + [gan_]
    for liunian in dayun.getLiuNian():
        gan2_ = liunian.getGanZhi()[0]     #获取流年的天干（gan2_）和地支（zhi2_）
        zhi2_ = liunian.getGanZhi()[1]
        fu2 = '*' if (gan2_, zhi2_) in zhus else " "  #检查这个干支组合是否与本命盘的四柱相同。如果相同，就标记一个星号，表示特殊的本命年
        zhi6_ = ''   #地支藏干计算（在八字中，每个地支都藏有一些天干，这叫做"藏干"。例如，寅木藏甲、丙、戊）
        for gan in 地支藏干字典[zhi2_]:   #从预定义的字典中获取流年地支的藏干，遍历这个地支的所有藏干  
            zhi6_ = zhi6_ + "{}{}　".format(gan, 十神关系表[me][gan])   #对于流年地支中的每个相关天干，代码在计算每个藏干与日主（me）的十神关系
        # 大运地地支作用关系
        zhi__ = set()
        for item in zhis2:
            for type_ in 地支合会破刑害字典[zhi2_]:
                if type_ == '破':
                    continue
                if item in 地支合会破刑害字典[zhi2_][type_]:
                    zhi__.add(type_ + ":" + item)
        zhi__ = '  '.join(zhi__)
        #《打印流年》
        empty = chr(12288)
        if zhi2_ in 地支空亡字典[zhus[2]]:
            empty = '地支空亡'       
        age = liunian.getAge()
        year_str = str(liunian.getYear())
        ganzhi = gan2_ + zhi2_
        out = "{age:<3d}岁    {year:<7s}   {ganzhi:<5s}   {shi_shen}    {empty} {fu}     {gan}:{十神关系}{yinyang}      {zhi}:{地支_十神关系}{yinyang}          {zhi_info}".format(
            # 原作者写的是：{gan}:{十神关系}{yinyang}{天干间合冲关系判断:{fill}<6s}{zhi_info}{zhi}{yinyang}{地支_十神关系}
            # - {zhi_canggan:{fill}<10s} {other}".format(
            age=age, year=year_str, ganzhi=ganzhi, shi_shen=十神关系表[me][gan2_], empty=empty, fu=fu2,gan=gan2_,fill=chr(12288),
            十神关系=十神关系表[me][gan2_],yinyang=计算阴阳属性(zhi2_), 天干间合冲关系判断=天干间合冲关系判断(gan2_, gans2), zhi=zhi2_, 地支_十神关系=十神关系表[me][zhi2_],zhi_info=zhi__ ,other='')  #zhi__ 是用于存储大运地支与本命盘地支刑冲合害关系的关系
            #zhi_canggan=zhi6_)

        print(out)



if 本命盘四个天干名字列表 is not None and 本命盘四个地支名字列表 is not None:
    user_choice = 显示四柱八字命盘结果的界面(list(本命盘四个天干名字列表), list(本命盘四个地支名字列表), 四个天干十神列表,四个地支十神列表)   # 调用函数，在GUI中显示四柱八字和十神标签，并获取用户选择

if user_choice:   # 根据用户选择决定是否继续打出其他信息
    pass  # 用户选择继续显示其他信息，默认行为.这里可以保留原有的脚本继续执行
else:
    import sys    # 用户选择只显示四柱八字，结束脚本
    sys.exit()