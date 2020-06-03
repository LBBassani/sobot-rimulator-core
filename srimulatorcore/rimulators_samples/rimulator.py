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


# import default robot kherepa III
from ..sobots_samples.kheperaiii.kheperaiii import Kheperaiii

from ..models.map.map_manager import MapManager
from ..models.robot.robot import Robot
from ..models.world.world import World

from ..views.world_view import WorldView

from ..sim_exceptions.collision_exception import CollisionException
from ..sim_exceptions.goal_reached_exception import GoalReachedException

REFRESH_RATE = 20.0 # hertz

class Rimulator:

  def __init__( self, robot_types = [(Kheperaiii, (0,0))] ):

    self.is_running = False
    self.robot_types = robot_types

    self.viewer = None
    
    # create the map manager
    self.map_manager = MapManager()
    
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds
    
    
  def initialize_sim( self, random=False ):
    
    # create the simulation world
    self.world = World( self.period )
    
    # create the robot
    for robot_type in self.robot_types:
      self.update_robot(robot_type)
    
    # generate a random environment
    if random:
      self.map_manager.random_map( self.world )
    else:
      self.map_manager.apply_to_world( self.world )
    
    if self.viewer is None:
      raise Exception("No viewer assigned")
    # create the world view
    self.world_view = WorldView( self.world, self.viewer )
    
    # render the initial world
    self.draw_world()
    
    
  def play_sim( self ):
    self.is_running = True  
    
  def pause_sim( self ):
    if self.is_running:
      self.is_running = False
      return True
    return False   
    
  def step_sim_once( self ):
    if self.is_running:
      self.pause_sim()
    self.step_sim()
    
    
  def end_sim( self, alert_text='' ):
    self.pause_sim()
    
    
  def reset_sim( self ):
    self.pause_sim()
    self.initialize_sim()
    
    
  def save_map( self, filename ):
    self.map_manager.save_map( filename )
    
    
  def load_map( self, filename ):
    self.map_manager.load_map( filename )
    self.reset_sim()
    
    
  def random_map( self ):
    self.pause_sim()
    self.initialize_sim( random = True )
    
    
  def draw_world( self ):                # start a fresh frame
    self.world_view.draw_world_to_frame(self.world.robots[0].pose.vposition())   # draw the world onto the frame    


  def step_sim( self ):
    # increment the simulation
    self.world.step()
    

  def update_robot(self , robot_type):
    robot, rposition = robot_type
    robot = robot()
    robot.update_position(rposition[0], rposition[1])
    self.world.add_robot( robot )
  
  def add_robot(self, robot_type):
    self.robot_types.append(robot_type)

  def add_viewer(self, viewer):
    self.viewer = viewer