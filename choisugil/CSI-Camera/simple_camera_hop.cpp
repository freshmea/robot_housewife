// simple_camera.cpp
// MIT License
// Copyright (c) 2019-2022 JetsonHacks
// See LICENSE for OpenCV license and additional information
// Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
// NVIDIA Jetson Nano Developer Kit using OpenCV
// Drivers for the camera and OpenCV are included in the base image

#include <opencv2/opencv.hpp>

std::string gstreamer_pipeline (int sensor_id, int capture_width, int capture_height, int display_width, int display_height, int framerate, int flip_method) {
    return "nvarguscamerasrc sensor-id=" + std::to_string(sensor_id) + " ! video/x-raw(memory:NVMM), width=(int)" + std::to_string(capture_width) + ", height=(int)" +
           std::to_string(capture_height) + ", framerate=(fraction)" + std::to_string(framerate) +
           "/1 ! nvvidconv flip-method=" + std::to_string(flip_method) + " ! video/x-raw, width=(int)" + std::to_string(display_width) + ", height=(int)" +
           std::to_string(display_height) + ", format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}



int main()
{
    int sensor_id = 0 ;	
    int capture_width = 1280 ;
    int capture_height = 720 ;
    int display_width = 1280 ;
    int display_height = 720 ;
    int framerate = 30 ;
    int flip_method = 0 ;

    std::string pipeline1 = gstreamer_pipeline(
		sensor_id,
		capture_width,
		capture_height,
		display_width,
		display_height,
		framerate,
		flip_method);
    std::cout << "Using pipeline1: \n\t" << pipeline1 << "\n";
    
    sensor_id = 1 ;
    std::string pipeline2 = gstreamer_pipeline(
		sensor_id,
		capture_width,
		capture_height,
		display_width,
		display_height,
		framerate,
		flip_method);
    std::cout << "Using pipeline2: \n\t" << pipeline2 << "\n";
 
    cv::VideoCapture cap1(pipeline1, cv::CAP_GSTREAMER);
    if(!cap1.isOpened()) {
		std::cout<<"Failed to open camera."<<std::endl;
		return (-1);
    }
    
    cv::VideoCapture cap2(pipeline2, cv::CAP_GSTREAMER);
    if(!cap2.isOpened()) {
		std::cout<<"Failed to open camera."<<std::endl;
		return (-1);
    }

    cv::Mat img1, img2;

    cv::namedWindow("CSI Camera1", cv::WINDOW_AUTOSIZE);
    cv::namedWindow("CSI Camera2", cv::WINDOW_AUTOSIZE);

    std::cout << "Hit ESC to exit" << "\n" ;


	camera_info_msg_.header.img1_id = cxt_.camera_img1_id_;
	camera_info_pub_ = create_publisher<sensor_msgs::msg::CameraInfo>("camera_info", 10);

    
    image_pub_ = create_publisher<sensor_msgs::msg::Image>("image_raw", 10);

    //cv::Mat frame;
	
	auto stamp = now();

	// Avoid copying image message if possible
	sensor_msgs::msg::Image::UniquePtr image_msg(new sensor_msgs::msg::Image());

	// Convert OpenCV Mat to ROS Image
	image_msg->header.stamp = stamp;
	image_msg->header.img1_id = cxt_.camera_img1_id_;
	image_msg->height = img1.rows;
	image_msg->width = img1.cols;
	image_msg->encoding = mat_type2encoding(img1.type());
	image_msg->is_bigendian = false;
	image_msg->step = static_cast<sensor_msgs::msg::Image::_step_type>(img1.step);
	image_msg->data.assign(img1.datastart, img1.dataend);

  // Publish
  image_pub_->publish(std::move(image_msg));
  if (camera_info_pub_) {
    camera_info_msg_.header.stamp = stamp;
    camera_info_pub_->publish(camera_info_msg_);
  }

  // Sleep if required
  if (cxt_.file_) {
    using namespace std::chrono_literals;
    next_stamp_ = next_stamp_ + rclcpp::Duration{1000000000ns / publish_fps_};
    auto wait = next_stamp_ - stamp;
    if (wait.nanoseconds() > 0) {
      std::this_thread::sleep_for(static_cast<std::chrono::nanoseconds>(wait.nanoseconds()));
    }
  }

    while(true)
    {
		if (!cap1.read(img1)) {
			std::cout<<"Capture read error"<<std::endl;
			break;
		}
		cap1 >> img1;
		cap2 >> img2;

		cv::imshow("CSI Camera1",img1);
		cv::imshow("CSI Camera2",img2);
		int keycode = cv::waitKey(10) & 0xff ; 
		if (keycode == 27) break ;
    }


    cap1.release();
    cap2.release();
    cv::destroyAllWindows() ;
    return 0;
}


