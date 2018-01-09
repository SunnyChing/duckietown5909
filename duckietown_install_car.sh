#!/usr/bin/env bash
set -e
set -x

# Install some packages that were missed in v1.1. Not necessary anymore in v1.2
sudo apt-get install ros-indigo-{tf-conversions,cv-bridge,image-transport,camera-info-manager,theora-image-transport,joy,image-proc} -y
sudo apt-get install ros-indigo-compressed-image-transport -y
sudo apt-get install libyaml-cpp-dev -y
ot
# # packages for the IMU
sudo apt-get install ros-indigo-phidgets-drivers
sudo apt-get install ros-indigo-imu-complementary-filter ros-indigo-imu-filter-madgwick

# # scipy for lane-filter
 sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
 #sudo pip install scipy --upgrade

#for line detector 
#sudo apt-get install python-sklearn
#sudo pip install -U scikit-learn  

#2017 version
#sudo pip install frozendict

#echo "Step 1) First need to make sure all scipy dependencies are installed properly"
#sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose -y
#echo "Step 2) Make sure the numpy, which scipy is dependent on is up-to-date"
#sudo pip install numpy --upgrade
#echo "Step 3) Make sure all the build dependencies of scipy is available"
#sudo apt-get build-dep python-scipy
#echo "Step 4) Rerun the upgrade"
#sudo pip install scipy --upgrade

# No compressed image
# $sudo apt-get install ros-indigo-compressed-image-transport
