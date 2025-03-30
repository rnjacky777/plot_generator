import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyArrowPatch


def draw_pie(dataframe: pd.DataFrame, colors: list, title: str):
    folder_path = './pie/'
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 6))
    total_count = dataframe[title].value_counts()
    colors = sns.color_palette(colors, len(dataframe))
    wedges, texts, autotexts = plt.pie(
        total_count, labels=total_count.index, autopct="%1.1f%%",
        colors=colors, pctdistance=0.85, textprops={'color': 'white'}
    )

    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    plt.gca().add_artist(centre_circle)

    for i, (wedge, pct) in enumerate(zip(wedges, total_count)):

        percentage = pct / sum(total_count) * 100
        if percentage < 10:
            autotexts[i].set_text("")
            texts[i].set_text("")

            angle = (wedge.theta2 + wedge.theta1) / 2
            x = (1.1 * wedge.r * np.cos(np.deg2rad(angle)))
            y = (1.1 * wedge.r * np.sin(np.deg2rad(angle)))

            arrow = FancyArrowPatch(
                (x, y), (1.3 * x, 1.3 * y), connectionstyle="arc3,rad=0.2",
                arrowstyle='->', lw=1.5, color=colors[i], mutation_scale=20
            )
            plt.gca().add_patch(arrow)

            plt.text(1.3 * x, 1.3 * y - 0.05,
                     f"{total_count.index[i]}: {pct:.1f}%", fontsize=12, color='black', fontweight='bold')

    for i, autotext in enumerate(autotexts):

        angle = (wedges[i].theta2 + wedges[i].theta1) / 2

        radius = (wedges[i].r * 0.80)
        x = radius * np.cos(np.deg2rad(angle))
        y = radius * np.sin(np.deg2rad(angle))

        autotext.set_position((x, y))
        autotext.set_color('white')

    plt.title(title, fontweight='bold', pad=15, x=0.45)
    plt.axis("equal")
    plt.legend(title=None, loc='upper left', bbox_to_anchor=(0.8, 1))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    title = title.replace('?', '_')

    plt.savefig(f'{folder_path}{title}.png')
    logging.info(f"Generate fig , title:{title}, type: pie")
