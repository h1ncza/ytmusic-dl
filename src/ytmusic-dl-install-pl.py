import ytmusicapi
import os
import subprocess
import requests
import sys
from colorama import Fore, Back, Style

ytdPath = sys._MEIPASS + os.sep + 'yt-dlp-bin'
if os.path.exists(os.path.expanduser('~') + os.sep + 'music'):
    basePath = os.path.join(os.path.expanduser('~'), 'music')
else:
    basePath = os.path.join(os.path.expanduser('~'), 'Music')

ytdlArgs = [ ytdPath, '-x', '--embed-metadata', '--embed-thumbnail', '--audio-quality', '0', '--format', 'best', '--audio-format', 'mp3', '--parse-metadata', 'playlist_index:%(track_number)s', '--parse-metadata', ':(?P<webpage_url>)', '--parse-metadata', ':(?P<synopsis>)', '--parse-metadata', ':(?P<description>)','-o']

def estabilishConnection():
    global ytm
    ytm = ytmusicapi.YTMusic()

def findingArtist():
    print(Fore.RED + "\nWYJDŹ Z PROGRAMU NACISKAJĄC CTRL+C, CTRL+Z ALBO CTRL+D W KAŻDEJ CHWILI!")
    while True:
        print(Fore.GREEN)
        try:
            searchResult = ytm.search(input(
                "\nSzukaj wykonawcy: "), filter='artists', ignore_spelling=False)
        except Exception as e:
            print(Fore.RED)
            print(e, '\n')
            continue

        if searchResult == []:
            print(Fore.RED + '\nPrzykro mi, ale nie znalazłam żadnych wykonawców o tym pseudonimie :(\nSpróbuj jeszcze raz.\n')
            continue

        else:
            while True:
                print(Fore.GREEN)
                print('\nZnalazłam następującego artystę: ',
                      searchResult[0]['artist'])
                print(Fore.CYAN + '\nDescription: ', ytm.get_artist(
                    searchResult[0]['browseId'])['description'])
                ans = input(Fore.GREEN + '\nWpisz Y i potwierdź klawiszem ENTER, żeby przejść do płyt tego wykonawcy, lub N żeby ponownie przeszukać bazę danych.\n>')
                if ans not in ('Y', 'y', 'N', 'n'):
                    print(Fore.RED + '\nProszę odpowiedz Y lub N.\n')
                    continue
                elif ans in ('y', 'Y'):
                    global artistIdFound
                    artistIdFound = searchResult[0]['browseId']
                    global artistName
                    artistName = ytm.get_artist(artistIdFound)['name']
                    print(Fore.GREEN + '\nPrzechodzimy do płyt: ', artistName, '\n')
                    return
                elif ans in ('n', 'N'):
                    break


def choosingAlbums():
    try:
        albumList = ytm.get_artist(artistIdFound)['albums']['results']
        print(Fore.BLUE)
        print(len(albumList), ' płyt długogrających dostępnych w bazie danych.')
        while True:
            for i in albumList:
                print(Fore.MAGENTA)
                print('[', albumList.index(i) + 1, ']', '->', i['title'], i['year'])

            aans1 = input(Fore.GREEN + '\nAby zapisać album na dysku, wpisz jego numer na liście powyżej i potwierdź klawiszem ENTER. Odpowiedz A, żeby zapisać WSZYSTKIE albumy.\nAby przejść do SINGLI tego artysty wpisz S.\n Wyjdź z programu wpisując Q\n> ')
            if aans1 in ('Q', 'q'):
                os._exit(0)
            if aans1 in ('S', 's'):
                break
            if aans1 in ('A', 'a'):
                for i in albumList:
                    playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                    url = 'https://music.youtube.com/playlist?list=' + playList
                    targetDir = basePath + os.sep + artistName + os.sep + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                    os.makedirs(targetDir, exist_ok=True)
                    print(Fore.GREEN + 'Zapisuję: ', i['title'])
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
                        print(Fore.GREEN + 'Zapisuję: ', i['title'])
                        argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                        subprocess.run(argS)
                continue
            else:
                print(Fore.RED +'Nieprawidłowy wybór!')
                continue


    except KeyError as ke:
        print(Fore.RED + 'Nie znaleziono żadnych płyt długogrających w bazie danych.')

def downloadingSingles():
    try:
        singleList = ytm.get_artist(artistIdFound)['singles']['results']
        print(Fore.BLUE)
        print(len(singleList), ' singli znalezionych w bazie danych.')
        while True:
            for i in singleList:
                print(Fore.MAGENTA)
                print('[', singleList.index(i) + 1, ']', '->', i['title'], i['year'])

            sans1 = input(Fore.GREEN + '\nAby zapisać singiel, wpisz jego numer na liście powyżej i potwierdź klawiszem ENTER. Wpisz A aby zapisać wszystkie lub Q aby opuścić program.\n> ')
            if sans1 in ('Q', 'q'):
                break
            if sans1 in ('A', 'a'):
                for i in singleList:
                    playList = ytm.get_album(i['browseId'])['audioPlaylistId']
                    url = 'https://music.youtube.com/playlist?list=' + playList
                    targetDir = basePath + os.sep + artistName + os.sep + 'SINGLES' + os.sep + 'SP ' + artistName + ' ' +i['title'] + ' ' + i['year'] + os.sep
                    os.makedirs(targetDir, exist_ok=True)
                    print(Fore.GREEN + 'Zapisuję ', i['title'])
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
                        print(Fore.GREEN + 'Zapisuję ', i['title'])
                        argS = ytdlArgs + [str(targetDir + '%(playlist_index)s. %(title)s.%(ext)s'), url]
                        subprocess.run(argS)
                continue
            else:
                print(Fore.RED + 'Nieprawidłowy wybór!')
                continue


    except KeyError as ke:
        print(Fore.RED + 'Nie znaleziono żadnych płyt długogrających w bazie danych.')


try:
    estabilishConnection()
    findingArtist()
    choosingAlbums()
    downloadingSingles()
except KeyboardInterrupt:
    print(Fore.MAGENTA + '\nDo zobaczenia, buziaki!')
except requests.exceptions.RequestException as e:
    print(Fore.RED + 'Program wymaga połączenia z internetem.')
