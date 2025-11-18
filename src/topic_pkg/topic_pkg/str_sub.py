import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 문자열 메시지 타입

class StringSubscriber(Node):

    def __init__(self):
        super().__init__('string_subscriber')
        # 토픽 이름: 'chatter' (퍼블리셔와 동일해야 함)
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # 수신된 문자열 출력 (%s 사용)
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    string_subscriber = StringSubscriber()
    rclpy.spin(string_subscriber)
    
    string_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()