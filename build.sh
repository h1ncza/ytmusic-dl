#!/bin/bash

grn=$(tput setaf 2)
red=$(tput setaf 1)
mag=$(tput setaf 5)
cya=$(tput setaf 6)
cnc=$(tput sgr0)

echo "This script requires$red pip$grn (the package installer for Python)$cnc and$red wget$grn (The non-interactive network downloader)$cnc programs."
echo "Install them from your GNU/Linux distribution repositories.$cnc"


echo "Choose your language version"
select REPLY in EN PL CANCEL; do
    case $REPLY in
        EN)
        vrs="ytmusic-dl-install-en.py"
        break;;
        PL)
        vrs="ytmusic-dl-install-pl.py"
        break;;
        CANCEL)
        exit 0;;
    esac
done


wget 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp' -O yt-dlp-bin
chmod +x yt-dlp-bin
pip install -r "./src/requirements.txt" --user
~/.local/bin/pyinstaller --distpath='./bin' --collect-all ytmusicapi --collect-all requests --collect-all colorama --add-binary 'yt-dlp-bin:.' --onefile --name ytmusic-dl "./src/"$vrs
rm -f yt-dlp-bin
rm -f *.spec
rm -r build

echo "You will find executable binary file in the$red bin$cnc directory"
echo "Remember to install$mag ffmpeg$cnc package from your distribution repositories"
