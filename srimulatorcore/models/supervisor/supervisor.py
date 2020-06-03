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

from ...utils import linalg2_util as linalg
from ...utils.pose import Pose
from .supervisor_controller_interface import SupervisorControllerInterface
from .supervisor_state_machine import SupervisorStateMachine


class Supervisor:

  def __init__(self):
    self.estimated_pose = None
    self.time = 0
    self.current_controller = None
    self.state_machine = None
    self.controllers = list()

  def make_view(self, viewer, supervisor, geometry ):
    raise(NotImplementedError)
  
  def update_position(self, x, y):
    self.estimated_pose.x = x
    self.estimated_pose.y = y

  # simulate this supervisor running for one time increment
  def step( self, dt ):
    # increment the internal clock time
    self.time += dt

    # NOTE: for simplicity, we assume that the onboard computer executes exactly one control loop for every simulation time increment
    # although technically this is not likely to be realistic, it is a good simplificiation

    # execute one full control loop
    self.execute()

  # execute one control loop
  def execute( self ):
    self.update_state()              # update state
    self.current_controller.execute() # apply the current controller
    self.send_robot_commands()       # output the generated control signals to the robot

  # update the estimated robot state and the control state
  def update_state( self ):
    raise(NotImplementedError)
  
  # update the estimated position of the robot
  def update_odometry( self ):
    raise(NotImplementedError)

  # generate and send the correct commands to the robot
  def send_robot_commands( self ):
   raise(NotImplementedError)
