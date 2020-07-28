# ROB 1514 Simulation

ROS package for the ROB 301 project simulation environment. Provides a
 [Gazebo](http://gazebosim.org/) world in which the labs can be completed.


## Install
Clone the repository into your catkin workspace:
```
git clone https://github.com/brandonwagstaff/rob301_simulation
```

You need to tell Gazebo where to find any custom models. Add the following
line to your `.bashrc`:
```
export GAZEBO_MODEL_PATH=<path_to_catkin_ws>/src/rob301_simulation/models:$GAZEBO_MODEL_PATH
```
where you've replaced `<path_to_catkin_ws>` with the actual path.

Build and source the workspace as per usual ROS procedure.

## Run
Once the workspace has been built and sourced, just run
```
roslaunch rob301_simulation lab_x.launch
```
to launch the world.

You can, of course, view all ROS topics using `rostopic list`. Topics for the
front-facing camera are prefixed with `/camera`, while the topics for the
side-facing camera are prefixed with `/head_camera`.

## TODO: 

- [] Update model from Turtlebot2 to Turtlebot3 - ideally we can set up a downward facing camera, and the 2D lidar.
- [] Finalize a strategy for providing students access to the virtual labs.
	- [] Set up a server with ROS that students can access via SSH. 
		- [] Need to find a suitable server machine that students can access from home
	- [] Testing gzweb for gazebo visualization via a web browser
	- [] Testing other graphical ssh options like X11 forwarding
- [] Create environments for each lab:
	- [] Lab 1 - Turtlebot3 Intro:
		- [] Gazebo world: Vvry simple world needed - add a few features to test out the robot in simulation
		- [] Lab report update to introduce the Gazebo simulation

	- [] Lab 2 - Pose-to-Pose Control:
		- [] Gazebo world: add markers on floor to indicate starting and final poses
		- [] Updates to the lab report

	- [] Lab 3 - Path-Following (PID Control):
		- [] Gazebo world: create a practice world with smaller tracks for students to implement their controllers
		- [] Gazebo world: create a race world with the simulated racecourse - will need to think how this can be done - either students can practice on this as much as they would like, or we can withhold the course and they can send us code to run
		- [] Update the existing line detection node to work in simulation
		- [] Updates to the lab report

	- [] Lab 4 - Kalman Filtering:
		- [] Gazebo world: Add a pillar (or possibly even model a CN tower), and any other desired aesthetics
		- [] Implement the planar lidar node 
		- [] Updates to the lab report

	- [] Project

## Notes
* Tested with Gazebo 7.0 with ROS Kinetic on Ubuntu 16.04.
