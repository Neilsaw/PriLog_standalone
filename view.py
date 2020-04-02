import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import sys
import os
from PIL import Image, ImageTk
import numpy as np
import threading
import app

ICON = "./picture/icon.ico"

images = []

capture_images = None

app_thread = None

# main_frame
BACKGROUND_TOP = "./picture/bg_top.png"
BUTTON_HOME = "./picture/home_button.png"
BUTTON_SELECT = "./picture/select_button.png"
BUTTON_SELECT_2 = "./picture/select_button_2.png"
BUTTON_START = "./picture/start_button.png"
BUTTON_START_2 = "./picture/start_button_2.png"

"""
# select_frame
BACKGROUND_DRAG = "./picture/bg_top_drag.png"
"""

# analyze_frame
BACKGROUND_ANALYZE = "./picture/bg_analyze.png"
BACKGROUND_CAPTURE = "./picture/bg_capture.png"

PICTURE_PATH = [
    BACKGROUND_TOP,
    BUTTON_HOME,
    BUTTON_SELECT,
    BUTTON_SELECT_2,
    BUTTON_START,
    BUTTON_START_2,
    #BACKGROUND_DRAG,
    BACKGROUND_ANALYZE,
    BACKGROUND_CAPTURE,
]

# main_frame
NUM_BACKGROUND_TOP = 0
NUM_BUTTON_HOME = 1
NUM_BUTTON_SELECT = 2
NUM_BUTTON_SELECT_2 = 3
NUM_BUTTON_START = 4
NUM_BUTTON_START_2 = 5

"""
# select_frame
NUM_BACKGROUND_DRAG = 6
"""

# analyze_frame
NUM_BACKGROUND_ANALYZE = 6
NUM_BACKGROUND_CAPTURE = 7

FILE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def change_page(page):
    page.tkraise()


def set_ub_text(self, input_text):
    self.ub_text.insert(tk.END, input_text + "\n")


def set_ub_capture(self, frame):
    global capture_images

    work_img = Image.fromarray(frame)
    work_img = work_img.resize((384, 216))
    work_img = ImageTk.PhotoImage(work_img)
    capture_images = work_img
    self.capture_area.configure(image=work_img, width=400, height=226)


def thread_init():
    global app_thread

    if app_thread:
        app.set_analyze_status()
        app_thread.join()
        app_thread = None


class Frame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('PriLog')
        self.geometry("960x540")
        self.resizable(width=False, height=False)
        self.iconbitmap(default=ICON)

        # ---------------------画像の設定---------------------
        for i in range(len(PICTURE_PATH)):
            work_img = Image.open(PICTURE_PATH[i])
            work_img = ImageTk.PhotoImage(work_img)
            images.append(work_img)

        # -----------------------------画面設定-----------------------------
        # ---------------------MAIN画面の設定---------------------
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg = tk.Label(self.main_frame, image=images[NUM_BACKGROUND_TOP], bd=0)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.main_frame, width=960, height=0, bg="#272727", font=("", 18))
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        self.header_bt_home_1 = tk.Label(self.main_frame, image=images[NUM_BUTTON_HOME],
                                         width=95, height=26, bg="#272727")
        self.header_bt_home_1.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home_1.bind("<Enter>", self.bt_home_select)
        self.header_bt_home_1.bind("<ButtonRelease-1>", self.bt_change_to_home)
        self.header_bt_home_1.place(x=0, y=0)

        # 入力フォームを設定 (layer:3)
        self.text_box = tk.Entry(self.main_frame, width=38, fg="#a0a0a0", bg="#FFFFFF",
                                 bd=5, font=("Yu Gothic UI", 12), relief="flat")
        self.text_box.place(x=267, y=278)

        # SELECTボタン設定 (layer:4)
        self.bt_select = tk.Label(self.main_frame, image=images[NUM_BUTTON_SELECT],
                                  width=72, height=33, bg="#94DADE", bd=0)
        self.bt_select.bind("<Leave>", self.bt_select_nm)
        self.bt_select.bind("<Enter>", self.bt_select_nm_select)
        self.bt_select.bind("<ButtonRelease-1>", self.bt_select_push)
        self.bt_select.place(x=621, y=278)

        # STARTボタン設定 (layer:5)
        self.bt_start = tk.Label(self.main_frame, image=images[NUM_BUTTON_START],
                                 width=72, height=33, bg="#94DADE", bd=0)
        self.bt_start.bind("<Leave>", self.bt_start_nm)
        self.bt_start.bind("<Enter>", self.bt_start_nm_select)
        self.bt_start.bind("<ButtonRelease-1>", self.bt_start_push)
        self.bt_start.place(x=444, y=347)

        """
        # ---------------------選択画面の設定---------------------
        self.select = tk.Frame()
        self.select.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg = tk.Label(self.select, image=imgs[NUM_BACKGROUND_DRAG], bd=0)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.select, width=960, height=0, bg="#272727", font=("", 18))
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        self.header_bt_home_2 = tk.Label(self.select, image=imgs[NUM_BUTTON_HOME], width=95, height=26, bg="#272727")
        self.header_bt_home_2.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home_2.bind("<Enter>", self.bt_home_select)
        self.header_bt_home_2.bind("<ButtonRelease-1>", self.bt_change_to_home)
        self.header_bt_home_2.place(x=0, y=0)
        """
        
        # ---------------------解析画面の設定---------------------
        self.analyze_frame = tk.Frame()
        self.analyze_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_ANALYZE], bd=0)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.analyze_frame, width=960, height=0, bg="#272727", font=("", 18))
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        self.header_bt_home_2 = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_HOME],
                                         width=95, height=26, bg="#272727")
        self.header_bt_home_2.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home_2.bind("<Enter>", self.bt_home_select)
        self.header_bt_home_2.bind("<ButtonRelease-1>", self.bt_change_to_home)
        self.header_bt_home_2.place(x=0, y=0)

        # 画像エリアを設定 (layer:3)
        self.capture_area = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_CAPTURE],
                                     width=398, height=112, bg="#272727", font=("", 1), bd=0)
        self.capture_area.place(x=39, y=147)

        # UBエリアを設定 (layer:4)
        self.ub_area = tk.Label(self.analyze_frame, image="",
                                width=363, height=202, bg="#272727", font=("", 1), bd=0)
        self.ub_area.place(x=538, y=59)

        # UB入力欄背景1を設定 (layer:5)
        self.ub_area = tk.Label(self.analyze_frame, image="",
                                width=332, height=187, bg="#d4edf4", font=("", 1), bd=0)
        self.ub_area.place(x=555, y=75)

        # UB入力欄背景2を設定 (layer:6)
        self.ub_area = tk.Label(self.analyze_frame, image="",
                                width=0, height=187, bg="#ffffff", font=("", 1), bd=0)
        self.ub_area.place(x=872, y=75)

        # UB入力欄背景3を設定 (layer:7)
        self.ub_area = tk.Label(self.analyze_frame, image="",
                                width=14, height=187, bg="#f0f0f0", font=("", 1), bd=0)
        self.ub_area.place(x=873, y=75)

        # UB入力欄を設定 (layer:8)
        self.ub_text = tk.scrolledtext.ScrolledText(self.analyze_frame, width=34, height=16,
                                                    fg="#4d4d4d", bg="#d4edf4", bd=0, font=("メイリオ", 11), relief="flat")
        self.ub_text.place(x=564, y=79)
        """
        # 入力フォームを設定 (layer:3)
        self.text_box = tk.Entry(self.analyze_frame, width=38, fg="#a0a0a0", bg="#FFFFFF",
                                 bd=5, font=("Yu Gothic UI", 12), relief="flat")
        self.text_box.place(x=267, y=278)

        # SELECTボタン設定 (layer:4)
        self.bt_select = tk.Label(self.analyze_frame, image=imgs[NUM_BUTTON_SELECT],
                                  width=72, height=33, bg="#94DADE", bd=0)
        self.bt_select.bind("<Leave>", self.bt_select_nm)
        self.bt_select.bind("<Enter>", self.bt_select_nm_select)
        self.bt_select.bind("<ButtonRelease-1>", self.bt_select_push)
        self.bt_select.place(x=621, y=278)

        # STARTボタン設定 (layer:5)
        self.bt_start = tk.Label(self.analyze_frame, image=imgs[NUM_BUTTON_START],
                                 width=72, height=33, bg="#94DADE", bd=0)
        self.bt_start.bind("<Leave>", self.bt_start_nm)
        self.bt_start.bind("<Enter>", self.bt_start_nm_select)
        self.bt_start.bind("<ButtonRelease-1>", self.bt_start_push)
        self.bt_start.place(x=444, y=347)
        """

        self.main_frame.tkraise()
        #self.analyze_frame.tkraise()

    # -----------------------------イベント設定-----------------------------

    # ---------------------ヘッダーの設定---------------------
    # Homeボタン用イベント (layer:2)
    def bt_home_nm(self, event):
        self.header_bt_home_1.configure(bg="#272727", cursor="arrow")
        self.header_bt_home_2.configure(bg="#272727", cursor="arrow")

    def bt_home_select(self, event):
        self.header_bt_home_1.configure(bg="#585858", cursor="hand2")
        self.header_bt_home_2.configure(bg="#585858", cursor="hand2")

    def bt_change_to_home(self, event):
        self.main_frame.tkraise()
        self.text_box.delete(0, tk.END)
        self.capture_area.configure(image="", width=398, height=112)
        thread_init()

    # ---------------------MAIN画面の設定---------------------
    # SELECTボタン用イベント (layer:4)
    def bt_select_nm(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT], bg="#94DADE", cursor="arrow")

    def bt_select_nm_select(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT_2], bg="#599ea2", cursor="hand2")

    def bt_select_push(self, event):
        global FILE_DIR

        file_type = [("", ".mp4")]
        initial_dir = FILE_DIR
        file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

        if file != "":
            self.text_box.delete(0, tk.END)
            self.text_box.insert(tk.END, file)

            FILE_DIR = os.path.dirname(file)
            self.bt_start_push(self)

    # STARTボタン用イベント (layer:5)
    def bt_start_nm(self, event):
        self.bt_start.configure(image=images[NUM_BUTTON_START], bg="#94DADE", cursor="arrow")

    def bt_start_nm_select(self, event):
        self.bt_start.configure(image=images[NUM_BUTTON_START_2], bg="#599ea2", cursor="hand2")

    def bt_start_push(self, event):
        global app_thread

        input_text = self.text_box.get()
        file_path = input_text.strip()
        file_status, movie_path = app.analyze_transition_check(file_path)

        if file_status is app.NO_ERROR:
            self.analyze_frame.tkraise()
            self.text_box.delete(0, tk.END)
            self.ub_text.delete('1.0', tk.END)
            self.capture_area.configure(image="")
            thread_init()
            app_thread = threading.Thread(target=app.analyze_movie, args=(movie_path, self))
            app_thread.start()


if __name__ == "__main__":
    f = Frame()
    f.mainloop()
    thread_init()
