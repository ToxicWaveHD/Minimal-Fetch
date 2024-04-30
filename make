#!/bin/bash
sudo mkdir /usr/share/mfetch
sudo mkdir /usr/share/mfetch/colour/
sudo mkdir /usr/share/mfetch/logos/
mkdir ~/.config/mfetch/
mkdir ~/.cache/mfetch/

sudo cp mfetch /usr/bin/mfetch
sudo chmod +x /usr/bin/mfetch

sudo cp -r colour/* /usr/share/mfetch/colour/
sudo cp -r logos/* /usr/share/mfetch/logos/
sudo cp cimage.py /usr/share/mfetch/
sudo cp neofetch.py /usr/share/mfetch/

cp options ~/.config/mfetch/
