import tkinter as tk
import pandas as pd
import json
import os
from util.barplot_1 import draw_bar_plot
from util.barplot_2 import draw_bar_plot_2
from util.pie import draw_pie

df = None
title_list = None
selected_items = {}
colors = ["#B64C2E", "#BC6B49", "#CB8F6F", "#DCAE92","#E8C9B6"]
def import_sheet_info():
    global df, title_list
    sheet_id = entry.get()
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    title_list = df.columns.tolist()
    print(f"標題列表已載入: {title_list}")  # 輸出載入的標題列表

    # 初始化 selected_items 字典，每個標題的預設值為 "pie"
    global selected_items
    selected_items = {title: "none" for title in title_list}  # 將標題列表轉為字典，預設值為 "pie"

    # 隱藏輸入框和import按鈕
    entry.pack_forget()  # 隱藏輸入框
    button.pack_forget()  # 隱藏import按鈕

def update_selection(item, value):
    selected_items[item] = value  # 當選擇的選項更改時，更新字典中的值
    print(f"更新選項: {item} -> {value}")  # 打印更新的選項，可以在這裡進行其他操作
def output_pic():
    global df, title_list,selected_items
    if selected_items: 
        for item in selected_items:
            match selected_items[item]:
                case "pie":
                    try:
                        draw_pie(dataframe=df,colors=colors,title=item)
                    except Exception as ex:
                        print(ex)
                case "bar1":
                    try:
                        draw_bar_plot(dataframe=df,colors=colors,title=item)
                    except Exception as ex:
                        print(ex)
                case "bar2":
                    try:
                        draw_bar_plot_2(dataframe=df,colors=colors,title=item)
                    except Exception as ex:
                        print(ex)
                case _:
                    pass
    else:
        print("Please import google sheet")

def display_title_list():
    global selected_items
    if not title_list:  # 如果標題列表為空
        print("標題列表為空，請先匯入資料")  # 用來檢查為什麼沒反應
        return

    # 清除舊的內容
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # 根據 title_list 為每一個項目創建一個下拉選單
    chart_options = ["pie", "bar1", "bar2","none"]
    for item in title_list:
        var = tk.StringVar(root)
        # 如果已經有儲存的選擇設定，使用它，否則預設為 "pie"
        var.set(selected_items.get(item, chart_options[0]))  

        frame_item = tk.Frame(scrollable_frame)  # 為每個項目創建一個frame來包含選單和標題

        # 創建OptionMenu
        dropdown = tk.OptionMenu(frame_item, var, *chart_options)
        dropdown.pack(side="left", fill="x", pady=5, padx=10)  # 設定適當的間隔和排版方式

        # 監聽選擇變更，並更新字典中的選擇
        var.trace_add("write", lambda name, index, mode, var=var, item=item: update_selection(item, var.get()))

        # 創建Label來顯示標題
        title_label = tk.Label(frame_item, text=item, font=("Arial", 10))
        title_label.pack(side="left", padx=10)

        # 將frame_item加入scrollable_frame
        frame_item.pack(fill="x", pady=2)

    print("標題選單已顯示")  # 用來檢查是否成功顯示選單

    # 顯示儲存按鈕
    save_button.pack(pady=20)

def save_selection():
    # 儲存選擇結果到字典中，從 `StringVar` 中提取值
    result_dict = {item: selected_items[item] for item in selected_items}
    result_label.config(text=f"選擇結果: {result_dict}")
    print(result_dict)  # 輸出結果，可以將其寫入檔案等

    # 儲存結果，這裡可以將結果寫入文件或其他處理
    with open("selected_items.json", "w") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)

    # 儲存後隱藏標題選單並顯示結果
    hide_title_list()

def hide_title_list():
    # 隱藏標題選單
    for widget in scrollable_frame.winfo_children():
        widget.pack_forget()

    # 顯示已儲存的結果
    result_label.pack(pady=20)  # 顯示結果標籤
    save_button.pack_forget()  # 隱藏儲存按鈕
    result_label.config(text="選擇結果已儲存")

# 建立主視窗
root = tk.Tk()
root.title("選擇圖表類型")
root.geometry("500x600")

# 創建外層 Frame（包含滾動區域）
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# 創建 Canvas & Scrollbar
canvas = tk.Canvas(frame)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# 讓 Frame 可滾動
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# 在 Canvas 上創建可滾動的視窗
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# 綁定滑鼠滾動
def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows 滑鼠滾動
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux 滑鼠滾動上
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux 滑鼠滾動下

# 顯示 Canvas 和 Scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 加入輸入框
entry = tk.Entry(root, font=("Arial", 12))
entry.insert(0, "請輸入 ID")
entry.pack(pady=5)

# 按鈕
button = tk.Button(root, text="Import", command=import_sheet_info, font=("Arial", 12))
button2 = tk.Button(root, text="顯示標題選單", command=display_title_list, font=("Arial", 12))
button3 = tk.Button(root, text="Button", command=output_pic, font=("Arial", 12))

button.pack(pady=10)
button2.pack(pady=10)
button3.pack(pady=10)

# 顯示結果的標籤
result_label = tk.Label(root, text="尚未儲存結果", font=("Arial", 12))
result_label.pack(pady=10)

# 儲存結果按鈕（會顯示並重新顯示）
save_button = tk.Button(root, text="儲存設定", command=save_selection, font=("Arial", 12))

# 執行視窗
root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()
