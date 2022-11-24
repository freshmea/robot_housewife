import rclpy, sys
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped 
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from nav2_msgs.action import FollowWaypoints
from rcl_interfaces.srv import SetParameters, GetParameters, ListParameters
from rclpy.exceptions import ParameterNotDeclaredException
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterValue
#from rcl_interfaces.msg import Parameter, ParameterType

# from rclpy.duration import Duration # Handles time for ROS 2
 
class ClientFollowPoints(Node):

    def __init__(self):
        super().__init__('client_follow_points')
        self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')
        
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.spin_method)
        
        qos_profile = QoSProfile(depth=10)
        self.cli = self.create_client(GetParameters, 'move_by_param/get_parameters')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetParameters.Request()
        self.declare_parameter('navi_go_stop', 'stop')
        
    def spin_method(self):
        self.send_request()
        response = self.future.result()
        print(response.values[0]._string_value)
        
    def send_request(self):
        self.req.names = ['navi_go_stop']
        self.future = self.cli.call_async(self.req)

    def send_points(self, points):
        msg = FollowWaypoints.Goal()
        msg.poses = points

        self._client.wait_for_server()
        self._send_goal_future = self._client.send_goal_async(msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.missed_waypoints))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))
        
    def publish_points(self, x, y, z):
        rgoal = PoseStamped()
        rgoal.header.frame_id = "map"
        rgoal.header.stamp.sec = 0
        rgoal.header.stamp.nanosec = 0
        rgoal.pose.position.x = x
        rgoal.pose.position.y = y
        rgoal.pose.position.z = z
        rgoal.pose.orientation.w = 1.0
        print(rgoal)
        #mgoal = [rgoal]
        #follow_points_client.send_points(mgoal)
        #time.sleep(1)

def main(args=None):
    client.send_request()
    rclpy.init(args=args)

    follow_points_client = ClientFollowPoints()
    print('client inited')
    '''
    while 1:
	    #rgoal = PoseStamped()
	    #rgoal.header.frame_id = "map"
	    #rgoal.header.stamp.sec = 0
	    #rgoal.header.stamp.nanosec = 0
	    #rgoal.pose.position.z = -0.00143
	    #rgoal.pose.orientation.w = 1.0
	    #rgoal.pose.position.x = 0.292
	    #rgoal.pose.position.y = -0.398
	    follow_points_client.publish_points(-0.71, 1.20, -0.00143)
	    follow_points_client.send_points(mgoal)
	    follow_points_client.publish_points(0.112, 1.2, -0.00137)
	    follow_points_client.send_points(mgoal)
	    follow_points_client.publish_points(0.0857, 0.253, -0.00143)
	    follow_points_client.send_points(mgoal)
	    follow_points_client.publish_points(-0.651,0.247, 0.00256)
	    follow_points_client.send_points(mgoal)
	    #print(rgoal)
	    #mgoal = [rgoal]
	    #follow_points_client.send_points(mgoal)
	    rclpy.spin(follow_points_client)
	'''    
	    

action success
1. turtle_sim teleop 확인
2. 실행할때 4개 좌표 이동
3. while문 삭제

