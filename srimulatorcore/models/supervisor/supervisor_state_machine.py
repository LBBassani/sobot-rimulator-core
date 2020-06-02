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

from enum import Enum

class Condition(Enum):
  pass

class State(Enum):
  pass

class SupervisorStateMachine:

  def __init__( self , states , conditions ):
    self.supervisor = None
    self.states = states
    self.conditions = conditions
    
  def update_state( self ):
    raise(NotImplementedError)

  # === STATE PROCEDURES ===
  def execute_state( self , state):
    raise(NotImplementedError)

  # === STATE TRANSITIONS ===
  def transition_to_state( self , state):
    raise(NotImplementedError)

  # === CONDITIONS ===
  def is_condition_true( self , condition):
    raise(NotImplementedError)
    

  # === FOR DEBUGGING ===
  def _print_debug_info( self ):
    print ("\n ======== \n")
    print ("STATES: ")
    for state in self.states:
      print(state.name)
    print ("")
    print ("CONDITIONS:")
    for condition in self.conditions:
      print(condition.name, ":", self.is_condition_true(condition))
