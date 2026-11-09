import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist
from rm_msgs.msg import WheelLegCmd

class WheelLegController(Node):
    def __init__(self):
        super().__init__('wheel_leg_controller')
        
        self.cmd_pub = self.create_publisher(WheelLegCmd, '/actuator_cmd', 10)
        
        self.create_subscription(JointState, '/joint_states', self.joint_cb, 10)
        self.create_subscription(Imu, '/imu', self.imu_cb, 10)
        self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_cb, 10)
        
        self.timer = self.create_timer(0.002, self.control_loop)
        
        self.current_joint_state = None
        self.target_vel_x = 0.0

    def joint_cb(self, msg):
        self.current_joint_state = msg

    def imu_cb(self, msg):
        pass

    def cmd_vel_cb(self, msg):
        self.target_vel_x = msg.linear.x

    def control_loop(self):
        if self.current_joint_state is None:
            return

        cmd = WheelLegCmd()
        
        cmd.right_phi1 = 0.0
        cmd.right_phi4 = 0.0
        cmd.left_phi1 = 0.0
        cmd.left_phi4 = 0.0
        
        cmd.right_wheel = 0.1 
        cmd.left_wheel = 0.1 
        
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = WheelLegController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
