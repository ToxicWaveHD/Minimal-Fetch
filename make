#!/bin/bash
sudo chmod +x /usr/bin/mfetch

sudo mkdir /usr/share/mfetch
mkdir ~/.config/mfetch/
mkdir ~/.cache/mfetch/

sudo cp usr-bin/* /usr/bin/
sudo cp -r usr-share-mfetch/* /usr/share/mfetch
cp home-config-mfetch/* ~/.config/mfetch/
cp -r home-cache/* ~/.cache/mfetch/
