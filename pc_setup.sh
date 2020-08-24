### Before running, to remove the requirement of multiple pwd entries, run:
### sudo echo 'user ALL=(ALL:ALL) NOPASSWD:/home/rob301/test.sh' >> /etc/sudoers


cd ~/
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install ros-kinetic-turtlebot3
sudo apt-get -y install ros-kinetic-turtlebot3-simulations

### Populate the .bashrc
echo 'source /opt/ros/kinetic/setup.bash' >> ~/.bashrc
echo 'source ~/catkin_ws/devel/setup.bash' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=waffle_pi' >> ~/.bashrc
echo 'export GAZEBO_MODEL_PATH=~/catkin_ws/src/rob301_simulation/models:$GAZEBO_MODEL_PATH' >> ~/.bashrc

echo 'export ROS_HOSTNAME=localhost' >> ~/.bashrc

### on user 1 only:
echo 'export ROS_PORT="11311"' >> ~/.bashrc
echo 'export GAZEBO_PORT="11345"' >> ~/.bashrc
echo 'export GZWEB_PORT="8080"' >> ~/.bashrc

### on user 2 only:
#echo 'export ROS_PORT="11312"' >> ~/.bashrc
#echo 'export GAZEBO_PORT="11346"' >> ~/.bashrc
#echo 'export GZWEB_PORT="8081"' >> ~/.bashrc

### for both users:

echo 'export ROS_MASTER_URI="http://localhost:$ROS_PORT"' >> ~/.bashrc
echo 'export GAZEBO_MASTER_URI="http://localhost:$GAZEBO_PORT"' >> ~/.bashrc

mkdir ~/catkin_ws
mkdir ~/catkin_ws/src
cd catkin_ws/src
git clone https://github.com/brandonwagstaff/rob301_simulation.git

cd ~/catkin_ws 
catkin_make

## gzweb
sudo apt-get install -y gazebo7 libgazebo7-dev
sudo apt-get install -y libjansson-dev nodejs-legacy libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential python-software-properties
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
cd ~/
git clone https://github.com/osrf/gzweb
cd gzweb
git checkout gzweb_1.4.0
source /usr/share/gazebo/setup.sh
npm run deploy --- -m

## add any custom models to proper locations
Sudo cp -r /opt/ros/kinetic/share/turtlebot3_description ~/gzweb/http/client/assets

