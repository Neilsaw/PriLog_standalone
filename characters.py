# -*- coding: utf-8 -*-

# キャラクターレベル 2020/12/22 現在
LEVEL = 184

# キャラクター名一覧(mask)
characters_name_mask = [
    "アオイ",
    "アオイ(編入生)",
    "アカリ",
    "アカリ(エンジェル)",
    "アキノ",
    "アキノ(☆6以降)",
    "アキノ(クリスマス)",
    "アヤネ",
    "アヤネ(☆6以降)",
    "アヤネ(クリスマス)",
    "アユミ",
    "アユミ(ワンダー)",
    "アリサ",
    "アン",
    "アンナ",
    "アンナ(サマー)",
    "イオ",
    "イオ(☆6以降)",
    "イオ(サマー)",
    "イノリ",
    "イリヤ",
    "イリヤ(クリスマス)",
    "ウヅキ(デレマス)",
    "エミリア",
    "エリコ",
    "エリコ(バレンタイン)",
    "カオリ",
    "カオリ(サマー)",
    "カスミ",
    "カスミ(マジカル)",
    "カヤ",
    "キャル",
    "キャル(☆6以降)",
    "キャル(サマー)",
    "キャル(ニューイヤー)",
    "キョウカ",
    "キョウカ(ハロウィン)",
    "クウカ",
    "クウカ(オーエド)",
    "クリスティーナ",
    "クリスティーナ(クリスマス)",
    "クルミ",
    "クルミ(クリスマス)",
    "グレア",
    "クロエ",
    "コッコロ",
    "コッコロ(☆6以降)",
    "コッコロ(サマー)",
    "コッコロ(ニューイヤー)",
    "コッコロ(プリンセス)",
    "サレン",
    "サレン(☆6以降)",
    "サレン(サマー)",
    "サレン(クリスマス)",
    "ジータ",
    "シオリ",
    "シオリ(マジカル)",
    "シズル",
    "シズル(☆6以降)",
    "シズル(バレンタイン)",
    "シノブ",
    "シノブ(ハロウィン)",
    "ジュン",
    "ジュン(サマー)",
    "スズナ",
    "スズナ(☆6以降)",
    "スズナ(サマー)",
    "スズメ",
    "スズメ(サマー)",
    "スズメ(ニューイヤー)",
    "タマキ",
    "タマキ(☆6以降)",
    "タマキ(サマー)",
    "チエル",
    "チカ",
    "チカ(クリスマス)",
    "ツムギ",
    "ツムギ(ハロウィン)",
    "トモ",
    "トモ(マジカル)",
    "ナナカ",
    "ナナカ(サマー)",
    "ニノン",
    "ニノン(☆6以降)",
    "ニノン(オーエド)",
    "ネネカ",
    "ノゾミ",
    "ノゾミ(クリスマス)",
    "ハツネ",
    "ハツネ(☆6以降)",
    "ハツネ(サマー)",
    "ヒヨリ",
    "ヒヨリ(☆6以降)",
    "ヒヨリ(ニューイヤー)",
    "ペコリーヌ",
    "ペコリーヌ(☆6以降)",
    "ペコリーヌ(サマー)",
    "ペコリーヌ(プリンセス)",
    "マコト",
    "マコト(サマー)",
    "マツリ",
    "マツリ(ハロウィン)",
    "マヒル",
    "マヒル(☆6以降)",
    "マヒル(レンジャー)",
    "マホ",
    "マホ(☆6以降)",
    "マホ(サマー)",
    "ミオ(デレマス)",
    "ミサキ",
    "ミサキ(ハロウィン)",
    "ミサト",
    "ミサト(サマー)",
    "ミソギ",
    "ミソギ(ハロウィン)",
    "ミツキ",
    "ミフユ",
    "ミフユ(☆6以降)",
    "ミフユ(サマー)",
    "ミミ",
    "ミミ(ハロウィン)",
    "ミヤコ",
    "ミヤコ(ハロウィン)",
    "ムイミ",
    "モニカ",
    "モニカ(マジカル)",
    "ユイ",
    "ユイ(☆6以降)",
    "ユイ(ニューイヤー)",
    "ユイ(プリンセス)",
    "ユカリ",
    "ユカリ(☆6以降)",
    "ユカリ(クリスマス)",
    "ユキ",
    "ユニ",
    "ヨリ",
    "ヨリ(エンジェル)",
    "ラビリスタ",
    "ラム",
    "リノ",
    "リノ(☆6以降)",
    "リノ(ワンダー)",
    "リマ",
    "リマ(☆6以降)",
    "リン",
    "リン(レンジャー)",
    "リン(デレマス)",
    "ルゥ",
    "ルカ",
    "ルカ(サマー)",
    "ルナ",
    "レイ",
    "レイ(☆6以降)",
    "レイ(ニューイヤー)",
    "レイ(ハロウィン)",
    "レム",
]

# キャラクター名一覧
characters_name = [
    "アオイ",
    "アオイ(編入生)",
    "アカリ",
    "アカリ(エンジェル)",
    "アキノ",
    "アキノ",      # ☆6以降
    "アキノ(クリスマス)",
    "アヤネ",
    "アヤネ",      # ☆6以降
    "アヤネ(クリスマス)",
    "アユミ",
    "アユミ(ワンダー)",
    "アリサ",
    "アン",
    "アンナ",
    "アンナ(サマー)",
    "イオ",
    "イオ",      # ☆6以降
    "イオ(サマー)",
    "イノリ",
    "イリヤ",
    "イリヤ(クリスマス)",
    "ウヅキ(デレマス)",
    "エミリア",
    "エリコ",
    "エリコ(バレンタイン)",
    "カオリ",
    "カオリ(サマー)",
    "カスミ",
    "カスミ(マジカル)",
    "カヤ",
    "キャル",
    "キャル",      # ☆6以降
    "キャル(サマー)",
    "キャル(ニューイヤー)",
    "キョウカ",
    "キョウカ(ハロウィン)",
    "クウカ",
    "クウカ(オーエド)",
    "クリスティーナ",
    "クリスティーナ(クリスマス)",
    "クルミ",
    "クルミ(クリスマス)",
    "グレア",
    "クロエ",
    "コッコロ",
    "コッコロ",      # ☆6以降
    "コッコロ(サマー)",
    "コッコロ(ニューイヤー)",
    "コッコロ(プリンセス)",
    "サレン",
    "サレン",      # ☆6以降
    "サレン(サマー)",
    "サレン(クリスマス)",
    "ジータ",
    "シオリ",
    "シオリ(マジカル)",
    "シズル",
    "シズル",      # ☆6以降
    "シズル(バレンタイン)",
    "シノブ",
    "シノブ(ハロウィン)",
    "ジュン",
    "ジュン(サマー)",
    "スズナ",
    "スズナ",      # ☆6以降
    "スズナ(サマー)",
    "スズメ",
    "スズメ(サマー)",
    "スズメ(ニューイヤー)",
    "タマキ",
    "タマキ",      # ☆6以降
    "タマキ(サマー)",
    "チエル",
    "チカ",
    "チカ(クリスマス)",
    "ツムギ",
    "ツムギ(ハロウィン)",
    "トモ",
    "トモ(マジカル)",
    "ナナカ",
    "ナナカ(サマー)",
    "ニノン",
    "ニノン",      # ☆6以降
    "ニノン(オーエド)",
    "ネネカ",
    "ノゾミ",
    "ノゾミ(クリスマス)",
    "ハツネ",
    "ハツネ",      # ☆6以降
    "ハツネ(サマー)",
    "ヒヨリ",
    "ヒヨリ",      # ☆6以降
    "ヒヨリ(ニューイヤー)",
    "ペコリーヌ",
    "ペコリーヌ",      # ☆6以降
    "ペコリーヌ(サマー)",
    "ペコリーヌ(プリンセス)",
    "マコト",
    "マコト(サマー)",
    "マツリ",
    "マツリ(ハロウィン)",
    "マヒル",
    "マヒル",      # ☆6以降
    "マヒル(レンジャー)",
    "マホ",
    "マホ",      # ☆6以降
    "マホ(サマー)",
    "ミオ(デレマス)",
    "ミサキ",
    "ミサキ(ハロウィン)",
    "ミサト",
    "ミサト(サマー)",
    "ミソギ",
    "ミソギ(ハロウィン)",
    "ミツキ",
    "ミフユ",
    "ミフユ",      # ☆6以降
    "ミフユ(サマー)",
    "ミミ",
    "ミミ(ハロウィン)",
    "ミヤコ",
    "ミヤコ(ハロウィン)",
    "ムイミ",
    "モニカ",
    "モニカ(マジカル)",
    "ユイ",
    "ユイ",      # ☆6以降
    "ユイ(ニューイヤー)",
    "ユイ(プリンセス)",
    "ユカリ",
    "ユカリ",      # ☆6以降
    "ユカリ(クリスマス)",
    "ユキ",
    "ユニ",
    "ヨリ",
    "ヨリ(エンジェル)",
    "ラビリスタ",
    "ラム",
    "リノ",
    "リノ",      # ☆6以降
    "リノ(ワンダー)",
    "リマ",
    "リマ",      # ☆6以降
    "リン",
    "リン(レンジャー)",
    "リン(デレマス)",
    "ルゥ",
    "ルカ",
    "ルカ(サマー)",
    "ルナ",
    "レイ",
    "レイ",      # ☆6以降
    "レイ(ニューイヤー)",
    "レイ(ハロウィン)",
    "レム",
]

# 攻撃属性
PHYSICAL = 0
MAGICAL = 1
PHYSICAL_AND_MAGICAL = 2
EMPTY = 3

# テーブル格納位置
UB = 0
UB_ALTER = 1
S1 = 2
S1_ALTER = 3
S2 = 4
S2_ALTER = 5

# UB属性テーブル　キャラクターの攻撃属性に一致させる
ub_type_table = [
    # アオイ
    PHYSICAL,
    # アオイ(編入生)
    PHYSICAL,
    # アカリ
    MAGICAL,
    # アカリ(エンジェル)
    MAGICAL,
    # アキノ
    PHYSICAL,
    # アキノ(☆6以降)
    PHYSICAL,
    # アキノ(クリスマス)
    PHYSICAL,
    # アヤネ
    PHYSICAL,
    # アヤネ(☆6以降)
    PHYSICAL,
    # アヤネ(クリスマス)
    PHYSICAL,
    # アユミ
    PHYSICAL,
    # アユミ(ワンダー)
    PHYSICAL,
    # アリサ
    PHYSICAL,
    # アン
    MAGICAL,
    # アンナ
    MAGICAL,
    # アンナ(サマー)
    MAGICAL,
    # イオ
    MAGICAL,
    # イオ(☆6以降)
    MAGICAL,
    # イオ(サマー)
    MAGICAL,
    # イノリ
    PHYSICAL,
    # イリヤ
    MAGICAL,
    # イリヤ(クリスマス)
    MAGICAL,
    # ウヅキ(デレマス)
    PHYSICAL,
    # エミリア
    MAGICAL,
    # エリコ
    PHYSICAL,
    # エリコ(バレンタイン)
    PHYSICAL,
    # カオリ
    PHYSICAL,
    # カオリ(サマー)
    PHYSICAL,
    # カスミ
    MAGICAL,
    # カスミ(マジカル)
    MAGICAL,
    # カヤ
    PHYSICAL,
    # キャル
    MAGICAL,
    # キャル(☆6以降)
    MAGICAL,
    # キャル(サマー)
    MAGICAL,
    # キャル(ニューイヤー)
    MAGICAL,
    # キョウカ
    MAGICAL,
    # キョウカ(ハロウィン)
    MAGICAL,
    # クウカ
    PHYSICAL,
    # クウカ(オーエド)
    MAGICAL,
    # クリスティーナ
    PHYSICAL,
    # クリスティーナ(クリスマス)
    PHYSICAL,
    # クルミ
    PHYSICAL,
    # クルミ(クリスマス)
    PHYSICAL,
    # グレア
    MAGICAL,
    # クロエ
    PHYSICAL,
    # コッコロ
    PHYSICAL,
    # コッコロ(☆6以降)
    PHYSICAL,
    # コッコロ(サマー)
    PHYSICAL,
    # コッコロ(ニューイヤー)
    PHYSICAL,
    # コッコロ(プリンセス)
    PHYSICAL,
    # サレン
    PHYSICAL,
    # サレン(☆6以降)
    PHYSICAL,
    # サレン(サマー)
    PHYSICAL,
    # サレン(クリスマス)
    PHYSICAL,
    # ジータ
    PHYSICAL,
    # シオリ
    PHYSICAL,
    # シオリ(マジカル)
    PHYSICAL,
    # シズル
    PHYSICAL,
    # シズル(☆6以降)
    PHYSICAL,
    # シズル(バレンタイン)
    PHYSICAL,
    # シノブ
    PHYSICAL,
    # シノブ(ハロウィン)
    PHYSICAL,
    # ジュン
    PHYSICAL,
    # ジュン(サマー)
    PHYSICAL,
    # スズナ
    PHYSICAL,
    # スズナ(☆6以降)
    PHYSICAL,
    # スズナ(サマー)
    PHYSICAL,
    # スズメ
    MAGICAL,
    # スズメ(サマー)
    MAGICAL,
    # スズメ(ニューイヤー)
    MAGICAL,
    # タマキ
    PHYSICAL,
    # タマキ(☆6以降)
    PHYSICAL,
    # タマキ(サマー)
    PHYSICAL,
    # チエル
    PHYSICAL,
    # チカ
    MAGICAL,
    # チカ(クリスマス)
    MAGICAL,
    # ツムギ
    PHYSICAL,
    # ツムギ(ハロウィン)
    PHYSICAL,
    # トモ
    PHYSICAL,
    # トモ(マジカル)
    MAGICAL,
    # ナナカ
    MAGICAL,
    # ナナカ(サマー)
    MAGICAL,
    # ニノン
    PHYSICAL,
    # ニノン(☆6以降)
    PHYSICAL,
    # ニノン(オーエド)
    PHYSICAL,
    # ネネカ
    MAGICAL,
    # ノゾミ
    PHYSICAL,
    # ノゾミ(クリスマス)
    PHYSICAL,
    # ハツネ
    MAGICAL,
    # ハツネ(☆6以降)
    MAGICAL,
    # ハツネ(サマー)
    MAGICAL,
    # ヒヨリ
    PHYSICAL,
    # ヒヨリ(☆6以降)
    PHYSICAL,
    # ヒヨリ(ニューイヤー)
    PHYSICAL,
    # ペコリーヌ
    PHYSICAL,
    # ペコリーヌ(☆6以降)
    PHYSICAL,
    # ペコリーヌ(サマー)
    PHYSICAL,
    # ペコリーヌ(プリンセス)
    PHYSICAL,
    # マコト
    PHYSICAL,
    # マコト(サマー)
    PHYSICAL,
    # マツリ
    PHYSICAL,
    # マツリ(ハロウィン)
    PHYSICAL,
    # マヒル
    PHYSICAL,
    # マヒル(☆6以降)
    PHYSICAL,
    # マヒル(レンジャー)
    PHYSICAL,
    # マホ
    MAGICAL,
    # マホ(☆6以降)
    MAGICAL,
    # マホ(サマー)
    MAGICAL,
    # ミオ(デレマス)
    MAGICAL,
    # ミサキ
    MAGICAL,
    # ミサキ(ハロウィン)
    MAGICAL,
    # ミサト
    MAGICAL,
    # ミサト(サマー)
    MAGICAL,
    # ミソギ
    PHYSICAL,
    # ミソギ(ハロウィン)
    PHYSICAL,
    # ミツキ
    PHYSICAL,
    # ミフユ
    PHYSICAL,
    # ミフユ(☆6以降)
    PHYSICAL,
    # ミフユ(サマー)
    PHYSICAL,
    # ミミ
    PHYSICAL,
    # ミミ(ハロウィン)
    PHYSICAL,
    # ミヤコ
    PHYSICAL,
    # ミヤコ(ハロウィン)
    PHYSICAL,
    # ムイミ
    PHYSICAL,
    # モニカ
    PHYSICAL,
    # モニカ(マジカル)
    PHYSICAL,
    # ユイ
    MAGICAL,
    # ユイ(☆6以降)
    MAGICAL,
    # ユイ(ニューイヤー)
    MAGICAL,
    # ユイ(プリンセス)
    MAGICAL,
    # ユカリ
    PHYSICAL,
    # ユカリ(☆6以降)
    PHYSICAL,
    # ユカリ(クリスマス)
    PHYSICAL,
    # ユキ
    MAGICAL,
    # ユニ
    MAGICAL,
    # ヨリ
    MAGICAL,
    # ヨリ(エンジェル)
    MAGICAL,
    # ラビリスタ
    PHYSICAL,
    # ラム
    MAGICAL,
    # リノ
    PHYSICAL,
    # リノ(☆6以降)
    PHYSICAL,
    # リノ(ワンダー)
    PHYSICAL,
    # リマ
    PHYSICAL,
    # リマ(☆6以降)
    PHYSICAL,
    # リン
    PHYSICAL,
    # リン(レンジャー)
    PHYSICAL,
    # リン(デレマス)
    PHYSICAL,
    # ルゥ
    MAGICAL,
    # ルカ
    PHYSICAL,
    # ルカ(サマー)
    PHYSICAL,
    # ルナ
    MAGICAL,
    # レイ
    PHYSICAL,
    # レイ(☆6以降)
    PHYSICAL,
    # レイ(ニューイヤー)
    PHYSICAL,
    # レイ(ハロウィン)
    PHYSICAL,
    # レム
    PHYSICAL,
]

# UB時間基本 1 = 1fps (1 sec = 30fps) 分からないやつはこれ
UB_TIME_DEFAULT = 120

# UB時間テーブル　1 = 1fps (1 sec = 30fps) UB検出から完了までの時間
ub_time_table = [
    # アオイ
    50,
    # アオイ(編入生)
    130,
    # アカリ
    70,
    # アカリ(エンジェル)
    160,
    # アキノ
    UB_TIME_DEFAULT,
    # アキノ(☆6以降)
    220,
    # アキノ(クリスマス)
    200,
    # アヤネ
    UB_TIME_DEFAULT,
    # アヤネ(☆6以降)
    220,
    # アヤネ(クリスマス)
    120,
    # アユミ
    110,
    # アユミ(ワンダー)
    130,
    # アリサ
    90,
    # アン
    130,
    # アンナ
    160,
    # アンナ(サマー)
    140,
    # イオ
    UB_TIME_DEFAULT,
    # イオ(☆6以降)
    180,
    # イオ(サマー)
    110,
    # イノリ
    90,
    # イリヤ
    100,
    # イリヤ(クリスマス)
    120,
    # ウヅキ(デレマス)
    110,
    # エミリア
    90,
    # エリコ
    110,
    # エリコ(バレンタイン)
    180,
    # カオリ
    70,
    # カオリ(サマー)
    110,
    # カスミ
    90,
    # カスミ(マジカル)
    130,
    # カヤ
    80,
    # キャル
    UB_TIME_DEFAULT,
    # キャル(☆6以降)
    130,
    # キャル(サマー)
    60,
    # キャル(ニューイヤー)
    140,
    # キョウカ
    90,
    # キョウカ(ハロウィン)
    150,
    # クウカ
    50,
    # クウカ(オーエド)
    150,
    # クリスティーナ
    110,
    # クリスティーナ(クリスマス)
    120,
    # クルミ
    50,
    # クルミ(クリスマス)
    100,
    # グレア
    100,
    # クロエ
    120,
    # コッコロ
    UB_TIME_DEFAULT,
    # コッコロ(☆6以降)
    160,
    # コッコロ(サマー)
    70,
    # コッコロ(ニューイヤー)
    150,
    # コッコロ(プリンセス)
    180,
    # サレン
    UB_TIME_DEFAULT,
    # サレン(☆6以降)
    140,
    # サレン(サマー)
    150,
    # サレン(クリスマス)
    80,
    # ジータ
    120,
    # シオリ
    70,
    # シオリ(マジカル)
    130,
    # シズル
    UB_TIME_DEFAULT,
    # シズル(☆6以降)
    200,
    # シズル(バレンタイン)
    100,
    # シノブ
    40,
    # シノブ(ハロウィン)
    140,
    # ジュン
    40,
    # ジュン(サマー)
    110,
    # スズナ
    70,
    # スズナ(☆6以降)
    220,
    # スズナ(サマー)
    200,
    # スズメ
    110,
    # スズメ(サマー)
    80,
    # スズメ(ニューイヤー)
    160,
    # タマキ
    UB_TIME_DEFAULT,
    # タマキ(☆6以降)
    180,
    # タマキ(サマー)
    110,
    # チエル
    160,
    # チカ
    80,
    # チカ(クリスマス)
    60,
    # ツムギ
    70,
    # ツムギ(ハロウィン)
    110,
    # トモ
    70,
    # トモ(マジカル)
    110,
    # ナナカ
    120,
    # ナナカ(サマー)
    120,
    # ニノン
    120,
    # ニノン(☆6以降)
    130,
    # ニノン(オーエド)
    80,
    # ネネカ
    120,
    # ノゾミ
    130,
    # ノゾミ(クリスマス)
    180,
    # ハツネ
    UB_TIME_DEFAULT,
    # ハツネ(☆6以降)
    190,
    # ハツネ(サマー)
    90,
    # ヒヨリ
    UB_TIME_DEFAULT,
    # ヒヨリ(☆6以降)
    190,
    # ヒヨリ(ニューイヤー)
    120,
    # ペコリーヌ
    UB_TIME_DEFAULT,
    # ペコリーヌ(☆6以降)
    140,
    # ペコリーヌ(サマー)
    70,
    # ペコリーヌ(プリンセス)
    170,
    # マコト
    60,
    # マコト(サマー)
    150,
    # マツリ
    110,
    # マツリ(ハロウィン)
    120,
    # マヒル
    90,
    # マヒル(☆6以降)
    200,
    # マヒル(レンジャー)
    70,
    # マホ
    UB_TIME_DEFAULT,
    # マホ(☆6以降)
    240,
    # マホ(サマー)
    140,
    # ミオ(デレマス)
    160,
    # ミサキ
    110,
    # ミサキ(ハロウィン)
    90,
    # ミサト
    120,
    # ミサト(サマー)
    110,
    # ミソギ
    120,
    # ミソギ(ハロウィン)
    120,
    # ミツキ
    100,
    # ミフユ
    UB_TIME_DEFAULT,
    # ミフユ(☆6以降)
    230,
    # ミフユ(サマー)
    100,
    # ミミ
    120,
    # ミミ(ハロウィン)
    150,
    # ミヤコ
    90,
    # ミヤコ(ハロウィン)
    130,
    # ムイミ
    160,
    # モニカ
    90,
    # モニカ(マジカル)
    100,
    # ユイ
    UB_TIME_DEFAULT,
    # ユイ(☆6以降)
    200,
    # ユイ(ニューイヤー)
    120,
    # ユイ(プリンセス)
    170,
    # ユカリ
    UB_TIME_DEFAULT,
    # ユカリ(☆6以降)
    210,
    # ユカリ(クリスマス)
    110,
    # ユキ
    110,
    # ユニ
    110,
    # ヨリ
    90,
    # ヨリ(エンジェル)
    140,
    # ラビリスタ
    120,
    # ラム
    120,
    # リノ
    UB_TIME_DEFAULT,
    # リノ(☆6以降)
    240,
    # リノ(ワンダー)
    140,
    # リマ
    UB_TIME_DEFAULT,
    # リマ(☆6以降)
    150,
    # リン
    110,
    # リン(レンジャー)
    120,
    # リン(デレマス)
    120,
    # ルゥ
    110,
    # ルカ
    90,
    # ルカ(サマー)
    120,
    # ルナ
    100,
    # レイ
    UB_TIME_DEFAULT,
    # レイ(☆6以降)
    160,
    # レイ(ニューイヤー)
    110,
    # レイ(ハロウィン)
    130,
    # レム
    140,
]