#!/bin/sh
wine /home/czincz/.wine/drive_c/users/czincz/AppData/Local/Programs/Python/Python311/Scripts/pyinstaller.exe --collect-all ytmusicapi --collect-all requests --add-binary 'yt-dlp.exe;.' --add-binary 'ffmpeg.exe;.' --onefile ytmuzyka-dl.py
