import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyArrowPatch


def draw_pie(dataframe:pd.DataFrame,colors:list,title:str):
    folder_path = './pie/'
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False 
    plt.figure(figsize=(10, 6))
    total_count = dataframe[title].value_counts()
    colors = sns.color_palette(colors, len(dataframe))
    wedges, texts, autotexts = plt.pie(
       total_count, labels=total_count.index, autopct="%1.1f%%",  # 自動顯示百分比
        colors=colors, pctdistance=0.85, textprops={'color': 'white'}
    )

    # 添加中心圓
    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    plt.gca().add_artist(centre_circle)
    # 取得圓餅圖的坐標，並手動添加注釋線條
    for i, (wedge, pct) in enumerate(zip(wedges, total_count)):
        # 只處理小於10%數值
        percentage = pct / sum(total_count) * 100
        if percentage < 10:
            autotexts[i].set_text("")  # 移除內部標註
            texts[i].set_text("")
            # 計算每個扇形的角度，將百分比標籤移到外圓
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = (1.1 * wedge.r * np.cos(np.deg2rad(angle)))
            y = (1.1 * wedge.r * np.sin(np.deg2rad(angle)))

            # 使用 FancyArrowPatch 繪製彎曲的線條
            arrow = FancyArrowPatch(
                (x, y), (1.3 * x, 1.3 * y), connectionstyle="arc3,rad=0.2",
                arrowstyle='->', lw=1.5, color=colors[i], mutation_scale=20
            )
            plt.gca().add_patch(arrow)
            
            # 顯示標註文字
            plt.text(1.3 * x, 1.3 * y - 0.05, f"{total_count.index[i]}: {pct:.1f}%", fontsize=12, color='black', fontweight='bold')
    
    
    # 重新顯示內部的百分比，並調整顯示位置以在扇形厚度中間
    for i, autotext in enumerate(autotexts):
        # 計算扇形的角度
        angle = (wedges[i].theta2 + wedges[i].theta1) / 2
        # 計算文字的 x 和 y 位置，確保其位於圓餅圖的厚度中心
        radius = (wedges[i].r *0.80)  # 從圓心向外偏移，確保在圓餅圖的厚度中間
        x = radius * np.cos(np.deg2rad(angle))
        y = radius * np.sin(np.deg2rad(angle))

        # 微調位置，將標籤放在扇形的厚度中間，避免超出圓餅圖
        autotext.set_position((x, y))  # 將百分比放在扇形的中心
        autotext.set_color('white')  # 設置百分比顏色為白色


    plt.title(title, fontweight='bold',pad=15, x=0.45)
    plt.axis("equal")
    # 顯示圖例，並將顏色與類別匹配
    plt.legend(title=None, loc='upper left', bbox_to_anchor=(0.8, 1))


    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 處理文件名中的非法字符
    title = title.replace('?', '_')  # 你可以根據需要處理其他字符

    # 儲存圖片
    plt.savefig(f'{folder_path}{title}.png')
    print