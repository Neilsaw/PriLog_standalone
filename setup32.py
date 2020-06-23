from distutils.core import setup
import setuptools
import py2exe

option = {
    "compressed": 1,
    "optimize": 2,
    "bundle_files": 3,
}

setup(
    name="PriLog",
    author="Neilus",
    url="https://prilog.jp/",
    options={"py2exe": option},
    windows=[
        {"script": "view.py",
         "icon_resources": [(1, "./resource/image/icon.ico")],
         "dest_base": "PriLog",
         }
    ],
    zipfile="lib/library.zip",
)
