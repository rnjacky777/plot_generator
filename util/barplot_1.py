import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

def draw_bar_plot(dataframe: pd.DataFrame, colors: list, title: str):
    folder_path = './barplot_1/'
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(6, 6))
    total_count = dataframe[title].value_counts()
    colors = sns.color_palette(colors, len(dataframe))
    ax = sns.barplot(y=total_count.index, x=total_count.values,
                     palette=colors, orient='h')


    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


    plt.title(title, fontweight='bold', pad=20)
    plt.xlabel("")
    plt.ylabel("")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    title = title.replace('?', '_')  
    plt.savefig(f'{folder_path}{title}.png')
    logging.info(f"Generate fig , title:{title}, type: bar1")


