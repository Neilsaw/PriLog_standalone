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

SECTION3_POSITION = "position"
SECTION3_1 = "window_x_position"
SECTION3_2 = "window_y_position"

MOVIE_PATH_DEFAULT = os.path.abspath(os.path.dirname(sys.argv[0]))
IMAGE_FORMAT_DEFAULT = ".png"
IMAGE_FORMAT_ANOTHER = ".jpg"
LENGTH_LIMIT_DEFAULT = "True"
LENGTH_LIMIT_ANOTHER = "False"
WINDOW_POSITION_X_DEFAULT = "200"
WINDOW_POSITION_Y_DEFAULT = "200"


def create_config(init, path, image, limit, position_x, position_y):
    if init:
        movie_path = MOVIE_PATH_DEFAULT
        image_format = IMAGE_FORMAT_DEFAULT
        length_limit = LENGTH_LIMIT_DEFAULT
        window_x_position = WINDOW_POSITION_X_DEFAULT
        window_y_position = WINDOW_POSITION_Y_DEFAULT
    else:
        movie_path = path
        image_format = image
        length_limit = limit
        window_x_position = position_x
        window_y_position = position_y

    config = configparser.ConfigParser()
    section1 = SECTION1_PATH
    config.add_section(section1)
    config.set(section1, SECTION1_1, movie_path)

    section2 = SECTION2_SETTING
    config.add_section(section2)
    config.set(section2, SECTION2_1, image_format)
    config.set(section2, SECTION2_2, length_limit)

    section3 = SECTION3_POSITION
    config.add_section(section3)
    config.set(section3, SECTION3_1, window_x_position)
    config.set(section3, SECTION3_2, window_y_position)

    with open(CONFIG_FILE, "w") as file:
        config.write(file)


def read_config():
    movie_path = MOVIE_PATH_DEFAULT
    image_format = IMAGE_FORMAT_DEFAULT
    length_limit = LENGTH_LIMIT_DEFAULT
    window_x_position = WINDOW_POSITION_X_DEFAULT
    window_y_position = WINDOW_POSITION_X_DEFAULT

    if not os.path.exists(CONFIG_FILE):
        # コンフィグファイルが存在しない場合は初期化
        create_config(True, None, None, None, None, None)
    else:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        section1 = SECTION1_PATH
        tmp_movie_path = config.get(section1, SECTION1_1)
        if os.path.exists(tmp_movie_path):
            movie_path = tmp_movie_path

        section2 = SECTION2_SETTING
        tmp_image_format = config.get(section2, SECTION2_1)
        if tmp_image_format == IMAGE_FORMAT_ANOTHER:
            image_format = IMAGE_FORMAT_ANOTHER

        tmp_length_limit = config.get(section2, SECTION2_2)
        if tmp_length_limit == LENGTH_LIMIT_ANOTHER:
            length_limit = LENGTH_LIMIT_ANOTHER

        section3 = SECTION3_POSITION
        tmp_window_x_position = config.get(section3, SECTION3_1)
        tmp_window_y_position = config.get(section3, SECTION3_2)
        if tmp_window_x_position.isdecimal() and tmp_window_y_position.isdecimal():
            window_x_position = tmp_window_x_position
            window_y_position = tmp_window_y_position

        create_config(False, movie_path, image_format, length_limit, window_x_position, window_y_position)

    return movie_path, image_format, length_limit, window_x_position, window_y_position
