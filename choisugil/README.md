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
- - -
# 2022_11_28
- - -
* 신호를 받아쓸 때 manipulator 움직여서 캔 집기. 
* 슬램후에 네비게이션 작동 문제. 
	* 본 교실에서 했을 때 지도가 정상적으로 그려지지 않음. - 바퀴가 헛돌아서 오돔 데이터가 손상, 매니퓰레이터 때문에 뒤쪽 신호가 가려짐. 
	 --> 지도 그리는 장소를 다른 곳으로 바꿈. 잘 그려짐. 
* 4개의 포인트로 이동 하는 노드를 만듬. 파라미터 겟셋 을 이용함. 
* callback 함수의 status 를 이용. 책 336 page 참고. (ROS2 로 시작하는로봇 프로그래밍)
* camera topic 제작 어려움. 
- - -
# 2022_11_29
- - -
* c++ opencv cam 을 바꾸어서 카메라 토픽 발행.
* 저장공간 부족으로 시스템 다운 --> 다시 포맷. no space left on device
* 오픈메뉴플레이터 코드 작성 teleopkey
- - -
# 2022_11_30
- - -
* 메인 코드 작성. wfmp_ex.py
* 메인 코드에서 웨이포인트 노드로 위치 전송. (go1, go2, go3, go4, )
	* 이동하는 중에도 방향이 바뀔 수 있게 만듬. 
* move_tb3.py 노드 작성. - 쓰레기깡통을 발견했을 때, 자기 위치 중심에서 깡통 앞으로 이동.
	* 회전을 하기 위해서 IMU 센서의 각도 값을 이용. 
- - -
# 2022_12_01
- - -
* 발표 영상 제작
	* 네 포인트를 패트롤 하는 영상
	* 쓰레기 깡통을 주어서 휴지통에 버리는 영상
	* 스테레오 카메라를 통해서 depth map 확인 하는 여상
	* 깡통발견 영상. OpenCV
* 뒷 정리.
* 발표 자료 정리. 

