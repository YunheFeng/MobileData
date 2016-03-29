#!/bin/sh

# prompts first

ssh-keygen
ssh-copy-id lanterns2.eecs.utk.edu

sudo chown zlu12 /local
sudo chown zlu12 /mydata

svn co --password Xiaoyan0308 https://com1333.eecs.utk.edu:8443/svn/source/Codes/MobileData /local/MobileData
svn co --password Xiaoyan0308 https://com1333.eecs.utk.edu:8443/svn/source/Codes/Scripts /local/Scripts

scp lanterns2.eecs.utk.edu:/local_scratch/Datasets/mobile_data.tar.gz /mydata
tar xzvf /mydata/mobile_data.tar.gz -C /mydata
scp lanterns2.eecs.utk.edu:/local_scratch/check_points.tar.gz /mydata
tar xzvf /mydata/check_points.tar.gz -C /mydata

sudo apt-get update
sudo apt-get -y install vim python-scipy python-shapely 

ln -s /mydata/mobile_data /local/MobileData/datasets
ln -s /mydata/check_points /local/MobileData/results/check_points
sudo ln -s /local/Scripts/vimrc.local /etc/vim/vimrc.local

# cd /local/MobileData
# sudo chmod +x /local/MobileData/simple.sh 
# /local/MobileData/simple.sh &
# tail -f /local/MobileData/log

echo "You are all set."
