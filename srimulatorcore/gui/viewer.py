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


# Abstract class Viewer
class Viewer:
  
  def __init__( self, simulator ):
    # bind the simulator
    self.simulator = simulator
    self.draw_invisibles = False
    
  def new_frame( self ):
    raise(NotImplementedError)
    
    
  def draw_frame( self , x = 0 , y = 0):
    raise(NotImplementedError)
    
    
  def control_panel_state_init( self ):
    raise(NotImplementedError)
    
    
  def control_panel_state_playing( self ):
    raise(NotImplementedError)
    
    
  def control_panel_state_paused( self ):
    raise(NotImplementedError)
    
    
  def control_panel_state_finished( self, alert_text ):
    raise(NotImplementedError)
    
    
  # EVENT HANDLERS:
  def on_play( self, widget ):
    self.simulator.play_sim()
    
  def on_stop( self, widget ):
    self.simulator.pause_sim()
    
    
  def on_step( self, widget ):
    self.simulator.step_sim_once()
    
    
  def on_reset( self, widget ):
    self.simulator.reset_sim()
    
    
  def on_save_map( self, widget ):
    raise(NotImplementedError)
    
    
  def on_load_map( self, widget ):
    raise(NotImplementedError)
      
      
  def on_random_map( self, widget ):
    self.simulator.random_map()
    
    
  def on_draw_invisibles( self, widget ):    
    # toggle the draw_invisibles state
    self.draw_invisibles = not self.draw_invisibles
    if self.draw_invisibles:
      self.decorate_draw_invisibles_button_active()
    else:
      self.decorate_draw_invisibles_button_inactive()
    self.simulator.draw_world()
    
    
  def on_expose( self, widget, event ):
    raise(NotImplementedError)
    
    
  def on_delete( self, widget, event ):
    
    raise(NotImplementedError)
    
    
  def decorate_draw_invisibles_button_active( self ):
    raise(NotImplementedError)
    
    
  def decorate_draw_invisibles_button_inactive( self ):
    raise(NotImplementedError)