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





from ....utils import linalg2_util as linalg
from ..views.controllers_views.avoid_obstacles_controller_view import AvoidObstaclesControllerView
from ..views.controllers_views.follow_wall_controller_view import FollowWallControllerView
from ..views.controllers_views.go_to_goal_controller_view import GoToGoalControllerView
from ..views.controllers_views.gtg_and_ao_controller_view import GTGAndAOControllerView
from ..supervisor.supervisor import ControlState
from ....views.supervisor_view import SupervisorView

class KheperaiiiSupervisorView(SupervisorView):

  def __init__( self, viewer, supervisor, robot_geometry ):
    self.viewer = viewer
    self.supervisor = supervisor
    self.supervisor_state_machine = supervisor.state_machine

    # controller views
    self.go_to_goal_controller_view = GoToGoalControllerView( viewer,
                                                              supervisor )
    self.avoid_obstacles_controller_view = AvoidObstaclesControllerView( viewer,
                                                                         supervisor )
    self.gtg_and_ao_controller_view = GTGAndAOControllerView( viewer,
                                                              supervisor )
    self.follow_wall_controller_view = FollowWallControllerView(  viewer,
                                                                  supervisor )

    # additional information for rendering
    self.robot_geometry = robot_geometry      # robot geometry
    self.robot_estimated_traverse_path = []   # path taken by robot's internal image

 
  # draw the current controller's state to the frame
  def _draw_current_controller_to_frame( self , ref_pose = [0.0, 0.0] ):
    current_state = self.supervisor_state_machine.current_state
    if current_state == ControlState.GO_TO_GOAL:
      self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame(ref_pose)
    elif current_state == ControlState.AVOID_OBSTACLES:
      self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame(ref_pose)
    elif current_state == ControlState.GTG_AND_AO:
      self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame(ref_pose)
    elif current_state in [ ControlState.SLIDE_LEFT, ControlState.SLIDE_RIGHT ]:
      self.follow_wall_controller_view.draw_active_follow_wall_controller_to_frame(ref_pose)

  # draw all of the controllers's to the frame
  def _draw_all_controllers_to_frame( self , ref_pose = [0.0, 0.0] ):
    self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame( ref_pose )
    self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame( ref_pose )
    # self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame()
    self.follow_wall_controller_view.draw_complete_follow_wall_controller_to_frame( ref_pose )
