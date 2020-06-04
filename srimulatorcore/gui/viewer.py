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

from .frame import Frame
# Abstract class Viewer
class Viewer:
  
  def __init__( self, simulator ):
    # bind the simulator
    self.simulator = simulator
    self.current_frame = None
    
  def new_frame( self ):
    self.current_frame = Frame()
    
  def draw_frame( self , x = 0 , y = 0):
    raise(NotImplementedError)
    