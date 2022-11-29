import rclpy, sys
from rclpy.node import Node
from rclpy.qos import QoSProfile

from geometry_msgs.msg import Twist
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType
from std_msgs.msg import String
from param_tutorial.getchar import Getchar

from rcl_interfaces.srv import SetParameters, GetParameters, ListParameters
from rclpy.parameter import Parameter

class ByParam(Node):
    def __init__(self):
        super().__init__('move_by_param')
        qos_profile = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', qos_profile)
        self.tw = Twist()
        timer_period = 1  # seconds
        #self.timer = self.create_timer(timer_period, self.move_turtle)
    
        self.cli = self.create_client(SetParameters, 'client_follow_points/set_parameters')
        self.declare_parameter('go_turtle', 'stop')
        self.req = SetParameters.Request()
    '''
    def send_request(self, key):
        if key == 'go1':
            self.req.parameters = [Parameter(name='go_turtle', value='go1').to_parameter_msg()]
            #self.future = self.cli.call_async(self.req)
        elif key == 'go2':
            self.req.parameters = [Parameter(name='go_turtle', value='go2').to_parameter_msg()]
            #self.future = self.cli.call_async(self.req)
    '''
    '''
    def move_turtle(self):
        param = self.get_parameter('go_turtle').get_parameter_value().string_value
        if param =='go1':
            self.tw.linear.x = 0.5
            self.tw.angular.z  = 0.25
        elif param =='go2':
            self.tw.linear.x = 0.0
            self.tw.angular.z  = 0.0
        else:
            pass
        self.pub.publish(self.tw)

        self.get_logger().info('turtle %s!' % param)
       
        
        self.set_parameters([rclpy.parameter.Parameter(
                        'go_turtle',
                        rclpy.Parameter.Type.STRING,
                        'go'
                    )])
    '''
'''
def main():
    rclpy.init()
    node = ByParam()
    node.move_turtle()

    rclpy.spin(node)
'''
def main(args=None):
    rclpy.init(args=args)

    node = ByParam()
    
    print('test')
    try:
        kb = Getchar()
        key =''
        while rclpy.ok():
            key = kb.getch()
            if key == '1':
                node.req.parameters = [Parameter(name='go_turtle', value='go1').to_parameter_msg()]
                node.future = node.cli.call_async(node.req)
            else:
                pass
    
    except KeyboardInterrupt:
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
            node.destroy_node()
            rclpy.shutdown()
             
    rclpy.spin(node)
if __name__ == '__main__':
    main()
