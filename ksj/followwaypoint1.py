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
        super().__init__('waffle_main')
        self.declare_parameter("navi_go_stop", "stop")
        self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')
        
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.start)
        #self.timer = self.create_timer(timer_period, self.spin_method)
        
        qos_profile = QoSProfile(depth=10)
        self.cli = self.create_client(GetParameters, 'waffle_main/get_parameters')
        self.cli_set = self.create_client(SetParameters, 'waffle_main/set_parameters')
        while not self.cli_set.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('set service not available, waiting again...')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetParameters.Request()
        self.req_set = SetParameters.Request()
        #self.declare_parameter('navi_go_stop', 'stop')
        
    
    def start(self):
        param = self.get_parameter('navi_go_stop').get_parameter_value().string_value
        self.send_request()

        if param == 'go1':
            rgoal = PoseStamped()
            rgoal.header.frame_id = "map"
            rgoal.header.stamp.sec = 0
            rgoal.header.stamp.nanosec = 0
            
            rgoal.pose.position.z = -0.00143
            rgoal.pose.position.x = -0.469
            rgoal.pose.position.y = 0.782

            rgoal.pose.orientation.w = 1.0
            print(rgoal)
            mgoal = [rgoal]

            self.send_points(mgoal)
            
        elif param == 'go2':
            print('success2')
            
            rgoal = PoseStamped()
            rgoal.header.frame_id = "map"
            rgoal.header.stamp.sec = 0
            rgoal.header.stamp.nanosec = 0
           
            rgoal.pose.position.z = -0.00143
            rgoal.pose.position.x = -1.8
            rgoal.pose.position.y = 0.928

            rgoal.pose.orientation.w = 1.0
            print(rgoal)
            mgoal = [rgoal]

            self.send_points(mgoal)
            
        elif param == 'go3':
            print('success3')
            
            rgoal = PoseStamped()
            rgoal.header.frame_id = "map"
            rgoal.header.stamp.sec = 0
            rgoal.header.stamp.nanosec = 0
           
            rgoal.pose.position.z = 0.00247
            rgoal.pose.position.x = -1.77
            rgoal.pose.position.y = 0.098

            rgoal.pose.orientation.w = 1.0
            print(rgoal)
            mgoal = [rgoal]

            self.send_points(mgoal)
            
        elif param == 'go4':
            print('success4')
            
            rgoal = PoseStamped()
            rgoal.header.frame_id = "map"
            rgoal.header.stamp.sec = 0
            rgoal.header.stamp.nanosec = 0
           
            rgoal.pose.position.z = -0.00143
            rgoal.pose.position.x = -0.548
            rgoal.pose.position.y = 0.0746

            rgoal.pose.orientation.w = 1.0
            print(rgoal)
            mgoal = [rgoal]

            self.send_points(mgoal)
            
        elif param == 'stop':
            print('stop move')
            rgoal = PoseStamped()
            rgoal.header.frame_id = "map"
            rgoal.header.stamp.sec = 0
            rgoal.header.stamp.nanosec = 0
            
            rgoal.pose.position.z = -0.00143
            rgoal.pose.position.x = -1.09
            rgoal.pose.position.y = 0.483

            rgoal.pose.orientation.w = 1.0
            print(rgoal)
            mgoal = [rgoal]

            self.send_points(mgoal)
        
        else:
            pass
            
        print(param)

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
        param = self.get_parameter('navi_go_stop').get_parameter_value().string_value
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            print(result)
            if param == "go1":
                self.set_parameters([rclpy.parameter.Parameter('navi_go_stop', rclpy.Parameter.Type.STRING, 'go2')])
                #self.req_set.parameters = [Parameter(name='navi_go_stop', value='go2').to_parameter_msg()]
                #self.future = self.cli_set.call_async(self.req_set) 
            elif param == "go2":
                self.set_parameters([rclpy.parameter.Parameter('navi_go_stop', rclpy.Parameter.Type.STRING, 'go3')]) 
            elif param == "go3":
                self.set_parameters([rclpy.parameter.Parameter('navi_go_stop', rclpy.Parameter.Type.STRING, 'go4')])
            elif param == "go4":
                self.set_parameters([rclpy.parameter.Parameter('navi_go_stop', rclpy.Parameter.Type.STRING, 'go1')])
            elif param == "stop":
                self.set_parameters([rclpy.parameter.Parameter('navi_go_stop', rclpy.Parameter.Type.STRING, 'go1')])
                
                self.get_logger().info('Result: {0}'.format(result.missed_waypoints))
            else:
                pass

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        # self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))
        
    def send_request(self):
        self.req.names = ['navi_go_stop']
        self.future = self.cli.call_async(self.req) 
    
def main(args=None):
    rclpy.init(args=args)

    follow_points_client = ClientFollowPoints()
    #follow_points_client.send_request()
    print('client inited')
    
    #follow_points_client.start()
    
    rclpy.spin(follow_points_client)

