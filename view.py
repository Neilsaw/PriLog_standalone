# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import os
import subprocess
from PIL import Image, ImageTk
import threading
import app
import myconfig
import bg_maker

VERSION = "v0.6.0"

ICON = "./resource/image/icon.ico"

images = []

capture_image = None

app_thread = None

analyze_status = True
setting_status = False

popup_message_y = 540
popup_message_active = False

POPUP_MESSAGE_START = 540
POPUP_MESSAGE_STOP = 518

IMAGE_PATH = "./"
SETTING_IMAGE = []

# main_frame
BACKGROUND_BASE = "./resource/image/bg.png"
BACKGROUND_TOP = "./resource/image/bg/over_bg_top.png"
BUTTON_HOME = "./resource/image/button/home_button.png"
BUTTON_SETTING = "./resource/image/button/setting_button.png"
BUTTON_SELECT = "./resource/image/button/select_button.png"
BUTTON_SELECT_2 = "./resource/image/button/select_button_2.png"
BUTTON_START = "./resource/image/button/start_button.png"
BUTTON_START_2 = "./resource/image/button/start_button_2.png"

# analyze_frame
BACKGROUND_ANALYZE = "./resource/image/bg/over_bg_analyze.png"
BACKGROUND_CAPTURE = "./resource/image/bg/bg_capture.png"
BUTTON_DO = "./resource/image/button/do_button.png"
BUTTON_DO_2 = "./resource/image/button/do_button_2.png"
BUTTON_STOP = "./resource/image/button/stop_button.png"
BUTTON_STOP_2 = "./resource/image/button/stop_button_2.png"
BUTTON_END = "./resource/image/button/end_button.png"
BUTTON_END_2 = "./resource/image/button/end_button_2.png"

# result_frame
BUTTON_RESET = "./resource/image/button/reset_button.png"
BUTTON_COPY = "./resource/image/button/copy_button.png"

# setting_menu
BASE_SETTING = "./resource/image/setting/setting_base.png"
BUTTON_IMAGE_SELECT = "./resource/image/setting/image_select_button.png"
BUTTON_IMAGE_SELECT_2 = "./resource/image/setting/image_select_button_2.png"
BUTTON_PNG_ON = "./resource/image/setting/png_button_on.png"
BUTTON_PNG_OFF = "./resource/image/setting/png_button_off.png"
BUTTON_JPG_ON = "./resource/image/setting/jpg_button_on.png"
BUTTON_JPG_OFF = "./resource/image/setting/jpg_button_off.png"
BUTTON_LIMIT_TRUE_ON = "./resource/image/setting/limit_true_button_on.png"
BUTTON_LIMIT_TRUE_OFF = "./resource/image/setting/limit_true_button_off.png"
BUTTON_LIMIT_FALSE_ON = "./resource/image/setting/limit_false_button_on.png"
BUTTON_LIMIT_FALSE_OFF = "./resource/image/setting/limit_false_button_off.png"
BUTTON_EXIT = "./resource/image/setting/exit_button.png"
BUTTON_EXIT_2 = "./resource/image/setting/exit_button_2.png"

PICTURE_PATH = [
    BACKGROUND_BASE,
    BACKGROUND_TOP,
    BUTTON_HOME,
    BUTTON_SETTING,
    BUTTON_SELECT,
    BUTTON_SELECT_2,
    BUTTON_START,
    BUTTON_START_2,
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
    BUTTON_IMAGE_SELECT,
    BUTTON_IMAGE_SELECT_2,
    BUTTON_PNG_ON,
    BUTTON_PNG_OFF,
    BUTTON_JPG_ON,
    BUTTON_JPG_OFF,
    BUTTON_LIMIT_TRUE_ON,
    BUTTON_LIMIT_TRUE_OFF,
    BUTTON_LIMIT_FALSE_ON,
    BUTTON_LIMIT_FALSE_OFF,
    BUTTON_EXIT,
    BUTTON_EXIT_2,
]

# main_frame
NUM_BACKGROUND_BASE = 0
NUM_BACKGROUND_TOP = 1
NUM_BUTTON_HOME = 2
NUM_BUTTON_SETTING = 3
NUM_BUTTON_SELECT = 4
NUM_BUTTON_SELECT_2 = 5
NUM_BUTTON_START = 6
NUM_BUTTON_START_2 = 7

# analyze_frame
NUM_BACKGROUND_ANALYZE = 8
NUM_BACKGROUND_CAPTURE = 9
NUM_BUTTON_DO = 10
NUM_BUTTON_DO_2 = 11
NUM_BUTTON_STOP = 12
NUM_BUTTON_STOP_2 = 13
NUM_BUTTON_END = 14
NUM_BUTTON_END_2 = 15

# reset_frame
NUM_BUTTON_RESET = 16
NUM_BUTTON_COPY = 17

# setting_menu
NUM_BASE_SETTING = 18
NUM_BUTTON_IMAGE_SELECT = 19
NUM_BUTTON_IMAGE_SELECT_2 = 20
NUM_BUTTON_PNG_ON = 21
NUM_BUTTON_PNG_OFF = 22
NUM_BUTTON_JPG_ON = 23
NUM_BUTTON_JPG_OFF = 24
NUM_BUTTON_LIMIT_TRUE_ON = 25
NUM_BUTTON_LIMIT_TRUE_OFF = 26
NUM_BUTTON_LIMIT_FALSE_ON = 27
NUM_BUTTON_LIMIT_FALSE_OFF = 28
NUM_BUTTON_EXIT = 29
NUM_BUTTON_EXIT_2 = 30

MOVIE_PATH = myconfig.MOVIE_PATH_DEFAULT
IMAGE_FORMAT = myconfig.IMAGE_FORMAT_DEFAULT
LENGTH_LIMIT = myconfig.LENGTH_LIMIT_DEFAULT
ENEMY_UB = myconfig.ENEMY_UB_DEFAULT
WINDOW_X_POSITION = myconfig.WINDOW_POSITION_X_DEFAULT
WINDOW_Y_POSITION = myconfig.WINDOW_POSITION_Y_DEFAULT


def load_config():
    # コンフィグファイルから設定を取得する
    global MOVIE_PATH
    global IMAGE_FORMAT
    global LENGTH_LIMIT
    global ENEMY_UB
    global WINDOW_X_POSITION
    global WINDOW_Y_POSITION

    MOVIE_PATH, IMAGE_FORMAT, LENGTH_LIMIT, ENEMY_UB, WINDOW_X_POSITION, WINDOW_Y_POSITION = myconfig.read_config()


def save_config():
    # コンフィグファイルに設定を保存する
    global WINDOW_X_POSITION
    global WINDOW_Y_POSITION

    WINDOW_X_POSITION = str(f.winfo_rootx())
    WINDOW_Y_POSITION = str(f.winfo_rooty())
    myconfig.create_config(False, MOVIE_PATH, IMAGE_FORMAT, LENGTH_LIMIT, ENEMY_UB, WINDOW_X_POSITION, WINDOW_Y_POSITION)


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
        app_thread.setDaemon(True)
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
        self.geometry("+" + WINDOW_X_POSITION + "+" + WINDOW_Y_POSITION)

        self.resizable(width=False, height=False)
        self.iconbitmap(default=ICON)

        # ---------------------画像の設定---------------------
        for i in range(len(PICTURE_PATH)):
            try:
                work_img = Image.open(PICTURE_PATH[i])
                if i == NUM_BACKGROUND_TOP or i == NUM_BACKGROUND_ANALYZE:
                    work_img = bg_maker.bg_editor(Image.open(PICTURE_PATH[NUM_BACKGROUND_BASE]), work_img)
            except FileNotFoundError:
                work_img = Image.new("RGB", (960, 540), (128, 128, 128))
                work_img.save(PICTURE_PATH[i])

            work_img = ImageTk.PhotoImage(work_img)
            images.append(work_img)

        # -----------------------------画面設定-----------------------------
        # ---------------------MAIN画面の設定---------------------
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg_main = tk.Label(self.main_frame, image=images[NUM_BACKGROUND_TOP], bd=0)
        self.bg_main.bind("<ButtonRelease-1>", self.clear_view_parts)         # フォーカス/設定画面初期化
        self.bg_main.pack(fill="x")

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
        self.text_box.bind("<Return>", self.bt_start_push)  # 設定画面初期化
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
                                          bd=0, text="")
        self.setting_menu_main.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_main.place(x=-267, y=30)

        # 設定画面サンプル画像を設定 (layer:top+1)
        menu_image = (Image.open(BACKGROUND_BASE)).resize((160, 90)).copy()
        SETTING_IMAGE.clear()
        SETTING_IMAGE.append(ImageTk.PhotoImage(menu_image))

        self.setting_menu_image_main = tk.Label(self.main_frame, image=SETTING_IMAGE[0], width=160, height=90, bd=0, text="")
        self.setting_menu_image_main.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_image_main.place(x=-245, y=95)

        # 設定画面画像選択ボタンを設定 (layer:top+2)
        self.setting_menu_image_select_main = tk.Label(self.main_frame, image=images[NUM_BUTTON_IMAGE_SELECT],
                                              width=57, height=31, bd=0)
        self.setting_menu_image_select_main.bind("<Leave>", self.bt_setting_menu_image_select_nm)
        self.setting_menu_image_select_main.bind("<Enter>", self.bt_setting_menu_image_select_select)
        self.setting_menu_image_select_main.bind("<ButtonRelease-1>", self.bt_setting_menu_image_select_push)
        self.setting_menu_image_select_main.place(x=-66, y=158)

        # png / jpg 設定取得
        if IMAGE_FORMAT == ".png":
            png_index = NUM_BUTTON_PNG_ON
            jpg_index = NUM_BUTTON_JPG_OFF
        else:
            png_index = NUM_BUTTON_PNG_OFF
            jpg_index = NUM_BUTTON_JPG_ON

        # 設定画面PNGボタンを設定 (layer:top+3)
        self.setting_menu_bt_png_main = tk.Label(self.main_frame, image=images[png_index], width=70, height=17, bd=0)
        self.setting_menu_bt_png_main.bind("<Leave>", self.bt_setting_menu_png_nm)
        self.setting_menu_bt_png_main.bind("<Enter>", self.bt_setting_menu_png_select)
        self.setting_menu_bt_png_main.bind("<ButtonRelease-1>", self.bt_setting_menu_png_push)
        self.setting_menu_bt_png_main.place(x=-246, y=239)

        # 設定画面JPGボタンを設定 (layer:top+4)
        self.setting_menu_bt_jpg_main = tk.Label(self.main_frame, image=images[jpg_index], width=70, height=17, bd=0)
        self.setting_menu_bt_jpg_main.bind("<Leave>", self.bt_setting_menu_jpg_nm)
        self.setting_menu_bt_jpg_main.bind("<Enter>", self.bt_setting_menu_jpg_select)
        self.setting_menu_bt_jpg_main.bind("<ButtonRelease-1>", self.bt_setting_menu_jpg_push)
        self.setting_menu_bt_jpg_main.place(x=-149, y=239)

        # True / False 設定取得
        if LENGTH_LIMIT == "True":
            true_index = NUM_BUTTON_LIMIT_TRUE_ON
            false_index = NUM_BUTTON_LIMIT_FALSE_OFF
        else:
            true_index = NUM_BUTTON_LIMIT_TRUE_OFF
            false_index = NUM_BUTTON_LIMIT_FALSE_ON

        # 設定画面動画時間制限ありボタンを設定 (layer:top+5)
        self.setting_menu_bt_limit_true_main = tk.Label(self.main_frame, image=images[true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_true_main.bind("<Leave>", self.bt_setting_menu_limit_true_nm)
        self.setting_menu_bt_limit_true_main.bind("<Enter>", self.bt_setting_menu_limit_true_select)
        self.setting_menu_bt_limit_true_main.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_true_push)
        self.setting_menu_bt_limit_true_main.place(x=-246, y=314)

        # 設定画面動画時間制限なしボタンを設定 (layer:top+6)
        self.setting_menu_bt_limit_false_main = tk.Label(self.main_frame, image=images[false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_false_main.bind("<Leave>", self.bt_setting_menu_limit_false_nm)
        self.setting_menu_bt_limit_false_main.bind("<Enter>", self.bt_setting_menu_limit_false_select)
        self.setting_menu_bt_limit_false_main.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_false_push)
        self.setting_menu_bt_limit_false_main.place(x=-149, y=314)

        # True / False 設定取得
        if ENEMY_UB == "True":
            enemy_true_index = NUM_BUTTON_LIMIT_TRUE_ON
            enemy_false_index = NUM_BUTTON_LIMIT_FALSE_OFF
        else:
            enemy_true_index = NUM_BUTTON_LIMIT_TRUE_OFF
            enemy_false_index = NUM_BUTTON_LIMIT_FALSE_ON

        # 設定画面敵UB表示ありボタンを設定 (layer:top+7)
        self.setting_menu_bt_enemy_true_main = tk.Label(self.main_frame, image=images[enemy_true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_true_main.bind("<Leave>", self.bt_setting_menu_enemy_true_nm)
        self.setting_menu_bt_enemy_true_main.bind("<Enter>", self.bt_setting_menu_enemy_true_select)
        self.setting_menu_bt_enemy_true_main.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_true_push)
        self.setting_menu_bt_enemy_true_main.place(x=-246, y=389)

        # 設定画面敵UB表示なしボタンを設定 (layer:top+8)
        self.setting_menu_bt_enemy_false_main = tk.Label(self.main_frame, image=images[enemy_false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_false_main.bind("<Leave>", self.bt_setting_menu_enemy_false_nm)
        self.setting_menu_bt_enemy_false_main.bind("<Enter>", self.bt_setting_menu_enemy_false_select)
        self.setting_menu_bt_enemy_false_main.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_false_push)
        self.setting_menu_bt_enemy_false_main.place(x=-149, y=389)

        # 設定画面閉じるボタンを設定 (layer:top+9)
        self.setting_menu_bt_exit_main = tk.Label(self.main_frame, image=images[NUM_BUTTON_EXIT], width=63, height=25, bd=0)
        self.setting_menu_bt_exit_main.bind("<Leave>", self.bt_setting_menu_exit_nm)
        self.setting_menu_bt_exit_main.bind("<Enter>", self.bt_setting_menu_exit_select)
        self.setting_menu_bt_exit_main.bind("<ButtonRelease-1>", self.bt_setting_menu_exit_push)
        self.setting_menu_bt_exit_main.place(x=-165, y=502)

        # 設定画面バージョン情報を設定 (layer:top+10)
        self.setting_menu_version_main = tk.Label(self.main_frame, image="", width=6, height=1, fg="#E2E2E2",
                                             bg="#272727", bd=0, font=("メイリオ", 8), text=VERSION)
        self.setting_menu_version_main.place(x=-262, y=505)

        # フォーカス解除用ダミーを設定 (layer:None)
        self.focus_dummy = tk.Label(self.main_frame)
        self.focus_dummy.place(x=1000, y=1000)
        
        # ---------------------解析画面の設定---------------------
        self.analyze_frame = tk.Frame()
        self.analyze_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg_analyze = tk.Label(self.analyze_frame, image=images[NUM_BACKGROUND_ANALYZE], bd=0)
        self.bg_analyze.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.bg_analyze.pack(fill="x")

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
                                            width=95, height=26, bg="#272727")
        self.header_bt_setting_analyze.bind("<Leave>", self.header_bt_setting_nm)
        self.header_bt_setting_analyze.bind("<Enter>", self.header_bt_setting_select)
        self.header_bt_setting_analyze.bind("<ButtonRelease-1>", self.header_bt_setting_push)
        self.header_bt_setting_analyze.place(x=100, y=0)

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
        
        # 設定画面を設定 (layer:top)
        self.setting_menu_analyze = tk.Label(self.analyze_frame, image=images[NUM_BASE_SETTING], width=267, height=510,
                                          bd=0, text="")
        self.setting_menu_analyze.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_analyze.place(x=-267, y=30)

        # 設定画面サンプル画像を設定 (layer:top+1)
        self.setting_menu_image_analyze = tk.Label(self.analyze_frame, image=SETTING_IMAGE[0], width=160, height=90, bd=0, text="")
        self.setting_menu_image_analyze.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_image_analyze.place(x=-245, y=95)

        # 設定画面画像選択ボタンを設定 (layer:top+2)
        self.setting_menu_image_select_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_IMAGE_SELECT],
                                              width=57, height=31, bd=0)
        self.setting_menu_image_select_analyze.bind("<Leave>", self.bt_setting_menu_image_select_nm)
        self.setting_menu_image_select_analyze.bind("<Enter>", self.bt_setting_menu_image_select_select)
        self.setting_menu_image_select_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_image_select_push)
        self.setting_menu_image_select_analyze.place(x=-66, y=158)

        # 設定画面PNGボタンを設定 (layer:top+3)
        self.setting_menu_bt_png_analyze = tk.Label(self.analyze_frame, image=images[png_index], width=70, height=17, bd=0)
        self.setting_menu_bt_png_analyze.bind("<Leave>", self.bt_setting_menu_png_nm)
        self.setting_menu_bt_png_analyze.bind("<Enter>", self.bt_setting_menu_png_select)
        self.setting_menu_bt_png_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_png_push)
        self.setting_menu_bt_png_analyze.place(x=-246, y=239)

        # 設定画面JPGボタンを設定 (layer:top+4)
        self.setting_menu_bt_jpg_analyze = tk.Label(self.analyze_frame, image=images[jpg_index], width=70, height=17, bd=0)
        self.setting_menu_bt_jpg_analyze.bind("<Leave>", self.bt_setting_menu_jpg_nm)
        self.setting_menu_bt_jpg_analyze.bind("<Enter>", self.bt_setting_menu_jpg_select)
        self.setting_menu_bt_jpg_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_jpg_push)
        self.setting_menu_bt_jpg_analyze.place(x=-149, y=239)

        # 設定画面動画時間制限ありボタンを設定 (layer:top+5)
        self.setting_menu_bt_limit_true_analyze = tk.Label(self.analyze_frame, image=images[true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_true_analyze.bind("<Leave>", self.bt_setting_menu_limit_true_nm)
        self.setting_menu_bt_limit_true_analyze.bind("<Enter>", self.bt_setting_menu_limit_true_select)
        self.setting_menu_bt_limit_true_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_true_push)
        self.setting_menu_bt_limit_true_analyze.place(x=-246, y=314)

        # 設定画面動画時間制限なしボタンを設定 (layer:top+6)
        self.setting_menu_bt_limit_false_analyze = tk.Label(self.analyze_frame, image=images[false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_false_analyze.bind("<Leave>", self.bt_setting_menu_limit_false_nm)
        self.setting_menu_bt_limit_false_analyze.bind("<Enter>", self.bt_setting_menu_limit_false_select)
        self.setting_menu_bt_limit_false_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_false_push)
        self.setting_menu_bt_limit_false_analyze.place(x=-149, y=314)

        # 設定画面敵UB表示ありボタンを設定 (layer:top+7)
        self.setting_menu_bt_enemy_true_analyze = tk.Label(self.analyze_frame, image=images[enemy_true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_true_analyze.bind("<Leave>", self.bt_setting_menu_enemy_true_nm)
        self.setting_menu_bt_enemy_true_analyze.bind("<Enter>", self.bt_setting_menu_enemy_true_select)
        self.setting_menu_bt_enemy_true_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_true_push)
        self.setting_menu_bt_enemy_true_analyze.place(x=-246, y=389)

        # 設定画面敵UB表示なしボタンを設定 (layer:top+8)
        self.setting_menu_bt_enemy_false_analyze = tk.Label(self.analyze_frame, image=images[enemy_false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_false_analyze.bind("<Leave>", self.bt_setting_menu_enemy_false_nm)
        self.setting_menu_bt_enemy_false_analyze.bind("<Enter>", self.bt_setting_menu_enemy_false_select)
        self.setting_menu_bt_enemy_false_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_false_push)
        self.setting_menu_bt_enemy_false_analyze.place(x=-149, y=389)

        # 設定画面閉じるボタンを設定 (layer:top+9)
        self.setting_menu_bt_exit_analyze = tk.Label(self.analyze_frame, image=images[NUM_BUTTON_EXIT], width=63, height=25, bd=0)
        self.setting_menu_bt_exit_analyze.bind("<Leave>", self.bt_setting_menu_exit_nm)
        self.setting_menu_bt_exit_analyze.bind("<Enter>", self.bt_setting_menu_exit_select)
        self.setting_menu_bt_exit_analyze.bind("<ButtonRelease-1>", self.bt_setting_menu_exit_push)
        self.setting_menu_bt_exit_analyze.place(x=-165, y=502)

        # 設定画面バージョン情報を設定 (layer:top+10)
        self.setting_menu_version_analyze = tk.Label(self.analyze_frame, image="", width=6, height=1, fg="#E2E2E2",
                                             bg="#272727", bd=0, font=("メイリオ", 8), text=VERSION)
        self.setting_menu_version_analyze.place(x=-262, y=505)

        # ---------------------結果画面の設定---------------------
        self.result_frame = tk.Frame()
        self.result_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        self.bg_result = tk.Label(self.result_frame, image=images[NUM_BACKGROUND_ANALYZE], bd=0)
        self.bg_result.bind("<ButtonRelease-1>", self.clear_view_parts)  # フォーカス/設定画面初期化
        self.bg_result.pack(fill="x")

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
                                            width=95, height=26, bg="#272727")
        self.header_bt_setting_result.bind("<Leave>", self.header_bt_setting_nm)
        self.header_bt_setting_result.bind("<Enter>", self.header_bt_setting_select)
        self.header_bt_setting_result.bind("<ButtonRelease-1>", self.header_bt_setting_push)
        self.header_bt_setting_result.place(x=100, y=0)

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
        
        # 設定画面を設定 (layer:top)
        self.setting_menu_result = tk.Label(self.result_frame, image=images[NUM_BASE_SETTING], width=267, height=510,
                                          bd=0, text="")
        self.setting_menu_result.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_result.place(x=-267, y=30)

        # 設定画面サンプル画像を設定 (layer:top+1)
        self.setting_menu_image_result = tk.Label(self.result_frame, image=SETTING_IMAGE[0], width=160, height=90, bd=0, text="")
        self.setting_menu_image_result.bind("<ButtonRelease-1>", self.clear_focus)  # フォーカス初期化
        self.setting_menu_image_result.place(x=-245, y=95)

        # 設定画面画像選択ボタンを設定 (layer:top+2)
        self.setting_menu_image_select_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_IMAGE_SELECT],
                                              width=57, height=31, bd=0)
        self.setting_menu_image_select_result.bind("<Leave>", self.bt_setting_menu_image_select_nm)
        self.setting_menu_image_select_result.bind("<Enter>", self.bt_setting_menu_image_select_select)
        self.setting_menu_image_select_result.bind("<ButtonRelease-1>", self.bt_setting_menu_image_select_push)
        self.setting_menu_image_select_result.place(x=-66, y=158)

        # 設定画面PNGボタンを設定 (layer:top+3)
        self.setting_menu_bt_png_result = tk.Label(self.result_frame, image=images[png_index], width=70, height=17, bd=0)
        self.setting_menu_bt_png_result.bind("<Leave>", self.bt_setting_menu_png_nm)
        self.setting_menu_bt_png_result.bind("<Enter>", self.bt_setting_menu_png_select)
        self.setting_menu_bt_png_result.bind("<ButtonRelease-1>", self.bt_setting_menu_png_push)
        self.setting_menu_bt_png_result.place(x=-246, y=239)

        # 設定画面JPGボタンを設定 (layer:top+4)
        self.setting_menu_bt_jpg_result = tk.Label(self.result_frame, image=images[jpg_index], width=70, height=17, bd=0)
        self.setting_menu_bt_jpg_result.bind("<Leave>", self.bt_setting_menu_jpg_nm)
        self.setting_menu_bt_jpg_result.bind("<Enter>", self.bt_setting_menu_jpg_select)
        self.setting_menu_bt_jpg_result.bind("<ButtonRelease-1>", self.bt_setting_menu_jpg_push)
        self.setting_menu_bt_jpg_result.place(x=-149, y=239)

        # 設定画面動画時間制限ありボタンを設定 (layer:top+5)
        self.setting_menu_bt_limit_true_result = tk.Label(self.result_frame, image=images[true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_true_result.bind("<Leave>", self.bt_setting_menu_limit_true_nm)
        self.setting_menu_bt_limit_true_result.bind("<Enter>", self.bt_setting_menu_limit_true_select)
        self.setting_menu_bt_limit_true_result.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_true_push)
        self.setting_menu_bt_limit_true_result.place(x=-246, y=314)

        # 設定画面動画時間制限なしボタンを設定 (layer:top+6)
        self.setting_menu_bt_limit_false_result = tk.Label(self.result_frame, image=images[false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_limit_false_result.bind("<Leave>", self.bt_setting_menu_limit_false_nm)
        self.setting_menu_bt_limit_false_result.bind("<Enter>", self.bt_setting_menu_limit_false_select)
        self.setting_menu_bt_limit_false_result.bind("<ButtonRelease-1>", self.bt_setting_menu_limit_false_push)
        self.setting_menu_bt_limit_false_result.place(x=-149, y=314)

        # 設定画面敵UB表示ありボタンを設定 (layer:top+7)
        self.setting_menu_bt_enemy_true_result = tk.Label(self.result_frame, image=images[enemy_true_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_true_result.bind("<Leave>", self.bt_setting_menu_enemy_true_nm)
        self.setting_menu_bt_enemy_true_result.bind("<Enter>", self.bt_setting_menu_enemy_true_select)
        self.setting_menu_bt_enemy_true_result.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_true_push)
        self.setting_menu_bt_enemy_true_result.place(x=-246, y=389)

        # 設定画面敵UB表示なしボタンを設定 (layer:top+8)
        self.setting_menu_bt_enemy_false_result = tk.Label(self.result_frame, image=images[enemy_false_index], width=70, height=17, bd=0)
        self.setting_menu_bt_enemy_false_result.bind("<Leave>", self.bt_setting_menu_enemy_false_nm)
        self.setting_menu_bt_enemy_false_result.bind("<Enter>", self.bt_setting_menu_enemy_false_select)
        self.setting_menu_bt_enemy_false_result.bind("<ButtonRelease-1>", self.bt_setting_menu_enemy_false_push)
        self.setting_menu_bt_enemy_false_result.place(x=-149, y=389)

        # 設定画面閉じるボタンを設定 (layer:top+9)
        self.setting_menu_bt_exit_result = tk.Label(self.result_frame, image=images[NUM_BUTTON_EXIT], width=63, height=25, bd=0)
        self.setting_menu_bt_exit_result.bind("<Leave>", self.bt_setting_menu_exit_nm)
        self.setting_menu_bt_exit_result.bind("<Enter>", self.bt_setting_menu_exit_select)
        self.setting_menu_bt_exit_result.bind("<ButtonRelease-1>", self.bt_setting_menu_exit_push)
        self.setting_menu_bt_exit_result.place(x=-165, y=502)

        # 設定画面バージョン情報を設定 (layer:top+10)
        self.setting_menu_version_result = tk.Label(self.result_frame, image="", width=6, height=1, fg="#E2E2E2",
                                             bg="#272727", bd=0, font=("メイリオ", 8), text=VERSION)
        self.setting_menu_version_result.place(x=-262, y=505)

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

            # 設定位置を初期化
            self.setting_menu_place_forget()

            # 設定画面を画面内に配置する
            self.setting_menu_place_in()
            setting_status = True

    # 設定画面用イベント (layer:Top)
    def clear_setting(self, event):
        global setting_status

        # 設定位置を初期化
        self.setting_menu_place_forget()

        # 設定画面を画面外に配置する
        self.setting_menu_place_out()
        setting_status = False

    def setting_menu_place_in(self):
        # 設定画面を画面内に配置する

        # MAIN画面設定画面の配置
        self.setting_menu_main.place(x=0, y=30)
        self.setting_menu_image_main.place(x=22, y=95)
        self.setting_menu_image_select_main.place(x=201, y=158)
        self.setting_menu_bt_png_main.place(x=21, y=239)
        self.setting_menu_bt_jpg_main.place(x=118, y=239)
        self.setting_menu_bt_limit_true_main.place(x=21, y=314)
        self.setting_menu_bt_limit_false_main.place(x=118, y=314)
        self.setting_menu_bt_enemy_true_main.place(x=21, y=389)
        self.setting_menu_bt_enemy_false_main.place(x=118, y=389)
        self.setting_menu_bt_exit_main.place(x=102, y=502)
        self.setting_menu_version_main.place(x=5, y=502)

        # 解析画面設定画面の配置
        self.setting_menu_analyze.place(x=0, y=30)
        self.setting_menu_image_analyze.place(x=22, y=95)
        self.setting_menu_image_select_analyze.place(x=201, y=158)
        self.setting_menu_bt_png_analyze.place(x=21, y=239)
        self.setting_menu_bt_jpg_analyze.place(x=118, y=239)
        self.setting_menu_bt_limit_true_analyze.place(x=21, y=314)
        self.setting_menu_bt_limit_false_analyze.place(x=118, y=314)
        self.setting_menu_bt_enemy_true_analyze.place(x=21, y=389)
        self.setting_menu_bt_enemy_false_analyze.place(x=118, y=389)
        self.setting_menu_bt_exit_analyze.place(x=102, y=502)
        self.setting_menu_version_analyze.place(x=5, y=502)

        # 結果画面設定画面の配置
        self.setting_menu_result.place(x=0, y=30)
        self.setting_menu_image_result.place(x=22, y=95)
        self.setting_menu_image_select_result.place(x=201, y=158)
        self.setting_menu_bt_png_result.place(x=21, y=239)
        self.setting_menu_bt_jpg_result.place(x=118, y=239)
        self.setting_menu_bt_limit_true_result.place(x=21, y=314)
        self.setting_menu_bt_limit_false_result.place(x=118, y=314)
        self.setting_menu_bt_enemy_true_result.place(x=21, y=389)
        self.setting_menu_bt_enemy_false_result.place(x=118, y=389)
        self.setting_menu_bt_exit_result.place(x=102, y=502)
        self.setting_menu_version_result.place(x=5, y=502)

    def setting_menu_place_out(self):
        # 設定画面を画面外に配置する

        # MAIN画面設定画面の配置
        self.setting_menu_main.place(x=-267, y=30)
        self.setting_menu_image_main.place(x=-245, y=95)
        self.setting_menu_image_select_main.place(x=-66, y=158)
        self.setting_menu_bt_png_main.place(x=-246, y=239)
        self.setting_menu_bt_jpg_main.place(x=-149, y=239)
        self.setting_menu_bt_limit_true_main.place(x=-246, y=314)
        self.setting_menu_bt_limit_false_main.place(x=-149, y=314)
        self.setting_menu_bt_enemy_true_main.place(x=-246, y=389)
        self.setting_menu_bt_enemy_false_main.place(x=-149, y=389)
        self.setting_menu_bt_exit_main.place(x=-165, y=502)
        self.setting_menu_version_main.place(x=-262, y=505)

        # 解析画面設定画面の配置
        self.setting_menu_analyze.place(x=-267, y=30)
        self.setting_menu_image_analyze.place(x=-245, y=95)
        self.setting_menu_image_select_analyze.place(x=-66, y=158)
        self.setting_menu_bt_png_analyze.place(x=-246, y=239)
        self.setting_menu_bt_jpg_analyze.place(x=-149, y=239)
        self.setting_menu_bt_limit_true_analyze.place(x=-246, y=314)
        self.setting_menu_bt_limit_false_analyze.place(x=-149, y=314)
        self.setting_menu_bt_enemy_true_analyze.place(x=-246, y=389)
        self.setting_menu_bt_enemy_false_analyze.place(x=-149, y=389)
        self.setting_menu_bt_exit_analyze.place(x=-165, y=502)
        self.setting_menu_version_analyze.place(x=-262, y=505)

        # 結果画面設定画面の配置
        self.setting_menu_result.place(x=-267, y=30)
        self.setting_menu_image_result.place(x=-245, y=95)
        self.setting_menu_image_select_result.place(x=-66, y=158)
        self.setting_menu_bt_png_result.place(x=-246, y=239)
        self.setting_menu_bt_jpg_result.place(x=-149, y=239)
        self.setting_menu_bt_limit_true_result.place(x=-246, y=314)
        self.setting_menu_bt_limit_false_result.place(x=-149, y=314)
        self.setting_menu_bt_enemy_true_result.place(x=-246, y=389)
        self.setting_menu_bt_enemy_false_result.place(x=-149, y=389)
        self.setting_menu_bt_exit_result.place(x=-165, y=502)
        self.setting_menu_version_result.place(x=-262, y=505)

    def setting_menu_place_forget(self):
        # 設定画面配置位置を初期化する

        # MAIN画面設定画面の初期化
        self.setting_menu_main.place_forget()
        self.setting_menu_image_main.place_forget()
        self.setting_menu_image_select_main.place_forget()
        self.setting_menu_bt_png_main.place_forget()
        self.setting_menu_bt_jpg_main.place_forget()
        self.setting_menu_bt_limit_true_main.place_forget()
        self.setting_menu_bt_limit_false_main.place_forget()
        self.setting_menu_bt_enemy_true_main.place_forget()
        self.setting_menu_bt_enemy_false_main.place_forget()
        self.setting_menu_bt_exit_main.place_forget()
        self.setting_menu_version_main.place_forget()

        # 解析画面設定画面の初期化
        self.setting_menu_analyze.place_forget()
        self.setting_menu_image_analyze.place_forget()
        self.setting_menu_image_select_analyze.place_forget()
        self.setting_menu_bt_png_analyze.place_forget()
        self.setting_menu_bt_jpg_analyze.place_forget()
        self.setting_menu_bt_limit_true_analyze.place_forget()
        self.setting_menu_bt_limit_false_analyze.place_forget()
        self.setting_menu_bt_enemy_true_analyze.place_forget()
        self.setting_menu_bt_enemy_false_analyze.place_forget()
        self.setting_menu_bt_exit_analyze.place_forget()
        self.setting_menu_version_analyze.place_forget()

        # 結果画面設定画面の初期化
        self.setting_menu_result.place_forget()
        self.setting_menu_image_result.place_forget()
        self.setting_menu_image_select_result.place_forget()
        self.setting_menu_bt_png_result.place_forget()
        self.setting_menu_bt_jpg_result.place_forget()
        self.setting_menu_bt_limit_true_result.place_forget()
        self.setting_menu_bt_limit_false_result.place_forget()
        self.setting_menu_bt_enemy_true_result.place_forget()
        self.setting_menu_bt_enemy_false_result.place_forget()
        self.setting_menu_bt_exit_result.place_forget()
        self.setting_menu_version_result.place_forget()

    # 設定画面画像選択ボタン用イベント (layer:top+2)
    def bt_setting_menu_image_select_nm(self, event):
        self.setting_menu_image_select_main.configure(image=images[NUM_BUTTON_IMAGE_SELECT], cursor="arrow")
        self.setting_menu_image_select_analyze.configure(image=images[NUM_BUTTON_IMAGE_SELECT], cursor="arrow")
        self.setting_menu_image_select_result.configure(image=images[NUM_BUTTON_IMAGE_SELECT], cursor="arrow")

    def bt_setting_menu_image_select_select(self, event):
        self.setting_menu_image_select_main.configure(image=images[NUM_BUTTON_IMAGE_SELECT_2], cursor="hand2")
        self.setting_menu_image_select_analyze.configure(image=images[NUM_BUTTON_IMAGE_SELECT_2], cursor="hand2")
        self.setting_menu_image_select_result.configure(image=images[NUM_BUTTON_IMAGE_SELECT_2], cursor="hand2")

    def bt_setting_menu_image_select_push(self, event):
        global IMAGE_PATH
        self.bt_setting_menu_image_select_nm(self)

        file_type = [("", ".png;*.jpg")]
        initial_dir = IMAGE_PATH
        file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

        if file != "":
            # 背景の保存
            base_image = (Image.open(file)).resize((960, 540))
            base_image.save(BACKGROUND_BASE)
            base_image_save = ImageTk.PhotoImage(base_image)
            images[NUM_BACKGROUND_BASE] = base_image_save

            # MAIN画面背景の設定
            bg_main = bg_maker.bg_editor(base_image, Image.open(PICTURE_PATH[NUM_BACKGROUND_TOP]))
            bg_main = ImageTk.PhotoImage(bg_main)
            self.bg_main.configure(image=bg_main)
            images[NUM_BACKGROUND_TOP] = bg_main

            # 解析/結果画面背景の設定
            bg_analyze = bg_maker.bg_editor(base_image, Image.open(PICTURE_PATH[NUM_BACKGROUND_ANALYZE]))
            bg_analyze = ImageTk.PhotoImage(bg_analyze)
            self.bg_analyze.configure(image=bg_analyze)
            self.bg_result.configure(image=bg_analyze)
            images[NUM_BACKGROUND_ANALYZE] = bg_analyze

            # setting画面画像の設定
            menu_image = base_image.resize((160, 90))
            menu_image = ImageTk.PhotoImage(menu_image)
            self.setting_menu_image_main.configure(image=menu_image)
            self.setting_menu_image_analyze.configure(image=menu_image)
            self.setting_menu_image_result.configure(image=menu_image)
            SETTING_IMAGE.clear()
            SETTING_IMAGE.append(menu_image)

            # 画像パスの保存
            IMAGE_PATH = os.path.dirname(file)

    # 設定画面PNGボタン用イベント (layer:top+3)
    def bt_setting_menu_png_nm(self, event):
        self.setting_menu_bt_png_main.configure(cursor="arrow")
        self.setting_menu_bt_png_analyze.configure(cursor="arrow")
        self.setting_menu_bt_png_result.configure(cursor="arrow")

    def bt_setting_menu_png_select(self, event):
        self.setting_menu_bt_png_main.configure(cursor="hand2")
        self.setting_menu_bt_png_analyze.configure(cursor="hand2")
        self.setting_menu_bt_png_result.configure(cursor="hand2")

    def bt_setting_menu_png_push(self, event):
        global IMAGE_FORMAT

        if IMAGE_FORMAT != ".png":
            IMAGE_FORMAT = ".png"
            self.setting_menu_bt_png_main.configure(image=images[NUM_BUTTON_PNG_ON])
            self.setting_menu_bt_png_analyze.configure(image=images[NUM_BUTTON_PNG_ON])
            self.setting_menu_bt_png_result.configure(image=images[NUM_BUTTON_PNG_ON])
            self.setting_menu_bt_jpg_main.configure(image=images[NUM_BUTTON_JPG_OFF])
            self.setting_menu_bt_jpg_analyze.configure(image=images[NUM_BUTTON_JPG_OFF])
            self.setting_menu_bt_jpg_result.configure(image=images[NUM_BUTTON_JPG_OFF])
            save_config()

    # 設定画面JPGボタン用イベント (layer:top+4)
    def bt_setting_menu_jpg_nm(self, event):
        self.setting_menu_bt_jpg_main.configure(cursor="arrow")
        self.setting_menu_bt_jpg_analyze.configure(cursor="arrow")
        self.setting_menu_bt_jpg_result.configure(cursor="arrow")

    def bt_setting_menu_jpg_select(self, event):
        self.setting_menu_bt_jpg_main.configure(cursor="hand2")
        self.setting_menu_bt_jpg_analyze.configure(cursor="hand2")
        self.setting_menu_bt_jpg_result.configure(cursor="hand2")

    def bt_setting_menu_jpg_push(self, event):
        global IMAGE_FORMAT

        if IMAGE_FORMAT != ".jpg":
            IMAGE_FORMAT = ".jpg"
            self.setting_menu_bt_jpg_main.configure(image=images[NUM_BUTTON_JPG_ON])
            self.setting_menu_bt_jpg_analyze.configure(image=images[NUM_BUTTON_JPG_ON])
            self.setting_menu_bt_jpg_result.configure(image=images[NUM_BUTTON_JPG_ON])
            self.setting_menu_bt_png_main.configure(image=images[NUM_BUTTON_PNG_OFF])
            self.setting_menu_bt_png_analyze.configure(image=images[NUM_BUTTON_PNG_OFF])
            self.setting_menu_bt_png_result.configure(image=images[NUM_BUTTON_PNG_OFF])
            save_config()

    # 設定画面動画時間制限ありボタン用イベント (layer:top+5)
    def bt_setting_menu_limit_true_nm(self, event):
        self.setting_menu_bt_limit_true_main.configure(cursor="arrow")
        self.setting_menu_bt_limit_true_analyze.configure(cursor="arrow")
        self.setting_menu_bt_limit_true_result.configure(cursor="arrow")

    def bt_setting_menu_limit_true_select(self, event):
        self.setting_menu_bt_limit_true_main.configure(cursor="hand2")
        self.setting_menu_bt_limit_true_analyze.configure(cursor="hand2")
        self.setting_menu_bt_limit_true_result.configure(cursor="hand2")

    def bt_setting_menu_limit_true_push(self, event):
        global LENGTH_LIMIT

        if LENGTH_LIMIT != "True":
            LENGTH_LIMIT = "True"
            self.setting_menu_bt_limit_true_main.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_limit_true_analyze.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_limit_true_result.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_limit_false_main.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            self.setting_menu_bt_limit_false_analyze.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            self.setting_menu_bt_limit_false_result.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            save_config()

    # 設定画面動画時間制限なしボタン用イベント (layer:top+6)
    def bt_setting_menu_limit_false_nm(self, event):
        self.setting_menu_bt_limit_false_main.configure(cursor="arrow")
        self.setting_menu_bt_limit_false_analyze.configure(cursor="arrow")
        self.setting_menu_bt_limit_false_result.configure(cursor="arrow")

    def bt_setting_menu_limit_false_select(self, event):
        self.setting_menu_bt_limit_false_main.configure(cursor="hand2")
        self.setting_menu_bt_limit_false_analyze.configure(cursor="hand2")
        self.setting_menu_bt_limit_false_result.configure(cursor="hand2")

    def bt_setting_menu_limit_false_push(self, event):
        global LENGTH_LIMIT

        if LENGTH_LIMIT != "False":
            LENGTH_LIMIT = "False"
            self.setting_menu_bt_limit_false_main.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_limit_false_analyze.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_limit_false_result.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_limit_true_main.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            self.setting_menu_bt_limit_true_analyze.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            self.setting_menu_bt_limit_true_result.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            save_config()

    # 設定画面敵UB表示ありボタン用イベント (layer:top+7)
    def bt_setting_menu_enemy_true_nm(self, event):
        self.setting_menu_bt_enemy_true_main.configure(cursor="arrow")
        self.setting_menu_bt_enemy_true_analyze.configure(cursor="arrow")
        self.setting_menu_bt_enemy_true_result.configure(cursor="arrow")

    def bt_setting_menu_enemy_true_select(self, event):
        self.setting_menu_bt_enemy_true_main.configure(cursor="hand2")
        self.setting_menu_bt_enemy_true_analyze.configure(cursor="hand2")
        self.setting_menu_bt_enemy_true_result.configure(cursor="hand2")

    def bt_setting_menu_enemy_true_push(self, event):
        global ENEMY_UB

        if ENEMY_UB != "True":
            ENEMY_UB = "True"
            self.setting_menu_bt_enemy_true_main.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_enemy_true_analyze.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_enemy_true_result.configure(image=images[NUM_BUTTON_LIMIT_TRUE_ON])
            self.setting_menu_bt_enemy_false_main.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            self.setting_menu_bt_enemy_false_analyze.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            self.setting_menu_bt_enemy_false_result.configure(image=images[NUM_BUTTON_LIMIT_FALSE_OFF])
            save_config()

    # 設定画面敵UB表示なしボタン用イベント (layer:top+8)
    def bt_setting_menu_enemy_false_nm(self, event):
        self.setting_menu_bt_enemy_false_main.configure(cursor="arrow")
        self.setting_menu_bt_enemy_false_analyze.configure(cursor="arrow")
        self.setting_menu_bt_enemy_false_result.configure(cursor="arrow")

    def bt_setting_menu_enemy_false_select(self, event):
        self.setting_menu_bt_enemy_false_main.configure(cursor="hand2")
        self.setting_menu_bt_enemy_false_analyze.configure(cursor="hand2")
        self.setting_menu_bt_enemy_false_result.configure(cursor="hand2")

    def bt_setting_menu_enemy_false_push(self, event):
        global ENEMY_UB

        if ENEMY_UB != "False":
            ENEMY_UB = "False"
            self.setting_menu_bt_enemy_false_main.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_enemy_false_analyze.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_enemy_false_result.configure(image=images[NUM_BUTTON_LIMIT_FALSE_ON])
            self.setting_menu_bt_enemy_true_main.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            self.setting_menu_bt_enemy_true_analyze.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            self.setting_menu_bt_enemy_true_result.configure(image=images[NUM_BUTTON_LIMIT_TRUE_OFF])
            save_config()

    # 設定画面閉じるボタン用イベント (layer:top+9)
    def bt_setting_menu_exit_nm(self, event):
        self.setting_menu_bt_exit_main.configure(image=images[NUM_BUTTON_EXIT], cursor="arrow")
        self.setting_menu_bt_exit_analyze.configure(image=images[NUM_BUTTON_EXIT], cursor="arrow")
        self.setting_menu_bt_exit_result.configure(image=images[NUM_BUTTON_EXIT], cursor="arrow")

    def bt_setting_menu_exit_select(self, event):
        self.setting_menu_bt_exit_main.configure(image=images[NUM_BUTTON_EXIT_2], cursor="hand2")
        self.setting_menu_bt_exit_analyze.configure(image=images[NUM_BUTTON_EXIT_2], cursor="hand2")
        self.setting_menu_bt_exit_result.configure(image=images[NUM_BUTTON_EXIT_2], cursor="hand2")

    def bt_setting_menu_exit_push(self, event):
        self.bt_setting_menu_exit_nm(self)
        self.clear_setting(self)

    # ---------------------MAIN画面(layer:4~)の設定---------------------
    # SELECTボタン用イベント (layer:6)
    def bt_select_nm(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT], bg="#94DADE", cursor="arrow")

    def bt_select_select(self, event):
        self.bt_select.configure(image=images[NUM_BUTTON_SELECT_2], bg="#599EA2", cursor="hand2")

    def bt_select_push(self, event):
        global MOVIE_PATH

        # フォーカス/設定画面を初期化
        self.clear_view_parts(self)

        file_type = [("", ".mp4")]
        initial_dir = MOVIE_PATH
        file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

        if file != "":
            self.text_box.delete(0, tk.END)
            self.text_box.insert(tk.END, file)

            MOVIE_PATH = os.path.dirname(file)
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
            app.set_image_format(IMAGE_FORMAT)
            app.set_length_limit(LENGTH_LIMIT)
            app.set_enemy_ub(ENEMY_UB)
            app_thread = threading.Thread(target=app.analyze_transition_check, args=(file_path, self))
            app_thread.setDaemon(True)
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


def on_closing():
    # 強制終了時安全に停止させる
    save_config()
    f.quit()


if __name__ == "__main__":
    load_config()
    f = Frame()
    f.protocol("WM_DELETE_WINDOW", on_closing)
    f.mainloop()
