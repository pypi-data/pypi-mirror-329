import os
import sys
import time
import ctypes
import shutil
import random
import winreg
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import subprocess
import pkg_resources
import colorama

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass

colorama.init()

class FunnyPopup:
    def __init__(self, root):
        self.root = root
        self.q4_count = 100
        self.max_count = 100
        self.failure_count = 0

    def show_q1(self):
        response = messagebox.askquestion("Python", "你蠢吗？", icon="question")
        if response == 'yes':
            self.show_q2()
        else:
            self.show_q3()

    def show_q2(self):
        messagebox.showinfo("Python", "的确如此")
        self.show_q4()

    def show_q3(self):
        messagebox.showinfo("Python", "不，你愚蠢至极，或者请你证明自己不愚蠢")
        self.show_q4()

    def show_q4(self):
        message = f'数字为：{self.q4_count}\n按顺序执行：\n1. 该数字能被7整除按中止；\n2. 该数字能被5整除按重试；\n3. 该数字能被4整除按重试；\n4. 该数字能被11整除请按中止；\n5. 该数字不满足以上任意一条规则请按忽略。\n第{self.failure_count}次失败'
        default_button = random.choice(['abort', 'retry', 'ignore'])
        response = messagebox.askquestion("Python", message, default=default_button, icon='question', type=messagebox.ABORTRETRYIGNORE)
        if response == 'abort' or response == 'retry' or response == 'ignore':
            if self.q4_count % 7 == 0:
                if response == 'abort':
                    self.q4_count -= 3
                else:
                    self.q4_count += 10
                    self.failure_count += 1
            elif self.q4_count % 5 == 0:
                if response == 'retry':
                    self.q4_count -= 2
                else:
                    self.q4_count += 10
                    self.failure_count += 1
            elif self.q4_count % 4 == 0:
                if response == 'retry':
                    self.q4_count -= 3
                else:
                    self.q4_count += 10
                    self.failure_count += 1
            elif self.q4_count % 11 == 0:
                if response == 'abort':
                    self.q4_count -= random.randint(0, 7)
                else:
                    self.q4_count += 10
                    self.failure_count += 1
            else:
                if response == 'ignore':
                    self.q4_count -= random.randint(0, 3)
                else:
                    self.q4_count += 10
                    self.failure_count += 1
        if self.q4_count <= 0 or self.failure_count >= 25:
            self.show_q5()
        else:
            self.show_q4()
        
    def show_q5(self):
        while True:
            messagebox.showinfo("Python", "你被耍了", icon='warning')

def main():
    root = tk.Tk()
    root.withdraw()
    funny_popup = FunnyPopup(root)
    funny_popup.show_q1()
    root.mainloop()

def hello(name='夏星河'):
    text = f'你好，{name}！'
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.5)
    print()
    text = '......你 可 真 是 够 蠢 的'
    for char in text:
        print(f'\033[31m{char}', end='', flush=True)
        time.sleep(0.5)
    print('\033[0m')
    for i in range(100):
        print("夏星河太蠢了！" + (i % 10) * "！")
        time.sleep(0.1)
    main()
