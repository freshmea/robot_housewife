import rclpy, sys
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from rcl_interfaces.srv import SetParameters, GetParameters, ListParameters
from rclpy.exceptions import ParameterNotDeclaredException
from rclpy.parameter import Parameter
#from rcl_interfaces.msg import Parameter, ParameterType

SVC_MSG = (sys.argv[1])

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('req_set_param')
        qos_profile = QoSProfile(depth=10)
        self.cli_set = self.create_client(SetParameters, 'move_by_param/set_parameters')
        while not self.cli_set.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('set service not available, waiting again...')
        self.req_set = SetParameters.Request()
        # self.declare_parameter('go_turtle', 'none')
        # self.srv = self.create_service(AddTwoints, 'add_two', self.call_back)

    def send_request(self):
        self.req_set.parameters = [Parameter(name='go_turtle', value=SVC_MSG).to_parameter_msg()]
        self.future = self.cli_set.call_async(self.req_set) 
        
        # this->get_parameter("my_parameter").get_parameter_value().get<std::string>();
    # def call_back(self, request, response):
    #     respose.sum = arg
    #     return response



def main(args=None):
    rclpy.init(args=args)

    client = MinimalClientAsync()
    client.send_request()
    while rclpy.ok():
        rclpy.spin_once(client)
        response = client.future.result()
        if client.future.done():
            try:
                response = client.future.result()
            except Exception as e:
                client.get_logger().info(
                    'Service call failed %r' % (e,))
            print(response)
            break

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
