#!/bin/bash

echo "---------------------------------------"
echo "|              duckiebot              |"
echo "|   TENDA W311MA Wifi Dongle Driver   |"
echo "|            Installation             |"
echo "|                START                |"
echo "---------------------------------------"
echo ""

echo ""
echo "-------------------------------------------------"
echo "| Step 1 | Edit /etc/modules configuration file |"
echo "-------------------------------------------------"
sudo bash -c 'echo "rt2870sta" >> /etc/modules'
echo ""

echo ""
echo "-------------------------------------------------------------------"
echo "| Step 2 | Edit /etc/modprobe.d/blacklist.conf configuration file |"
echo "-------------------------------------------------------------------"
sudo bash -c 'echo "" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "#---------------------------------------------------------------------------" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "# Blacklist below drivers to ensure rt2870sta TENDA_W311MA is working fine." >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "#---------------------------------------------------------------------------" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2800pci" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2800lib" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2x00usb" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2x00pci" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2x00lib" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt2860sta" >> /etc/modprobe.d/blacklist.conf'
sudo bash -c 'echo "blacklist rt3090sta" >> /etc/modprobe.d/blacklist.conf'
echo ""

echo ""
echo "------------------------------------------------------------"
echo "| Step 3 | Edit /etc/network/interfaces configuration file |"
echo "------------------------------------------------------------"
sudo bash -c 'echo "" >> /etc/network/interfaces'
sudo bash -c 'echo "#-----------------------------------------------" >> /etc/network/interfaces'
sudo bash -c 'echo "# Wifi Setting - ra0 - TENDA_W311MA Wifi Dongle" >> /etc/network/interfaces'
sudo bash -c 'echo "#-----------------------------------------------" >> /etc/network/interfaces'
sudo bash -c 'echo "allow-hotplug ra0" >> /etc/network/interfaces'
sudo bash -c 'echo "iface ra0 inet manual" >> /etc/network/interfaces'
sudo bash -c 'echo "wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf" >> /etc/network/interfaces'
sudo bash -c 'echo "iface default inet dhcp" >> /etc/network/interfaces'
echo ""

echo ""
echo "----------------------------------------------------------------------------"
echo "| Step 4 | Edit /etc/wpa_supplicant/wpa_supplicant.conf configuration file |"
echo "----------------------------------------------------------------------------"
sudo bash -c 'echo "" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "#------------------------------------------------------------" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "# Define prefered Wifi Network to be connected automatically" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "#------------------------------------------------------------" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    ssid=\"RACECAR\"" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    scan_ssid=1" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    psk=\"59165916\"" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    priority=9" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    ssid=\"hoggietown\"" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    scan_ssid=1" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    psk=\"59095909\"" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "    priority=8" >> /etc/wpa_supplicant/wpa_supplicant.conf'
sudo bash -c 'echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf'
echo ""

echo ""
echo "---------------------------------------"
echo "| Step 5 | Download TENDA wifi driver |"
echo "---------------------------------------"
cd ~/
mkdir Downloads
cd ~/Downloads
wget https://www.dropbox.com/s/42rh3qznynz4hai/TENDA_W311MA.tar.xz
echo ""

echo ""
echo "--------------------------------------"
echo "| Step 6 | Extract TENDA wifi driver |"
echo "--------------------------------------"
cd ~/Downloads
tar xf TENDA_W311MA.tar.xz
echo ""

echo ""
echo "-------------------------------------------"
echo "| Step 7 | Reinstalling the linux-headers |"
echo "-------------------------------------------"
cd /lib/modules
sudo apt-get remove 3.18.0-20-rpi2 -y
sudo apt-get remove 3.18.0-25-rpi2 -y
sudo apt-get install 3.18.0-20-rpi2 -y
echo ""

echo ""
echo "------------------------------------------"
echo "| Step 8 | Install the TENDA wifi driver |"
echo "------------------------------------------"
cd ~/Downloads/TENDA_W311MA
sudo make
sudo make install
echo ""

echo ""
echo "---------------------------------------"
echo "|              duckiebot              |"
echo "|   TENDA W311MA Wifi Dongle Driver   |"
echo "|            Installation             |"
echo "|               FINISH                |"
echo "---------------------------------------"
echo ""

echo ""
echo "---------------------------------------------------------"
echo "| Step 9 | Reboot Raspberry Pi 2 and Wifi will be ready |"
echo "---------------------------------------------------------"
sleep 5s
sudo reboot

