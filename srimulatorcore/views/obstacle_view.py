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

class ObstacleView:

  def __init__( self, viewer, obstacle ):
    self.viewer = viewer
    self.obstacle = obstacle

  def draw_obstacle_to_frame( self , ref_pose = [0.0, 0.0]):
    obstacle = self.obstacle

    # draw the obstacle to the frame
    obstacle_poly = list(obstacle.global_geometry.vertexes)
    obstacle_poly = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , obstacle_poly ) )
    self.viewer.current_frame.add_polygons( [ obstacle_poly ],
                                            color = "dark red",
                                            alpha = 0.4 )

    # === FOR DEBUGGING: ===
    # self._draw_bounding_circle_to_frame()

  def _draw_bounding_circle_to_frame( self , ref_pose = [0.0, 0.0]):
    c, r = self.obstacle.global_geometry.bounding_circle
    c = list(c)
    c[0] = c[0] - ref_pose[0]
    c[1] = c[1] - ref_pose[1]
    self.viewer.current_frame.add_circle( pos = c,
                                          radius = r,
                                          color = "black",
                                          alpha = 0.2 )
