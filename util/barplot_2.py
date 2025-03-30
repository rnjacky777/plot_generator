import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 繪製縱向長條圖，調整柱子的寬度
def draw_bar_plot_2(dataframe:pd.DataFrame,colors:list,title:str):
    folder_path = './barplot_2/'
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False 
    plt.figure(figsize=(6, 6))
    total_count = dataframe[title].value_counts()
    colors = sns.color_palette(colors, len(dataframe))
    ax = sns.barplot(x=total_count.index, y=total_count.values, palette=colors)  # width 減少柱子寬度

    # 移除上、右邊框線
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 設定標題
    plt.title(title, fontweight='bold', pad=20)

    # 移除 x 軸標題
    plt.xlabel("")
    plt.ylabel("")

    # 顯示圖表
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 處理文件名中的非法字符
    title = title.replace('?', '_')  # 你可以根據需要處理其他字符

    # 儲存圖片
    plt.savefig(f'{folder_path}{title}.png')
