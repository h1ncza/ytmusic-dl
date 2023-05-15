# ytmusic-dl
This is a simple program to download premium quality albums, EPs and singles with complete metadata from youtube music.

### Requirements
This program depends on `ffmpeg` framework, which you need to download from your GNU/Linux distribution repositories.
Additionally, build script requires `wget` downloader and `pip` (the package installer for Python).

If you use an **Arch Linux** based distribution run:
`sudo pacman -S ffmpeg wget python-pip`

On **Debian** and **Ubuntu** derivatives:
`sudo apt install -y wget ffmpeg python3-pip`

On **Fedora** and derivatives:
`sudo dnf -y install ffmpeg python3-pip wget`

### Installation instructions
1. Clone the repository.
2. `cd` into the project directory
3. Run the `build.sh` bash script.
4. Script will provide you with single binary executable in the `bin` subdirectory.
### Usage
This is a fully interactive command line application. Just run `ytmusic-dl` from terminal and follow prompts.
