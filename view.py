import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import sys
import os
from PIL import Image, ImageTk
import threading
import app

ICON = "./picture/icon.ico"

images = []

capture_image = None

app_thread = None

analyze_status = True

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
BUTTON_DO = "./picture/do_button.png"
BUTTON_DO_2 = "./picture/do_button_2.png"
BUTTON_STOP = "./picture/stop_button.png"
BUTTON_STOP_2 = "./picture/stop_button_2.png"

PICTURE_PATH = [
    BACKGROUND_TOP,
    BUTTON_HOME,
    BUTTON_SELECT,
    BUTTON_SELECT_2,
    BUTTON_START,
    BUTTON_START_2,
    # BACKGROUND_DRAG,
    BACKGROUND_ANALYZE,
    BACKGROUND_CAPTURE,
    BUTTON_DO,
    BUTTON_DO_2,
    BUTTON_STOP,
    BUTTON_STOP_2,
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
NUM_BUTTON_DO = 8
NUM_BUTTON_DO_2 = 9
NUM_BUTTON_STOP = 10
NUM_BUTTON_STOP_2 = 11

FILE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def change_page(page):
    page.tkraise()


def set_ub_text(self, input_text):
    self.ub_text.insert(tk.END, input_text + "\n")
    self.ub_text.see("end")


def set_ub_capture(self, frame):
    global capture_image

    work_img = Image.fromarray(frame)
    work_img = work_img.resize((384, 216))
    work_img = ImageTk.PhotoImage(work_img)
    capture_image = work_img
    self.capture_area.configure(image=work_img, width=400, height=226)


def thread_init():
    global app_thread

    if app_thread:
        app.set_analyze_status_stop()
        app_thread.join()
        app_thread = None


def home_init(self):
    global images
    global capture_image
    global analyze_status

    self.main_frame.tkraise()
    self.text_box.delete(0, tk.END)
    self.capture_area.configure(image="", width=398, height=112)

    capture_image = None
    analyze_status = True

    thread_init()


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

        # ヘッダーHomeボタンを設定 (layer:2)
        self.header_bt_home_main = tk.Label(self.main_frame, image=images[NUM_BUTTON_HOME],
                                            width=95, height=26, bg="#272727")
        self.header_bt_home_main.bind("<Leave>", self.header_bt_home_nm)
        self.header_bt_home_main.bind("<Enter>", self.header_bt_home_select)
        self.header_bt_home_main.bind("<ButtonRelease-1>", self.header_bt_change_to_home)
        self.header_bt_home_main.place(x=0, y=0)

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

        # ヘッダーHomeボタンを設定 (layer:2)
        self.header_bt_home_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_HOME],
                                               width=95, height=26, bg="#272727")
        self.header_bt_home_analyze.bind("<Leave>", self.header_bt_home_nm)
        self.header_bt_home_analyze.bind("<Enter>", self.header_bt_home_select)
        self.header_bt_home_analyze.bind("<ButtonRelease-1>", self.header_bt_change_to_home)
        self.header_bt_home_analyze.place(x=0, y=0)

        # ボディHomeボタンを設定 (layer:3)
        self.body_bt_home = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_HOME],
                                     width=123, height=41, bg="#484848")
        self.body_bt_home.bind("<Leave>", self.body_bt_home_nm)
        self.body_bt_home.bind("<Enter>", self.body_bt_home_select)
        self.body_bt_home.bind("<ButtonRelease-1>", self.body_bt_change_to_home)
        self.body_bt_home.place(x=178, y=480)

        # ボディ一時停止/開始ボタンを設定 (layer:4)
        self.body_bt_do_stop = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_STOP],
                                        width=123, height=41, bg="#484848")
        self.body_bt_do_stop.bind("<Leave>", self.body_bt_do_stop_nm)
        self.body_bt_do_stop.bind("<Enter>", self.body_bt_do_stop_select)
        self.body_bt_do_stop.bind("<ButtonRelease-1>", self.body_bt_do_stop_change)
        self.body_bt_do_stop.place(x=659, y=480)

        # 画像エリアを設定 (layer:5)
        self.capture_area = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_CAPTURE],
                                     width=398, height=112, bg="#272727", font=("", 1), bd=0)
        self.capture_area.place(x=39, y=147)

        # UBテキストエリアを設定 (layer:6)
        self.ub_area = tk.Label(self.analyze_frame, image="",
                                width=363, height=202, bg="#272727", font=("", 1), bd=0)
        self.ub_area.place(x=538, y=59)

        # UB入力欄背景1を設定 (layer:7)
        self.ub_area_bg1 = tk.Label(self.analyze_frame, image="",
                                    width=332, height=187, bg="#d4edf4", font=("", 1), bd=0)
        self.ub_area_bg1.place(x=555, y=75)

        # UB入力欄背景2を設定 (layer:8)
        self.ub_area_bg2 = tk.Label(self.analyze_frame, image="",
                                    width=0, height=187, bg="#ffffff", font=("", 1), bd=0)
        self.ub_area_bg2.place(x=872, y=75)

        # UB入力欄背景3を設定 (layer:9)
        self.ub_area_bg3 = tk.Label(self.analyze_frame, image="",
                                    width=14, height=187, bg="#f0f0f0", font=("", 1), bd=0)
        self.ub_area_bg3.place(x=873, y=75)

        # UB入力欄を設定 (layer:10)
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

        # 初期化
        home_init(self)

    # -----------------------------イベント設定-----------------------------

    # ---------------------ヘッダー(layer:1~2)の設定---------------------
    # ヘッダーHomeボタン用イベント (layer:2)
    def header_bt_home_nm(self, event):
        self.header_bt_home_main.configure(bg="#272727", cursor="arrow")
        self.header_bt_home_analyze.configure(bg="#272727", cursor="arrow")

    def header_bt_home_select(self, event):
        self.header_bt_home_main.configure(bg="#585858", cursor="hand2")
        self.header_bt_home_analyze.configure(bg="#585858", cursor="hand2")

    def header_bt_change_to_home(self, event):
        home_init(self)

    # ---------------------MAIN画面(layer:3~)の設定---------------------
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
        global analyze_status

        input_text = self.text_box.get()
        file_path = input_text.strip()
        file_status, movie_path = app.analyze_transition_check(file_path)

        if file_status is app.NO_ERROR:
            self.analyze_frame.tkraise()
            self.text_box.delete(0, tk.END)
            self.ub_text.delete('1.0', tk.END)
            self.capture_area.configure(image="")
            analyze_status = True
            thread_init()
            app.set_analyze_status_do()
            app_thread = threading.Thread(target=app.analyze_movie, args=(movie_path, self))
            app_thread.start()

    # ---------------------解析画面(layer:3~)の設定---------------------
    # ボディHomeボタン用イベント (layer:3)
    def body_bt_home_nm(self, event):
        self.body_bt_home.configure(bg="#484848", cursor="arrow")

    def body_bt_home_select(self, event):
        self.body_bt_home.configure(bg="#303030", cursor="hand2")

    def body_bt_change_to_home(self, event):
        home_init(self)

    # ボディ一時停止/開始ボタン用イベント (layer:4)
    def body_bt_do_stop_nm(self, event):
        # 解析中ならばSTOP / 停止中ならばDOを表示
        do_stop = [NUM_BUTTON_DO, NUM_BUTTON_STOP]

        self.body_bt_do_stop.configure(image=images[do_stop[analyze_status]], bg="#484848", cursor="arrow")

    def body_bt_do_stop_select(self, event):
        # 解析中ならばSTOP / 停止中ならばDOを表示
        do_stop = [NUM_BUTTON_DO_2, NUM_BUTTON_STOP_2]

        self.body_bt_do_stop.configure(image=images[do_stop[analyze_status]], bg="#303030", cursor="hand2")

    def body_bt_do_stop_change(self, event):
        global analyze_status

        if analyze_status:
            # 解析中の場合一時停止
            app.set_analyze_status_pending()
        else:
            # 一時停止の場合は再開
            app.set_analyze_status_do()

        # 解析状態を反転させボタンに反映
        analyze_status = not analyze_status
        self.body_bt_do_stop_select(self)


if __name__ == "__main__":
    f = Frame()
    f.mainloop()
    thread_init()
