# ~/robot_ws/src/topic_service_action_rclpy_example/setup.py

import os
import glob

from setuptools import find_packages, setup

package_name = 'topic_service_action_rclpy_example'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob.glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'param'), glob.glob(os.path.join('param', '*.yaml'))),
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
    entry_points={
        'console_scripts': [
            'argument = topic_service_action_rclpy_example.argument:main',
            'calculator = topic_service_action_rclpy_example.calculator:main',
            'operator = topic_service_action_rclpy_example.operator:main',
            'checker = topic_service_action_rclpy_example.checker:main',

        ],
    },
)
