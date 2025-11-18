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
