# -*- coding: utf-8 -*-
import os
import sys
import configparser

CONFIG_FILE = "config.ini"

SECTION1_PATH = "path"
SECTION1_1 = "movie_path"

SECTION2_SETTING = "setting"
SECTION2_1 = "image_format"
SECTION2_2 = "length_limit"

MOVIE_PATH_DEFAULT = os.path.abspath(os.path.dirname(sys.argv[0]))
IMAGE_FORMAT_DEFAULT = ".png"
LENGTH_LIMIT_DEFAULT = "True"


def create_config(init, path, image, limit):
    if init:
        movie_path = MOVIE_PATH_DEFAULT
        image_format = IMAGE_FORMAT_DEFAULT
        length_limit = LENGTH_LIMIT_DEFAULT
    else:
        movie_path = path
        image_format = image
        length_limit = limit

    config = configparser.ConfigParser()
    section1 = SECTION1_PATH
    config.add_section(section1)
    config.set(section1, SECTION1_1, movie_path)

    section2 = SECTION2_SETTING
    config.add_section(section2)
    config.set(section2, SECTION2_1, image_format)
    config.set(section2, SECTION2_2, length_limit)

    with open(CONFIG_FILE, "w") as file:
        config.write(file)


def read_config():
    movie_path = MOVIE_PATH_DEFAULT
    image_format = IMAGE_FORMAT_DEFAULT
    length_limit = LENGTH_LIMIT_DEFAULT

    if not os.path.exists(CONFIG_FILE):
        # コンフィグファイルが存在しない場合は初期化
        create_config(True, None, None, None)
    else:
        config = configparser.ConfigParser()
        config.read("config.ini")

        section1 = SECTION1_PATH
        tmp_movie_path = config.get(section1, SECTION1_1)
        if os.path.exists(tmp_movie_path):
            movie_path = tmp_movie_path

        section2 = SECTION2_SETTING
        tmp_image_format = config.get(section2, SECTION2_1)
        if tmp_image_format != IMAGE_FORMAT_DEFAULT:
            image_format = ".jpg"

        tmp_length_limit = config.get(section2, SECTION2_2)
        if tmp_length_limit != LENGTH_LIMIT_DEFAULT:
            length_limit = "False"

        create_config(False, movie_path, image_format, length_limit)

    return movie_path, image_format, length_limit
