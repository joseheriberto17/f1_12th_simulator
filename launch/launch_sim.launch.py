# library to move between files and folders in the O.S.
import os

from ament_index_python.packages import get_package_share_directory

# libraries to define the Launch file and Function
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    # Incluir el archivo de lanzamiento robot_state_publisher, proporcionado por nuestro propio paquete. Forzar la activación del tiempo de simulación
    
    package_name='f1_12th_simulator_g01'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # Incluir el archivo de inicio de Gazebo, proporcionado por el paquete gazebo_ros
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Ejecuta el nodo spawner del paquete gazebo_ros. El nombre de la entidad no importa realmente si sólo tienes un único robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # Launch the Diff_Controller
    diff_drive_spawner = Node(
        package='controller_manager', 
        executable='spawner', 
        arguments=['diff_cont'])
		
		# Launch the Joint_Broadcaster
    joint_broad_spawner = Node(
        package='controller_manager', 
        executable='spawner', 
        arguments=['joint_broad'])
    
    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    
    twist_mux_node = Node(package='twist_mux', 
                    executable='twist_mux',
                    parameters=[twist_mux_params,{'use_sim_time': True}],
                    remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    )


    # Launch them all!
    return LaunchDescription([
        rsp,
        joystick,
        twist_mux_node,
        gazebo,
        spawn_entity,
		diff_drive_spawner,
        joint_broad_spawner
    ])