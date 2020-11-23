# -*- coding: utf-8 -*-
import numpy as np
import os
from pytube import YouTube
from pytube import extract
from pytube import exceptions
import time as tm
import datetime
import cv2
import itertools
import myconfig
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

# SPEED icon template
SPEED_DATA = []

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
SPEED_ICON_ROI = (0, 0, 0, 0)
MENU_LOC = (0, 0)

FRAME_THRESH = 200
SPEED_ICON_THRESH = 240

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
SPEED_THRESH = 0.4

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
ERROR_NOT_HD = 7

# キャッシュ格納数
CACHE_NUM = 5

# VIEWとのIF用
ANALYZE_DO = 0
ANALYZE_PENDING = 1
ANALYZE_STOP = 2
ANALYZE_END = 3

# VIEWとのIF用
MOVIE_DO = 0
MOVIE_STOP = 1

ENEMY_UB = "――――敵UB――――"

ANALYZE_STATUS = ANALYZE_DO
MOVIE_GET_STATUS = MOVIE_DO

SAVE_IMAGE_FORMAT = ".png"
MOVIE_LENGTH_LIMIT = "True"
ENEMY_UB_VIEW = "True"

RESULT_FILE_DIR = None

stream_dir = "tmp/"
if not os.path.exists(stream_dir):
    os.mkdir(stream_dir)

result_dir = "result/"
if not os.path.exists(result_dir):
    os.mkdir(result_dir)


def load_name():
    # json からキャラクター名読み込み
    global CHARACTERS

    json = myconfig.load_character_json()

    if not json:
        myconfig.create_character_json()
        return

    count = len(CHARACTERS)

    for i in range(count):
        CHARACTERS[i] = json[CHARACTERS[i]]


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
    global SPEED_DATA  # SPEED icon template

    if video_type is RESOLUTION_16_9:
        CHARACTERS_DATA = np.load("./resource/model/16_9/UB_name_16_9.npy")
        SEC_DATA = np.load("./resource/model/16_9/timer_sec_16_9.npy")
        MENU_DATA = np.load("./resource/model/16_9/menu_16_9.npy")
        SCORE_DATA = np.load("./resource/model/16_9/score_data_16_9.npy")
        DAMAGE_DATA = np.load("./resource/model/16_9/damage_data_16_9.npy")
        ICON_DATA = np.load("./resource/model/16_9/icon_data_16_9.npy")
        DETAIL_REPORT_DATA = np.load("./resource/model/16_9/detail_report_16_9.npy")
        CROWN_DATA = np.load("./resource/model/16_9/crown_16_9.npy")
        SPEED_DATA = np.load("./resource/model/16_9/speed_data_16_9.npy")

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
    global SPEED_ICON_ROI  # speed icon analyze roi

    global MENU_LOC              # MENU　ボタン　正位置
    global FRAME_THRESH          # 解析用下限値
    global SPEED_ICON_THRESH  # frame color thresh value
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
        SPEED_ICON_ROI = (1180, 616, 1271, 707)
        MENU_LOC = (63, 23)
        FRAME_THRESH = 200
        SPEED_ICON_THRESH = 240
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

    if MOVIE_LENGTH_LIMIT == "True":
        movie_length = yt.length
        if int(movie_length) > 600:
            return None, None, ERROR_TOO_LONG

    stream = yt.streams.get_by_itag(22)
    if stream is None:
        return None, None, ERROR_NOT_HD

    movie_title = stream.title
    movie_name = tm.time()
    movie_path = stream.download(stream_dir, str(movie_name))

    file_status = movie_check(movie_path)[0]

    return movie_path, movie_title, file_status


def analyze_movie(movie_path, file_type, self):
    global RESULT_FILE_DIR

    # 動画解析し結果をリストで返す
    start_time = tm.time()

    result_name = datetime.datetime.fromtimestamp(start_time)
    result_name = result_name.strftime('%Y-%m-%d_%H-%M-%S')

    result_file_dir = result_dir + result_name + "/"
    if not os.path.exists(result_file_dir):
        os.mkdir(result_file_dir)

    RESULT_FILE_DIR = result_file_dir
    # 動画の確認
    video_type = movie_check(movie_path)[1]

    video = cv2.VideoCapture(movie_path)

    frame_count = int(video.get(7))  # フレーム数を取得
    frame_rate = int(video.get(5))  # フレームレート(1フレームの時間単位はミリ秒)の取得

    load_name()
    model_init(video_type)
    roi_init(video_type)

    n = 0.34  # n秒ごと*

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
    speed_roi = SPEED_ICON_ROI

    ub_data = []
    ub_data_value = []
    time_data = []
    characters_find = []

    tmp_damage = []
    total_damage = False

    cap_interval = int(frame_rate * n)
    past_time = 90
    time_count = 0
    find_id = -1
    find_count = 0

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

        # VIEWからのスレッド途中完了
        if ANALYZE_STATUS is ANALYZE_END:
            break

        if i % cap_interval is 0:
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
                    speed_roi = np.array(SPEED_ICON_ROI) - np.array(roi_diff)

                    analyze_anna_icon_frame(work_frame, CHARACTER_ICON_ROI, characters_find)

                    # 検出状況を初期化
                    tmp_damage = []
                    total_damage = False
                    past_time = 90
                    time_count = 0
                    find_id = -1
                    find_count = 0

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
                            past_time = 90
                            time_count = 0
                            find_id = -1
                            find_count = 0

            else:
                # UB 検出処理
                # 時間を判定
                time_min = analyze_timer_frame(work_frame, min_roi, 2, time_min)
                time_sec10 = analyze_timer_frame(work_frame, tensec_roi, 6, time_sec10)
                time_sec1 = analyze_timer_frame(work_frame, onesec_roi, 10, time_sec1)

                find_time = time_min + ":" + time_sec10 + time_sec1
                now_time, is_same_time = time_check(time_min, time_sec10, time_sec1, past_time)

                is_normal_speed = analyze_speed(original_frame, speed_roi)

                if is_same_time:
                    #  count up if normal speed, neither, reset count
                    if is_normal_speed:
                        time_count += 1
                    else:
                        time_count = 0
                else:
                    time_count = 0
                    past_time = now_time

                if time_count >= 0:
                    # check friendly ub
                    ub_result, find_id, find_count = analyze_ub_frame(work_frame, ub_roi, time_min, time_sec10,
                                                                      time_sec1,
                                                                      ub_data, ub_data_value,
                                                                      characters_find, find_id, find_count, self)

                    if ub_result is FOUND:
                        # 検出時の画像をviewに渡す
                        send_capture_frame(original_frame, self)
                        save_txt(ub_data[-1], result_file_dir)
                        time_count = update_count(frame_rate, find_id, cap_interval)

                    elif ENEMY_UB_VIEW == "True" and is_normal_speed:
                        # check enemy ub
                        analyze_enemy_ub(time_count, work_frame, find_time, ub_data, original_frame, result_file_dir, self)

                # 総ダメージ検出処理
                # スコア表示の有無を確認
                ret = analyze_item_frame(work_frame, SCORE_DATA, score_roi)[0]

                if ret is True:
                    # 総ダメージ解析
                    ret = analyze_damage_frame(original_frame, damage_data_roi, tmp_damage)

                    if ret is True:
                        # 総ダメージ表示が存在の場合
                        total_damage = "総ダメージ\n" + ''.join(tmp_damage)
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
    time_data.append("処理時間 : {:.3f}".format(time_result) + "  sec")

    # YOUTUBEから取得した動画の場合削除
    if file_type is YOUTUBE:
        clear_path(movie_path)

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


def analyze_ub_frame(frame, roi, time_min, time_10sec, time_sec, ub_data, ub_data_value,
                     characters_find, past_id, past_count, self):
    # ub文字位置を解析　5キャラ見つけている場合は探索対象を5キャラにする
    analyze_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

    characters_num = len(CHARACTERS)
    ub_result = NOT_FOUND
    find_id = -1
    find_count = 0
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
            find_id = j

    if ub_result is FOUND:
        # UB データに対する処理
        tl = time_min + ":" + time_10sec + time_sec + "\t" + tmp_character[0]
        if len(ub_data) != 0 and ub_data[-1] == tl:
            # same time, same ub ignore
            find_count = past_count + 1
            return NOT_FOUND, find_id, find_count

        if find_id == past_id and past_count < 5:
            # in 50f time, same ub ignore
            find_count = past_count + 1
            return NOT_FOUND, find_id, find_count

        ub_data.append(tl)
        view.set_ub_text(self, time_min + ":" + time_10sec + time_sec + "\t" + tmp_character[0])
        ub_data_value.extend([[int(int(time_min) * 60 + int(time_10sec) * 10 + int(time_sec)), tmp_character[1]]])
        if tmp_character[1] not in characters_find:
            characters_find.append(tmp_character[1])

        return FOUND, find_id, find_count

    return NOT_FOUND, find_id, find_count


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


def time_check(time_min, time_sec10, time_sec1, past_time):
    now_time = int(time_min) * 60 + int(time_sec10) * 10 + int(time_sec1)
    if past_time != now_time:
        return now_time, False
    else:
        return now_time, True


def update_count(frame_rate, find_id, cap_interval):
    """update count after friendly ub


    Args
        frame_rate (int): movie fps
        find_id (int): find character id
        cap_interval (int): read frame interval


    Returns
        time_count (int): ub interval

    """
    return -1 * (frame_rate / 30) * int(cd.ub_time_table[find_id] / cap_interval)


def check_enemy_ub(time_count):
    """check enemy ub


    Args
        time_count (int): count up after ub


    Returns
        is_enemy_ub (boolean): enemy ub existence

    """
    if time_count > 9:
        return True
    else:
        return False


def analyze_enemy_ub(time_count, work_frame, find_time, ub_data, original_frame, result_file_dir, self):
    # check enemy ub
    is_enemy_ub = check_enemy_ub(time_count)
    if is_enemy_ub:
        menu_check = analyze_item_frame(work_frame, MENU_DATA, MENU_ROI)[0]
        if menu_check:
            tl = find_time + "\t" + ENEMY_UB
            if len(ub_data) != 0 and ub_data[-1] != tl:
                # same time, same ub ignore
                ub_data.append(tl)
                view.set_ub_text(self, tl)
                send_capture_frame(original_frame, self)
                save_txt(ub_data[-1], result_file_dir)


def analyze_speed(frame, roi):
    """analyze speed

    check speed icon for get speed

    Args
        frame (ndarray): original frame from movie
        roi (list): search roi

    Returns
        ret (boolean): find or not find speed up (x2 / x4) icon inactive


    """
    analyze_frame = cv2.resize(frame, dsize=(FRAME_COLS, FRAME_ROWS))
    analyze_frame = analyze_frame[roi[1]:roi[3], roi[0]:roi[2]]

    analyze_frame = cv2.cvtColor(analyze_frame, cv2.COLOR_RGB2GRAY)
    analyze_frame = cv2.threshold(analyze_frame, SPEED_ICON_THRESH, 255, cv2.THRESH_BINARY)[1]
    analyze_frame = cv2.bitwise_not(analyze_frame)

    speed_num = len(SPEED_DATA)

    for j in range(speed_num):
        result_temp = cv2.matchTemplate(analyze_frame, SPEED_DATA[j], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_temp)
        if max_val > SPEED_THRESH:
            # find speed up (x2 / x4) icon active
            return False

    return True


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

    if MOVIE_LENGTH_LIMIT == "True":
        if (frame_count / frame_rate) >= 600:
            video.release()
            return ERROR_TOO_LONG, None

    video.release()

    return NO_ERROR, video_type


def input_check(file_path):
    file_exist = os.path.exists(file_path)

    if file_exist is True:
        # FILE
        ext = os.path.splitext(file_path)[1]
        if ext == ".mp4" or ext == ".MP4":
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


def set_error_message(file_type, status):
    e_code = "[Error-U]"
    e_message = "予期せぬエラー"

    if file_type is FILE:

        if status is ERROR_TOO_LONG:
            e_code = "[Error-F2]"
            e_message = "動画時間が長いため解析できません\n現在の設定では10分未満に対応しております(設定で変更できます)"
        elif status is ERROR_NOT_SUPPORTED:
            e_code = "[Error-F3]"
            e_message = "申し訳ありません　動画の解像度に対応しておりません\n16:9の解像度の動画をご用意頂けますと解析できます"
        elif status is ERROR_CANT_GET_MOVIE:
            e_code = "[Error-F4]"
            e_message = ".mp4動画を選択できていないようです\nフォルダアイコンから選んでみてください"
    elif file_type is YOUTUBE:

        if status is ERROR_BAD_URL:
            e_code = "[Error-Y1]"
            e_message = "YouTubeの動画を見つけることができませんでした\nURLをYouTubeの共有よりコピーしてみてください"
        elif status is ERROR_TOO_LONG:
            e_code = "[Error-Y2]"
            e_message = "動画時間が長いため解析できません\n現在の設定では10分未満に対応しております(設定で変更できます)"
        elif status is ERROR_NOT_SUPPORTED:
            e_code = "[Error-Y3]"
            e_message = "申し訳ありません　動画の解像度に対応しておりません\n16:9の解像度以外の動画は今後対応致します"
        elif status is ERROR_CANT_GET_MOVIE:
            e_code = "[Error-Y4]"
            e_message = "HD画質(720p)の動画を取得できませんでした\n繰り返し発生する場合は解析できません　申し訳ありません"
        elif status is ERROR_NOT_HD:
            e_code = "[Error-Y7]"
            e_message = "HD画質(720p)の動画を取得できませんでした\n繰り返し発生する場合は解析できません　申し訳ありません"

    error_message = e_code + "\n" + e_message

    return error_message


def analyze_transition_check(file_path, self):
    status, file_type = input_check(file_path)

    movie_path = file_path
    error_message = ""

    if status is True:
        # 入力正常時
        if file_type is FILE:
            # FILEの場合の画面遷移
            file_status = movie_check(file_path)[0]

        elif file_type is YOUTUBE:
            # Youtubeの場合の画面遷移
            view.set_waiting_movie(self)
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

    if file_status is not NO_ERROR:
        error_message = set_error_message(file_type, file_status)

    if MOVIE_GET_STATUS is MOVIE_DO:
        # 動画取得継続
        view.set_movie_action(self, file_status, movie_path, file_type, error_message)
    else:
        # 動画取得終了
        if file_type is YOUTUBE:
            # YOUTUBEから取得した動画の場合
            clear_path(movie_path)

    return


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


def set_analyze_status_end():
    # 解析を途中完了させる
    global ANALYZE_STATUS

    ANALYZE_STATUS = ANALYZE_END


def send_capture_frame(frame, self):
    # 検出時の画像をviewに渡す
    capture_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    view.set_ub_capture(self, capture_frame)


def get_result_file_dir():
    # 結果ファイルのパスを取得
    return RESULT_FILE_DIR


def set_movie_status_do():
    global MOVIE_GET_STATUS

    MOVIE_GET_STATUS = MOVIE_DO


def set_movie_status_stop():
    global MOVIE_GET_STATUS

    MOVIE_GET_STATUS = MOVIE_STOP


def set_image_format(image_format):
    # 画像保存するフォーマットを形式(png or jpg) を取得する
    global SAVE_IMAGE_FORMAT

    SAVE_IMAGE_FORMAT = image_format


def set_length_limit(length_limit):
    # 動画解析の制限時間(あり or なし) を取得する
    global MOVIE_LENGTH_LIMIT

    MOVIE_LENGTH_LIMIT = length_limit


def set_enemy_ub(enemy_ub):
    # 敵UB表示(あり or なし) を取得する
    global ENEMY_UB_VIEW

    ENEMY_UB_VIEW = enemy_ub


def save_capture_frame(frame, path, name):
    # 検出時の画像を結果として保存する
    image_format = SAVE_IMAGE_FORMAT

    if image_format != ".png":
        image_format = ".jpg"

    save_name = path + name + image_format
    if os.path.exists(save_name):
        for i in itertools.count(1):
            save_name = "{}_{}{}".format(path + name, i, image_format)

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
