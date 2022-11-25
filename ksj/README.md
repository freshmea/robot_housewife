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
- - - - - - -
# 2022-11-22
- - - - - - -
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
- - - - - - - 
# 2022-11-23
- - - - - - -
* OpenManipulator를 OpenCR로 사용했을때 rqt nodr grape를 확인한 결과 delta_twist_cmd와 delta_joint_cmd가 정상 값이 나오지는 것을 확인
* Manipulator U2D2 사용해서 연결
	* turtlebot bringupr과 manipulator teleop와 충돌 오류 발생 
	* 같은 joint_states 사용으로 오류 발생을 확인하여 manipulator 코드에서 joint_states를 다른 이름으로 변경
	* home/colcon_ws/src/open_manipulator/open_manipulator_x_teleop/open_manipulator_x_teleop/script/test_teleop_keyboard.py에 
	  109번줄 joint_states -> joint_states2로 변경
	  home/colcon_ws/src/open_manipulator/open_manipulator_x_controller/src/open_manipulator_x_controller.cpp에 
	  87번줄 joint_states -> joint_states2로 변경
	* turtlebot bringup과 manipulator teleop가 오류없이 작동
* turtlebot3 Waffle Pi를 SLAM을 작동하려 했지만 신호가 약한 와이파이를 사용하여 오류 발생
	* 다른 와이파이 신호를 사용하여 정상 작동
- - - - - - -
# 2022-11-24
- - - - - - -
* Turtlebot3 Waffle Pi을 움지역 map그리기
	* ros2 launch turtlebot3_cartographer cartographer.launch.py 실행
	* ros2 run nav2_map_server map_saver_cli -f ~/map     --->   map저장
	* ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=$HOME/map.yaml ----> 저장한 map으로 navigation 실행
* 목표 위치로 보내기
	* map에 목적지를 좌표를 찾아 코드로 실행
* map을 돌아 다니면서 순찰하기
- - - - - - -
# 2022-11-25
- - - - - - -
* 4개의 좌표를 반복하여 돌아다니기
* parameter 사용
	* 파이썬 코드로 다른 노드에서 생성한 파라미터에 접근
* parameter_tutorial 해보기
