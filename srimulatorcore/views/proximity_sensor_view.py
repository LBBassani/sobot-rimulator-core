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





from math import sin, cos
from ..utils import linalg2_util as linalg

class ProximitySensorView:

  def __init__( self, viewer, proximity_sensor ):
    self.viewer = viewer
    self.proximity_sensor = proximity_sensor

  def draw_sensor_to_frame( self, ref_pose = [0.0, 0.0] ):
    proximity_sensor = self.proximity_sensor

    # grab proximity sensor pose values
    sensor_pos, sensor_theta = proximity_sensor.pose.vunpack()
    sensor_pos = list(sensor_pos)
    sensor_pos[0] = sensor_pos[0] - ref_pose[0]
    sensor_pos[1] = sensor_pos[1] - ref_pose[1]

    # build the sensor cone
    r = proximity_sensor.max_range
    phi = proximity_sensor.phi_view
    sensor_cone_poly = [ [0.0, 0.0],
                         [r*cos(-phi/2), r*sin(-phi/2)],
                         [r, 0.0],
                         [r*cos(phi/2), r*sin(phi/2)] ]
    sensor_cone_poly = linalg.rotate_and_translate_vectors( sensor_cone_poly,
                                                            sensor_theta,
                                                            sensor_pos )

    # shade the sensor cone according to positive detection
    if self.proximity_sensor.target_delta != None:
      alpha = 0.9 - 0.8*self.proximity_sensor.target_delta
    else:
      alpha = 0.1

    # add the sensor cone to the frame
    self.viewer.current_frame.add_polygons( [ sensor_cone_poly ],
                                            color = "red",
                                            alpha = alpha )

    # === FOR DEBUGGING: ===
    # self._draw_detector_line_to_frame()
    # self._draw_detector_line_origins_to_frame()
    # self._draw_bounding_circle_to_frame()
    # self._draw_detection_to_frame()

  def _draw_detection_to_frame( self , ref_pose = [0.0, 0.0]):
    target_delta = self.proximity_sensor.target_delta
    if target_delta != None:
      detector_endpoints = self.proximity_sensor.detector_line.vertexes
      detector_vector = linalg.sub( detector_endpoints[1], detector_endpoints[0] )
      target_vector = linalg.add( detector_endpoints[0], linalg.scale( detector_vector, target_delta ) )
      
      target_vector[0] = target_vector[0] - ref_pose[0]
      target_vector[1] = target_vector[1] - ref_pose[1]
      self.viewer.current_frame.add_circle( pos = target_vector,
                                            radius = 0.02,
                                            color = "black",
                                            alpha = 0.7 )
  
  def _draw_detector_line_to_frame( self , ref_pose = [0.0, 0.0]):
    vertexes = list(self.proximity_sensor.detector_line.vertexes)
    vertexes = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vertexes ) )
    self.viewer.current_frame.add_lines(  [ vertexes ],
                                          linewidth = 0.005,
                                          color = "black",
                                          alpha = 0.7 )

  def _draw_detector_line_origins_to_frame( self , ref_pose = [0.0, 0.0]):
    origin = self.proximity_sensor.detector_line.vertexes[0]
    self.viewer.current_frame.add_circle( pos = (origin[0] - ref_pose[0], origin[1] - ref_pose[1]),
                                          radius = 0.02,
                                          color = "black" )

  def _draw_bounding_circle_to_frame( self , ref_pose = [0.0, 0.0]):
    c, r = self.proximity_sensor.detector_line.bounding_circle
    c = list(c)
    c[0] = c[0] - ref_pose[0]
    c[1] = c[1] - ref_pose[1]
    self.viewer.current_frame.add_circle( pos = c,
                                          radius = r,
                                          color = "black",
                                          alpha = 0.2 )
    self.viewer.current_frame.add_circle( pos = c,
                                          radius = 0.005,
                                          color = "black",
                                          alpha = 0.3 )
