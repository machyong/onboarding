import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 문자열 메시지 타입

class StringPublisher(Node):

    def __init__(self):
        super().__init__('string_publisher')
        # 토픽 이름: 'chatter', 큐 사이즈: 10
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        
        # 1초마다 timer_callback 실행
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        # 문자열 데이터 할당
        msg.data = 'Hello World: %d' % self.i
        
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    string_publisher = StringPublisher()
    rclpy.spin(string_publisher)
    
    string_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()