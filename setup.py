from setuptools import find_packages, setup

package_name = 'mqtt_pkg'

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
    maintainer='innovedex',
    maintainer_email='innovedex@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'pub_led = mqtt_pkg.pub_led:main',
        'pub_servo = mqtt_pkg.pub_servo:main',
        'sub_button = mqtt_pkg.sub_button:main',
        'sub_button_pub_turtle = mqtt_pkg.sub_button_pub_turtle:main',
        ],
    },
)
