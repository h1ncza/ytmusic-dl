#!/bin/sh
pyinstaller.exe --collect-all ytmusicapi --collect-all requests --collect-all colorama--add-binary 'yt-dlp.exe:.' --onefile ytmusic-dl-color.py
