"""
Flip node for differential drive robot.

PUBLISHERS:
  + /cmd_vel (geometry_msgs/Twist)
    - Publishes velocity commands to the robot.
"""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class Flip(Node):
    """
    Flip node for differential drive robot.

    Minimal flip node:
    - Starts moving forward in x
    - Every <flip_interval> seconds, reverse the direction (multiply by -1)
    - Publishes to <cmd_vel_topic> with speed <speed>

    """

    def __init__(self):
        """Initialize the flip node."""
        super().__init__('flip')

        # Params
        self.declare_parameter('cmd_vel_topic', 'cmd_vel')
        self.declare_parameter('speed', 1.0)
        self.declare_parameter('flip_interval', 3.0)

        cmd_topic = self.get_parameter('cmd_vel_topic').value
        self.speed = float(self.get_parameter('speed').value)
        self.flip_interval = float(self.get_parameter('flip_interval').value)

        # Publisher
        self.cmd_pub = self.create_publisher(Twist, cmd_topic, 10)

        self.direction = 1.0
        self.last_flip_time = self.get_clock().now()

        self.timer = self.create_timer(0.1, self.flip_callback)

        self.get_logger().info(
            f'flip node started '
            f'(speed={self.speed}, interval={self.flip_interval} sec)'
        )

    def flip_callback(self):
        """Flips direction and publishes velocity."""
        now = self.get_clock().now()
        elapsed = (now - self.last_flip_time).nanoseconds * 1e-9

        # ---------------- Begin_Citation [1] ----------------
        if elapsed >= self.flip_interval:
            self.direction *= -1.0
            self.last_flip_time = now
        # ---------------- End_Citation [1] ----------------

        # Publish velocity
        cmd = Twist()
        cmd.linear.x = self.speed * self.direction
        self.cmd_pub.publish(cmd)


def main(args=None):
    """Spins the node."""
    rclpy.init(args=args)
    node = Flip()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
