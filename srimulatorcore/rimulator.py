
import pygtk
pygtk.require( '2.0' )
import gtk
import gobject

# import default robot kherepa III
from .sobots_samples.kheperaiii.kheperaiii import Kheperaiii

# import gui classes
from .gui.viewer import Viewer
from .gui.frame import Frame

from .models.map.map_manager import MapManager
from .models.robot.robot import Robot
from .models.world.world import World

from .views.world_view import WorldView

from .sim_exceptions.collision_exception import CollisionException
from .sim_exceptions.goal_reached_exception import GoalReachedException

REFRESH_RATE = 20.0 # hertz

class Rimulator:

  def __init__( self, robot_types = [(Kheperaiii, (0,0))] ):

    self.is_running = False
    self.robot_types = robot_types

    # create the GUI
    self.viewer = Viewer( self )
    
    # create the map manager
    self.map_manager = MapManager()
    
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds
    
    # gtk simulation event source - for simulation control
    self.sim_event_source = gobject.idle_add( self.initialize_sim, True ) # we use this opportunity to initialize the sim
    
    
    
  def initialize_sim( self, random=False ):
    # reset the viewer
    self.viewer.control_panel_state_init()
    
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
    
    # create the world view
    self.world_view = WorldView( self.world, self.viewer )
    
    # render the initial world
    self.draw_world()
    
    
  def play_sim( self ):
    self.is_running = True
    self._run_sim()
    self.viewer.control_panel_state_playing()
    
    
  def pause_sim( self ):
    if self.is_running:
      self.is_running = False
      gobject.source_remove( self.sim_event_source )
      self.viewer.control_panel_state_paused()
    
    
  def step_sim_once( self ):
    if self.is_running:
      self.pause_sim()
    self._step_sim()
    
    
  def end_sim( self, alert_text='' ):
    self.is_running = False
    gobject.source_remove( self.sim_event_source )
    self.viewer.control_panel_state_finished( alert_text )
    
    
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
    
    
  def draw_world( self ):
    self.viewer.new_frame()                 # start a fresh frame
    self.world_view.draw_world_to_frame(self.world.robots[0].pose.vposition())   # draw the world onto the frame
    self.viewer.draw_frame()                # render the frame
    
    
  def _run_sim( self ):
    self.sim_event_source = gobject.timeout_add( int( self.period * 1000 ), self._run_sim )
    self._step_sim()
    
    
  def _step_sim( self ):
    # increment the simulation
    try:
      self.world.step()
    except CollisionException:
      self.end_sim( 'Collision!' )
    except GoalReachedException:
      self.end_sim( 'Goal Reached!' )
      
    # draw the resulting world
    self.draw_world()

  def start_sobot_rimulator(self):
    # start gtk
    gtk.main()

  def update_robot(self , robot_type):
    robot, rposition = robot_type
    robot = robot()
    robot.update_position(rposition[0], rposition[1])
    self.world.add_robot( robot )
  
  def add_robot(self, robot_type):
    self.robot_types.append(robot_type)