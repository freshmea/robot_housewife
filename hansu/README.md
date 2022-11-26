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
#day2
- - -
* opoenCR 
* bringup fail!. check error message
* usb port setting misssing 
	* $ sudo cp `ros2 pkg prefix turtlebot3_bringup`/share/turtlebot3_bringup/script/99-turtlebot3-cdc.rules /etc/udev/rules.d/
	  $ sudo udevadm control --reload-rules
  	  $ sudo udevadm trigger
#11.24
https://github.com/clydemcqueen/opencv_cam
~ 등등 예제 실행
#11.25
https://github.com/clydemcqueen/opencv_cam 예제 활용해 publisher하는 노드(C++)를 통해 기존에 만들어놓은 subscriber(python)을 통해 받으려 시도
compressd_image를 image_raw로 받는 이미지 형태 변화하니 받아짐
![20221125_124537](https://user-images.githubusercontent.com/112480482/204091952-dabe8bc3-1a5c-4c59-b852-dedbec73640b.jpg)
![20221125_124748](https://user-images.githubusercontent.com/112480482/204091955-f4bfcc37-20d0-4237-9fe9-09733cc3cf83.jpg)
허나 위와 같이 초록색 화면뜸
