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

from .controllers_view import ControllerView

class SupervisorView:

  def __init__( self, viewer, supervisor, robot_geometry ):
    self.viewer = viewer
    self.supervisor = supervisor
    
    # controller views
    self.controllers_view = ControllerView(viewer, supervisor)
    # additional information for rendering
    self.robot_geometry = robot_geometry      # robot geometry
    self.robot_estimated_traverse_path = []   # path taken by robot's internal image

  # draw a representation of the supervisor's internal state to the frame
  def draw_supervisor_to_frame( self , ref_pose = [0.0, 0.0]):
    # update the estimated robot traverse path
    self.robot_estimated_traverse_path.append( self.supervisor.estimated_pose.vposition() )
    
    # draw the goal to frame
    self._draw_goal_to_frame( ref_pose )
    
    # draw the supervisor-generated data to frame if indicated
    if self.viewer.draw_invisibles:
      self._draw_robot_state_estimate_to_frame( ref_pose )
      self._draw_current_controller_to_frame( ref_pose )

    # === FOR DEBUGGING ===
    # self._draw_all_controllers_to_frame()

  def _draw_goal_to_frame( self , ref_pose = [0.0, 0.0]):
    goal = list(self.supervisor.goal)
    goal[0] = goal[0] - ref_pose[0]
    goal[1] = goal[1] - ref_pose[1]
    self.viewer.current_frame.add_circle( pos = goal,
                                          radius = 0.05,
                                          color = "dark green",
                                          alpha = 0.65 )
    self.viewer.current_frame.add_circle( pos = goal,
                                          radius = 0.01,
                                          color = "black",
                                          alpha = 0.5 )

  def _draw_robot_state_estimate_to_frame( self , ref_pose = [0.0, 0.0]):
    # draw the estimated position of the robot
    vertexes = self.robot_geometry.get_transformation_to_pose( self.supervisor.estimated_pose ).vertexes[:]
    vertexes.append( vertexes[0] )    # close the drawn polygon
    vertexes = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vertexes ) )
    self.viewer.current_frame.add_lines(  [ vertexes ],
                                          color = "black",
                                          linewidth = 0.0075,
                                          alpha = 0.5 )

    vertexes = list(self.robot_estimated_traverse_path)
    vertexes = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vertexes ) )
    # draw the estimated traverse path of the robot
    self.viewer.current_frame.add_lines(  [ vertexes ],
                                          linewidth = 0.005,
                                          color = "red",
                                          alpha = 0.5 )
  
  # draw the current controller's state to the frame
  def _draw_current_controller_to_frame( self , ref_pose = [0.0, 0.0]):
    current_controller = self.supervisor.current_controller
    self.controllers_view.draw_controller_to_frame(current_controller, ref_pose)

  # draw all of the controllers's to the frame
  def _draw_all_controllers_to_frame( self ,ref_pose = [0.0, 0.0] ):
    for controller in self.supervisor.controllers:
      self.controllers_view.draw_controller_to_frame(controller, ref_pose)
