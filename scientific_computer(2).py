import tkinter.font as tf
import tkinter as tk
from tkinter import ttk
from tkinter import *
import random
from functools import partial
import re
from math import *
from PIL import ImageTk, Image
import tkinter.font as tkFont


# ################# 游 戏 抽 卡 概 率 计 算 器 代 码 ####################
class Probability():
    def __init__(self):
        self.R = {
            "name": "R",
            "color": "#8EA477",
            "size": "20",
            "font": "微软雅黑",
            "person": "R"
        }
        self.SSR = {
            "name": "SSR",
            "color": "#E99067",
            "size": "90",
            "font": "微软雅黑",
            "person": "SSR"
        }

        self.num = 0
        self.tag_id = "0"
        self.success_rate = 0

        # 创建主窗口

        self.root = tk.Tk()
        self.root.title("游戏抽卡概率计算器")
        font = tkFont.Font(size=16, weight="bold")

        self.root.config(background="#E7F1E2")
        # 创建标签和输入框用于抽卡概率计算器
        self.gacha_label = tk.Label(self.root, text="当前抽卡次数：" + str(self.num), bg="#986347",fg="white")
        self.target_pity_label = tk.Label(self.root, text="保底次数:",bg="#E7F1E2",fg="#8EA477",font=font)
        self.success_probability_label = tk.Label(self.root, text="抽卡概率0~1000:",bg="#E7F1E2",fg="#8EA477",font=font)
        self.number = tk.Label(self.root, text="现有抽卡次数:",bg="#E7F1E2",fg="#8EA477",font=font)

        self.target_pity_entry = ttk.Entry(self.root, width=10)
        self.success_probability_entry = ttk.Entry(self.root, width=10)
        self.number_entry = ttk.Entry(self.root, width=10)
        self.calculate_gacha_button = tk.Button(self.root, text="计算",relief="raised", bd=1,bg="#986445",fg="white",width=10, command=self.calculate_gacha_probability)
        self.success_rate_label = tk.Label(self.root, text="抽卡成功率:",bg="#E7F1E2",fg="#8EA477",font=font)
        self.advice_label = tk.Label(self.root, text="建议:",bg="#E7F1E2",fg="#8EA477",font=font)



        self.one_lottery_button = tk.Button(self.root, text="单抽",relief="raised", bd=1,bg="#C4D1BD",width=10, command=self.one)
        self.ten_lottery_button = tk.Button(self.root, text="十连抽",relief="raised", bd=1,bg="#C4D1BD",width=10, command=self.ten)

        self.text = tk.Text(self.root, height=34,bg="#FBF8EA")

        self.gacha_label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)

        self.target_pity_label.grid(column=1, row=1, padx=10, pady=5)
        self.success_probability_label.grid(column=1, row=2, padx=10, pady=5)
        self.number.grid(column=1, row=3, padx=10, pady=5)

        self.target_pity_entry.grid(column=2, row=1, padx=10, pady=5)
        self.success_probability_entry.grid(column=2, row=2, padx=10, pady=5)
        self.number_entry.grid(column=2, row=3, padx=10, pady=5)

        self.calculate_gacha_button.grid(column=1, row=4, columnspan=2, padx=10, pady=5)
        self.success_rate_label.grid(column=1, row=5, columnspan=2, padx=10, pady=5)
        self.advice_label.grid(column=1, row=6, columnspan=2, padx=10, pady=5)

        self.one_lottery_button.grid(column=3, row=0, padx=10, pady=5)
        self.ten_lottery_button.grid(column=4, row=0, padx=10, pady=5)
        self.text.grid(column=3, row=1, columnspan=2, rowspan=6)

        self.root.mainloop()

    # 单抽
    def one(self):
        self.success_rate = float(int(self.success_probability_entry.get()) / 100)
        _res = self.get()
        self.insert_text(conf=_res["level"], message=_res["thing"])
        self.text.insert("end", "\n")
        self.text.see("end")
        self.gacha_label.config(text="当前抽卡次数：" + str(self.num))

    # 十连抽
    def ten(self):
        # 设置字体大小和颜色
        ft = tf.Font(family="微软雅黑", size="20")
        self.text.tag_add('tag' + self.tag_id, "end")
        self.text.tag_config('tag' + self.tag_id, foreground="#8EA477", font=ft)
        self.text.insert("end", "\n============== 十连抽 ==============\n", "tag" + self.tag_id)

        self.tag_id = str(int(self.tag_id) + 1)
        for i in range(10):
            self.one()

    # 抽卡规则
    def get(self):
        self.num += 1
        if self.num % int(self.target_pity_entry.get()) == 0:
            level = self.SSR
            thing = level["person"]
            return {
                "level": level,
                "thing": thing + "(保底抽中)"
            }
        else:
            if random.random() > float(int(self.success_probability_entry.get()) / 1000):
                level = self.R
                thing = level["person"]
            else:
                level = self.SSR
                thing = level["person"]

        return {
            "level": level,
            "thing": thing
        }

    # 添加日志到Text框
    def insert_text(self, message, conf):
        # 设置字体大小和颜色
        ft = tf.Font(family=conf["font"], size=conf["size"])
        self.text.tag_add('tag' + self.tag_id, "end")
        self.text.tag_config('tag' + self.tag_id, foreground=conf["color"], font=ft)
        self.text.insert("end", message + "\n", "tag" + self.tag_id)
        self.text.see("end")
        self.tag_id = str(int(self.tag_id) + 1)

    def calculate_gacha_probability(self):
        try:
            self.success_rate = float(int(self.success_probability_entry.get()) / 100)
            success_rate = 0
            for j in range(0,10000):
                success_count = 0
                for i in range(int(self.number_entry.get())):
                    data = self.get()
                    # print(data["thing"])
                    if data["thing"] != "R":
                        success_count += 1
                if success_count >= 1:
                    success_rate += 1
            success_rate = success_rate/10000
            self.num = 0
            print(success_rate)
            print(self.number_entry.get())
            self.success_rate_label.config(text="抽卡成功率: "+str(round(success_rate*100,2)) + "%")
            # 根据成功率给出建议
            if success_rate >= 0.8:
                self.advice_label.config(text="建议：稳了，直接冲！")
            elif 0.5 <= success_rate <= 0.8:
                self.advice_label.config(text="建议：概率很大，放心抽！")
            elif 0.2 <= success_rate <= 0.5:
                self.advice_label.config(text="建议：要不氪一点吧")
            else:
                self.advice_label.config(text="建议：要不氪亿点吧")
        except ValueError:
            self.success_rate_label.config(text="输入无效，请重新输入。")


# ################# 原神抽卡成功率计算器 ####################
class Genshin():
    def __init__(self):
        # 创建主窗口
        root = tk.Tk()
        root.config(background="#E2EDDB")

        root.title("原神抽卡成功率计算器")
        self.value_1 = tk.Label(root, text="原石",width=10, bg="#8EA478",fg="white",font=("黑体","9","bold"))
        self.value_2 = tk.Label(root, text="纠缠",width=10, bg="#8EA478",fg="white",font=("黑体","9","bold"))
        self.value_3 = tk.Label(root, text="星辉",width=10, bg="#8EA478",fg="white",font=("黑体","9","bold"))
        self.value_4 = tk.Label(root, text="结晶",width=10, bg="#8EA478",fg="white",font=("黑体","9","bold"))
        self.input_1 = tk.Entry(root, width=10)
        self.input_2 = tk.Entry(root, width=10)
        self.input_3 = tk.Entry(root, width=10)
        self.input_4 = tk.Entry(root, width=10)

        # 创建标签和输入框用于抽卡概率计算器
        # 角色池信息
        self.gacha_label = tk.Label(root, text="目标角色池信息", bg="#986347",fg="white")
        self.pity_count_label = tk.Label(root, text="距离上一金抽数", bg="#E2EDDB",fg="#8EA477")
        self.pity_count_entry = tk.Entry(root, width=10)

        self.calculate_gacha_button = tk.Button(root, text="计算",bg="#986445",fg="white",width=10, command=self.calculate_gacha_probability)
        self.success_rate_label = tk.Label(root, text="抽卡成功率:",bg="#E2EDDB",fg="#8EA477")
        self.advice_label = tk.Label(root, text="建议:",bg="#E2EDDB",fg="#8EA477")

        # 武器池信息
        self.gacha_label1 = tk.Label(root, text="目标武器池信息", bg="#986347",fg="white")
        self.pity_count_label1 = tk.Label(root, text="距离上一金抽数", bg="#E2EDDB",fg="#8EA477")
        self.pity_count_entry1 = tk.Entry(root, width=10)

        self.calculate_gacha_button1 = tk.Button(root, text="计算",bg="#986445",fg="white",width=10, command=self.calculate_gacha_probability1)
        self.success_rate_label1 = tk.Label(root, text="抽卡成功率:",bg="#E2EDDB",fg="#8EA477")
        self.advice_label1 = tk.Label(root, text="建议:",bg="#E2EDDB",fg="#8EA477")

        self.value_1.grid(column=1, row=0, padx=5, pady=10)
        self.input_1.grid(column=1, row=1, padx=5, pady=10)
        self.value_2.grid(column=2, row=0, padx=5, pady=10)
        self.input_2.grid(column=2, row=1, padx=5, pady=10)
        self.value_3.grid(column=3, row=0, padx=5, pady=10)
        self.input_3.grid(column=3, row=1, padx=5, pady=10)
        self.value_4.grid(column=4, row=0, padx=5, pady=10)
        self.input_4.grid(column=4, row=1, padx=5, pady=10)

        # 布局界面
        self.gacha_label.grid(column=1, row=2, columnspan=2, padx=10, pady=10)
        self.var = StringVar()

        self.bd = tk.Label(root, text="保底类型",bg="#E2EDDB",fg="#8EA477")
        self.bd.grid(column=1, row=3, padx=10, pady=10)
        self.bd_entry = ttk.Entry(root, width=10)
        self.bd_entry.grid(column=2, row=3, padx=10, pady=10)

        self.pity_count_label.grid(column=1, row=4, padx=10, pady=5)
        self.pity_count_entry.grid(column=2, row=4, padx=10, pady=5)
        self.calculate_gacha_button.grid(column=1, row=5, columnspan=2, padx=10, pady=5)
        self.success_rate_label.grid(column=1, row=6, columnspan=2, padx=10, pady=5)
        self.advice_label.grid(column=1, row=7, columnspan=2, padx=10, pady=5)

        self.gacha_label1.grid(column=3, row=2, columnspan=2, padx=10, pady=10)

        self.bd1 = tk.Label(root, text="保底类型",bg="#E2EDDB",fg="#8EA477")
        self.bd1.grid(column=3, row=3, padx=10, pady=10)
        self.bd_entry1 = ttk.Entry(root, width=10)
        self.bd_entry1.grid(column=4, row=3, padx=10, pady=10)
        self.pity_count_label1.grid(column=3, row=4, padx=10, pady=5)
        self.pity_count_entry1.grid(column=4, row=4, padx=10, pady=5)
        self.calculate_gacha_button1.grid(column=3, row=5, columnspan=2, padx=10, pady=5)
        self.success_rate_label1.grid(column=3, row=6, columnspan=2, padx=10, pady=5)
        self.advice_label1.grid(column=3, row=7, columnspan=2, padx=10, pady=5)
        self.num = 0
        self.num1 = 0

        root.mainloop()

    # 定义角色抽卡概率计算器函数
    def calculate_gacha_probability(self):
        input_1 = int(self.input_1.get())  # 原石  180个抽一次
        input_2 = int(self.input_2.get())  # 纠缠  抽一次
        input_3 = int(self.input_3.get())  # 星辉  抽到五星的10星辉 ，抽到4星的2星辉，5个星辉换1个纠缠
        input_4 = int(self.input_4.get())  # 结晶
        bd_entry = self.bd_entry.get()  # 保底类型
        pity_count_entry = int(self.pity_count_entry.get())  # 距离上一次

        # value = self.calculate_pity(bd_entry, input_1, input_4, input_2, input_3, pity_count_entry)
        total = 0
        for i in range(0, 10000):
            value = self.calculate_pity(bd_entry, input_1, input_4, input_2, input_3, pity_count_entry)
            total = total + value
        total = total / 10000
        self.success_rate_label.config(text="抽卡成功率：" + str(round(total*100,2)) + "%")
        if total >= 0.8:
            self.advice_label.config(text="建议：稳了，直接冲！")
        elif 0.5 <= total < 0.8:
            self.advice_label.config(text="建议：概率很大，放心抽！")
        elif 0.2 <= total < 0.5:
            self.advice_label.config(text="建议：要不氪一点吧")
        else:
            self.advice_label.config(text="建议：要不氪亿点吧")


    # 定义武器抽卡概率计算器函数
    def calculate_gacha_probability1(self):
        input_1 = int(self.input_1.get())  # 原石  180个抽一次
        input_2 = int(self.input_2.get())  # 纠缠  抽一次
        input_3 = int(self.input_3.get())  # 星辉  抽到五星的10星辉 ，抽到4星的2星辉，5个星辉换1个纠缠
        input_4 = int(self.input_4.get())  # 结晶
        bd_entry = self.bd_entry1.get()  # 保底类型
        pity_count_entry = int(self.pity_count_entry1.get())  # 距离上一次

        # value = self.calculate_pity(bd_entry, input_1, input_4, input_2, input_3, pity_count_entry)
        total = 0
        for i in range(0,10000):
            value = self.calculate_pity1(bd_entry, input_1, input_4, input_2, input_3, pity_count_entry)
            total = total +value
        total = total/10000
        self.success_rate_label1.config(text="抽卡成功率：" + str(round(total*100,2)) + "%")
        if total >= 0.8:
            self.advice_label1.config(text="建议：稳了，直接冲！")
        elif 0.5 <= total < 0.8:
            self.advice_label1.config(text="建议：概率很大，放心抽！")
        elif 0.2 <= total < 0.5:
            self.advice_label1.config(text="建议：要不氪一点吧")
        else:
            self.advice_label1.config(text="建议：要不氪亿点吧")


    # 角色池抽卡概率计算模拟          大小保底     原石         结晶           纠缠         星辉        当前抽数
    def calculate_pity(self, gacha_type, primogems, crystals, intertwined_fate, glitter, stardust_count):
        # 计算总抽数
        total_pulls = int((primogems + crystals) / 160 + intertwined_fate + glitter / 5)
        # 计算剩余抽数
        residue = total_pulls
        # 根据保底类型计算UP角色概率和保底抽数
        if gacha_type == "小保底":
            up_prob = 0.003
        else:
            up_prob = 0.006
            stardust_count += 90
        # 五星数量
        five_star_count = 0
        # 星辉剩余数量
        glitter = glitter % 5
        # 开始抽卡
        while residue >= 1:
            # 可抽数减1
            residue -= 1
            # 步数+1
            stardust_count += 1
            if stardust_count == 180:
                # 大到保底
                five_star_count += 1
                glitter += 10
                stardust_count = 0  # 抽数清0
                # print("大保底")
            elif stardust_count == 90:
                if random.random() < 0.5:
                    # 抽到UP角色
                    glitter += 10  # 星辉加10
                    five_star_count += 1  # 五星加1
                    stardust_count = 0  # 抽数清0
                    # print("抽中小保底")
            if stardust_count % 10 == 0:
                glitter += 2
                # print("新辉+2")
            if random.random() < up_prob:
                # 抽到五星角色
                five_star_count += 1
                glitter += 10  # 星辉加10
                five_star_count += 1  # 五星加1
                stardust_count = 0  # 抽数清0
                # print("抽中五星")
            # else:
            #     print("什么都没有")

            # 计算额外抽数
            extra_pulls = int(glitter / 5)
            residue += extra_pulls
            total_pulls += extra_pulls
            # print("==============================================")
            # print("星辉数量：", glitter)
            # print("额外抽数:", extra_pulls)
            # print("总抽数量:", total_pulls)
            # print("当前抽数", residue)
            # print("五星卡片:", five_star_count)
            glitter = glitter % 5

        # 五星次数
        # value = round((five_star_count / total_pulls) * 100, 4)
        if five_star_count >= 1:
            value = 1
        else:
            value = 0
        # print(value)
        return value

    # 角色池抽卡概率计算模拟
    def calculate_pity1(self, gacha_type, primogems, crystals, intertwined_fate, glitter, stardust_count):
        # 计算总抽数
        total_pulls = int((primogems + crystals) / 160 + intertwined_fate + glitter / 5)
        # 计算剩余抽数
        residue = total_pulls
        # 根据保底类型计算UP角色概率和保底抽数
        if gacha_type == "小保底":
            up_prob = 0.00525

        else:
            up_prob = 0.007
            stardust_count += 80
        # 五星数量
        five_star_count = 0
        # 星辉剩余数量
        glitter = glitter % 5
        # 开始抽卡
        while residue >= 1:
            # 可抽数减1
            residue -= 1
            # 步数+1
            stardust_count += 1
            if stardust_count == 160:
                # 大到保底
                five_star_count += 1
                glitter += 10
                stardust_count = 0  # 抽数清0
                # print("大保底")
            elif stardust_count == 80:
                if random.random() < 0.5:
                    # 抽到UP角色
                    glitter += 10  # 星辉加10
                    five_star_count += 1  # 五星加1
                    stardust_count = 0  # 抽数清0
                    # print("抽中小保底")
            if stardust_count % 10 == 0:
                glitter += 2
                # print("新辉+2")
            if random.random() < up_prob:
                # 抽到五星角色
                five_star_count += 1
                glitter += 10  # 星辉加10
                five_star_count += 1  # 五星加1
                stardust_count = 0  # 抽数清0
                # print("抽中五星")
            # else:
                # print("什么都没有")

            # 计算额外抽数
            extra_pulls = int(glitter / 5)
            residue += extra_pulls
            total_pulls += extra_pulls
            # print("==============================================")
            # print("星辉数量：", glitter)
            # print("额外抽数:", extra_pulls)
            # print("总抽数量:", total_pulls)
            # print("当前抽数", residue)
            # print("五星卡片:", five_star_count)
            glitter = glitter % 5

        # 五星次数
        # value = round((five_star_count / total_pulls) * 100, 4)
        if five_star_count >=1 :
            value = 1
        else:
            value = 0
        # print(value)
        return value
# ################# 科学计算器代码 ####################
class Calculator:
    def __init__(self):
        self.root = tk.Tk()  # 生成窗口
        self.root.title('科学计算器')  # 窗口的名字
        self.root.configure(bg='#FAF8EA')
        self.root.resizable(0, 0)  # 窗口大小可调性，分别表示x，y方向的可变性
        global label_text  # 定义全局变量
        label_text = StringVar()
        buju(self.root)
        self.root.mainloop()  # 进入消息循环（必需组件），否则生成的窗口一闪而过


# 将算式从字符串处理成列表，解决横杠是负号还是减号的问题
def formula_format(formula):
    """
    :param formula: str
    """
    formula = re.sub(' ', '', formula)  # 去掉算式中的空格s
    # 以 '横杠数字' 分割， 其中正则表达式：(\-\d+\.?\d*) 括号内：
    # \- 表示匹配横杠开头；\d+ 表示匹配数字1次或多次；\.?表示匹配小数点0次或1次;\d*表示匹配数字0次或多次。
    formula_list = [i for i in re.split('(-[\d+,π,e]\.?\d*)', formula) if i]
    final_formula = []  # 最终的算式列表
    for item in formula_list:
        # 算式以横杠开头，则第一个数字为负数，横杠为负号
        if len(final_formula) == 0 and re.match('-[\d+,π,e]\.?\d*$', item):
            final_formula.append(item)
            continue
        # 如果当前的算式列表最后一个元素是运算符['+', '-', '*', '/', '('， '取余'， '^'], 则横杠为减号
        if len(final_formula) > 0:
            if re.match('[\+\-\*\/\(\%\^]$', final_formula[-1]):
                final_formula.append(item)
                continue
        # 按照运算符分割开
        item_split = [i for i in re.split('([\+\-\*\/\(\)\%\^\√])', item) if i]
        final_formula += item_split
    return final_formula


# 判断是否是运算符，如果是返回True
def is_operator(e):
    """
    :param e: str
    :return: bool
    """
    opers = ['+', '-', '*', '/', '(', ')', '%', '^', '√', 'sin', 'arcsin', 'ln']
    return True if e in opers else False  # 在for循环中嵌套使用if和else语句


# 比较连续两个运算符来判断是压栈还是弹栈
def decision(tail_op, now_op):
    """
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1代表弹栈运算，0代表弹出运算符栈最后一个元素'('，-1表示压栈
    """
    # 定义4种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/', '%']  # %表示取余
    rate3 = ['^', '√', 'sin', 'arcsin', 'ln']
    rate4 = ['(']
    rate5 = [')']

    if tail_op in rate1:
        if now_op in rate2 or now_op in rate3 or now_op in rate4:
            return -1  # 说明当前运算符优先级高于运算符栈的最后一个运算符，需要压栈
        else:
            return 1  # 说明当前运算符优先级等于运算符栈的最后一个运算符，需要弹栈运算

    elif tail_op in rate2:
        if now_op in rate3 or now_op in rate4:
            return -1
        else:
            return 1

    elif tail_op in rate3:
        if now_op in rate4:
            return -1
        else:
            return 1

    elif tail_op in rate4:
        if now_op in rate5:
            return 0  # '('遇上')',需要弹出'('并丢掉')',表明该括号内的算式已计算完成并将结果压入数字栈中
        else:
            return -1  # 只要栈顶元素为'('且当前元素不是')'，都应压入栈中


# 传入两个数字，一个运算符，根据运算符不同返回相应结果
def calculate(n1, n2, operator):
    """
    :param n1: float
    :param n2: float
    :param operator: + - * / % ^
    :return: float
    """
    result = 0
    if operator == '+':
        result = n1 + n2
    if operator == '-':
        result = n1 - n2
    if operator == '*':
        result = n1 * n2
    if operator == '/':
        result = n1 / n2
    if operator == '%':
        result = n1 % n2     # 取余
    if operator == '^':
        result = n1 ** n2
    return result


# 括号内的算式求出计算结果后，计算√()、sin()或arcsin()
def gaojie(op_stack, num_stack):
    if op_stack[-1] == '√':
        op = op_stack.pop()
        num2 = num_stack.pop()
        num_stack.append(sqrt(num2))
    elif op_stack[-1] == 'sin':
        op = op_stack.pop()
        num2 = num_stack.pop()
        num_stack.append(sin(num2))
    elif op_stack[-1] == 'arcsin':
        op = op_stack.pop()
        num2 = num_stack.pop()
        num_stack.append(asin(num2))  #返回x的反正弦弧度值
    elif op_stack[-1] == 'ln':
        op = op_stack.pop()
        num2 = num_stack.pop()
        num_stack.append(log(num2))


# 负责遍历算式列表中的字符，决定压入数字栈中或压入运算符栈中或弹栈运算
def final_calc(formula_list):
    """
    :param formula_list: 算式列表
    :return: 计算结果
    """
    num_stack = []  # 数字栈
    op_stack = []  # 运算符栈
    for item in formula_list:
        operator = is_operator(item)
        # 压入数字栈
        if not operator:
            # π和e转换成可用于计算的值
            if item == 'π':
                num_stack.append(pi)
            elif item == '-π':
                num_stack.append(-pi)
            elif item == 'e':
                num_stack.append(e)
            elif item == '-e':
                num_stack.append(-e)
            else:
                num_stack.append(float(item))  # 字符串转换为浮点数
        # 如果是运算符
        else:
            while True:
                # 如果运算符栈为空，则无条件入栈
                if len(op_stack) == 0:
                    op_stack.append(item)
                    break
                # 决定压栈或弹栈
                tag = decision(op_stack[-1], item)
                # 如果是-1，则压入运算符栈并进入下一次循环
                if tag == -1:
                    op_stack.append(item)
                    break
                # 如果是0，则弹出运算符栈内最后一个'('并丢掉当前')'，进入下一次循环
                elif tag == 0:
                    op_stack.pop()
                    gaojie(op_stack, num_stack)  # '('前是'√'、'sin'或'arcsin'时，对括号内算式的计算结果作相应的运算
                    break
                # 如果是1，则弹出运算符栈内最后一个元素和数字栈内最后两个元素
                elif tag == 1:
                    if item in ['√', 'sin', 'arcsin']:
                        op_stack.append(item)
                        break
                    op = op_stack.pop()
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    # 将计算结果压入数字栈并接着循环，直到遇到break跳出循环
                    num_stack.append(calculate(num1, num2, op))
    # 大循环结束后，数字栈和运算符栈中可能还有元素的情况
    while len(op_stack) != 0:
        op = op_stack.pop()
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        num_stack.append(calculate(num1, num2, op))
    result = str(float(round(num_stack[0],10)))
    # 去掉无效的0和小数点，例：1.0转换为1
    if result[len(result) - 1] == '0' and result[len(result) - 2] == '.':
        result = result[0:-2]
    return result


# 生成计算器主界面
def buju(root):
    # label = Label(root, width=29, height=1, bd=3, bg='#E2F0F0', anchor='se',
    #               textvariable=label_text)  # 标签，可以显示文字或图片
    # label.grid(row=0, columnspan=5)  # 布局器，向窗口注册并显示控件； rowspan：设置单元格纵向跨越的列数

    entry = Entry(root, width=23, bg='#E2F0F0', justify="right", font=('微软雅黑', 12))  # 文本框（单行）
    entry.grid(row=1, column=0, columnspan=5, sticky=N + W + S + E, padx=5, pady=5)  # 设置控件周围x、y方向空白区域保留大小

    myButton = partial(tk.Button, root, width=5, cursor='hand2',bg="#FAF8EA",fg="#986445",)  # 偏函数：带有固定参数的函数
    button_sin = myButton(text='sin', command=lambda: get_input(entry, 'sin('))  # 按钮
    button_arcsin = myButton(text='arcsin', command=lambda: get_input(entry, 'arcsin('))
    button_exp = myButton(text='e', command=lambda: get_input(entry, 'e'))
    button_ln = myButton(text='ln', command=lambda: get_input(entry, 'ln('))
    button_xy = myButton(text='x^y', command=lambda: get_input(entry, '^'))

    button_sin.grid(row=2, column=0)
    button_arcsin.grid(row=2, column=1)
    button_exp.grid(row=2, column=2)
    button_ln.grid(row=2, column=3)
    button_xy.grid(row=2, column=4)

    button_shanyige = myButton(text='←', command=lambda: backspace(entry))  # command指定按钮消息的回调函数
    button_shanquanbu = myButton(text=' C ', command=lambda: clear(entry))
    button_zuokuohao = myButton(text='(', command=lambda: get_input(entry, '('))
    button_youkuohao = myButton(text=')', command=lambda: get_input(entry, ')'))
    button_genhao = myButton(text='√x', command=lambda: get_input(entry, '√('))
    button_shanyige.grid(row=3, column=0)
    button_shanquanbu.grid(row=3, column=1)
    button_zuokuohao.grid(row=3, column=2)
    button_youkuohao.grid(row=3, column=3)
    button_genhao.grid(row=3, column=4)

    button_7 = myButton(text=' 7 ', command=lambda: get_input(entry, '7'))
    button_8 = myButton(text=' 8 ', command=lambda: get_input(entry, '8'))
    button_9 = myButton(text=' 9 ', command=lambda: get_input(entry, '9'))
    button_chu = myButton(text=' / ', command=lambda: get_input(entry, '/'))
    button_yu = myButton(text='取余', command=lambda: get_input(entry, '%'))
    button_7.grid(row=4, column=0)
    button_8.grid(row=4, column=1)
    button_9.grid(row=4, column=2)
    button_chu.grid(row=4, column=3)
    button_yu.grid(row=4, column=4)

    button_4 = myButton(text=' 4 ', command=lambda: get_input(entry, '4'))
    button_5 = myButton(text=' 5 ', command=lambda: get_input(entry, '5'))
    button_6 = myButton(text=' 6 ', command=lambda: get_input(entry, '6'))
    button_cheng = myButton(text=' * ', command=lambda: get_input(entry, '*'))
    button_jiecheng = myButton(text='二进制', command=lambda: jinzhi(entry))
    button_4.grid(row=5, column=0)
    button_5.grid(row=5, column=1)
    button_6.grid(row=5, column=2)
    button_cheng.grid(row=5, column=3)
    button_jiecheng.grid(row=5, column=4)

    button_1 = myButton(text=' 1 ', command=lambda: get_input(entry, '1'), )
    button_2 = myButton(text=' 2 ', command=lambda: get_input(entry, '2'), )
    button_3 = myButton(text=' 3 ', command=lambda: get_input(entry, '3'))
    button_jian = myButton(text=' - ', command=lambda: get_input(entry, '-'))
    button_dengyu = myButton(text=' \n = \n ', command=lambda: calculator(entry))
    button_1.grid(row=6, column=0)
    button_2.grid(row=6, column=1)
    button_3.grid(row=6, column=2)
    button_jian.grid(row=6, column=3)
    button_dengyu.grid(row=6, column=4, rowspan=2)  # rowspan：设置单元格横向跨越的行数

    button_pai = myButton(text=' π ', command=lambda: get_input(entry, 'π'))
    button_0 = myButton(text=' 0 ', command=lambda: get_input(entry, '0'))
    button_xiaoshudian = myButton(text=' . ', command=lambda: get_input(entry, '.'))
    button_jia = myButton(text=' + ', command=lambda: get_input(entry, '+'))
    button_pai.grid(row=7, column=0)
    button_0.grid(row=7, column=1)
    button_xiaoshudian.grid(row=7, column=2)
    button_jia.grid(row=7, column=3)


# 删除最后一次输入内容
def backspace(entry):
    entry.delete(len(entry.get()) - 1)  # 删除文本框的最后一个输入值


# 删除所有输入内容和显示内容
def clear(entry):
    entry.delete(0, END)  # 删除文本框的所有内容
    label_text.set('')


# 点击计算器输入按钮后向文本框中添加内容
def get_input(entry, argu):
    formula = entry.get()
    for char in formula:
        if '\u4e00' <= char <= '\u9fa5':
            clear(entry)  # 删除文本框中的汉字显示，减少手动删除操作
    entry.insert(INSERT, argu)  # 使用END时，键盘敲入和按键输入组合操作会出错


# 十进制整数转换为二进制整数
def jinzhi(entry):
    try:
        formula = entry.get()
        if re.match('\d+$', formula):
            number = int(formula)
            cunchu = []  # 放置每次除以2后的余数
            result = ''
            while number:
                cunchu.append(number % 2)
                number //= 2  # 整数除法,返回商
            while cunchu:
                result += str(cunchu.pop())  # 将所有余数倒置得到结果
            clear(entry)
            entry.insert(END, result)
            label_text.set(''.join(formula + '='))
        else:
            clear(entry)
            entry.insert(END, '请输入十进制整数')
    except:
        clear(entry)
        entry.insert(END, '出错')


# 点击“=”后进行计算
def calculator(entry):
    try:
        formula = entry.get()
        # 输入内容只是数字或π或e时，仍显示该内容
        if re.match('-?[\d+,π,e]\.?\d*$', formula):
            label_text.set(''.join(formula + '='))
            return
        # 输入内容是算式时，显示其计算结果
        result = final_calc(formula_format(formula))
        clear(entry)
        entry.insert(END, result)  # 将结果输出到文本框中
        label_text.set(''.join(formula + '='))
    except:
        clear(entry)
        entry.insert(END, '出错')


# ################# 主函数入口 ####################
def main_program():
    root = tk.Tk()
    root.title("科学计算器+游戏抽卡概率计算器")
    root.geometry('960x563')
    # 加载图像
    image = Image.open("image.png")
    # 调整图像大小以适应窗口
    image = image.resize((960, 563), Image.ANTIALIAS)
    # 创建ImageTk对象
    background_image = ImageTk.PhotoImage(image)
    # 创建标签并设置背景图片
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    font = tkFont.Font(size=12, weight="bold")
    button1 = tk.Button(root, highlightthickness=0, text='游戏抽卡概率计算器', command=Probability,
                        height=3, width=20, bg="#986445",fg="white",font=font)
    button1.grid(column=0, row=0, padx=400, pady=60)

    button2 = tk.Button(root, highlightthickness=0, text='科 学 计 算 器', command=Calculator, height=3, width=20,
                        bg="#986445", fg="white",font=font)
    button2.grid(column=0, row=1, padx=400, pady=60)

    button3 = tk.Button(root, highlightthickness=0, text='原神抽卡成功率计算器', command=Genshin,
                        height=3, width=20,bg="#986445",fg="white",font=font)
    button3.grid(column=0, row=2, padx=400, pady=60)

    root.mainloop()

if __name__ == '__main__':
    main_program()
