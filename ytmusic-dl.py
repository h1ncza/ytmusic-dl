#!/usr/bin/python
import ytmusicapi
import os
import yt_dlp
import requests
import sys
import multiprocessing

# search_string = input("artist name: ")
# search_string = some_Variable
# search_string = input("ENTER SEARCH STRING: ")

search_string = sys.argv[1]
local_path = os.path.join(os.path.expanduser("~"), "music")

ydl_opts = {
    "external_downloader": {"default": "aria2c", "m3u8": "ffmpeg"},
    "extract_flat": "discard_in_playlist",
    "final_ext": "mp3",
    "format": "(bestaudio[acodec^=opus]/bestaudio)/best",
    "fragment_retries": 10,
    "ignoreerrors": True,
    "outtmpl": {
        "default": local_path + "%(playlist_index)s. %(title)s.%(ext)s",
        "pl_thumbnail": "",
    },
    "postprocessor_args": {
        "embedthumbnail+ffmpeg_o": [
            "-c:v",
            "mjpeg",
            "-vf",
            "crop='if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'",
        ]
    },
    "postprocessors": [
        {
            "actions": [
                (
                    yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                    "playlist_index",
                    "%(track_number)s",
                ),
                (
                    yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                    "",
                    "(?P<webpage_url>)",
                ),
                (
                    yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                    "",
                    "(?P<synopsis>)",
                ),
                (
                    yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                    "",
                    "(?P<description>)",
                ),
            ],
            "key": "MetadataParser",
            "when": "pre_process",
        },
        {
            "key": "FFmpegExtractAudio",
            "nopostoverwrites": False,
            "preferredcodec": "mp3",
            "preferredquality": "0",
        },
        {
            "add_chapters": True,
            "add_infojson": "if_exists",
            "add_metadata": True,
            "key": "FFmpegMetadata",
        },
        {"already_have_thumbnail": False, "key": "EmbedThumbnail"},
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
    ],
    "retries": 10,
    "writethumbnail": True,
    "simulate": False,
}

try:
    if sys.argv[2] == "debug":
        ydl_opts["simulate"] = True
except:
    pass


def estabilishConnection():
    global ytm
    ytm = ytmusicapi.YTMusic()


def findingArtist():
    try:
        searchResult = ytm.search(
            search_string,
            filter="artists",
            ignore_spelling=False,
        )
    except IndexError:
        print("usage: ytmusic-dl.py [artist]")
    except Exception as e:
        print(e)

    if searchResult == []:
        print("\nno artist matching your query found.\nPlease try again.\n")

    else:
        while True:
            print(
                "\nFound this artists name in the database: ",
                searchResult[0]["artist"],
            )
            print(
                "\nDescription: ",
                ytm.get_artist(searchResult[0]["browseId"])["description"],
            )
            ans = input(
                "\nType A and press enter to accept or any other key to exit.\n>"
            )
            if ans in ("A", "a"):
                global artistIdFound
                artistIdFound = searchResult[0]["browseId"]
                global artistName
                artistName = ytm.get_artist(artistIdFound)["name"]
                print("\nContinuing with: ", artistName, "\n")
                return
            else:
                break
                os._exit(0)


def choosingAlbums():
    playlist_urls = []
    #  = []

    try:
        playlist_browseId = ytm.get_artist(artistIdFound)["albums"]["browseId"]
        if type(playlist_browseId) == str:
            playlist_params = ytm.get_artist(artistIdFound)["albums"]["params"]
            albumList = ytm.get_artist_albums(playlist_browseId, playlist_params)
        else:
            albumList = ytm.get_artist(artistIdFound)["albums"]["results"]

    except Exception as e:
        print(e)

    print(len(albumList), " ALBUMS found in database.")
    for i in albumList:
        print("[", albumList.index(i) + 1, "]", "->", i["title"], i["year"])

    aans1 = ""

    while aans1 == "":
        aans1 = input(
            "\nTo download album, input corresponding number and press enter, or A+ENTER to download ALL albums.\n"
        )
        if aans1 in ("C", "c"):
            os._exit(0)

        elif aans1.isdecimal():
            for i in albumList:
                if int(aans1) == albumList.index(i) + 1:
                    # os.makedirs(local_path + os.sep + artistName, exist_ok=True)
                    album_dir = str(
                        local_path
                        + os.sep
                        + artistName
                        + os.sep
                        + artistName
                        + "-"
                        + i["title"]
                        + "-"
                        + i["year"]
                        + os.sep
                    )
                    URL = (
                        "https://music.youtube.com/playlist?list="
                        + ytm.get_album(i["browseId"])["audioPlaylistId"]
                    )
                    playlist_urls.append((URL, album_dir))

            return playlist_urls
            break

        elif aans1 in ("A", "a"):
            for i in albumList:
                album_dir = str(
                    local_path
                    + os.sep
                    + artistName
                    + os.sep
                    + artistName
                    + "-"
                    + i["title"]
                    + "-"
                    + i["year"]
                    + os.sep
                )
                playList = ytm.get_album(i["browseId"])["audioPlaylistId"]
                URL = "https://music.youtube.com/playlist?list=" + playList
                playlist_urls.append((URL, album_dir))

            return playlist_urls
            break

        else:
            print("Invalid input!")
            aans1 = ""
            continue


try:
    estabilishConnection()
    findingArtist()
except KeyboardInterrupt:
    print("\nExiting program")
except requests.exceptions.RequestException as e:
    print("You have to be connected to internet for this program to work.")

Albums_ = choosingAlbums()
print(Albums_)


def download_playlist(playlist, music_dir):
    new_ops = ydl_opts
    new_ops["outtmpl"]["default"] = music_dir + "%(playlist_index)s. %(title)s.%(ext)s"
    with yt_dlp.YoutubeDL(new_ops) as ydl:
        ydl.download(playlist)


with multiprocessing.Pool() as pool:
    pool.starmap(download_playlist, Albums_)
