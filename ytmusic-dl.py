#!/usr/bin/python

import ytmusicapi
import os
import subprocess
import requests
import sys

basePath = os.path.join(os.path.expanduser("~"), "music")
ytdlArgs = [
    "yt-dlp",
    "-x",
    "--embed-metadata",
    "--embed-thumbnail",
    "--audio-quality",
    "0",
    "--format",
    "best",
    "--audio-format",
    "mp3",
    "--parse-metadata",
    "playlist_index:%(track_number)s",
    "--parse-metadata",
    ":(?P<webpage_url>)",
    "--parse-metadata",
    ":(?P<synopsis>)",
    "--parse-metadata",
    ":(?P<description>)",
    "-o",
]


def estabilishConnection():
    global ytm
    ytm = ytmusicapi.YTMusic()


def findingArtist():
    try:
        searchResult = ytm.search(
            sys.argv[1],
            filter="artists",
            ignore_spelling=False,
        )
    except IndexError:
        print("usage: ytmusic-dl.py [artist]")
    except UnboundLocalError:
        print("usage: ytmusic-dl.py [artist]")

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
    try:
        albums_browseId = ytm.get_artist(artistIdFound)["albums"]["browseId"]
        if type(albums_browseId) == str:
            albums_params = ytm.get_artist(artistIdFound)["albums"]["params"]
            albumList = ytm.get_artist_albums(albums_browseId, albums_params)
        else:
            albumList = ytm.get_artist(artistIdFound)["albums"]["results"]

    except Exception as e:
        print(e)

    print(len(albumList), " ALBUMS found in database.")
    for i in albumList:
        print("[", albumList.index(i) + 1, "]", "->", i["title"], i["year"])

    while True:
        aans1 = input(
            "\nTo download album, input corresponding number and press enter, or A+ENTER to download ALL albums.\n To skip to singles download input S and confirm choice with Enter.\n Exit program at any time by pressing CTRL+C\n> "
        )
        if aans1 in ("S", "s"):
            break
        if aans1 in ("A", "a"):
            for i in albumList:
                playList = ytm.get_album(i["browseId"])["audioPlaylistId"]
                url = "https://music.youtube.com/playlist?list=" + playList
                targetDir = (
                    basePath
                    + os.sep
                    + artistName
                    + os.sep
                    + artistName
                    + " "
                    + i["title"]
                    + " "
                    + i["year"]
                    + os.sep
                )
                os.makedirs(targetDir, exist_ok=True)
                print("Downloading ", i["title"])
                argS = ytdlArgs + [
                    str(targetDir + "%(playlist_index)s. %(title)s.%(ext)s"),
                    url,
                ]
                subprocess.run(argS)
            break
        elif aans1.isdecimal() and int(aans1) in range(1, (len(albumList) + 1)):
            chAlb = int(aans1) - 1
            for i in albumList:
                if albumList.index(i) == chAlb:
                    playList = ytm.get_album(i["browseId"])["audioPlaylistId"]
                    url = "https://music.youtube.com/playlist?list=" + playList
                    targetDir = (
                        basePath
                        + os.sep
                        + artistName
                        + os.sep
                        + artistName
                        + " "
                        + i["title"]
                        + " "
                        + i["year"]
                        + os.sep
                    )
                    os.makedirs(targetDir, exist_ok=True)
                    print("Downloading ", i["title"])
                    argS = ytdlArgs + [
                        str(targetDir + "%(playlist_index)s. %(title)s.%(ext)s"),
                        url,
                    ]
                    subprocess.run(argS)
            continue
        else:
            print("Invalid input!")
            continue


try:
    estabilishConnection()
    findingArtist()
    choosingAlbums()
except KeyboardInterrupt:
    print("\nExiting program")
except requests.exceptions.RequestException as e:
    print("You have to be connected to internet for this program to work.")
except Exception as e:
    print(e)
