from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    'resources': ['ffmpeg/'],
    'plist': {
        'CFBundleName': 'MP3Converter',
        'CFBundleDisplayName': 'MP3Converter',
        'CFBundleIdentifier': 'com.yourname.mp3converter',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
