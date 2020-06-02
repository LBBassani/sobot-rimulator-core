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
from ....sim_exceptions.goal_reached_exception import GoalReachedException

from ....models.supervisor.supervisor_state_machine import SupervisorStateMachine, State, Condition

class ControlState(State):
  AT_GOAL         = 0
  GO_TO_GOAL      = 1
  AVOID_OBSTACLES = 2
  GTG_AND_AO      = 3
  SLIDE_LEFT      = 4
  SLIDE_RIGHT     = 5

class ControlCondition(Condition):
  AT_OBSTACLE     = 0
  DANGER          = 1
  NO_OBSTACLE     = 2
  PROGRESS_MADE   = 3
  SLIDE_LEFT      = 4
  SLIDE_RIGHT     = 5
  AT_GOAL         = 6


# event parameters
D_STOP = 0.05     # meters from goal
D_CAUTION = 0.15  # meters from obstacle
D_DANGER = 0.04   # meters from obstacle

# progress margin
PROGRESS_EPSILON = 0.05

class KheperaiiiSupervisorStateMachine(SupervisorStateMachine):

  def __init__( self, supervisor ):

    self.supervisor = supervisor

    # initialize state
    self.transition_to_state(ControlState.GO_TO_GOAL)

    # progress tracking
    self.best_distance_to_goal = float( "inf" )

  def update_state( self ):
    self.execute_state(self.current_state)

  # === STATE PROCEDURES ===
  def execute_state( self , state):
    if state == ControlState.AT_GOAL : self.execute_state_go_to_goal()
    elif state == ControlState.AVOID_OBSTACLES : self.execute_state_avoid_obstacles()
    elif state == ControlState.GO_TO_GOAL : self.execute_state_go_to_goal()
    elif state == ControlState.SLIDE_LEFT : self.execute_state_slide_left()
    elif state == ControlState.SLIDE_RIGHT : self.execute_state_slide_right()
    else: raise Exception( "undefined supervisor state or behavior" )


  def execute_state_go_to_goal( self ):
    if self.is_condition_true(ControlCondition.AT_GOAL):        
      self.transition_to_state(ControlState.AT_GOAL)
    elif self.is_condition_true(ControlCondition.DANGER):       self.transition_to_state(ControlState.AVOID_OBSTACLES)
    elif self.is_condition_true(ControlCondition.AT_OBSTACLE):
      sl = self.is_condition_true(ControlCondition.SLIDE_LEFT)
      sr = self.is_condition_true(ControlCondition.SLIDE_RIGHT)
      if sl and not sr:                 self.transition_to_state(ControlState.SLIDE_LEFT)
      elif sr and not sl:               self.transition_to_state(ControlState.SLIDE_RIGHT)


  def execute_state_avoid_obstacles( self ):
    if self.is_condition_true(ControlCondition.AT_GOAL):        self.transition_to_state(ControlState.AT_GOAL)
    elif not self.is_condition_true(ControlCondition.DANGER):
      sl = self.is_condition_true(ControlCondition.SLIDE_LEFT)
      sr = self.is_condition_true(ControlCondition.SLIDE_RIGHT)
      if sl and not sr:                 self.transition_to_state(ControlState.SLIDE_LEFT)
      elif sr and not sl:               self.transition_to_state(ControlState.SLIDE_RIGHT)
      elif not sr and not sl:           self.transition_to_state(ControlState.GO_TO_GOAL)
      # else: raise Exception( "cannot determine slide direction" )

  def execute_state_slide_left( self ):
    if self.is_condition_true(ControlCondition.AT_GOAL):        self.transition_to_state_at_goal()
    elif self.is_condition_true(ControlCondition.DANGER):       self.transition_to_state_avoid_obstacles()
    elif self.is_condition_true(ControlCondition.PROGRESS_MADE) and not self.is_condition_true(ControlCondition.SLIDE_LEFT):
      self.transition_to_state(ControlState.GO_TO_GOAL)

  def execute_state_slide_right( self ):
    if self.is_condition_true(ControlCondition.AT_GOAL):        self.transition_to_state_at_goal()
    elif self.is_condition_true(ControlCondition.DANGER):       self.transition_to_state_avoid_obstacles()
    elif self.is_condition_true(ControlCondition.PROGRESS_MADE) and not self.is_condition_true(ControlCondition.SLIDE_RIGHT):
      self.transition_to_state(ControlState.GO_TO_GOAL)

  # def execute_state_gtg_and_ao( self ):
  #   if self.is_condition_true(ControlCondition.AT_GOAL):        self.transition_to_state_at_goal()
  #   elif self.is_condition_true(ControlCondition.DANGER):       self.transition_to_state_avoid_obstacles()
  #   elif self.is_condition_true(ControlCondition.NO_OBSTACLE):  self.transition_to_state(ControlState.GO_TO_GOAL)

  # === STATE TRANSITIONS ===
  def transition_to_state( self , state):
    if state == ControlState.GO_TO_GOAL : self.transition_to_state_go_to_goal()
    elif state == ControlState.GTG_AND_AO : self.transition_to_state_gtg_and_ao()
    elif state == ControlState.SLIDE_LEFT : self.transition_to_state_slide_left()
    elif state == ControlState.SLIDE_RIGHT : self.transition_to_state_slide_right()
    elif state == ControlState.AT_GOAL : self.transition_to_state_at_goal()
    elif state == ControlState.AVOID_OBSTACLES : self.transition_to_state_avoid_obstacles()
    else : raise Exception( "undefined supervisor state or behavior" )

  def transition_to_state_at_goal( self ):
    self.current_state = ControlState.AT_GOAL
    raise GoalReachedException()

  def transition_to_state_avoid_obstacles( self ):
    self.current_state = ControlState.AVOID_OBSTACLES
    self.supervisor.current_controller = self.supervisor.avoid_obstacles_controller

  def transition_to_state_go_to_goal( self ):
    self.current_state = ControlState.GO_TO_GOAL
    self.supervisor.current_controller = self.supervisor.go_to_goal_controller

  def transition_to_state_slide_left( self ):
    self.current_state = ControlState.SLIDE_LEFT
    self._update_best_distance_to_goal()
    self.supervisor.current_controller = self.supervisor.follow_wall_controller

  def transition_to_state_slide_right( self ):
    self.current_state = ControlState.SLIDE_RIGHT
    self._update_best_distance_to_goal()
    self.supervisor.current_controller = self.supervisor.follow_wall_controller

  def transition_to_state_gtg_and_ao( self ):
    self.current_state = ControlState.GTG_AND_AO
    self.supervisor.current_controller = self.supervisor.gtg_and_ao_controller


  # === CONDITIONS ===
  def is_condition_true( self , condition):
    if condition == ControlCondition.AT_GOAL : return self.condition_at_goal()
    elif condition == ControlCondition.AT_OBSTACLE : return self.condition_at_obstacle()
    elif condition == ControlCondition.DANGER : return self.condition_danger()
    elif condition == ControlCondition.NO_OBSTACLE : return self.condition_no_obstacle()
    elif condition == ControlCondition.PROGRESS_MADE : return self.condition_progress_made()
    elif condition == ControlCondition.SLIDE_LEFT : return self.condition_slide_left()
    elif condition == ControlCondition.SLIDE_RIGHT : return self.condition_slide_right()
    else : raise Exception( "undefined supervisor state or behavior" )

  def condition_at_goal( self ):
    return linalg.distance( self.supervisor.estimated_pose.vposition(), self.supervisor.goal ) < D_STOP

  def condition_at_obstacle( self ):
    for d in self._forward_sensor_distances():
      if d < D_CAUTION: return True
    return False

  def condition_danger( self ):
    for d in self._forward_sensor_distances():
      if d < D_DANGER: return True
    return False

  def condition_no_obstacle( self ):
    for d in self._forward_sensor_distances():
      if d < D_CAUTION: return False
    return True
   
  def condition_progress_made( self ):
    return self._distance_to_goal() < self.best_distance_to_goal - PROGRESS_EPSILON

  def condition_slide_left( self ):
    heading_gtg = self.supervisor.go_to_goal_controller.gtg_heading_vector
    heading_ao = self.supervisor.avoid_obstacles_controller.ao_heading_vector
    heading_fwl = self.supervisor.follow_wall_controller.l_fw_heading_vector

    ao_cross_fwl = linalg.cross( heading_ao, heading_fwl )
    fwl_cross_gtg = linalg.cross( heading_fwl, heading_gtg )
    ao_cross_gtg = linalg.cross( heading_ao, heading_gtg )

    return( ( ao_cross_gtg > 0.0 and ao_cross_fwl > 0.0 and fwl_cross_gtg > 0.0 ) or
            ( ao_cross_gtg <= 0.0 and ao_cross_fwl <= 0.0 and fwl_cross_gtg <= 0.0 ) )

  def condition_slide_right( self ):
    heading_gtg = self.supervisor.go_to_goal_controller.gtg_heading_vector
    heading_ao = self.supervisor.avoid_obstacles_controller.ao_heading_vector
    heading_fwr = self.supervisor.follow_wall_controller.r_fw_heading_vector

    ao_cross_fwr = linalg.cross( heading_ao, heading_fwr )
    fwr_cross_gtg = linalg.cross( heading_fwr, heading_gtg )
    ao_cross_gtg = linalg.cross( heading_ao, heading_gtg )

    return( ( ao_cross_gtg > 0.0 and ao_cross_fwr > 0.0 and fwr_cross_gtg > 0.0 ) or
            ( ao_cross_gtg <= 0.0 and ao_cross_fwr <= 0.0 and fwr_cross_gtg <= 0.0 ) )


  # === helper methods === 
  def _forward_sensor_distances( self ):
    return self.supervisor.proximity_sensor_distances[1:7]

  def _distance_to_goal( self ):
    return linalg.distance( self.supervisor.estimated_pose.vposition(), self.supervisor.goal ) 

  def _update_best_distance_to_goal( self ):
    self.best_distance_to_goal = min( self.best_distance_to_goal, self._distance_to_goal() )
    

  # === FOR DEBUGGING ===
  def _print_debug_info( self ):
    print ("\n ======== \n")
    print ("STATE: ", self.current_state)
    print ("")
    print ("CONDITIONS:")
    print ("At Obstacle: " + str( self.is_condition_true(ControlCondition.AT_OBSTACLE) ))
    print ("Danger: " + str( self.is_condition_true(ControlCondition.DANGER) ))
    print ("No Obstacle: " + str( self.is_condition_true(ControlCondition.NO_OBSTACLE) ))
    print ("Progress Made: " + str( self.is_condition_true(ControlCondition.PROGRESS_MADE) ) + " ( Best Dist: " + str( round( self.best_distance_to_goal, 3 ) ) + ", Current Dist: " + str( round( self._distance_to_goal(), 3 ) ) + " )")
    print ("Slide Left: " + str( self.is_condition_true(ControlCondition.SLIDE_LEFT) ))
    print ("Slide Right: " + str( self.is_condition_true(ControlCondition.SLIDE_RIGHT) ))
