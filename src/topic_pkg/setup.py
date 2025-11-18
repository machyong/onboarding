from setuptools import find_packages, setup

package_name = 'topic_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yong',
    maintainer_email='lhybio07@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
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
