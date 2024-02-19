# Copyright 2020 ros2_control Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_path = get_package_share_directory("robot_controller")
    slam_toolbox_path = get_package_share_directory("slam_toolbox")

    slam_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            slam_toolbox_path, "launch"),
            "/online_sync_launch.py"]),
        launch_arguments={
            "use_sim_time": "false",
            "slam_params_file": os.path.join(pkg_path, "config", "mapper_params_online_sync.yaml"),
        }.items()
    )

    rviz_config_file = PathJoinSubstitution(
        [pkg_path, "rviz", "slam.rviz"]
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file]
    )

    robot_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path, "launch"),
                                       "/robot.launch.py"]),
        launch_arguments={"gui": "false"}.items()
    )

    return LaunchDescription([robot_node, rviz_node, slam_node])
