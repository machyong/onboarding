import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32 # Int32 메시지 타입 임포트
import time
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Int32, 'number_topic', 10)
        self.i = 0

    def pub_func(self):
        msg = Int32()
        msg.data = self.i # 메시지에 i 값을 담음
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data) # 발행 로그 출력
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()
    try:
        while rclpy.ok():
            minimal_publisher.pub_func()
            rclpy.spin_once(minimal_publisher, timeout_sec=0)

    except KeyboardInterrupt:
        pass

    # 노드 종료 정리
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
