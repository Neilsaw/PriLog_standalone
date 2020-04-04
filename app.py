# -*- coding: utf-8 -*-
import numpy as np
import os
from pytube import YouTube
from pytube import extract
from pytube import exceptions
import time as tm
import datetime
import cv2
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import sys
import urllib.parse
import itertools
import characters as cd
import after_caluculation as ac
import view

# キャラクター名テンプレート
CHARACTERS_DATA = []

# 時間テンプレート
SEC_DATA = []

# MENUテンプレート
MENU_DATA = []

# スコアテンプレート
SCORE_DATA = []

# ダメージ数値テンプレート
DAMAGE_DATA = []

# アンナアイコンテンプレート
ICON_DATA = []

# ダメージレポートテンプレート
DETAIL_REPORT_DATA = []

# 王冠テンプレート
CROWN_DATA = []

# キャラクター名一覧
CHARACTERS = cd.characters_name

# 数値一覧
NUMBERS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

# 解析可能な解像度 (割合)
FRAME_RESOLUTION = [
    # width, height
    (16, 9),        # RESOLUTION_16_9
]

RESOLUTION_16_9 = 0

# 画像認識範囲
UB_ROI = (0, 0, 0, 0)
MIN_ROI = (0, 0, 0, 0)
TEN_SEC_ROI = (0, 0, 0, 0)
ONE_SEC_ROI = (0, 0, 0, 0)
MENU_ROI = (0, 0, 0, 0)
SCORE_ROI = (0, 0, 0, 0)
DAMAGE_DATA_ROI = (0, 0, 0, 0)
CHARACTER_ICON_ROI = (0, 0, 0, 0)
DETAIL_REPORT_ROI = (0, 0, 0, 0)
CROWN_DATA_ROI = (0, 0, 0, 0)
MENU_LOC = (0, 0)

FRAME_THRESH = 200

FRAME_COLS = 1280
FRAME_ROWS = 720

# 時刻格納位置
TIMER_MIN = 2
TIMER_TEN_SEC = 1
TIMER_SEC = 0

# 認識判定値
UB_THRESH = 0.6
TIMER_THRESH = 0.6
ITEM_THRESH = 0.6
DAMAGE_THRESH = 0.65
ICON_THRESH = 0.6

FOUND = 1
NOT_FOUND = 0

# エラーリスト
NO_ERROR = 0
ERROR_BAD_URL = 1
ERROR_TOO_LONG = 2
ERROR_NOT_SUPPORTED = 3
ERROR_CANT_GET_MOVIE = 4
ERROR_REQUIRED_PARAM = 5
ERROR_PROCESS_FAILED = 6

# キャッシュ格納数
CACHE_NUM = 5

# VIEWとのIF用
ANALYZE_DO = 0
ANALYZE_PENDING = 1
ANALYZE_STOP = 2

ANALYZE_STATUS = ANALYZE_DO

stream_dir = "tmp/"
if not os.path.exists(stream_dir):
    os.mkdir(stream_dir)

cache_dir = "cache/"
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)

pending_dir = "pending/"
if not os.path.exists(pending_dir):
    os.mkdir(pending_dir)

result_dir = "result/"
if not os.path.exists(result_dir):
    os.mkdir(result_dir)


def cache_check(youtube_id):
    # キャッシュ有無の確認
    try:
        cache_path = cache_dir + urllib.parse.quote(youtube_id) + '.json'
        ret = json.load(open(cache_path))
        if len(ret) is CACHE_NUM:
            # キャッシュから取得した値の数が規定値
            return ret
        else:
            # 異常なキャッシュの場合
            clear_path(cache_path)
            return False

    except FileNotFoundError:
        return False


def pending_append(path):
    # 解析中のIDを保存
    try:
        with open(path, mode='w'):
            pass
    except FileExistsError:
        pass

    return


def clear_path(path):
    # ファイルの削除
    try:
        os.remove(path)
    except PermissionError:
        pass
    except FileNotFoundError:
        pass

    return


def get_youtube_id(url):
    # ID部分の取り出し
    try:
        ret = extract.video_id(url)
    except exceptions.RegexMatchError:
        ret = False

    return ret


def model_init(video_type):
    # 動画の種類ごとのモデル初期化処理
    global CHARACTERS_DATA          # キャラクター名テンプレート
    global SEC_DATA                 # 時間テンプレート
    global MENU_DATA                # MENUテンプレート
    global SCORE_DATA               # スコアテンプレート
    global DAMAGE_DATA              # ダメージ数値テンプレート
    global ICON_DATA                # アンナアイコンテンプレート
    global DETAIL_REPORT_DATA       # ダメージレポートテンプレート
    global CROWN_DATA               # 王冠テンプレート

    if video_type is RESOLUTION_16_9:
        CHARACTERS_DATA = np.load("model/16_9/UB_name_16_9.npy")
        SEC_DATA = np.load("model/16_9/timer_sec_16_9.npy")
        MENU_DATA = np.load("model/16_9/menu_16_9.npy")
        SCORE_DATA = np.load("model/16_9/score_data_16_9.npy")
        DAMAGE_DATA = np.load("model/16_9/damage_data_16_9.npy")
        ICON_DATA = np.load("model/16_9/icon_data_16_9.npy")
        DETAIL_REPORT_DATA = np.load("model/16_9/detail_report_16_9.npy")
        CROWN_DATA = np.load("model/16_9/crown_16_9.npy")

    return


def roi_init(video_type):
    # 動画の種類ごとのモデル初期化処理
    global UB_ROI                # UB名　解析位置
    global MIN_ROI               # 時刻　分　解析位置
    global TEN_SEC_ROI           # 時刻　10秒　解析位置
    global ONE_SEC_ROI           # 時刻　1秒　解析位置
    global MENU_ROI              # MENU　ボタン　解析位置
    global SCORE_ROI             # スコア　解析位置
    global DAMAGE_DATA_ROI       # ダメージ　解析位置
    global CHARACTER_ICON_ROI    # アイコン　解析位置
    global DETAIL_REPORT_ROI     # ダメージレポート　解析位置
    global CROWN_DATA_ROI        # 王冠　解析位置

    global MENU_LOC              # MENU　ボタン　正位置
    global FRAME_THRESH          # 解析用下限値
    global FRAME_COLS            # 横解像度
    global FRAME_ROWS            # 縦解像度

    if video_type is RESOLUTION_16_9:
        UB_ROI = (490, 98, 810, 132)
        MIN_ROI = (1068, 22, 1091, 44)
        TEN_SEC_ROI = (1089, 22, 1109, 44)
        ONE_SEC_ROI = (1103, 22, 1123, 44)
        MENU_ROI = (1100, 0, 1280, 90)
        SCORE_ROI = (160, 630, 290, 680)
        DAMAGE_DATA_ROI = (35, 50, 255, 100)
        CHARACTER_ICON_ROI = (234, 506, 1046, 668)
        DETAIL_REPORT_ROI = (519, 33, 759, 79)
        CROWN_DATA_ROI = (431, 152, 470, 182)
        MENU_LOC = (63, 23)
        FRAME_THRESH = 200
        FRAME_COLS = 1280
        FRAME_ROWS = 720

    return


def get_aspect_ratio(width, height):
    gcd = np.gcd(width, height)
    x = int(width / gcd)
    y = int(height / gcd)

    return x, y


def search(youtube_id):
    # youtubeの動画を検索し取得
    youtube_url = 'https://www.youtube.com/watch?v=' + youtube_id
    try:
        yt = YouTube(youtube_url)
    except:
        return None, None, ERROR_CANT_GET_MOVIE

    movie_thumbnail = yt.thumbnail_url
    movie_length = yt.length
    if int(movie_length) > 480:
        return None, None, ERROR_TOO_LONG

    stream = yt.streams.get_by_itag("22")
    if stream is None:
        return None, None, ERROR_NOT_SUPPORTED

    movie_title = stream.title
    movie_name = tm.time()
    movie_path = stream.download(stream_dir, str(movie_name))

    return movie_path, movie_title, NO_ERROR


def analyze_movie(movie_path, self):
    # 動画解析し結果をリストで返す
    start_time = tm.time()

    result_name = datetime.datetime.fromtimestamp(start_time)
    result_name = result_name.strftime('%Y-%m-%d_%H-%M-%S')

    result_file_dir = result_dir + result_name + "/"
    if not os.path.exists(result_file_dir):
        os.mkdir(result_file_dir)

    # 動画の確認
    video_type = movie_check(movie_path)[1]

    video = cv2.VideoCapture(movie_path)

    frame_count = int(video.get(7))  # フレーム数を取得
    frame_rate = int(video.get(5))  # フレームレート(1フレームの時間単位はミリ秒)の取得

    model_init(video_type)
    roi_init(video_type)

    n = 0.34  # n秒ごと*
    ub_interval = 0

    time_min = "1"
    time_sec10 = "3"
    time_sec1 = "0"

    menu_check = False

    min_roi = MIN_ROI
    tensec_roi = TEN_SEC_ROI
    onesec_roi = ONE_SEC_ROI
    ub_roi = UB_ROI
    score_roi = SCORE_ROI
    damage_data_roi = DAMAGE_DATA_ROI
    detail_report_roi = DETAIL_REPORT_ROI
    crown_data_roi = CROWN_DATA_ROI

    ub_data = []
    ub_data_value = []
    time_data = []
    characters_find = []

    tmp_damage = []
    total_damage = False

    cap_interval = int(frame_rate * n)
    skip_frame = 5 * cap_interval

    for i in range(frame_count):  # 動画の秒数を取得し、回す
        ret = video.grab()
        if ret is False:
            break

        # VIEWからのスレッド一時停止
        if ANALYZE_STATUS is ANALYZE_PENDING:
            while True:
                if ANALYZE_STATUS is ANALYZE_PENDING:
                    tm.sleep(0.2)
                else:
                    break

        # VIEWからのスレッド停止
        if ANALYZE_STATUS is ANALYZE_STOP:
            break

        if i % cap_interval is 0:
            if ((i - ub_interval) > skip_frame) or (ub_interval == 0):
                ret, original_frame = video.read()

                if ret is False:
                    break
                work_frame = edit_frame(original_frame)

                if menu_check is False:
                    menu_check, menu_loc = analyze_item_frame(work_frame, MENU_DATA, MENU_ROI)
                    if menu_check is True:
                        loc_diff = np.array(MENU_LOC) - np.array(menu_loc)
                        roi_diff = (loc_diff[0], loc_diff[1], loc_diff[0], loc_diff[1])
                        min_roi = np.array(MIN_ROI) - np.array(roi_diff)
                        tensec_roi = np.array(TEN_SEC_ROI) - np.array(roi_diff)
                        onesec_roi = np.array(ONE_SEC_ROI) - np.array(roi_diff)
                        ub_roi = np.array(UB_ROI) - np.array(roi_diff)
                        score_roi = np.array(SCORE_ROI) - np.array(roi_diff)
                        damage_data_roi = np.array(DAMAGE_DATA_ROI) - np.array(roi_diff)
                        detail_report_roi = np.array(DETAIL_REPORT_ROI) - np.array(roi_diff)
                        crown_data_roi = np.array(CROWN_DATA_ROI) - np.array(roi_diff)

                        analyze_anna_icon_frame(work_frame, CHARACTER_ICON_ROI, characters_find)

                        # 検出状況を初期化
                        tmp_damage = []
                        total_damage = False

                    elif total_damage is not False:
                        # ダメージレポート表示中
                        # 王冠の有無を確認
                        ret = analyze_item_frame(work_frame, CROWN_DATA, crown_data_roi)[0]

                        if ret is True:
                            # ダメージレポートの有無を確認
                            ret = analyze_item_frame(work_frame, DETAIL_REPORT_DATA, detail_report_roi)[0]

                            if ret is True:
                                # ダメージレポートが開かれている場合
                                # 検出時の画像をviewに渡す
                                send_capture_frame(original_frame, self)
                                save_capture_frame(original_frame, result_file_dir, "damage_report")

                                # 検出状況を初期化
                                tmp_damage = []
                                total_damage = False

                else:
                    # UB 検出処理
                    # 時間を判定
                    time_min = analyze_timer_frame(work_frame, min_roi, 2, time_min)
                    time_sec10 = analyze_timer_frame(work_frame, tensec_roi, 6, time_sec10)
                    time_sec1 = analyze_timer_frame(work_frame, onesec_roi, 10, time_sec1)

                    # UB文字を判定
                    ub_result = analyze_ub_frame(work_frame, ub_roi, time_min, time_sec10, time_sec1,
                                                 ub_data, ub_data_value, characters_find, self)

                    if ub_result is FOUND:
                        ub_interval = i
                        # 検出時の画像をviewに渡す
                        send_capture_frame(original_frame, self)
                        save_txt(ub_data[-1], result_file_dir)

                    # 総ダメージ検出処理
                    # スコア表示の有無を確認
                    ret = analyze_item_frame(work_frame, SCORE_DATA, score_roi)[0]

                    if ret is True:
                        # 総ダメージ解析
                        ret = analyze_damage_frame(original_frame, damage_data_roi, tmp_damage)

                        if ret is True:
                            # 総ダメージ表示が存在の場合
                            total_damage = "総ダメージ " + ''.join(tmp_damage)
                            print(total_damage)
                            input_txt_damage = "\n\n" + total_damage + "\n"
                            save_txt(input_txt_damage, result_file_dir)
                            view.set_ub_text(self, input_txt_damage)
                            # 検出時の画像をviewに渡す
                            send_capture_frame(original_frame, self)
                            save_capture_frame(original_frame, result_file_dir, "total_damage")

                            # 検出状況を初期化
                            menu_check = False

    video.release()

    # TLに対する後処理
    debuff_value = ac.make_ub_value_list(ub_data_value, characters_find)

    time_result = tm.time() - start_time
    time_data.append("動画時間 : {:.3f}".format(frame_count / frame_rate) + "  sec")
    print("動画時間 : {:.3f}".format(frame_count / frame_rate) + "  sec")
    time_data.append("処理時間 : {:.3f}".format(time_result) + "  sec")
    print("処理時間 : {:.3f}".format(time_result) + "  sec")

    # VIEWへの終了通知
    if ANALYZE_STATUS is not ANALYZE_STOP:
        view.set_result_frame(self)

    return ub_data, time_data, total_damage, debuff_value, NO_ERROR


def edit_frame(frame):
    # フレームを二値化
    work_frame = frame

    work_frame = cv2.resize(work_frame, dsize=(FRAME_COLS, FRAME_ROWS))
    work_frame = cv2.cvtColor(work_frame, cv2.COLOR_RGB2GRAY)
    work_frame = cv2.threshold(work_frame, FRAME_THRESH, 255, cv2.THRESH_BINARY)[1]
    work_frame = cv2.bitwise_not(work_frame)

    return work_frame


def analyze_ub_frame(frame, roi, time_min, time_10sec, time_sec, ub_data, ub_data_value, characters_find, self):
    # ub文字位置を解析　5キャラ見つけている場合は探索対象を5キャラにする
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    characters_num = len(CHARACTERS)
    ub_result = NOT_FOUND
    tmp_character = [False, 0]
    tmp_value = UB_THRESH

    # 全キャラ探索
    for j in range(characters_num):
        result_temp = cv2.matchTemplate(analyze_frame, CHARACTERS_DATA[j], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
        if max_val > tmp_value:
            # 前回取得したキャラクターより一致率が高い場合
            tmp_character = [CHARACTERS[j], j]
            tmp_value = max_val
            ub_result = FOUND

    if ub_result is FOUND:
        # UB データに対する処理
        ub_data.append(time_min + ":" + time_10sec + time_sec + "\t" + tmp_character[0])
        view.set_ub_text(self, time_min + ":" + time_10sec + time_sec + "\t" + tmp_character[0])
        ub_data_value.extend([[int(int(time_min) * 60 + int(time_10sec) * 10 + int(time_sec)), tmp_character[1]]])
        if tmp_character[1] not in characters_find:
            characters_find.append(tmp_character[1])

    return ub_result


def analyze_timer_frame(frame, roi, data_num, time_data):
    # 時刻位置の探索
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    tmp_number = time_data
    tmp_value = TIMER_THRESH

    for j in range(data_num):
        result_temp = cv2.matchTemplate(analyze_frame, SEC_DATA[j], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
        if max_val > tmp_value:
            tmp_number = NUMBERS[j]
            tmp_value = max_val

    return tmp_number


def analyze_item_frame(frame, data, roi):
    # 単一アイテムの有無を判定 単一の画像モデルの判定に使う
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    result_temp = cv2.matchTemplate(analyze_frame, data, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
    if max_val > ITEM_THRESH:
        return True, max_loc

    return False, None


def analyze_damage_frame(frame, roi, damage):
    # 総ダメージを判定
    analyze_frame = cv2.resize(frame, dsize=(FRAME_COLS, FRAME_ROWS))
    analyze_frame = analyze_frame[roi[1]:roi[3], roi[0]:roi[2]]

    analyze_frame = cv2.cvtColor(analyze_frame, cv2.COLOR_BGR2HSV)
    analyze_frame = cv2.inRange(analyze_frame, np.array([10, 120, 160]), np.array([40, 255, 255]))

    # 数値の存在位置特定
    find_list = find_damage_loc(analyze_frame)

    # 探索結果を座標の昇順で並べ替え
    find_list.sort()

    # 総ダメージ情報作成
    ret = make_damage_list(find_list, damage)

    return ret


def find_damage_loc(frame):
    # 数値の存在位置特定
    find_list = []
    number_num = len(NUMBERS)

    for i in range(number_num):
        # テンプレートマッチングで座標取得
        result_temp = cv2.matchTemplate(frame, DAMAGE_DATA[i], cv2.TM_CCOEFF_NORMED)
        loc = np.where(result_temp > DAMAGE_THRESH)[1]
        result_temp = result_temp.T

        # 重複を削除し昇順に並び替える
        loc = list(set(loc))
        sort_loc = sorted(np.sort(loc))

        loc_number = len(sort_loc)

        # 座標に応じて数値を格納する
        if loc_number == 0:
            # 未発見の場合
            find_list.append([0, i, 0])
        elif loc_number == 1:
            # 座標一つの場合
            find_list.append([sort_loc[0], i, max(result_temp[sort_loc[0]])])
        else:
            # 座標複数の場合
            temp_loc = sort_loc[0]
            temp_value = max(result_temp[sort_loc[0]])

            # +5の範囲の値を同一視する
            for j in range(loc_number - 1):

                if sort_loc[j + 1] > sort_loc[j] + 5:
                    # 異なる座標の場合
                    find_list.append([temp_loc, i, temp_value])
                    temp_loc = sort_loc[j + 1]
                    temp_value = max(result_temp[sort_loc[j + 1]])

                else:
                    # +5の範囲の座標の場合
                    value_after = max(result_temp[sort_loc[j + 1]])

                    if value_after > temp_value:
                        # 直近探査結果より精度が上ならば更新する
                        temp_loc = sort_loc[j + 1]
                        temp_value = value_after

            find_list.append([temp_loc, i, temp_value])

    return find_list


def make_damage_list(find_list, damage):
    # 総ダメージ情報作成
    ret = False
    temp_list = []

    list_num = len(find_list)

    # 探索結果の中で同一座標の被りを除外する
    for i in range(list_num):
        if find_list[i][0] != 0:
            if not temp_list:
                temp_list = find_list[i]
                ret = True

            if find_list[i][0] > temp_list[0] + 5:
                # 異なる座標の場合
                damage.append(str(temp_list[1]))
                temp_list = find_list[i]

            else:
                # +5の範囲の座標の場合
                if find_list[i][2] > temp_list[2]:
                    # 直近探査結果より精度が上ならば更新する
                    temp_list = find_list[i]

    if ret is True:
        damage.append(str(temp_list[1]))

    return ret


def analyze_anna_icon_frame(frame, roi, characters_find):
    # アンナの有無を確認　UBを使わない場合があるため
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    icon_num = len(ICON_DATA)

    for j in range(icon_num):
        result_temp = cv2.matchTemplate(analyze_frame, ICON_DATA[j], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
        if max_val > ICON_THRESH:
            characters_find.append(CHARACTERS.index('アンナ'))

    return


def main():
    root = tkinter.Tk()
    root.withdraw()

    file_type = [("", "*")]

    initial_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

    if file == "":
        print("No video source found")
        sys.exit(1)

    movie_path = file

    time_line, time_data, total_damage, debuff_value, status = analyze_movie(movie_path)

    if status is NO_ERROR:
        print("解析成功")
    else:
        print("申し訳ありません。非対応の解像度です。16:9の解像度に対応しています。")


# view用定義
FILE = 0
YOUTUBE = 1


# view用関数
def movie_check(movie_path):
    video = cv2.VideoCapture(movie_path)

    frame_count = int(video.get(7))
    frame_rate = int(video.get(5))

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    x, y = get_aspect_ratio(frame_width, frame_height)

    try:
        video_type = FRAME_RESOLUTION.index((x, y))
    except ValueError:
        video.release()
        return ERROR_NOT_SUPPORTED, None

    if (frame_count / frame_rate) >= 600:
        video.release()
        return ERROR_TOO_LONG, None

    video.release()

    return NO_ERROR, video_type


def check_input(file_path):
    file_exist = os.path.exists(file_path)

    if file_exist is True:
        # FILE
        ext = os.path.splitext(file_path)[1]
        if ext == ".mp4":
            # 拡張子がmp4
            return True, FILE

        return False, FILE

    elif file_path.startswith("http"):
        # YOUTUBE
        ret = get_youtube_id(file_path)

        if ret is not False:
            # YOUTUBE URLとして成立
            return True, YOUTUBE

        return False, YOUTUBE

    return False, FILE


def analyze_transition_check(file_path):
    status, file_type = check_input(file_path)

    movie_path = file_path

    if status is True:
        # 入力正常時
        if file_type is FILE:
            # FILEの場合の画面遷移
            file_status = movie_check(file_path)[0]

        elif file_type is YOUTUBE:
            # Youtubeの場合の画面遷移
            movie_path, movie_name, file_status = search(file_path)

        else:
            # 本来ならば到達しないコード
            file_status = ERROR_REQUIRED_PARAM

    elif status is False:
        # 入力異常時
        if file_type is FILE:
            # FILEのPATH異常
            file_status = ERROR_CANT_GET_MOVIE

        elif file_type is YOUTUBE:
            # YoutubeのURL異常
            file_status = ERROR_BAD_URL

        else:
            # 本来ならば到達しないコード
            file_status = ERROR_REQUIRED_PARAM

    else:
        # 本来ならば到達しないコード
        file_status = ERROR_REQUIRED_PARAM

    return file_status, movie_path


def set_analyze_status_do():
    # 解析を再開させる
    global ANALYZE_STATUS

    ANALYZE_STATUS = ANALYZE_DO


def set_analyze_status_pending():
    # 解析を一時停止させる
    global ANALYZE_STATUS

    ANALYZE_STATUS = ANALYZE_PENDING


def set_analyze_status_stop():
    # 解析を停止させる
    global ANALYZE_STATUS

    ANALYZE_STATUS = ANALYZE_STOP


def send_capture_frame(frame, self):
    # 検出時の画像をviewに渡す
    capture_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    view.set_ub_capture(self, capture_frame)


def save_capture_frame(frame, path, name):
    # 検出時の画像を結果として保存する
    save_name = path + name + ".png"
    if os.path.exists(save_name):
        for i in itertools.count(1):
            save_name = "{}_{}{}".format(path + name, i, ".png")

            if not os.path.exists(save_name):
                break

    cv2.imwrite(save_name, frame)


def save_txt(txt, path):
    # UBデータをテキストに保存する
    try:
        f = open(path + "ub_timeline.txt", "a")
        f.write(str(txt) + "\n")
        f.close()
    except PermissionError:
        pass


if __name__ == "__main__":
    main()
