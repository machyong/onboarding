import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32 # Int32 메시지 타입 임포트

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # 토픽 이름: 'number_topic', QOS 설정: 10
        # self.listener_callback 메서드를 콜백으로 설정
        self.subscription = self.create_subscription(
            Int32,
            'number_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # 수신된 데이터를 출력
        self.get_logger().info('I heard: "%d"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber) # 노드를 실행하고 수신된 데이터를 처리

    # 노드 종료
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()