# -*- coding: utf-8 -*-
import numpy as np
import os
import time as tm
import cv2
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import sys
import urllib.parse
import characters as cd
import after_caluculation as ac

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
MENU_THRESH = 0.6
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

stream_dir = "tmp/"
if not os.path.exists(stream_dir):
    os.mkdir(stream_dir)

cache_dir = "cache/"
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


pending_dir = "pending/"
if not os.path.exists(pending_dir):
    os.mkdir(pending_dir)


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


def model_init(video_type):
    # 動画の種類ごとのモデル初期化処理
    global CHARACTERS_DATA          # キャラクター名テンプレート
    global SEC_DATA                 # 時間テンプレート
    global MENU_DATA                # MENUテンプレート
    global SCORE_DATA               # スコアテンプレート
    global DAMAGE_DATA              # ダメージ数値テンプレート
    global ICON_DATA                # アンナアイコンテンプレート

    if video_type is RESOLUTION_16_9:
        CHARACTERS_DATA = np.load("model/16_9/UB_name_16_9.npy")
        SEC_DATA = np.load("model/16_9/timer_sec_16_9.npy")
        MENU_DATA = np.load("model/16_9/menu_16_9.npy")
        SCORE_DATA = np.load("model/16_9/score_data_16_9.npy")
        DAMAGE_DATA = np.load("model/16_9/damage_data_16_9.npy")
        ICON_DATA = np.load("model/16_9/icon_data_16_9.npy")

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


def analyze_movie(movie_path):
    # 動画解析し結果をリストで返す
    start_time = tm.time()
    video = cv2.VideoCapture(movie_path)

    frame_count = int(video.get(7))  # フレーム数を取得
    frame_rate = int(video.get(5))  # フレームレート(1フレームの時間単位はミリ秒)の取得

    frame_width = int(video.get(3))  # フレームの幅
    frame_height = int(video.get(4))  # フレームの高さ

    x, y = get_aspect_ratio(frame_width, frame_height)

    try:
        video_type = FRAME_RESOLUTION.index((x, y))
    except ValueError:
        video.release()

        return None, None, None, None, ERROR_NOT_SUPPORTED

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

    ub_data = []
    ub_data_value = []
    time_data = []
    characters_find = []

    tmp_damage = []
    total_damage = False

    cap_interval = int(frame_rate * n)
    skip_frame = 5 * cap_interval

    if (frame_count / frame_rate) < 600:  # 10分未満の動画しか見ない
        for i in range(frame_count):  # 動画の秒数を取得し、回す
            ret = video.grab()
            if ret is False:
                break

            if i % cap_interval is 0:
                if ((i - ub_interval) > skip_frame) or (ub_interval == 0):
                    ret, original_frame = video.read()

                    if ret is False:
                        break
                    work_frame = edit_frame(original_frame)

                    if menu_check is False:
                        menu_check, menu_loc = analyze_menu_frame(work_frame, MENU_DATA, MENU_ROI)
                        if menu_check is True:
                            loc_diff = np.array(MENU_LOC) - np.array(menu_loc)
                            roi_diff = (loc_diff[0], loc_diff[1], loc_diff[0], loc_diff[1])
                            min_roi = np.array(MIN_ROI) - np.array(roi_diff)
                            tensec_roi = np.array(TEN_SEC_ROI) - np.array(roi_diff)
                            onesec_roi = np.array(ONE_SEC_ROI) - np.array(roi_diff)
                            ub_roi = np.array(UB_ROI) - np.array(roi_diff)
                            score_roi = np.array(SCORE_ROI) - np.array(roi_diff)
                            damage_data_roi = np.array(DAMAGE_DATA_ROI) - np.array(roi_diff)

                            analyze_anna_icon_frame(work_frame, CHARACTER_ICON_ROI, characters_find)

                    else:
                        if time_min is "1":
                            time_min = analyze_timer_frame(work_frame, min_roi, 2, time_min)

                        time_sec10 = analyze_timer_frame(work_frame, tensec_roi, 6, time_sec10)
                        time_sec1 = analyze_timer_frame(work_frame, onesec_roi, 10, time_sec1)

                        ub_result = analyze_ub_frame(work_frame, ub_roi, time_min, time_sec10, time_sec1,
                                                     ub_data, ub_data_value, characters_find)

                        if ub_result is FOUND:
                            ub_interval = i

                        # スコア表示の有無を確認
                        ret = analyze_score_frame(work_frame, SCORE_DATA, score_roi)

                        if ret is True:
                            # 総ダメージ解析
                            ret = analyze_damage_frame(original_frame, damage_data_roi, tmp_damage)

                            if ret is True:
                                total_damage = "総ダメージ " + ''.join(tmp_damage)
                                print(total_damage)

                            break

    video.release()

    # TLに対する後処理
    debuff_value = ac.make_ub_value_list(ub_data_value, characters_find)

    time_result = tm.time() - start_time
    time_data.append("動画時間 : {:.3f}".format(frame_count / frame_rate) + "  sec")
    print("動画時間 : {:.3f}".format(frame_count / frame_rate) + "  sec")
    time_data.append("処理時間 : {:.3f}".format(time_result) + "  sec")
    print("処理時間 : {:.3f}".format(time_result) + "  sec")

    return ub_data, time_data, total_damage, debuff_value, NO_ERROR


def edit_frame(frame):
    # フレームを二値化
    work_frame = frame

    work_frame = cv2.resize(work_frame, dsize=(FRAME_COLS, FRAME_ROWS))
    work_frame = cv2.cvtColor(work_frame, cv2.COLOR_RGB2GRAY)
    work_frame = cv2.threshold(work_frame, FRAME_THRESH, 255, cv2.THRESH_BINARY)[1]
    work_frame = cv2.bitwise_not(work_frame)

    return work_frame


def analyze_ub_frame(frame, roi, time_min, time_10sec, time_sec, ub_data, ub_data_value, characters_find):
    # ub文字位置を解析　5キャラ見つけている場合は探索対象を5キャラにする
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    characters_num = len(CHARACTERS)
    ub_result = NOT_FOUND
    tmp_character = [False, 0]
    tmp_value = UB_THRESH

    if len(characters_find) < 5:
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
            ub_data.append(time_min + ":" + time_10sec + time_sec + " " + tmp_character[0])
            print(time_min + ":" + time_10sec + time_sec + " " + tmp_character[0])
            ub_data_value.extend([[int(int(time_min) * 60 + int(time_10sec) * 10 + int(time_sec)), tmp_character[1]]])
            if tmp_character[1] not in characters_find:
                characters_find.append(tmp_character[1])
    else:
        for j in range(5):
            # 5キャラのみの探索
            result_temp = cv2.matchTemplate(analyze_frame, CHARACTERS_DATA[characters_find[j]], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
            if max_val > tmp_value:
                # 前回取得したキャラクターより一致率が高い場合
                tmp_character = [CHARACTERS[characters_find[j]], characters_find[j]]
                tmp_value = max_val
                ub_result = FOUND

        if ub_result is FOUND:
            ub_data.append(time_min + ":" + time_10sec + time_sec + " " + tmp_character[0])
            print(time_min + ":" + time_10sec + time_sec + " " + tmp_character[0])
            ub_data_value.extend([[int(int(time_min) * 60 + int(time_10sec) * 10 + int(time_sec)), tmp_character[1]]])

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


def analyze_menu_frame(frame, menu, roi):
    # menuの有無を確認し開始判定に用いる
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    result_temp = cv2.matchTemplate(analyze_frame, menu, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
    if max_val > MENU_THRESH:
        return True, max_loc

    return False, None


def analyze_score_frame(frame, score, roi):
    # scoreの有無を確認し終了判定に用いる
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    result_temp = cv2.matchTemplate(analyze_frame, score, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
    if max_val > MENU_THRESH:
        return True

    return False


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


if __name__ == "__main__":
    main()
