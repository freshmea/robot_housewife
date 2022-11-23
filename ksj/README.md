# robot_housewife
자율주행로봇 로봇청소기엄마, 가정관리사, 가정부, 로봇노예, 로봇집사, 로봇가정비서, 자비스

- - -
# day1
- - -
* OpenMANIPULATOR 조립.
	* Opencr로 bringup fail.
	* U2D2로 연결 후 bringup success.
	* Manipulator teleop_keyboard 조작
	* 회전하면서 Marker를 찾으러 node.find_marker를 while문을 사용했지만 코드는 한번만 실행 후 
	  while문을 종료 못함 
* TurtleBot3 Waffle Pi 조립.
	* Waffle Pi에 Manipulator 연결
- - -
#day2
- - -
* Manipulator opoenCR bringup 시도
	* bringup fail
	* TB3 & OpenMANIPULATOR 예제로 다시 bring
* Software Setup
	* $ sudo apt install ros-foxy-dynamixel-sdk ros-foxy-ros2-control ros-foxy-ros2-
	   controllers ros-foxy-gripper-controllers ros-foxy-moveit
  	  $ cd ~/turtlebot3_ws/src/
  	  $ git clone -b foxy-devel https://github.com/ROBOTIS-GIT/turtlebot3_manipulation.git
  	  $ cd ~/turtlebot3_ws && colcon build --symlink-install
* OpenCR Setup
	* $ export OPENCR_PORT=/dev/ttyACM0
	* $ export OPENCR_MODEL=turtlebot3_manipulation
	* $ rm -rf ./opencr_update.tar.bz2
	* $ wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS2/
	    latest opencr_update.tar.bz2
	* $ tar -xvf opencr_update.tar.bz2
	* $ cd ./opencr_update
	* $ ./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
* Bringup
	* $ ros2 launch turtlebot3_manipulation_bringup hardware.launch.py
	* success bringup!
* $ ros2 run turtlebot3_manipulation_teleop turtlebot3_manipulation_teleop 작동 했지만 
  바퀴만 움직이고 manipulator 작동하지 않음
* ros2 launch turtlebot3_manipulation_moveit_config servo.launch.py 시도
	* [ERROR]: Could not find requested resource in ament index
	* sudo apt install ros-foxy-moveit-servo
	* [component_container-1] [WARN]: Stale command. Try a larger 'incoming_command_timeout' parameter?
	[component_container-1] [WARN]: Close to a singularity, decelerating 오류 발생
