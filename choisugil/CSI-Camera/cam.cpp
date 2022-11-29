#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <cstdio>
#include <memory>
#include <string>

using namespace std;
using namespace cv;

#define ROS_NODE_NAME "usb_camera_publisher"
#define ROS_CAMERA_TOPIC_NAME "snowdeer_camera_topic"

void (*breakCapture)(int);
void signalingHandler(int signo) {
  printf("'Ctrl + C'(%d) processing...\n", signo);

  exit(1);
}

string mat_type2encoding(int mat_type) {
  switch (mat_type) {
    case CV_8UC1:
      return "mono8";
    case CV_8UC3:
      return "bgr8";
    case CV_16SC1:
      return "mono16";
    case CV_8UC4:
      return "rgba8";
    default:
      throw std::runtime_error("Unsupported encoding type");
  }
}

void convert_frame_to_message(const cv::Mat & frame, size_t frame_id, 
  sensor_msgs::msg::Image::SharedPtr msg) {
  
  msg->height = frame.rows;
  msg->width = frame.cols;
  msg->encoding = mat_type2encoding(frame.type());
  msg->step = static_cast<sensor_msgs::msg::Image::_step_type>(frame.step);
  size_t size = frame.step * frame.rows;
  msg->data.resize(size);
  memcpy(&msg->data[0], frame.data, size);
  msg->header.frame_id = std::to_string(frame_id);
}

int main(int argc, char** argv) {
  breakCapture = signal(SIGINT, signalingHandler);

  rclcpp::init(argc, argv);

  rmw_qos_reliability_policy_t reliability_policy = RMW_QOS_POLICY_RELIABILITY_RELIABLE;
  rmw_qos_history_policy_t history_policy = RMW_QOS_POLICY_HISTORY_KEEP_ALL;

  size_t depth = 10;
  double freq = 30.0;
  size_t width = 320;
  size_t height = 240;
  setvbuf(stdout, NULL, _IONBF, BUFSIZ);

  
  auto node = rclcpp::Node::make_shared(ROS_NODE_NAME);
  rmw_qos_profile_t custom_camera_qos_profile = rmw_qos_profile_default;
  custom_camera_qos_profile.depth = depth;
  custom_camera_qos_profile.reliability = reliability_policy;
  custom_camera_qos_profile.history = history_policy;

  auto publisher1 = node->create_publisher<sensor_msgs::msg::Image>(
    ROS_CAMERA_TOPIC_NAME, custom_camera_qos_profile);

  rclcpp::WallRate loop_rate(freq);

  VideoCapture cap;
  if(!cap.open(0)) return 0;
  
  cap.set(CV_CAP_PROP_FRAME_WIDTH, static_cast<double>(width));
  cap.set(CV_CAP_PROP_FRAME_HEIGHT, static_cast<double>(height));

  if (!cap.isOpened()) {
    printf("Could not open video stream!!\n");
    return 1;
  }
  
  Mat frame;
  auto msg = std::make_shared<sensor_msgs::msg::Image>();
  msg->is_bigendian = false;

  size_t i = 1;

  while (rclcpp::ok()) {
    cap >> frame;

    if (!frame.empty()) {
      convert_frame_to_message(frame, i, msg);
    }

    if (!frame.empty()) {
      CvMat cvframe = frame;
      cvShowImage("Camera", &cvframe);
      if( waitKey(10) == 27 ) break;

      printf("Publishing image #%zd\n", i);
      publisher->publish(msg);
      ++i;

      if(i > 10000000) i = 0;
    }

    rclcpp::spin_some(node);
    loop_rate.sleep();
  }

  rclcpp::shutdown();

  return 0;
}
