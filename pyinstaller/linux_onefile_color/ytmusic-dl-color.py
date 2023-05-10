import ytmusicapi
import os
import subprocess
import requests
from colorama import Fore, Back, Style

basePath = os.path.join(os.path.expanduser('~'), 'music')
ytdlArgs = ytdlArgs = ['yt-dlp', '-x', '--embed-metadata', '--embed-thumbnail', '--audio-quality', '0', '--format', 'best', '--audio-format', 'mp3', '--parse-metadata', 'playlist_index:%(track_number)s', '--parse-metadata', ':(?P<webpage_url>)', '--parse-metadata', ':(?P<synopsis>)', '--parse-metadata', ':(?P<description>)','-o']


def estabilishConnection():
    global ytm
    ytm = ytmusicapi.YTMusic()


def findingArtist():
    print(Fore.RED + "\nPRESS CTRL+C TO EXIT PROGRAM AT ANYTIME")
    while True:
        try:
            print(Fore.GREEN)
            searchResult = ytm.search(input('\nPlease enter the artist to search for: '), filter='artists', ignore_spelling=False)
        except Exception as e:
            print(Fore.RED)
            print(e, '\n')
            continue

        if searchResult == []:
            print(Fore.RED)
            print('\nno artist matching your query found.\nPlease try again.\n')
            continue

        else:
            while True:
                print(Fore.GREEN)
                print('\nFound this artists name in the database: ',
                      searchResult[0]['artist'])
                print(Fore.CYAN)
                print('\nDescription: ', ytm.get_artist(
                    searchResult[0]['browseId'])['description'])
                ans = input('\nType Y and press enter to browse albums, or N to go back to searching database.\n>')
                if ans not in ('Y', 'y', 'N', 'n'):
                    print(Fore.RED)
                    print('\nPlease answer Y or N.\n')
                    continue
                elif ans in ('y', 'Y'):
                    global artistIdFound
                    artistIdFound = searchResult[0]['browseId']
                    global artistName
                    artistName = ytm.get_artist(artistIdFound)['name']
                    print(Fore.GREEN)
                    print('\nContinuing with: ', artistName, '\n')
                    return
                elif ans in ('n', 'N'):
                    break


def choosingAlbums():
    try:
        albumList = ytm.get_artist(artistIdFound)['albums']['results']
        print(Fore.BLUE)
        print(len(albumList), ' ALBUMS found in database.')
        while True:
            for i in albumList:
                print(Fore.MAGENTA)
                print('[', albumList.index(i) + 1, ']', '->', i['title'], i['year'])
            print(Fore.GREEN)
            aans1 = input('\nTo download album, input corresponding number and press enter, or A+ENTER to download ALL albums.\n To skip to singles download input S and confirm choice with Enter.\n Exit program at any time by pressing CTRL+C\n> ')
            if aans1 in ('S', 's'):
                break
            if aans1 in ('A', 'a'):
                for i in albumList:
                    playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                    url = 'https://music.youtube.com/playlist?list=' + playList
                    targetDir = basePath + os.sep + artistName + os.sep + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                    os.makedirs(targetDir, exist_ok=True)
                    print(Fore.GREEN)
                    print('Downloading ', i['title'])
                    argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                    subprocess.run(argS)
                break
            elif aans1.isdecimal() and int(aans1) in range(1,(len(albumList) + 1)):
                chAlb = int(aans1) - 1
                for i in albumList:
                    if albumList.index(i) == chAlb:
                        playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                        url = 'https://music.youtube.com/playlist?list=' + playList
                        targetDir = basePath + os.sep + artistName + os.sep + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                        os.makedirs(targetDir, exist_ok=True)
                        print(Fore.GREEN)
                        print('Downloading ', i['title'])
                        argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                        subprocess.run(argS)
                continue
            else:
                print(Fore.RED)
                print('Invalid input!')
                continue


    except KeyError as ke:
        print(Fore.RED)
        print('No albums found in database.')

def downloadingSingles():
    try:
        singleList = ytm.get_artist(artistIdFound)['singles']['results']
        print(Fore.BLUE)
        print(len(singleList), ' SINGLES found in database.')
        while True:
            for i in singleList:
                print(Fore.MAGENTA)
                print('[', singleList.index(i) + 1, ']', '->', i['title'], i['year'])
            print(Fore.GREEN)
            sans1 = input('\nTo download single, input corresponding number and press enter, or A+ENTER to download ALL singles.\n To exit program input Q and confirm choice with Enter.\n Exit program at any time by pressing CTRL+C\n> ')
            if sans1 in ('Q', 'q'):
                break
            if sans1 in ('A', 'a'):
                for i in singleList:
                    playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                    url = 'https://music.youtube.com/playlist?list=' + playList
                    targetDir = basePath + os.sep + artistName + os.sep + 'SINGLES' + os.sep + 'SP ' + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                    os.makedirs(targetDir, exist_ok=True)
                    print(Fore.GREEN)
                    print('Downloading ', i['title'])
                    argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                    subprocess.run(argS)
                break
            elif sans1.isdecimal() and int(sans1) in range(1,(len(singleList) + 1)):
                chAlb = int(sans1) - 1
                for i in singleList:
                    if singleList.index(i) == chAlb:
                        playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                        url = 'https://music.youtube.com/playlist?list=' + playList
                        targetDir = basePath + os.sep + artistName + os.sep + 'SINGLES' + os.sep + 'SP ' + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                        os.makedirs(targetDir, exist_ok=True)
                        print(Fore.GREEN)
                        print('Downloading ', i['title'])
                        argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                        subprocess.run(argS)
                continue
            else:
                print(Fore.RED)
                print('Invalid input!')
                continue


    except KeyError as ke:
        print(Fore.RED)
        print('No singles found in database.')

try:
    estabilishConnection()
    findingArtist()
    choosingAlbums()
    downloadingSingles()
except KeyboardInterrupt:
    print(Fore.MAGENTA)
    print('\nExiting program')
except requests.exceptions.RequestException as e:
    print(Fore.RED)
    print('You have to be connected to internet for this program to work.')
