#!/bin/sh
pyinstaller.exe --collect-all ytmusicapi --collect-all requests --add-binary 'yt-dlp.exe:.' --onefile ytmusic-dl.py
