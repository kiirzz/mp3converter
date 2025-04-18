from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    'resources': ['ffmpeg/'],  # Đóng gói thư mục ffmpeg vào app
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
