import math
from tkinter import ttk
import tkinter as tk  # 导入一个第三方库，用于制作桌面软件
import tkinter.font as tf
from tkinter import *
import random
from functools import partial
import re
from math import *

# ################# 游 戏 抽 卡 概 率 计 算 器代码 ####################
class Genshin_Impact():
    def __init__(self):
        self.R = {
            "name": "R",
            "color": "blue",
            "size": "20",
            "font": "微软雅黑",
            "person": ["冷刃", "黑缨枪", "白缨枪", "翡玉法球", "飞天大御剑", "暗铁剑", "旅行剑", "钢轮弓",
                       "吃鱼虎刀", "沾染龙血的剑", "以理服人", "异世界行记", "甲级宝钰", "翡玉法球"]
        }
        self.SSR = {
            "name": "SSR",
            "color": "yellow",
            "size": "20",
            "font": "微软雅黑",
            "person": ["迪卢克", "七七", "琴", "莫娜", "刻晴"]
        }

        self.num = 0
        self.tag_id = "0"
        self.success_rate = 0

        # 创建主窗口
        root = tk.Tk()
        root.title("游 戏 抽 卡 概 率 计 算 器")
        # 创建标签和输入框用于抽卡概率计算器
        self.gacha_label = ttk.Label(root, text="当前抽卡次数：" + str(self.num))
        self.pity_count_label = ttk.Label(root, text="当前保底次数:")
        self.target_pity_label = ttk.Label(root, text="目标保底次数:")
        self.success_probability_label = ttk.Label(root, text="抽卡概率0~100:")
        self.pity_count_entry = ttk.Entry(root, width=10)
        self.target_pity_entry = ttk.Entry(root, width=10)
        self.success_probability_entry = ttk.Entry(root, width=10)
        self.calculate_gacha_button = ttk.Button(root, text="计算", command=self.calculate_gacha_probability)
        self.success_rate_label = ttk.Label(root, text="抽卡成功率:")
        self.advice_label = ttk.Label(root, text="建议:")

        self.one_lottery_button = ttk.Button(root, text="单抽", command=self.one)
        self.ten_lottery_button = ttk.Button(root, text="十连抽", command=self.ten)
        self.text = tk.Text(root, bg="gray", height=34)

        self.gacha_label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.pity_count_label.grid(column=1, row=1, padx=10, pady=5)
        self.target_pity_label.grid(column=1, row=2, padx=10, pady=5)
        self.success_probability_label.grid(column=1, row=3, padx=10, pady=5)
        self.pity_count_entry.grid(column=2, row=1, padx=10, pady=5)
        self.target_pity_entry.grid(column=2, row=2, padx=10, pady=5)
        self.success_probability_entry.grid(column=2, row=3, padx=10, pady=5)
        self.calculate_gacha_button.grid(column=1, row=4, columnspan=2, padx=10, pady=5)
        self.success_rate_label.grid(column=1, row=5, columnspan=2, padx=10, pady=5)
        self.advice_label.grid(column=1, row=6, columnspan=2, padx=10, pady=5)

        self.one_lottery_button.grid(column=3, row=0, padx=10, pady=5)
        self.ten_lottery_button.grid(column=4, row=0, padx=10, pady=5)
        self.text.grid(column=3, row=1, columnspan=2, rowspan=6)
        root.mainloop()

    # 单抽
    def one(self):
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
        self.text.tag_config('tag' + self.tag_id, foreground="yellow", font=ft)
        self.text.insert("end", "\n============== 十连抽 ==============\n", "tag" + self.tag_id)

        self.tag_id = str(int(self.tag_id) + 1)
        for i in range(10):
            self.one()

    # 抽卡规则
    def get(self):

        self.num += 1
        if random.random() > success_rate:
            level = self.R
            index = random.randrange(len(level["person"]))
            thing = level["person"][index]
        else:
            level = self.SSR
            index = random.randrange(len(level["person"]))
            thing = level["person"][index]
            input_text = self.pity_count_entry.get()  # 获取输入框的值
            self.pity_count_entry.delete(0, tk.END)  # 清空文本框
            self.pity_count_entry.insert(0, str(int(input_text) + 1))  # 设置新文本
            self.calculate_gacha_probability()
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
        global success_rate
        try:
            pity_count = int(self.pity_count_entry.get())
            target_pity = int(self.target_pity_entry.get())
            success_probability = float(self.success_probability_entry.get()) / 100
            # 计算抽卡成功率
            success_rate = 1 - math.pow(1 - success_probability, target_pity - pity_count)
            self.success_rate_label.config(text=f"抽卡成功率: {success_rate:.2%}")
            # 根据成功率给出建议
            if success_rate >= 0.5:
                self.advice_label.config(text="建议：可以继续抽卡")
            else:
                self.advice_label.config(text="建议：不值得继续抽卡")
        except ValueError:
            self.success_rate_label.config(text="输入无效，请重新输入。")


# ################# 科学计算器代码 ####################
class Calculator:
    def __init__(self):
        root = tk.Tk()  # 生成窗口
        root.title('科学计算器')  # 窗口的名字
        root.resizable(0, 0)  # 窗口大小可调性，分别表示x，y方向的可变性
        global label_text  # 定义全局变量
        label_text = StringVar()
        buju(root)
        root.mainloop()  # 进入消息循环（必需组件），否则生成的窗口一闪而过


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
        # 如果当前的算式列表最后一个元素是运算符['+', '-', '*', '/', '('， '%'， '^'], 则横杠为减号
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
    rate2 = ['*', '/', '%']
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
        result = n1 % n2
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
        num_stack.append(asin(num2))
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
    result = str(num_stack[0])
    # 去掉无效的0和小数点，例：1.0转换为1
    if result[len(result) - 1] == '0' and result[len(result) - 2] == '.':
        result = result[0:-2]
    return result


# 生成计算器主界面
def buju(root):
    label = Label(root, width=29, height=1, bd=3, bg='#87C1EF', anchor='se',
                  textvariable=label_text)  # 标签，可以显示文字或图片
    label.grid(row=0, columnspan=5)  # 布局器，向窗口注册并显示控件； rowspan：设置单元格纵向跨越的列数

    entry = Entry(root, width=23, bd=3, bg='#87C1EF', justify="right", font=('微软雅黑', 12))  # 文本框（单行）
    entry.grid(row=1, column=0, columnspan=5, sticky=N + W + S + E, padx=5, pady=5)  # 设置控件周围x、y方向空白区域保留大小

    myButton = partial(Button, root, width=5, cursor='hand2', activebackground='#90EE90')  # 偏函数：带有固定参数的函数
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
    button_yu = myButton(text='%', command=lambda: get_input(entry, '%'))
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

    button_1 = myButton(text=' 1 ', command=lambda: get_input(entry, '1'))
    button_2 = myButton(text=' 2 ', command=lambda: get_input(entry, '2'))
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
    root.geometry('600x600')

    button2 = tk.Button(root, text='科 学 计 算 器', command=Calculator, height=3, width=20)
    button2.grid(column=0, row=1, padx=220)

    button1 = tk.Button(root, text='游 戏 抽 卡 概 率 计 算 器', command=Genshin_Impact, height=3, width=20)
    button1.grid(column=0, row=0, padx=220, pady=120)

    root.mainloop()


if __name__ == '__main__':
    main_program()
