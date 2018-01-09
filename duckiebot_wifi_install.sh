#!/bin/bash

echo "---------------------"
echo "|     duckiebot     |"
echo "|   Wifi - Dongle   |"
echo "|    Installation   |"
echo "|      START        |"
echo "---------------------"
echo ""

echo ""
echo "------------------------------------------------------------"
echo "| Step 1 | Edit /etc/network/interfaces configuration file |"
echo "------------------------------------------------------------"
sudo bash -c 'echo "" >> /etc/network/interfaces'
sudo bash -c 'echo "#----------------------" >> /etc/network/interfaces'
sudo bash -c 'echo "# Wifi Setting - wlan0" >> /etc/network/interfaces'
sudo bash -c 'echo "#----------------------" >> /etc/network/interfaces'
sudo bash -c 'echo "allow-hotplug wlan0" >> /etc/network/interfaces'
sudo bash -c 'echo "iface wlan0 inet manual" >> /etc/network/interfaces'
sudo bash -c 'echo "wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf" >> /etc/network/interfaces'
sudo bash -c 'echo "iface default inet dhcp" >> /etc/network/interfaces'
echo ""

echo ""
echo "----------------------------------------------------------------------------"
echo "| Step 2 | Edit /etc/wpa_supplicant/wpa_supplicant.conf configuration file |"
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
echo "--------------------------------------------------------------------------------"
echo "| Step 3 | Remove /etc/udev/rules.d/70-persistent-net.rules configuration file |"
echo "--------------------------------------------------------------------------------"
sudo rm -rf /etc/udev/rules.d/70-persistent-net.rules # it will reproduce after reboot
echo ""

echo ""
echo "---------------------"
echo "|     duckiebot     |"
echo "|   Wifi - Dongle   |"
echo "|    Installation   |"
echo "|      FINISH       |"
echo "---------------------"
echo ""

echo ""
echo "---------------------------------------------------------"
echo "| Step 9 | Reboot Raspberry Pi 2 and Wifi will be ready |"
echo "---------------------------------------------------------"
sleep 5s
sudo reboot

