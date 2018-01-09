#!/bin/bash

echo "----------------------------------------"
echo "|     Resizing Partition - SD Card     |"
echo "|                PART 2                |"              
echo "|                START                 |"
echo "----------------------------------------"
echo ""

echo ""
echo "----------------------------------------------------------"
echo "| Step 1 | Performing on-line resizing of /dev/mmcblk0p2 |"
echo "----------------------------------------------------------"
sudo resize2fs -p /dev/mmcblk0p2
df -h
sleep 5s
echo ""

echo ""
echo "----------------------------------------"
echo "|     Resizing Partition - SD Card     |"
echo "|                PART 2                |"
echo "|                FINISH                |"
echo "----------------------------------------"
echo ""

echo ""
echo "-------------------"
echo "| Step 4 | Reboot |"
echo "-------------------"
sleep 5s
sudo reboot

