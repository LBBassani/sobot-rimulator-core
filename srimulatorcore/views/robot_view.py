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


from ..utils import linalg2_util as linalg
from .proximity_sensor_view import ProximitySensorView
from .supervisor_view import SupervisorView


class RobotView:
  
  def __init__( self, viewer, robot ):
    self.viewer = viewer
    self.robot = robot

    # add the supervisor views for this robot
    self.supervisor_view = robot.supervisor.make_view( viewer, robot.supervisor, robot.geometry )
    
    # add the IR sensor views for this robot
    self.ir_sensor_views = []
    for ir_sensor in robot.ir_sensors:
      self.ir_sensor_views.append( ProximitySensorView( viewer, ir_sensor ) )

    self.traverse_path = []  # this robot's traverse path

  def draw_robot_to_frame( self , ref_pose = [0.0, 0.0]):
    # update the robot traverse path
    position = self.robot.pose.vposition()
    self.traverse_path.append( position )
    
    # draw the internal state ( supervisor ) to the frame
    self.supervisor_view.draw_supervisor_to_frame( ref_pose )

    # draw the IR sensors to the frame if indicated
    if self.viewer.draw_invisibles:
      for ir_sensor_view in self.ir_sensor_views:
        ir_sensor_view.draw_sensor_to_frame( ref_pose )

    # draw the robot
    robot_bottom = list(self.robot.global_geometry.vertexes)
    robot_bottom = list ( map (lambda x : [x[0] - ref_pose[0] , x[1] - ref_pose[1] ] , robot_bottom ) )
    self.viewer.current_frame.add_polygons( [ robot_bottom ],
                                            color = "blue",
                                            alpha = 0.5 ) 
    # add decoration
    robot_pos, robot_theta = self.robot.pose.vunpack()
    robot_top = linalg.rotate_and_translate_vectors( self.robot.get_top_plate(), robot_theta, robot_pos )
    robot_top = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] ,robot_top ) )
    self.viewer.current_frame.add_polygons( [ robot_top ],
                                            color = "black",
                                            alpha = 0.5 )
    
    # draw the robot's traverse path if indicated
    if self.viewer.draw_invisibles:
      self._draw_traverse_path_to_frame( ref_pose )

  def _draw_traverse_path_to_frame( self , ref_pose = [0.0, 0.0] ):
    path = list( map( lambda x : [ x[0] - ref_pose[0] , x[1] - ref_pose[1] ] , self.traverse_path ) )
    self.viewer.current_frame.add_lines(  [ path ],
                                          color = "black",
                                          linewidth = 0.01 )

  # draws the traverse path as dots weighted according to robot speed
  def _draw_rich_traverse_path_to_frame( self , ref_pose = [0.0, 0.0]):
    # when robot is moving fast, draw small, opaque dots
    # when robot is moving slow, draw large, transparent dots
    d_min,  d_max = 0.0, 0.01574  # possible distances between dots
    r_min,  r_max = 0.007, 0.02   # dot radius
    a_min,  a_max = 0.3, 0.55     # dot alpha value
    m_r = ( r_max - r_min ) / ( d_min - d_max )
    b_r = r_max - m_r*d_min
    m_a = ( a_max - a_min ) / ( r_min - r_max )
    b_a = a_max - m_a*r_min
    
    prev_posn = self.traverse_path[0]
    frame = self.viewer.current_frame
    for posn in self.traverse_path[1::1]:
      d = linalg.distance( posn, prev_posn )
      r = ( m_r*d ) + b_r
      a = ( m_a*r ) + b_a
      frame.add_circle( pos = posn,
                        radius = r,
                        color = "black",
                        alpha = a)

      prev_posn = posn
