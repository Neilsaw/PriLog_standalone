import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import sys
import os
import subprocess
from PIL import Image, ImageTk
import threading
import app

ICON = "./picture/icon.ico"

images = []

capture_image = None

app_thread = None

analyze_status = True
setting_status = False

popup_message_y = 540
popup_message_active = False

POPUP_MESSAGE_START = 540
POPUP_MESSAGE_STOP = 518

# main_frame
BACKGROUND_TOP = "./picture/bg_top.png"
BUTTON_HOME = "./picture/home_button.png"
BUTTON_SETTING = "./picture/setting_button.png"
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
BUTTON_END = "./picture/end_button.png"
BUTTON_END_2 = "./picture/end_button_2.png"

# result_frame
BUTTON_RESET = "./picture/reset_button.png"
BUTTON_COPY = "./picture/copy_button.png"

# setting_menu
BASE_SETTING = "./picture/setting_base.png"

PICTURE_PATH = [
    BACKGROUND_TOP,
    BUTTON_HOME,
    BUTTON_SETTING,
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
    BUTTON_END,
    BUTTON_END_2,
    BUTTON_RESET,
    BUTTON_COPY,
    BASE_SETTING,
]

# main_frame
NUM_BACKGROUND_TOP = 0
NUM_BUTTON_HOME = 1
NUM_BUTTON_SETTING = 2
NUM_BUTTON_SELECT = 3
NUM_BUTTON_SELECT_2 = 4
NUM_BUTTON_START = 5
NUM_BUTTON_START_2 = 6

"""
# select_frame
NUM_BACKGROUND_DRAG = 6
"""

# analyze_frame
NUM_BACKGROUND_ANALYZE = 7
NUM_BACKGROUND_CAPTURE = 8
NUM_BUTTON_DO = 9
NUM_BUTTON_DO_2 = 10
NUM_BUTTON_STOP = 11
NUM_BUTTON_STOP_2 = 12
NUM_BUTTON_END = 13
NUM_BUTTON_END_2 = 14

# reset_frame
NUM_BUTTON_RESET = 15
NUM_BUTTON_COPY = 16

# setting_menu
NUM_BASE_SETTING = 17

FILE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def set_waiting_movie(self):
    text = "動画取得中..."
    self.update_popup_message_main_init(text)


def set_ub_text(self, input_text):
    self.ub_text_analyze.insert(tk.END, input_text + "\n")
    self.ub_text_analyze.see("end")


def set_ub_capture(self, frame):
    global capture_image

    work_img = Image.fromarray(frame)
    work_img = work_img.resize((384, 216))
    work_img = ImageTk.PhotoImage(work_img)
    capture_image = work_img
    self.capture_area_analyze.configure(image=work_img, width=400, height=226)


def set_movie_action(self, status, path, ftype, error):
    # 選択した動画に対する動作を設定する
    global app_thread
    global analyze_status

    app_thread_init()
    self.after(15, self.update_popup_message_main_down)
    if status is app.NO_ERROR:
        self.analyze_frame.tkraise()
        self.text_box.delete(0, tk.END)
        self.ub_text_analyze.delete('1.0', tk.END)
        self.capture_area_analyze.configure(image="")
        analyze_status = True
        app.set_analyze_status_do()
        app_thread = threading.Thread(target=app.analyze_movie, args=(path, ftype, self))
        app_thread.start()
    else:
        self.set_error_message(error)


def set_result_frame(self):
    global images
    global analyze_status

    copy_ub_text(self)

    if capture_image:
        self.capture_area_result.configure(image=capture_image, width=400, height=226)

    analyze_status = False

    self.result_frame.tkraise()

    # result遷移時に初期化せず、リセット時に使用する
    # self.ub_text_analyze.delete("1.0", tk.END)
    self.capture_area_analyze.configure(image="", width=398, height=112)

    text = "解析完了"
    self.update_popup_message_result_init(text)


def copy_ub_text(self):
    # analyze時のub_textをresultのub_textにコピーする
    analyze_txt = self.ub_text_analyze.get("1.0", tk.END)
    analyze_txt = analyze_txt.rstrip()
    analyze_txt = analyze_txt + "\n\n"

    self.ub_text_result.delete('1.0', tk.END)
    self.ub_text_result.insert("1.0", analyze_txt)
    self.ub_text_result.see("end")


def app_thread_init():
    global app_thread

    if app_thread:
        app.set_analyze_status_stop()
        app.set_movie_status_stop()
        app_thread = None


def home_init(self):
    global images
    global capture_image
    global analyze_status
    global setting_status
    global popup_message_active

    self.main_frame.tkraise()
    self.text_box.delete(0, tk.END)
    self.ub_text_analyze.delete('1.0', tk.END)
    self.ub_text_result.delete('1.0', tk.END)
    self.capture_area_analyze.configure(image="", width=398, height=112)
    self.capture_area_result.configure(image="", width=398, height=112)

    capture_image = None
    analyze_status = True
    setting_status = False

    popup_message_active = False
    self.popup_message_main.place_forget()
    self.popup_message_result.place_forget()
    self.clear_view_parts(self)

    self.error_message_main.configure(text="")
    self.clear_error_message()

    app_thread_init()


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
        self.bg.bind("<ButtonRelease-1>", self.clear_view_parts)         # フォーカス/設定画面初期化
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.main_frame, width=960, height=0, bg="#272727", font=("", 18))
        self.header.bind("<ButtonRelease-1>", self.clear_view_parts)         # フォーカス/設定画面初期化
        self.header.place(x=0, y=0)

        # ヘッダーHomeボタンを設定 (layer:2)
        self.header_bt_home_main = tk.Label(self.main_frame, image=images[NUM_BUTTON_HOME],
                                            width=95, height=26, bg="#272727")
        self.header_bt_home_main.bind("<Leave>", self.header_bt_home_nm)
        self.header_bt_home_main.bind("<Enter>", self.header_bt_home_select)
        self.header_bt_home_main.bind("<ButtonRelease-1>", self.header_bt_home_push)
        self.header_bt_home_main.place(x=0, y=0)

        # ヘッダー設定ボタンを設定 (layer:3)
        self.header_bt_setting_main = tk.Label(self.main_frame, image=images[NUM_BUTTON_SETTING],
                                            width=95, height=26, bg="#272727")
        self.header_bt_setting_main.bind("<Leave>", self.header_bt_setting_nm)
        self.header_bt_setting_main.bind("<Enter>", self.header_bt_setting_select)
        self.header_bt_setting_main.bind("<ButtonRelease-1>", self.header_bt_setting_push)
        self.header_bt_setting_main.place(x=100, y=0)

        # 入力フォームを設定 (layer:4)
        self.text_box = tk.Entry(self.main_frame, width=38, fg="#A0A0A0", bg="#FFFFFF",
                                 bd=5, font=("Yu Gothic UI", 12), relief="flat")
        self.text_box.bind("<ButtonRelease-1>", self.clear_setting)         # 設定画面初期化
        self.text_box.place(x=267, y=278)

        # エラーメッセージフォームを設定 (layer:5)
        self.error_message_main = tk.Label(self.main_frame)

        # SELECTボタン設定 (layer:6)
        self.bt_select = tk.Label(self.main_frame, image=images[NUM_BUTTON_SELECT],
                                  width=72, height=33, bg="#94DADE", bd=0)
        self.bt_select.bind("<Leave>", self.bt_select_nm)
        self.bt_select.bind("<Enter>", self.bt_select_select)
        self.bt_select.bind("<ButtonRelease-1>", self.bt_select_push)
        self.bt_select.place(x=621, y=278)

        # STARTボタン設定 (layer:7)
        self.bt_start = tk.Label(self.main_frame, image=images[NUM_BUTTON_START],
                                 width=72, height=33, bg="#94DADE", bd=0)
        self.bt_start.bind("<Leave>", self.bt_start_nm)
        self.bt_start.bind("<Enter>", self.bt_start_select)
        self.bt_start.bind("<ButtonRelease-1>", self.bt_start_push)
        self.bt_start.place(x=444, y=347)

        # ポップアップメッセージを設定 (layer:top)
        self.popup_message_main = tk.Label(self.main_frame, image="", width=18, height=1, fg="#E2E2E2",
                                             bg="#323232", bd=0, font=("メイリオ", 10), text="")
        self.popup_message_main.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.popup_message_main.place(x=0, y=540)

        # 設定画面を設定 (layer:top)
        self.setting_menu_main = tk.Label(self.main_frame, image=images[NUM_BASE_SETTING], width=267, height=510,
                                          bg="#272727", bd=0, font=("メイリオ", 10), text="")
        self.setting_menu_main.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_main.place(x=-267, y=30)

        # フォーカス解除用ダミーを設定 (layer:None)
        self.focus_dummy = tk.Label(self.main_frame)
        self.focus_dummy.place(x=1000, y=1000)
        
        # ---------------------解析画面の設定---------------------
        self.analyze_frame = tk.Frame()
        self.analyze_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_ANALYZE], bd=0)
        self.bg.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.analyze_frame, width=960, height=0, bg="#272727", font=("", 18))
        self.header.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.header.place(x=0, y=0)

        # ヘッダーHomeボタンを設定 (layer:2)
        self.header_bt_home_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_HOME],
                                               width=95, height=26, bg="#272727")
        self.header_bt_home_analyze.bind("<Leave>", self.header_bt_home_nm)
        self.header_bt_home_analyze.bind("<Enter>", self.header_bt_home_select)
        self.header_bt_home_analyze.bind("<ButtonRelease-1>", self.header_bt_home_push)
        self.header_bt_home_analyze.place(x=0, y=0)

        # ヘッダー設定ボタンを設定 (layer:3)
        self.header_bt_setting_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_SETTING],
                                            width=70, height=26, bg="#272727")
        self.header_bt_setting_analyze.bind("<Leave>", self.header_bt_setting_nm)
        self.header_bt_setting_analyze.bind("<Enter>", self.header_bt_setting_select)
        self.header_bt_setting_analyze.bind("<ButtonRelease-1>", self.header_bt_setting_push)
        self.header_bt_setting_analyze.place(x=886, y=0)

        # ボディHomeボタンを設定 (layer:4)
        self.body_bt_home_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_HOME],
                                             width=123, height=41, bg="#484848")
        self.body_bt_home_analyze.bind("<Leave>", self.body_bt_home_analyze_nm)
        self.body_bt_home_analyze.bind("<Enter>", self.body_bt_home_analyze_select)
        self.body_bt_home_analyze.bind("<ButtonRelease-1>", self.body_bt_home_analyze_push)
        self.body_bt_home_analyze.place(x=178, y=480)

        # ボディ一時停止/開始ボタンを設定 (layer:5)
        self.body_bt_do_stop = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_STOP],
                                        width=100, height=30, bg="#484848")
        self.body_bt_do_stop.bind("<Leave>", self.body_bt_do_stop_nm)
        self.body_bt_do_stop.bind("<Enter>", self.body_bt_do_stop_select)
        self.body_bt_do_stop.bind("<ButtonRelease-1>", self.body_bt_do_stop_push)
        self.body_bt_do_stop.place(x=554, y=485)

        # ボディ完了ボタンを設定 (layer:6)
        self.body_bt_end = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_END],
                                        width=100, height=30, bg="#484848")
        self.body_bt_end.bind("<Leave>", self.body_bt_end_nm)
        self.body_bt_end.bind("<Enter>", self.body_bt_end_select)
        self.body_bt_end.bind("<ButtonRelease-1>", self.body_bt_end_push)
        self.body_bt_end.place(x=783, y=485)

        # 画像エリアを設定 (layer:7)
        self.capture_area_analyze = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_CAPTURE],
                                             width=398, height=112, bg="#272727", font=("", 1), bd=0)
        self.capture_area_analyze.bind("<Leave>", self.capture_area_analyze_nm)
        self.capture_area_analyze.bind("<Enter>", self.capture_area_analyze_select)
        self.capture_area_analyze.bind("<ButtonRelease-1>", self.capture_area_analyze_push)
        self.capture_area_analyze.place(x=39, y=147)

        # UBテキストエリアを設定 (layer:8)
        self.ub_area_analyze = tk.Label(self.analyze_frame, image="",
                                        width=363, height=202, bg="#272727", font=("", 1), bd=0)
        self.ub_area_analyze.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_analyze.place(x=538, y=59)

        # UB入力欄背景1を設定 (layer:9)
        self.ub_area_analyze_bg1 = tk.Label(self.analyze_frame, image="",
                                            width=332, height=187, bg="#D4EDF4", font=("", 1), bd=0)
        self.ub_area_analyze_bg1.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_analyze_bg1.place(x=555, y=75)

        # UB入力欄背景2を設定 (layer:10)
        self.ub_area_analyze_bg2 = tk.Label(self.analyze_frame, image="",
                                            width=0, height=187, bg="#FFFFFF", font=("", 1), bd=0)
        self.ub_area_analyze_bg2.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_analyze_bg2.place(x=872, y=75)

        # UB入力欄背景3を設定 (layer:11)
        self.ub_area_analyze_bg3 = tk.Label(self.analyze_frame, image="",
                                            width=14, height=187, bg="#F0F0F0", font=("", 1), bd=0)
        self.ub_area_analyze_bg3.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_analyze_bg3.place(x=873, y=75)

        # UB入力欄を設定 (layer:12)
        self.ub_text_analyze = tk.scrolledtext.ScrolledText(self.analyze_frame, width=34, height=16, fg="#4D4D4D",
                                                            bg="#D4EDF4", bd=0, font=("メイリオ", 11), relief="flat")
        self.ub_text_analyze.bind("<ButtonRelease-1>", self.clear_setting)  # 設定画面初期化
        self.ub_text_analyze.place(x=564, y=79)

        # ---------------------結果画面の設定---------------------
        self.result_frame = tk.Frame()
        self.result_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg = tk.Label(self.result_frame, image=images[NUM_BACKGROUND_ANALYZE], bd=0)
        self.bg.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.result_frame, width=960, height=0, bg="#272727", font=("", 18))
        self.header.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.header.place(x=0, y=0)

        # ヘッダーHomeボタンを設定 (layer:2)
        self.header_bt_home_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_HOME],
                                              width=95, height=26, bg="#272727")
        self.header_bt_home_result.bind("<Leave>", self.header_bt_home_nm)
        self.header_bt_home_result.bind("<Enter>", self.header_bt_home_select)
        self.header_bt_home_result.bind("<ButtonRelease-1>", self.header_bt_home_push)
        self.header_bt_home_result.place(x=0, y=0)

        # ヘッダー設定ボタンを設定 (layer:3)
        self.header_bt_setting_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_SETTING],
                                            width=70, height=26, bg="#272727")
        self.header_bt_setting_result.bind("<Leave>", self.header_bt_setting_nm)
        self.header_bt_setting_result.bind("<Enter>", self.header_bt_setting_select)
        self.header_bt_setting_result.bind("<ButtonRelease-1>", self.header_bt_setting_push)
        self.header_bt_setting_result.place(x=886, y=0)

        # ボディHomeボタンを設定 (layer:4)
        self.body_bt_home_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_HOME],
                                     width=123, height=41, bg="#484848")
        self.body_bt_home_result.bind("<Leave>", self.body_bt_home_result_nm)
        self.body_bt_home_result.bind("<Enter>", self.body_bt_home_result_select)
        self.body_bt_home_result.bind("<ButtonRelease-1>", self.body_bt_home_result_push)
        self.body_bt_home_result.place(x=178, y=480)

        # ボディRESETボタンを設定 (layer:5)
        self.body_bt_reset_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_RESET],
                                     width=60, height=30, bg="#484848")
        self.body_bt_reset_result.bind("<Leave>", self.body_bt_reset_result_nm)
        self.body_bt_reset_result.bind("<Enter>", self.body_bt_reset_result_select)
        self.body_bt_reset_result.bind("<ButtonRelease-1>", self.body_bt_reset_result_push)
        self.body_bt_reset_result.place(x=554, y=485)

        # ボディCOPYボタンを設定 (layer:6)
        self.body_bt_copy_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_COPY],
                                        width=100, height=30, bg="#484848")
        self.body_bt_copy_result.bind("<Leave>", self.body_bt_copy_result_nm)
        self.body_bt_copy_result.bind("<Enter>", self.body_bt_copy_result_select)
        self.body_bt_copy_result.bind("<ButtonRelease-1>", self.body_bt_copy_result_push)
        self.body_bt_copy_result.place(x=783, y=485)

        # 画像エリアを設定 (layer:7)
        self.capture_area_result = tk.Label(self.result_frame, image=images[NUM_BACKGROUND_CAPTURE],
                                     width=398, height=112, bg="#272727", font=("", 1), bd=0)
        self.capture_area_result.bind("<Leave>", self.capture_area_result_nm)
        self.capture_area_result.bind("<Enter>", self.capture_area_result_select)
        self.capture_area_result.bind("<ButtonRelease-1>", self.capture_area_result_push)
        self.capture_area_result.place(x=39, y=147)

        # UBテキストエリアを設定 (layer:8)
        self.ub_area_result = tk.Label(self.result_frame, image="",
                                       width=363, height=202, bg="#272727", font=("", 1), bd=0)
        self.ub_area_result.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_result.place(x=538, y=59)

        # UB入力欄背景1を設定 (layer:9)
        self.ub_area_result_bg1 = tk.Label(self.result_frame, image="",
                                           width=332, height=187, bg="#D4EDF4", font=("", 1), bd=0)
        self.ub_area_result_bg1.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_result_bg1.place(x=555, y=75)

        # UB入力欄背景2を設定 (layer:10)
        self.ub_area_result_bg2 = tk.Label(self.result_frame, image="",
                                           width=0, height=187, bg="#FFFFFF", font=("", 1), bd=0)
        self.ub_area_result_bg2.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_result_bg2.place(x=872, y=75)

        # UB入力欄背景3を設定 (layer:11)
        self.ub_area_result_bg3 = tk.Label(self.result_frame, image="",
                                           width=14, height=187, bg="#F0F0F0", font=("", 1), bd=0)
        self.ub_area_result_bg3.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.ub_area_result_bg3.place(x=873, y=75)

        # UB入力欄を設定 (layer:12)
        self.ub_text_result = tk.scrolledtext.ScrolledText(self.result_frame, width=34, height=16, fg="#4D4D4D",
                                                           bg="#D4EDF4", bd=0, font=("メイリオ", 11), relief="flat")
        self.ub_text_result.bind("<ButtonRelease-1>", self.clear_setting)  # 設定画面初期化
        self.ub_text_result.place(x=564, y=79)

        # ポップアップメッセージを設定 (layer:top)
        self.popup_message_result = tk.Label(self.result_frame, image="", width=18, height=1, fg="#E2E2E2",
                                             bg="#323232", bd=0, font=("メイリオ", 10), text="")
        self.popup_message_result.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.popup_message_result.place(x=0, y=540)

        # 初期化
        home_init(self)

    # -----------------------------イベント設定-----------------------------

    # ---------------------ヘッダー(layer:1~2)の設定---------------------
    # ヘッダーHomeボタン用イベント (layer:2)
    def header_bt_home_nm(self, event):
        self.header_bt_home_main.configure(bg="#272727", cursor="arrow")
        self.header_bt_home_analyze.configure(bg="#272727", cursor="arrow")
        self.header_bt_home_result.configure(bg="#272727", cursor="arrow")

    def header_bt_home_select(self, event):
        self.header_bt_home_main.configure(bg="#585858", cursor="hand2")
        self.header_bt_home_analyze.configure(bg="#585858", cursor="hand2")
        self.header_bt_home_result.configure(bg="#585858", cursor="hand2")

    def header_bt_home_push(self, event):
        home_init(self)

    # ヘッダー設定ボタン用イベント (layer:3)
    def header_bt_setting_nm(self, event):
        self.header_bt_setting_main.configure(bg="#272727", cursor="arrow")
        self.header_bt_setting_analyze.configure(bg="#272727", cursor="arrow")
        self.header_bt_setting_result.configure(bg="#272727", cursor="arrow")

    def header_bt_setting_select(self, event):
        self.header_bt_setting_main.configure(bg="#585858", cursor="hand2")
        self.header_bt_setting_analyze.configure(bg="#585858", cursor="hand2")
        self.header_bt_setting_result.configure(bg="#585858", cursor="hand2")

    def header_bt_setting_push(self, event):
        global setting_status
        # フォーカスを初期化
        self.clear_focus(self)

        if setting_status:
            # 設定画面展開中は格納する
            self.clear_setting(self)
        else:
            # 設定画面格納中は展開する
            self.setting_menu_main.place_forget()
            self.setting_menu_main.place(x=0, y=30)
            setting_status = True

    # 設定画面用イベント (layer:Top)
    def clear_setting(self, event):
        global setting_status
        self.setting_menu_main.place_forget()
        self.setting_menu_main.place(x=-267, y=30)
        setting_status = False

    # ---------------------MAIN画面(layer:4~)の設定---------------------
    # SELECTボタン用イベント (layer:6)
    def bt_select_nm(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT], bg="#94DADE", cursor="arrow")

    def bt_select_select(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT_2], bg="#599EA2", cursor="hand2")

    def bt_select_push(self, event):
        global FILE_DIR

        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        file_type = [("", ".mp4")]
        initial_dir = FILE_DIR
        file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

        if file != "":
            self.text_box.delete(0, tk.END)
            self.text_box.insert(tk.END, file)

            FILE_DIR = os.path.dirname(file)
            self.bt_start_push(self)

    # STARTボタン用イベント (layer:7)
    def bt_start_nm(self, event):
        self.bt_start.configure(image=images[NUM_BUTTON_START], bg="#94DADE", cursor="arrow")

    def bt_start_select(self, event):
        self.bt_start.configure(image=images[NUM_BUTTON_START_2], bg="#599EA2", cursor="hand2")

    def bt_start_push(self, event):
        global app_thread

        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        input_text = self.text_box.get()
        file_path = input_text.strip()
        if file_path is not "":
            app_thread_init()
            app.set_movie_status_do()
            app_thread = threading.Thread(target=app.analyze_transition_check, args=(file_path, self))
            app_thread.start()

    # ポップアップメッセージ用 (layer:top)
    def update_popup_message_main_init(self, text):
        global popup_message_y
        global popup_message_active

        if popup_message_active is False:
            popup_message_active = True
            popup_message_y = POPUP_MESSAGE_START
            self.popup_message_main.configure(text=text)
            self.popup_message_main.place(x=0, y=popup_message_y)
            self.after(10, self.update_popup_message_main_up)

    def update_popup_message_main_up(self):
        global popup_message_y

        if popup_message_active is True:
            if popup_message_y > POPUP_MESSAGE_STOP:
                popup_message_y -= 1
                self.popup_message_main.place(x=0, y=popup_message_y)
                self.after(10, self.update_popup_message_main_up)
            else:
                # 上昇完了
                # set_movie_actionで下降する
                pass
        else:
            self.popup_message_main.place_forget()

    def update_popup_message_main_down(self):
        global popup_message_y
        global popup_message_active

        if popup_message_active is True:
            if popup_message_y < POPUP_MESSAGE_START:
                popup_message_y += 1
                self.popup_message_main.place(x=0, y=popup_message_y)
                self.after(15, self.update_popup_message_main_down)
            else:
                # 下降完了
                self.popup_message_main.place_forget()
                popup_message_active = False
        else:
            self.popup_message_main.place_forget()

    # エラーメッセージフォーム用 (layer:top)
    def set_error_message(self, error):
        self.error_message_main.place_forget()
        self.error_message_main = tk.Label(self.main_frame, image="", width=50, height=2, fg="#E2E2E2", bg="#323232",
                                           bd=10, font=("メイリオ", 10), text=error, justify="left", anchor="w")
        self.error_message_main.place(x=269, y=178)

    def clear_error_message(self):
        self.error_message_main.place_forget()

    # フォーカス解除用ダミー用 (layer:None)
    def clear_focus(self, event):
        self.focus_dummy.focus_set()

    # ---------------------解析画面(layer:4~)の設定---------------------
    # ボディHomeボタン用イベント (layer:4)
    def body_bt_home_analyze_nm(self, event):
        self.body_bt_home_analyze.configure(bg="#484848", cursor="arrow")

    def body_bt_home_analyze_select(self, event):
        self.body_bt_home_analyze.configure(bg="#303030", cursor="hand2")

    def body_bt_home_analyze_push(self, event):
        home_init(self)

    # ボディ一時停止/開始ボタン用イベント (layer:5)
    def body_bt_do_stop_nm(self, event):
        # 解析中ならばSTOP / 停止中ならばDOを表示
        do_stop = [NUM_BUTTON_DO, NUM_BUTTON_STOP]

        self.body_bt_do_stop.configure(image=images[do_stop[analyze_status]], bg="#484848", cursor="arrow")

    def body_bt_do_stop_select(self, event):
        # 解析中ならばSTOP / 停止中ならばDOを表示
        do_stop = [NUM_BUTTON_DO_2, NUM_BUTTON_STOP_2]

        self.body_bt_do_stop.configure(image=images[do_stop[analyze_status]], bg="#303030", cursor="hand2")

    def body_bt_do_stop_push(self, event):
        global analyze_status

        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        if analyze_status:
            # 解析中の場合一時停止
            app.set_analyze_status_pending()
        else:
            # 一時停止の場合は再開
            app.set_analyze_status_do()

        # 解析状態を反転させボタンに反映
        analyze_status = not analyze_status
        self.body_bt_do_stop_select(self)

    # ボディ完了ボタン用イベント (layer:6)
    def body_bt_end_nm(self, event):
        self.body_bt_end.configure(image=images[NUM_BUTTON_END], bg="#484848", cursor="arrow")

    def body_bt_end_select(self, event):
        self.body_bt_end.configure(image=images[NUM_BUTTON_END_2], bg="#303030", cursor="hand2")

    def body_bt_end_push(self, event):
        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        app.set_analyze_status_end()

    # 画像エリア用イベント (layer:7)
    def capture_area_analyze_nm(self, event):
        self.capture_area_analyze.configure(bg="#272727", cursor="arrow")

    def capture_area_analyze_select(self, event):
        if not analyze_status:
            # 一時停止中の場合のみ有効
            self.capture_area_analyze.configure(bg="#585858", cursor="hand2")

    def capture_area_analyze_push(self, event):
        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        if not analyze_status:
            # 一時停止中の場合のみ有効
            result_path = app.get_result_file_dir()
            subprocess.run('explorer {}'.format(result_path.replace("/", "\\")))

    # ---------------------結果画面(layer:4~)の設定---------------------
    # ボディHomeボタン用イベント (layer:4)
    def body_bt_home_result_nm(self, event):
        self.body_bt_home_result.configure(bg="#484848", cursor="arrow")

    def body_bt_home_result_select(self, event):
        self.body_bt_home_result.configure(bg="#303030", cursor="hand2")

    def body_bt_home_result_push(self, event):
        home_init(self)

    # ボディRESETボタン用イベント (layer:5)
    def body_bt_reset_result_nm(self, event):
        self.body_bt_reset_result.configure(bg="#484848", cursor="arrow")

    def body_bt_reset_result_select(self, event):
        self.body_bt_reset_result.configure(bg="#303030", cursor="hand2")

    def body_bt_reset_result_push(self, event):
        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        copy_ub_text(self)

        text = "TLを初期化しました"
        self.update_popup_message_result_init(text)

    # ボディCOPYボタン用イベント (layer:6)
    def body_bt_copy_result_nm(self, event):
        self.body_bt_copy_result.configure(bg="#484848", cursor="arrow")

    def body_bt_copy_result_select(self, event):
        self.body_bt_copy_result.configure(bg="#303030", cursor="hand2")

    def body_bt_copy_result_push(self, event):
        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        result_txt = self.ub_text_result.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(result_txt)

        text = "コピーしました"
        self.update_popup_message_result_init(text)

    # 画像エリア用イベント (layer:7)
    def capture_area_result_nm(self, event):
        self.capture_area_result.configure(bg="#272727", cursor="arrow")

    def capture_area_result_select(self, event):
        self.capture_area_result.configure(bg="#585858", cursor="hand2")

    def capture_area_result_push(self, event):
        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        result_path = app.get_result_file_dir()
        subprocess.run('explorer {}'.format(result_path.replace("/", "\\")))

    # ポップアップメッセージ用 (layer:top)
    def update_popup_message_result_init(self, text):
        global popup_message_y
        global popup_message_active

        if popup_message_active is False:
            popup_message_active = True
            popup_message_y = POPUP_MESSAGE_START
            self.popup_message_result.configure(text=text)
            self.popup_message_result.place(x=0, y=popup_message_y)
            self.after(10, self.update_popup_message_result_up)

    def update_popup_message_result_up(self):
        global popup_message_y

        if popup_message_active is True:
            if popup_message_y > POPUP_MESSAGE_STOP:
                popup_message_y -= 1
                self.popup_message_result.place(x=0, y=popup_message_y)
                self.after(10, self.update_popup_message_result_up)
            else:
                # 上昇完了
                self.after(2000, self.update_popup_message_result_down)
        else:
            self.popup_message_result.place_forget()

    def update_popup_message_result_down(self):
        global popup_message_y
        global popup_message_active

        if popup_message_active is True:
            if popup_message_y < POPUP_MESSAGE_START:
                popup_message_y += 1
                self.popup_message_result.place(x=0, y=popup_message_y)
                self.after(15, self.update_popup_message_result_down)
            else:
                # 下降完了
                self.popup_message_result.place_forget()
                popup_message_active = False
        else:
            self.popup_message_result.place_forget()

    # ---------------------統合処理の設定---------------------
    def clear_view_parts(self, event):
        self.clear_focus(self)
        self.clear_setting(self)


if __name__ == "__main__":
    f = Frame()
    f.mainloop()
    app_thread_init()
