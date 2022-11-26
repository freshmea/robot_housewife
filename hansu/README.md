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
- - -
11/6 
- - -
slam/navi 작동
노트북 캠: ros2 run usb_cam usb_cam_node_exe
rasicam-pub_tb3_pose2d.py-img_compressed2raw.py-aruco_node.py-track_maker2.

- - -
11/7 
- - -
cv_bridge 이용한 ros2 pub,sub 작성 

publising
![Screenshot from 2022-11-18 11-38-49](https://user-images.githubusercontent.com/112480482/202604390-327d1f9c-015f-42d2-871f-b223c8b27095.png)

subsribe
![Screenshot from 2022-11-18 11-39-30](https://user-images.githubusercontent.com/112480482/202604399-17a192cd-c418-4142-a64e-fa17a9695889.png)

![video](https://user-images.githubusercontent.com/112480482/202604423-f87d1d74-d445-42a3-a207-0e5c9bc8cff9.png)
video 출력

- - -
11/8 
- - -
노트북캠에 완성한 pub, sub에 yolo를 추가하여 구동 성공

- - -
11/9 
- - -
인식한 객체를 둘러쌓은 박스의 크기(1m기준)를 기준으로 크기(픽셀)에 비례하여 거리를 측정할려하였으나 박스인식이 유동적이여서 처음 객체를 인식했을 때 정중앙의 좌표를 구해 그 방향으로 터틀봇3의 각도를 돌려놓고 라이다로 거리 측정 후 특정 위치까지 전진 후 매니퓰레이터 작동해야겠다 구상

- - -
11/10 
- - -
터틀봇3와 ros2 sub 구동 성공

    -robot_ws/src/cv_basics/pub,sub 수정

![Screenshot from 2022-11-18 11-57-00](https://user-images.githubusercontent.com/112480482/202607015-10e69a95-898f-4686-a4fd-a681f1a8aeb4.png)

- - -
#11.24
- - -
https://github.com/clydemcqueen/opencv_cam
~ 등등 예제 실행

- - -
#11.25
- - -
https://github.com/clydemcqueen/opencv_cam 예제 활용해 publisher하는 노드(C++)를 통해 기존에 만들어놓은 subscriber(python)을 통해 받으려 시도
compressd_image를 image_raw로 받는 이미지 형태 변화하니 받아짐
![20221125_124537](https://user-images.githubusercontent.com/112480482/204091952-dabe8bc3-1a5c-4c59-b852-dedbec73640b.jpg)
![20221125_124748](https://user-images.githubusercontent.com/112480482/204091955-f4bfcc37-20d0-4237-9fe9-09733cc3cf83.jpg)
허나 위와 같이 초록색 화면뜸
