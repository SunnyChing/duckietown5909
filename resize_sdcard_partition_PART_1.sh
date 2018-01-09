#!/bin/bash

echo "----------------------------------------"
echo "|     Resizing Partition - SD Card     |"
echo "|                PART 1                |"              
echo "|                START                 |"
echo "----------------------------------------"
echo ""

echo ""
echo "-------------------------------------------"
echo "| Step 1 | Show SD Card Partitions Status |"
echo "-------------------------------------------"
df -h
sleep 5s
echo ""

echo ""
echo "------------------------------------------------"
echo "| Step 2 | Expand SD Card Partition to maximum |"
echo "------------------------------------------------"
(
echo p # Show up the blocks' size of each partitions inside the SD Card
echo d # Delete the partition
echo 2 # Partition 2 selected [mmcblk0p2]
echo n # Add new partition
echo p # Primary partition type selected
echo 2 # Partition 2 selected [mmcblk0p2]
echo   # First sector (Accept default)
echo   # Last sector (Accept default)
echo w # Write changes
) | sudo fdisk -u /dev/mmcblk0
echo ""

echo ""
echo "----------------------------------------"
echo "|     Resizing Partition - SD Card     |"
echo "|                PART 1                |"
echo "|                FINISH                |"
echo "----------------------------------------"
echo ""

echo ""
echo "----------------------------------------"
echo "|        Remember to run PART 2        |"
echo "|              file name:              |"
echo "|   resize_sdcard_partition_PART_2.sh  |"
echo "|                  to                  |"
echo "|                finish                |"
echo "|     Resizing Partition - SD Card     |"
echo "----------------------------------------"
sleep 8s
echo ""

echo ""
echo "-------------------"
echo "| Step 4 | Reboot |"
echo "-------------------"
sleep 3s
sudo reboot

