import rclpy
from rclpy.node import Node
from rclpy.task import Future
# 1. my_package에서 서비스 인터페이스 임포트
from my_interface.srv import StringService 
import sys # 명령줄 인수를 사용하기 위함

class StringServiceClient(Node):

    def __init__(self):
        super().__init__('string_service_client_node')
        
        # 2. 서비스 클라이언트 생성: 서비스 타입, 서비스 이름 지정
        self.cli = self.create_client(
            StringService, 
            'string_manipulation' # 서버와 동일한 서비스 이름
        )
        
        # 3. 서비스 사용 가능 대기
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service is not available, waiting...')
        
        self.get_logger().info('✅ String Service Client is Ready.')
        
        # 요청 객체 생성
        self.request = StringService.Request()

    def send_request(self, input_str):
        """서비스 요청을 보내고 비동기 결과를 반환"""
        self.request.input_string = input_str
        # 비동기 호출
        self.future: Future = self.cli.call_async(self.request)
        return self.future

def main(args=None):
    rclpy.init(args=args)
    client_node = StringServiceClient()
    
    # 명령줄 인수가 없으면 기본 문자열 사용
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "default ros2 client message"
    
    client_node.get_logger().info(f'Requesting service with: "{input_text}"')

    # 서비스 요청 전송
    future = client_node.send_request(input_text)
    
    # 결과가 도착할 때까지 노드를 스핀
    rclpy.spin_until_future_complete(client_node, future)
    
    if future.result() is not None:
        response = future.result()
        client_node.get_logger().info(f'🌟 Received Response: "{response.output_string}"')
    else:
        client_node.get_logger().error(f'Service call failed: {future.exception()}')

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()