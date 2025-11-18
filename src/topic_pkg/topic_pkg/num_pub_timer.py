import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32 # Int32 메시지 타입 임포트

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # 토픽 이름: 'number_topic', QOS 설정: 10
        self.publisher_ = self.create_publisher(Int32, 'number_topic', 10)
        self.i = 0
        # 0.5초(500ms)마다 timer_callback 메서드를 호출
        timer_period = 0.5  
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Int32()
        msg.data = self.i # 메시지에 i 값을 담음
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data) # 발행 로그 출력
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher) # 노드를 실행하고 콜백 함수들을 처리

    # 노드 종료
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()