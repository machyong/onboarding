import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # 서비스 타입 임포트

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        # 서비스 서버 생성
        # 타입: AddTwoInts, 이름: 'add_two_ints', 콜백: add_two_ints_callback
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        # 요청(request)으로 들어온 a와 b를 더해서 응답(response)의 sum에 넣음
        response.sum = request.a + request.b
        
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        # 처리된 응답 객체를 반환
        return response

def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()