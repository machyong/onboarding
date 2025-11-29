<aside>
💡

### 주의사항!!

```bash
**저도 gpt씁니다. 제 코드가 명확한 정답이 아니며 하다가 막힐 시 참고용으로 사용하세요.**
```

</aside>

### 1. 숫자 토픽 주고받기

1. 토픽 패키지 생성

```bash
ros2 pkg create topic_pkg --build-type ament_python --dependencies rclpy std_msgs 
```

1. publish코드 만들기

num_pub.py

```python
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

```

1. subscribe 코드 만들기

num_sub.py

```python
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
```

1. [setup.py](http://setup.py) 수정
    
    ![image.png](attachment:23ba0925-b8d9-44c9-a114-27189e585983:image.png)
    

```python
    entry_points={
        'console_scripts': [
        # [실행 파일 이름] = [패키지 이름].[모듈 이름]:[함수 이름]
        'num_pub = topic_pkg.num_pub:main',
        'num_sub = topic_pkg.num_sub:main',
        ],
    },
```

### 2. 타이머 콜백 추가

1. 타이머 콜백 추가된 py파일 생성

num_pub_timer.py

```python
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
```

1. [setup.py](http://setup.py) 수정

```python
    entry_points={
        'console_scripts': [
        # [실행 파일 이름] = [패키지 이름].[모듈 이름]:[함수 이름]
        'num_pub = topic_pkg.num_pub:main',
        'num_sub = topic_pkg.num_sub:main',
        # 추가
        'num_pub_timer = topic_pkg.num_pub_timer:main',
        ],
    },
)
```

### 3. 서로 다른 컴퓨터 간의 토픽 주고 받기

1. 서로 같은 인터넷 연결망에 들어가 있어야 한다.
2. ip 확인

```bash
ifconfig
```

![image.png](attachment:7fe23078-b394-4008-a5f7-e370cae6b3d1:image.png)

1. ping test

```bash
ping 192.168.0.4 # 상대방의 ip adress 입력
```

1. 주고받을 topic간의 데이터 타입, 토픽 이름 확인
2. 한쪽은 pub, 한쪽은 sub 실행

### 4. 문자 토픽 주고받기

1. publish 노드 생성

srt_pub.py

```python
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
```

2subscribe 노드 생성

str_sub.py

```python
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
```

1. setup.py수정

```python
    entry_points={
        'console_scripts': [
        # [실행 파일 이름] = [패키지 이름].[모듈 이름]:[함수 이름]
        'num_pub = topic_pkg.num_pub:main',
        'num_sub = topic_pkg.num_sub:main',
        'num_pub_timer = topic_pkg.num_pub_timer:main',
        # 추가
        'str_pub = topic_pkg.str_pub:main',
        'str_sub = topic_pkg.str_sub:main',
        ],
    },
)
```

### 5. 숫자 서비스 주고 받기

1. 패키지 생성

```bash
ros2 pkg create --build-type ament_cmake my_interface
```

1. service interface 생성

my_interface/srv/StringService.srv

```
# 요청 (Request)
string input_string
---
# 응답 (Response)
string output_string
```

3. Cmake_list.txt 수정

```
cmake_minimum_required(VERSION 3.8)
project(my_interface)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED) # 이 줄을 추가
find_package(std_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# 추가
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/StringService.srv"
  DEPENDENCIES std_msgs # 필요하다면 ROS 기본 메시지 타입 의존성을 추가합니다.
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 3. 설치 명령에 인터페이스 파일 추가 (설치 부분)
install(
  DIRECTORY include
  DESTINATION share/${PROJECT_NAME}
)

# 아래와 같이 서비스 파일을 설치 목록에 추가합니다.
install(
  FILES
    srv/StringService.srv
  DESTINATION share/${PROJECT_NAME}/srv
)

ament_package()
```

4. packge.xml 수정

```
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_interface</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="lhybio07@gmail.com">yong</maintainer>
  <license>TODO: License declaration</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  # 빌드 시 필요
  <build_depend>rosidl_default_generators</build_depend>
  <build_depend>std_msgs</build_depend>
  # 실행 시 필요
  <exec_depend>rosidl_default_runtime</exec_depend>
  <exec_depend>std_msgs</exec_depend>

  # 이 패키지가 인터페이스를 포함하고 있음을 명시
  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>

```

5. service pkg 이동

1. clinent 노드 생성

str_cli.py

```python
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
```

7. server 노드 생성

str_serv.py

```python
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
```

1. package.xml수정

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>service_pkg</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="lhybio07@gmail.com">yong</maintainer>
  <license>TODO: License declaration</license>

  <depend>rclpy</depend>
  <depend>example_interfaces</depend>
  <depend>my_interface</depend>
  <exec_depend>rosidl_default_runtime</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>
  

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>

```

9. setup.cfg 수정

```xml
[develop]
script_dir=$base/lib/service_pkg
[install]
install_scripts=$base/lib/service_pkg
# 여기가 추가 쓰실 때 주석은 빼 주세요.
[entry_points]
console_scripts =
    string_server = string_tools.server_node:main
    string_client = string_tools.client_node:main

```

[10.setup.py](http://10.setup.py) 수정

```python
    entry_points={
        'console_scripts': [
        'num_cli = service_pkg.num_cli:main',
        'num_serv = service_pkg.num_serv:main',
        # 추가
        'str_cli = service_pkg.str_cli:main',
        'str_serv = service_pkg.str_serv:main',
        ],
    } 
```

github 참조

[Git 연동 및 사용 (Ubuntu+VSCode)](https://www.notion.so/Git-Ubuntu-VSCode-209a666db85481ec964bef510326b717?pvs=21) 

[Github token 받기](https://www.notion.so/Github-token-2af6dc09a30a80739100c17a8d1945f2?pvs=21)

답지 깃허브

https://github.com/machyong/onboarding.git
