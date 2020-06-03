# Sobot Rimulator - A Robot Programming Tool (Modified Version)
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# Modified by Lorena B. Bassani
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email lorenabassani12@gmail.com for questions, comments, or to report bugs.


from math import sin, cos, pi, log, radians

from ....utils import linalg2_util as linalg
from ....utils.pose import Pose
from .supervisor_controller_interface import KheperaiiiSupervisorControllerInterface
from .supervisor_state_machine import KheperaiiiSupervisorStateMachine, ControlState
from ....models.supervisor.supervisor import Supervisor

from ..controllers.avoid_obstacles_controller import KheperaiiiAvoidObstaclesController
from ..controllers.follow_wall_controller import KheperaiiiFollowWallController
from ..controllers.go_to_angle_controller import KheperaiiiGoToAngleController
from ..controllers.go_to_goal_controller import KheperaiiiGoToGoalController
from ..controllers.gtg_and_ao_controller import KheperaiiiGTGAndAOController

from ..views.supervisor_view import KheperaiiiSupervisorView

# control parameters
K3_TRANS_VEL_LIMIT = 0.3148     # m/s
K3_ANG_VEL_LIMIT = 2.2763       # rad/s

class KheperaiiiSupervisor(Supervisor):

  def __init__( self, robot_interface,                            # the interface through which this supervisor will interact with the robot
                      wheel_radius,                               # the radius of a drive wheel on the robot
                      wheel_base_length,                          # the robot's wheel base
                      wheel_encoder_ticks_per_rev,                # the number of wheel encoder ticks per revolution of a drive wheel
                      sensor_placements,                          # placement pose of the sensors on the robot body
                      sensor_range,
                      goal = [ 0.0, 0.0 ],                        # the goal to which this supervisor will guide the robot
                      initial_pose_args = [ 0.0, 0.0, 0.0 ] ):    # the pose the robot will have when control begins
    
    # internal clock time in seconds
    self.time = 0.0

    # robot representation
    # NOTE: the supervisor does NOT have access to the physical robot, only the robot's interface
    self.robot = robot_interface

    # proximity sensor information
    self.proximity_sensor_placements = [ Pose( rawpose[0], rawpose[1], radians( rawpose[2] ) ) for rawpose in sensor_placements ]
    self.proximity_sensor_max_range = sensor_range

    # odometry information
    self.robot_wheel_radius = wheel_radius
    self.robot_wheel_base_length = wheel_base_length
    self.wheel_encoder_ticks_per_revolution = wheel_encoder_ticks_per_rev
    self.prev_ticks_left = 0
    self.prev_ticks_right = 0

    # controllers
    self.controllers = list()
    controller_interface = KheperaiiiSupervisorControllerInterface( self )
    self.go_to_angle_controller = KheperaiiiGoToAngleController( controller_interface )
    self.controllers.append(self.go_to_angle_controller)
    self.go_to_goal_controller = KheperaiiiGoToGoalController( controller_interface )
    self.controllers.append(self.go_to_goal_controller)
    self.avoid_obstacles_controller = KheperaiiiAvoidObstaclesController( controller_interface )
    self.controllers.append(self.avoid_obstacles_controller)
    self.gtg_and_ao_controller = KheperaiiiGTGAndAOController( controller_interface )
    self.controllers.append(self.gtg_and_ao_controller)
    self.follow_wall_controller = KheperaiiiFollowWallController( controller_interface )
    self.controllers.append(self.follow_wall_controller)

    # state machine
    self.state_machine = KheperaiiiSupervisorStateMachine( self )

    # state
    self.proximity_sensor_distances = [ 0.0, 0.0 ] * len( sensor_placements )   # sensor distances
    self.estimated_pose = Pose( *initial_pose_args )                            # estimated pose
    self.current_controller = self.go_to_goal_controller                        # current controller

    # goal
    self.goal = goal

    # control bounds
    self.v_max = K3_TRANS_VEL_LIMIT
    self.omega_max = K3_ANG_VEL_LIMIT

    # CONTROL OUTPUTS - UNICYCLE
    self.v_output = 0.0
    self.omega_output = 0.0


  # update the estimated robot state and the control state
  def update_state( self ):
    # update estimated robot state from sensor readings
    self._update_proximity_sensor_distances()
    self.update_odometry()
    
    # calculate new heading vectors for each controller
    self._update_controller_headings()

    # update the control state
    self.state_machine.update_state()
  
  # calculate updated heading vectors for the active controllers
  def _update_controller_headings( self ):
    self.go_to_goal_controller.update_heading()
    self.avoid_obstacles_controller.update_heading()
    self.gtg_and_ao_controller.update_heading()
    self.follow_wall_controller.update_heading()

  # update the distances indicated by the proximity sensors
  def _update_proximity_sensor_distances( self ):
    self.proximity_sensor_distances = [ 0.02-( log(readval/3960.0) )/30.0
                                        for readval in self.robot.read_proximity_sensors() ]

  # update the estimated position of the robot using it's wheel encoder readings
  def update_odometry( self ):
    R = self.robot_wheel_radius
    N = float( self.wheel_encoder_ticks_per_revolution )

    # read the wheel encoder values
    ticks_left, ticks_right = self.robot.read_wheel_encoders()

    # get the difference in ticks since the last iteration
    d_ticks_left = ticks_left - self.prev_ticks_left
    d_ticks_right = ticks_right - self.prev_ticks_right
    
    # estimate the wheel movements
    d_left_wheel = 2*pi*R*( d_ticks_left / N )
    d_right_wheel = 2*pi*R*( d_ticks_right / N )
    d_center = 0.5 * ( d_left_wheel + d_right_wheel )

    # calculate the new pose
    prev_x, prev_y, prev_theta = self.estimated_pose.sunpack()
    new_x = prev_x + ( d_center * cos( prev_theta ) )
    new_y = prev_y + ( d_center * sin( prev_theta ) )
    new_theta = prev_theta + ( ( d_right_wheel - d_left_wheel ) / self.robot_wheel_base_length )

    # update the pose estimate with the new values
    self.estimated_pose.supdate( new_x, new_y, new_theta )

    # save the current tick count for the next iteration
    self.prev_ticks_left = ticks_left
    self.prev_ticks_right = ticks_right

  # generate and send the correct commands to the robot
  def send_robot_commands( self ):
    # limit the speeds:
    v = max( min( self.v_output, self.v_max ), -self.v_max )
    omega = max( min( self.omega_output, self.omega_max ), -self.omega_max )

    # send the drive commands to the robot
    v_l, v_r = self._uni_to_diff( v, omega )
    self.robot.set_wheel_drive_rates( v_l, v_r )

  def _uni_to_diff( self, v, omega ):
    # v = translational velocity (m/s)
    # omega = angular velocity (rad/s)
    
    R = self.robot_wheel_radius
    L = self.robot_wheel_base_length
    
    v_l = ( (2.0 * v) - (omega*L) ) / (2.0 * R)
    v_r = ( (2.0 * v) + (omega*L) ) / (2.0 * R)
    
    return v_l, v_r
    
  def _diff_to_uni( self, v_l, v_r ):
    # v_l = left-wheel angular velocity (rad/s)
    # v_r = right-wheel angular velocity (rad/s)
    
    R = self.robot_wheel_radius
    L = self.robot_wheel_base_length
    
    v = ( R / 2.0 ) * ( v_r + v_l )
    omega = ( R / L ) * ( v_r - v_l )
    
    return v, omega

  def make_view(self, viewer, supervisor, geometry):
    return KheperaiiiSupervisorView(viewer, supervisor, geometry)