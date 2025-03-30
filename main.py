import tkinter as tk
import pandas as pd
import config
import logging
from util.barplot_1 import draw_bar_plot
from util.barplot_2 import draw_bar_plot_2
from util.pie import draw_pie

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def import_sheet_info():
    url = config.get_database_url(entry.get())
    logging.info(f"Get url: {url}")

    config.df = pd.read_csv(url)
    logging.info("Read data frame")

    # each title in title list default is None
    config.title_list = {title: "none" for title in config.df.columns.tolist()}
    logging.info(f"Initial title list: {config.title_list}")

    entry.pack_forget()
    button.pack_forget()
    logging.info("Disable sheet id field and import btn")


def update_selection(item, value):
    config.title_list[item] = value
    logging.info(f"Update {item} -> {value}")


def output_pic():
    for item in config.title_list:
        try:
            match config.title_list[item]:
                case "pie":
                    draw_pie(dataframe=config.df,
                             colors=config.colors, title=item)
                case "bar1":
                    draw_bar_plot(dataframe=config.df,
                                  colors=config.colors, title=item)
                case "bar2":
                    draw_bar_plot_2(dataframe=config.df,
                                    colors=config.colors, title=item)
                case "none":
                    pass
                case _:
                    raise ValueError(
                        f"Unsupport plot type {config.title_list[item]}")
        except Exception as ex:
            logging.warning(f"{ex}")


def display_title_list():

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    chart_options = ["pie", "bar1", "bar2", "none"]
    for item in config.title_list:
        var = tk.StringVar(root)
        var.set(config.title_list[item])
        frame_item = tk.Frame(scrollable_frame)

        dropdown = tk.OptionMenu(frame_item, var, *chart_options)
        dropdown.pack(side="left", fill="x", pady=5, padx=10) 


        var.trace_add("write", lambda name, index, mode, var=var,
                      item=item: update_selection(item, var.get()))


        title_label = tk.Label(frame_item, text=item, font=("Arial", 10))
        title_label.pack(side="left", padx=10)
        frame_item.pack(fill="x", pady=2)

    save_button.pack(pady=20)


def save_selection():
    for widget in scrollable_frame.winfo_children():
        widget.pack_forget()
    save_button.pack_forget()


def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")


def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 顯示 Canvas 和 Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return canvas, scrollable_frame


if __name__ == "__main__":

    root = tk.Tk()
    root.title("選擇圖表類型")
    root.geometry("500x600")

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas, scrollable_frame = create_scrollable_frame(frame)

    entry = tk.Entry(root, font=("Arial", 12))
    entry.insert(0, "請輸入 ID")
    entry.pack(pady=5)

    # 按鈕框架
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    button = tk.Button(button_frame, text="Import",
                       command=import_sheet_info, font=("Arial", 12))
    button2 = tk.Button(button_frame, text="Display title list",
                        command=display_title_list, font=("Arial", 12))
    button3 = tk.Button(button_frame, text="Generate plot",
                        command=output_pic, font=("Arial", 12))
    button.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

    save_button = tk.Button(
        root, text="儲存設定", command=save_selection, font=("Arial", 12))
    save_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()
