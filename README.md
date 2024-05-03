# Minimal-Fetch Version 1.0 BETA

Minimal fetch is a more aesthetically pleasing system fetching tool written in Python!
It is still heavily in beta but it is at a stage where I'm ready to share.

## What it actually looks like
<img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-08.png" align="center" width="600px"/>
 
<details>
  <summary>More logos: </summary>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-08_1.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-09.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-10.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-10_1.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-10_2.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-11.png" align="center" width="600px"/>
  <br></br>

  <img src="https://github.com/ToxicWaveHD/Minimal-Fetch/blob/main/prev/2024-04-30_21-11_1.png" align="center" width="600px"/>
  <br></br>
</details>

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

## Planned for version 2.0
**Yes that's right 1.1 BETA is moving to 2.0 because I felt the update was packed full of the necessary features before the final release**
Although version 1.0 has only recently been released 1.1 has already been planned and is just around the corner
The 1.1 beta should include:

1. Significantly faster loading times. **DONE and pending**
2. A custom info grabber **DONE and pending**
3. Removed Neofetch and Psutil dependency **DONE and pending**
4. A few more logos including but probably not limited to Voidlinux, ZorinOS, Opensuse and LinuxMint
5. Neater and more modular code **DONE and pending**

6. Fix script breaking without GPU **DONE and pending**
7. Fix "dat" recall from unknown distros

Any improvements, features or new logos would be very welcome :)
