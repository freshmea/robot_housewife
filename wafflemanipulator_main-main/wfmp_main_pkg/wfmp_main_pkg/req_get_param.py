import rclpy, sys
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from rcl_interfaces.srv import SetParameters, GetParameters, ListParameters
from rclpy.exceptions import ParameterNotDeclaredException
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterValue
#from rcl_interfaces.msg import Parameter, ParameterType


class ReqGetParam(Node):
    def __init__(self):
        super().__init__('req_get_param')
        qos_profile = QoSProfile(depth=10)
        self.cli = self.create_client(GetParameters, 'move_by_param/get_parameters')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetParameters.Request()
        self.declare_parameter('go_turtle', 'stop')
    def send_request(self):
        self.req.names = ['go_turtle']
        self.future = self.cli.call_async(self.req)



def main(args=None):
    rclpy.init(args=args)

    client = ReqGetParam()
    client.send_request()

    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            try:
                response = client.future.result()
                print(response.values[0]._string_value)
                # print(Parameter('go_turtle', list, value=response.values))
                """
                cl_interfaces.srv.GetParameters_Response(values=[rcl_interfaces.msg.ParameterValue(type=4, bool_value=False, integer_value=0, double_value=0.0, string_value='go', byte_array_value=[], bool_array_value=[], integer_array_value=[], double_array_value=[], string_array_value=[])])
                """
            except Exception as e:
                client.get_logger().info(
                    'Service call failed %r' % (e,))
            break

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
