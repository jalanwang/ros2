from setuptools import find_packages, setup

package_name = 'my_move_turtle_pkg'

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
    maintainer='robot',
    maintainer_email='jalanwang@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    # entry_points: setuptools entry points for creating command-line scripts.
    # 'console_scripts' 항목은 설치 시 실행 가능한 커맨드(스크립트)를 생성합니다.
    # 형식: '<스크립트이름> = <모듈경로>:<콜러블>'
    # 예: 아래 설정은 패키지를 설치한 후 `move_turtle` 명령을 실행하면
    # `my_move_turtle_pkg.move_turtle` 모듈의 `main()` 함수를 호출합니다.
    entry_points={
        'console_scripts': [
            # `move_turtle` 명령 -> my_move_turtle_pkg.move_turtle:main()
            'move_turtle = my_move_turtle_pkg.move_turtle:main',
            #'turtle_cmd_and_pose = my_move_turtle_pkg.turtle_cmd_and_pose:main',
            #'turtle_cmd_and_pose = my_move_turtle_pkg.turtle_cmd_and_pose1:main',
            'turtle_cmd_and_pose = my_move_turtle_pkg.turtle_cmd_and_pose2:main',
            #'my_service_server = my_move_turtle_pkg.my_service_server:main',
            #'my_service_server = my_move_turtle_pkg.my_service_server1:main',
            #'my_service_server = my_move_turtle_pkg.my_service_server2:main',
            'my_service_server = my_move_turtle_pkg.my_service_server3:main',
            #'dist_turtle_action_server = my_move_turtle_pkg.dist_turtle_action_server:main',
            'dist_turtle_action_server = my_move_turtle_pkg.dist_turtle_action_server1:main',
            'turtlesim_subscriber = my_move_turtle_pkg.turtlesim_subscriber:main',
            'my_multi_thread = my_move_turtle_pkg.my_multi_thread:main',

        ],
    },
)
