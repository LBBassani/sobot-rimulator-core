# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
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
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.


class Robot:

  def __init__( self ):
    self.pose = Pose([0.0, 0.0, 0.0])
    self.supervisor = None
    self.global_geometry = None
    self.geometry = None

  # simulate the robot's motion over the given time interval
  def step_motion( self, dt ):
    raise(NotImplementedError)
  
  # set the drive rates (angular velocities) for this robot's wheels in rad/s 
  def set_wheel_drive_rates( self, v_l, v_r ):
    raise(NotImplementedError)

  def get_top_plate( self ):
    raise(NotImplementedError)

  def update_position( self, x, y):
    self.pose.x = x
    self.pose.y = y
    self.global_geometry = self.geometry.get_transformation_to_pose( self.pose )
    self.supervisor.update_position(x, y)