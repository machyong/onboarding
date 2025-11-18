from setuptools import find_packages, setup

package_name = 'service_pkg'

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
        'num_cli = service_pkg.num_cli:main',
        'num_serv = service_pkg.num_serv:main',
        # 추가
        'str_cli = service_pkg.str_cli:main',
        'str_serv = service_pkg.str_serv:main',
        ],
    }
)
