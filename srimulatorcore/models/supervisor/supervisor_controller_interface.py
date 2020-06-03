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


# an interfacing allowing a controller to interact with its supervisor 
class SupervisorControllerInterface:

  def __init__( self, supervisor ):
    self.supervisor = supervisor

  # get the current control state
  def current_state( self ):
    raise(NotImplementedError)

  # get the supervisor's internal pose estimation
  def estimated_pose( self ):
    raise(NotImplementedError)

  # get the placement poses of the robot's sensors
  def sensor_placements( self , sensor):
    raise(NotImplementedError)

  # get the velocity limit of the supervisor
  def v_max( self ):
    raise(NotImplementedError)

  # get the supervisor's goal
  def goal( self ):
    raise(NotImplementedError)

  # get the supervisor's internal clock time
  def time( self ):
    return self.supervisor.time

  # set the outputs of the supervisor
  def set_outputs( self, **kwargs ):
    raise(NotImplementedError)