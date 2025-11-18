import rclpy
from rclpy.node import Node
# 1. my_package에서 서비스 인터페이스 임포트
from my_interface.srv import StringService 

class StringServiceServer(Node):

    def __init__(self):
        super().__init__('string_service_server_node')
        
        # 2. 서비스 서버 생성: 서비스 타입, 서비스 이름, 콜백 함수 지정
        self.srv = self.create_service(
            StringService, 
            'string_manipulation',  # 서비스 이름
            self.string_manipulation_callback
        )
        self.get_logger().info('✅ String Service Server is Ready.')

    def string_manipulation_callback(self, request, response):
        """요청 문자열을 받아 응답 문자열을 처리하는 콜백 함수"""
        
        input_str = request.input_string
        self.get_logger().info(f'📦 Incoming Request: "{input_str}"')
        
        # 요청 문자열을 대문자로 변환
        processed_str = input_str.upper() 
        
        # 응답 객체에 결과 문자열 저장
        response.output_string = processed_str
        
        self.get_logger().info(f'📤 Sending Response: "{processed_str}"')
        
        # 응답 객체 반환
        return response

def main(args=None):
    rclpy.init(args=args)
    server_node = StringServiceServer()
    try:
        rclpy.spin(server_node)
    except KeyboardInterrupt:
        pass
    server_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()