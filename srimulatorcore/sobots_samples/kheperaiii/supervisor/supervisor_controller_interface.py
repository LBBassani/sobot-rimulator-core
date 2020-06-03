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


from ....models.supervisor.supervisor_controller_interface import SupervisorControllerInterface
from ....models.sensors.proximity_sensor import ProximitySensor

# an interfacing allowing a controller to interact with its supervisor 
class KheperaiiiSupervisorControllerInterface(SupervisorControllerInterface):

  def __init__( self, supervisor ):
    self.supervisor = supervisor

  # get the current control state
  def current_state( self ):
    return self.supervisor.state_machine.current_state

  # get the supervisor's internal pose estimation
  def estimated_pose( self ):
    return self.supervisor.estimated_pose

  # get the placement poses of the robot's sensors
  def proximity_sensor_placements( self ):
    return self.supervisor.proximity_sensor_placements

  # get the robot's proximity sensor read values converted to real distances in meters
  def proximity_sensor_distances( self ):
    return self.supervisor.proximity_sensor_distances

  # get true/false indicators for which sensors are actually detecting obstacles
  def proximity_sensor_positive_detections( self ):
    sensor_range = self.supervisor.proximity_sensor_max_range
    return [ d < sensor_range - 0.001 for d in self.proximity_sensor_distances() ]

  # get the velocity limit of the supervisor
  def v_max( self ):
    return self.supervisor.v_max

  # get the supervisor's goal
  def goal( self ):
    return self.supervisor.goal

  # get the supervisor's internal clock time
  def time( self ):
    return self.supervisor.time

  # set the outputs of the supervisor
  def set_outputs( self, **kwargs ):
    self.supervisor.v_output = kwargs.get('v')
    self.supervisor.omega_output = kwargs.get('omega')

  # get the placement poses of the robot's sensors
  def sensor_placements( self , sensor):
    if type(sensor) is ProximitySensor:
      return self.proximity_sensor_placements()
    else :
      raise Exception(" Not valid Sensor Type")
