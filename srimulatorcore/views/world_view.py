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





from .obstacle_view import ObstacleView
from .robot_view import RobotView

class WorldView:

  def __init__( self, world, viewer ):
    # bind the viewer
    self.viewer = viewer
    
    # initialize views for world objects
    self.robot_views = []
    for robot in world.robots: self.add_robot( robot )

    self.obstacle_views = []
    for obstacle in world.obstacles: self.add_obstacle( obstacle )

  def add_robot( self, robot ):
    robot_view = RobotView( self.viewer, robot )
    self.robot_views.append( robot_view )

  def add_obstacle( self, obstacle ):
    obstacle_view = ObstacleView( self.viewer, obstacle )
    self.obstacle_views.append( obstacle_view )

  def draw_world_to_frame( self , ref_pose = [0.0, 0.0]):    
    # draw all the robots
    for robot_view in self.robot_views:
      robot_view.draw_robot_to_frame( ref_pose )
    # draw all the obstacles
    for obstacle_view in self.obstacle_views:
      obstacle_view.draw_obstacle_to_frame( ref_pose )

