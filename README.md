# Minimal-Fetch Version 1.0

Minimal fetch is a more aesthetically pleasing system fetching tool!

## What it actually looks like
<img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev.png" align="center" width="600px"/>


STILL A WIP DO NOT EXPECT IT TO BE FLAWLESS  (Please do report any issues you find)

## Install with
```
$ git clone https://github.com/ToxicWaveHD/Minimal-Fetch.git
$ cd Minimal-Fetch/
$ chmod +x make
$ ./make
```
And simply run with
```
$ mfetch
```
Note: this requires the dependencies: `neofetch`, `python3`, `pillow` and `psutil`

You can install the dependencies with

For Ubuntu/Debian-based: ```$ sudo apt install neofetch python3 python3-pillow python3-psutil```

For Arch-based: ```$ sudo pacman -S neofetch python3 python-pillow python-psutil```


## Config howto
WARNING FAIL-SAFES HAVE YET TO BE ADDED IF YOU ENCOUNTER ANY ERRORS WHILE RUNNING AFTER EDITING THE CONFIG REVERT ANY CHANGES MADE

The config is located at ```~/.config/mfetch/options```

True/False statements MUST be capitalised

The os logo has to be a directory in ```/usr/share/mfetch/logos```

## Todo
1. Make a custom information grabber (rather than have the neofetch dependency 💀)
2. Add more customization options
3. Maybe upload it to AUR if I decide to finish it.

Any improvements, features or new logos would be very welcome :)
