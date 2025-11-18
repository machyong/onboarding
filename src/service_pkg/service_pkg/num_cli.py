import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        # 클라이언트 생성
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # 1초마다 서비스가 준비되었는지 확인
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        # 요청 객체 생성 및 고정 값 설정
        self.req = AddTwoInts.Request()
        self.a = 7
        self.b = 12

    def send_request(self, a, b):
        # 함수 인자로 a, b를 받지만, 내부적으로는 self.a, self.b를 사용하도록 작성하셨습니다.
        self.req.a = self.a
        self.req.b = self.b
        
        # 비동기 요청 전송 (결과는 future 객체로 받음)
        self.future = self.cli.call_async(self.req)
        
        # 결과를 받을 때까지 대기 (Blocking)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()

    # send_request 함수 정의에 인자 2개가 필요하므로 넣어줍니다.
    # (작성하신 로직상 여기 숫자가 무엇이든 7+12가 실행됩니다)
    response = minimal_client.send_request(minimal_client.a, minimal_client.b)
    
    minimal_client.get_logger().info(
        'Result of add_two_ints: %d + %d = %d' %
        (minimal_client.a, minimal_client.b, response.sum))

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()