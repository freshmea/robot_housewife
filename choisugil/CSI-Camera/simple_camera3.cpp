// simple_camera.cpp
// MIT License
// Copyright (c) 2019-2022 JetsonHacks
// See LICENSE for OpenCV license and additional information
// Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
// NVIDIA Jetson Nano Developer Kit using OpenCV
// Drivers for the camera and OpenCV are included in the base image
#include "opencv_cam/opencv_cam_node.hpp"

#include <iostream>

#include "camera_calibration_parsers/parse.hpp"

#include <opencv2/opencv.hpp>

std::string gstreamer_pipeline (int sensor_id, int capture_width, int capture_height, int display_width, int display_height, int framerate, int flip_method) {
    return "nvarguscamerasrc sensor-id=" + std::to_string(sensor_id) + " ! video/x-raw(memory:NVMM), width=(int)" + std::to_string(capture_width) + ", height=(int)" +
           std::to_string(capture_height) + ", framerate=(fraction)" + std::to_string(framerate) +
           "/1 ! nvvidconv flip-method=" + std::to_string(flip_method) + " ! video/x-raw, width=(int)" + std::to_string(display_width) + ", height=(int)" +
           std::to_string(display_height) + ", format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}



int main()
{

    assert(!cxt_.camera_info_path_.empty()); // readCalibration will crash if file_name is ""
    std::string camera_name1;
    if (camera_calibration_parsers::readCalibration(cxt_.camera_info_path_, camera_name1, camera_info_msg_1)) {
      RCLCPP_INFO(get_logger(), "got camera info for '%s'", camera_name.c_str());
      camera_info_msg_1.header.frame_id = cxt_.camera_frame_id_;
      camera_info_pub_1 = create_publisher<sensor_msgs::msg::CameraInfo>("camera_info", 10);
    } else {
      RCLCPP_ERROR(get_logger(), "cannot get camera info, will not publish");
      camera_info_pub_1 = nullptr;
    }

    image_pub_1 = create_publisher<sensor_msgs::msg::Image>("image_raw1", 10);
    
    assert(!cxt_.camera_info_path_.empty()); // readCalibration will crash if file_name is ""
    std::string camera_name2;
    if (camera_calibration_parsers::readCalibration(cxt_.camera_info_path_, camera_name2, camera_info_msg_2)) {
      RCLCPP_INFO(get_logger(), "got camera info for '%s'", camera_name.c_str());
      camera_info_msg_2.header.frame_id = cxt_.camera_frame_id_;
      camera_info_pub_2 = create_publisher<sensor_msgs::msg::CameraInfo>("camera_info", 10);
    } else {
      RCLCPP_ERROR(get_logger(), "cannot get camera info, will not publish");
      camera_info_pub_2 = nullptr;
    }

    image_pub_2 = create_publisher<sensor_msgs::msg::Image>("image_raw2", 10);


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
	sensor_msgs::msg::Image::UniquePtr image_msg1(new sensor_msgs::msg::Image());
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
	sensor_msgs::msg::Image::UniquePtr image_msg2(new sensor_msgs::msg::Image());
    std::cout << "Using pipeline2: \n\t" << pipeline2 << "\n";
    
    auto stamp = now();
    image_msg1->header.stamp = stamp;
    image_msg1->header.frame_id = cxt_.camera_frame_id_;
    image_msg1->height = frame.rows;
    image_msg1->width = frame.cols;
    image_msg1->encoding = mat_type2encoding(frame.type());
    image_msg1->is_bigendian = false;
    image_msg1->step = static_cast<sensor_msgs::msg::Image::_step_type>(frame.step);
    image_msg1->data.assign(frame.datastart, frame.dataend);
    
    image_msg2->header.stamp = stamp;
    image_msg2->header.frame_id = cxt_.camera_frame_id_;
    image_msg2->height = frame.rows;
    image_msg2->width = frame.cols;
    image_msg2->encoding = mat_type2encoding(frame.type());
    image_msg2->is_bigendian = false;
    image_msg2->step = static_cast<sensor_msgs::msg::Image::_step_type>(frame.step);
    image_msg2->data.assign(frame.datastart, frame.dataend);
      
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

    // cv::namedWindow("CSI Camera1", cv::WINDOW_AUTOSIZE);
    // cv::namedWindow("CSI Camera2", cv::WINDOW_AUTOSIZE);
    
    image_pub_1->publish(std::move(image_msg1));
      if (camera_info_pub_1) {
        camera_info_msg_1.header.stamp = stamp;
        camera_info_pub_1->publish(camera_info_msg_1);
      }
    image_pub_2->publish(std::move(image_msg2));
      if (camera_info_pub_2) {
        camera_info_msg_2.header.stamp = stamp;
        camera_info_pub_2->publish(camera_info_msg_2);
      }
      
    std::cout << "Hit ESC to exit" << "\n" ;

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


