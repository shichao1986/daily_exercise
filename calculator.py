# coding: utf-8

import tkinter as Tkinter
import os
import tkinter.filedialog as tkFileDialog

import random

def generate_sum_number(bundary):
    assert isinstance(bundary, int) and bundary >= 10, '请输入大于10的整数'
    a = int(random.random() * (bundary))
    b = int(random.random() * (bundary - a))

    return a, b

def generate_minus_number(bundary, negative_allow=False):
    assert isinstance(bundary, int) and bundary >= 10, '请输入大于10的整数'
    a = int(random.random() * bundary)
    if negative_allow:
        b = int(random.random() * bundary)
    else:
        b = int(random.random() * a)

    return a, b


if __name__ == '__main__':
    for i in range(100):
        add1, add2 = generate_sum_number(10)
        print('{} + {} = {}'.format(add1, add2, add1 + add2))


