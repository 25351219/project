import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import curve_fit
import matplotlib.font_manager as fm
import pandas as pd


def xintai():
    x = [1, 2, 3, 4]
    positive = [42.18, 56.84, 68.67, 61.10]
    negetive = [54.68, 36.49, 28.92, 28.01]
    neutral = [3.12, 6.67, 2.41, 10.90]
    positive1 = plt.plot(x, positive, lw=2, ls="-", label='positive')
    negetive1 = plt.plot(x, negetive, lw=2, ls="-", label='negetive')
    neutral1 = plt.plot(x, neutral, lw=2, ls="-", label='neutral')
    plt.xlabel('stage')
    plt.ylabel('%')
    plt.legend(loc=4)  # 指定legend的位置右下角
    plt.title('attitude')
    plt.show()


def bingzhuang(data1, label1, color1, stage):
    plt.xlim(0, 8)
    plt.ylim(0, 8)
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['left'].set_color('none')
    plt.gca().spines['bottom'].set_color('none')
    wedges, texts, autotexts = plt.pie(x=data1,colors=color1, autopct='%1.1f%%', pctdistance=0.45, labeldistance=1.15
            , startangle=110, center=(3,4), radius=3.4, wedgeprops= {'linewidth':1,'edgecolor':'white'},
            textprops= {'fontsize':6,'color':'black'}, frame=1,counterclock= False)
    plt.xticks(())
    plt.yticks(())
    plt.legend(wedges, label1, loc=4)
    plt.title(stage)
    plt.show()
if __name__ == '__main__':
    data1 = [38.28, 33.59, 23.44, 4.69]
    label1 = ['happy_love', 'sad_guilty', 'angry_hatred', 'surprise_afraid']
    color1 = ['burlywood', 'lightsteelblue', 'lightcoral', 'darkgrey' ]
    stage1 = 'stage1'
    bingzhuang(data1,label1,color1,stage1)
    data2 = [46.75, 22.72, 22.72, 4.12, 3.69]
    label2 = ['happy_love', 'sad_guilty', 'angry_hatred', 'surprise_afraid', 'other emotion']
    color2 = ['burlywood', 'lightsteelblue', 'lightcoral', 'darkgrey', 'skyblue']
    stage2 = 'stage2'
    bingzhuang(data2, label2, color2, stage2)
    data3 = [48.79, 29.52, 13.86, 4.22, 3.61]
    label3 = ['happy_love', 'sad_guilty', 'angry_hatred', 'surprise_afraid', 'other emotion']
    color3 = ['burlywood', 'lightsteelblue', 'lightcoral', 'darkgrey', 'skyblue']
    stage3 = 'stage3'
    bingzhuang(data3, label3, color3, stage3)
    data4= [52.83, 18.42, 19.18, 4.79, 4.79]
    label4= ['happy_love', 'sad_guilty', 'angry_hatred', 'surprise_afraid', 'other emotion']
    color4= ['burlywood', 'lightsteelblue', 'lightcoral', 'darkgrey', 'skyblue']
    stage4= 'stage4'
    bingzhuang(data4, label4, color4, stage4)
    xintai()