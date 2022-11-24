# robot_housewife
자율주행로봇 로봇청소기엄마, 가정관리사, 가정부, 로봇노예, 로봇집사, 로봇가정비서, 자비스

- - -
# day1
- - -
* 로봇 조립 및 sd 카드 이미지 설치.
	* https://omorobot.com/docs/ros2-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0-jetson-nano/
	* xubuntu 20.04 버전으로 설치. 
	* 아이디/비번 aa/aa 로 설정
* 
* 터미네이터 설치.
* ros 설치. 
- - -
# day2
- - -
* opoenCR 
* bringup fail!. check error message
* usb port setting misssing 
	* $ sudo cp `ros2 pkg prefix turtlebot3_bringup`/share/turtlebot3_bringup/script/99-turtlebot3-cdc.rules /etc/udev/rules.d/
	  $ sudo udevadm control --reload-rules
  	  $ sudo udevadm trigger
- - -
# 2022_11_21
- - -
* 스테레오 카메라 설치 
* 상부 터틀봇3 메뉴퓰레이터 설치.
* openCR setup 
	* https://emanual.robotis.com/docs/en/platform/turtlebot3/manipulation/#manipulation
	* 	$ export OPENCR_PORT=/dev/ttyACM0
		$ export OPENCR_MODEL=turtlebot3_manipulation
		$ rm -rf ./opencr_update.tar.bz2
		$ wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS2/latest/opencr_update.tar.bz2
		$ tar -xvf opencr_update.tar.bz2
		$ cd ./opencr_update
		$ ./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
* IMX219-83 스테레오 카메라, 듀얼 IMX219, 8 메가 픽셀, 깊이 비전 및 스테레오 비전
 카메라 설치.
- - - 
# 2022_11_22
- - -
* 카메라 설치.stereo camera imx219-83 
* jetson nano 에서 인식은 되는데, python code 에서 작동이안됨. 
* gstreamer 재설치 과정에서 image 망가짐. 다시 설치. 
* open-manipulator-x 설치 후 turtlebot3_manipulation 을 설치 해야지 작동이 됨. 
* OpenCR setup 시 sudo dpkg --add-architectur armhf, sudo apt update, sudo apt install libc6:armhf 를 설치하고 openCR_turtlebot3_manipulator 를 설치 해야함. 
- - -
# 2022_11_23
- - -
* open_manipulator_x_teleop 패키지의 teleop_keyboard 로 turtlebot3
* turtlebot3 의 브링업과 open_manipulator 의 브링업이 충돌을일으김. (토픽명, joint_states) 
	* ros2 launch turtlebot3_bringup robot.launch.py
	* ros2 launch open_manipulator_x_controller open_manipulator_x_controller.launch.py
* teleop_keyboard.py -> 109 joint_states --->joint_states2
* src/open_manipulator/open_manipulator_x_controller/src/open_manipulator_x_controller.cpp  ->87 joint_states --->joint_States2 
* topic 이름을 바꾸어서 해결.
* open_manipulator에 전원연결을 하기 위해서 u2d2 power board에 전원 선납땜. 
- - -
# 2022_11_24
- - -
* todo :
	* 내비게이션 완성 시키기.
	* 주행을하면서 명령을받기.
	* 어떤 기본 코드를 무엇을 쓸것인가? 
* open_manipulator 사용. 
	* navigation 실행.
	* followwaypoint 로 움직이기. 

