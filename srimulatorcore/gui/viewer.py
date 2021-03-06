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

DEFAULT_VIEW_PIX_W = 400    # pixels
DEFAULT_VIEW_PIX_H = 400    # pixels
DEFAULT_ZOOM = 50          # pixels per meter
MAJOR_GRIDLINE_INTERVAL = 1.0 # meters
MAJOR_GRIDLINE_SUBDIVISIONS = 5  # minor gridlines for every major gridline

# Abstract class Viewer
class Viewer:
  
  def __init__( self, simulator ):
    # bind the simulator
    self.simulator = simulator
    self.current_frame = None
    self.view_height_pixels = DEFAULT_VIEW_PIX_H
    self.pixels_per_meter = DEFAULT_ZOOM
    self.view_width_pixels = DEFAULT_VIEW_PIX_W
    self.view_height_pixels = DEFAULT_VIEW_PIX_H
    self.draw_invisibles = True
    
  def new_frame( self ):
    self.current_frame = Frame()
    
  def draw_frame( self , x = 0 , y = 0):
    raise(NotImplementedError)

  def _draw_grid_to_frame( self ):
    # NOTE: THIS FORMULA ASSUMES THE FOLLOWING:
    # - Window size never changes
    # - Window is always centered at (0, 0)

    # calculate minor gridline interval
    minor_gridline_interval = MAJOR_GRIDLINE_INTERVAL / MAJOR_GRIDLINE_SUBDIVISIONS
    
    # determine world space to draw grid upon
    meters_per_pixel = 1.0 / self.pixels_per_meter
    width = meters_per_pixel * self.view_width_pixels
    height = meters_per_pixel * self.view_height_pixels
    x_halfwidth = width * 0.5
    y_halfwidth = height * 0.5
    
    x_max = int( x_halfwidth / minor_gridline_interval )
    y_max = int( y_halfwidth / minor_gridline_interval )

    # build the gridlines
    major_lines_accum = []                  # accumulator for major gridlines
    minor_lines_accum = []                  # accumulator for minor gridlines

    for i in range( x_max + 1 ):            # build the vertical gridlines
      x = i * minor_gridline_interval

      if x % MAJOR_GRIDLINE_INTERVAL == 0:                        # sort major from minor
        accum = major_lines_accum
      else:
        accum = minor_lines_accum

      accum.append( [ [ x, -y_halfwidth ], [ x , y_halfwidth ] ] )   # positive-side gridline
      accum.append( [ [ -x, -y_halfwidth ], [ -x , y_halfwidth ] ] ) # negative-side gridline

    for j in range( y_max + 1 ):            # build the horizontal gridlines
      y = j * minor_gridline_interval

      if y % MAJOR_GRIDLINE_INTERVAL == 0:                        # sort major from minor
        accum = major_lines_accum
      else:
        accum = minor_lines_accum

      accum.append( [ [ -x_halfwidth , y ], [ x_halfwidth , y ] ] )     # positive-side gridline
      accum.append( [ [ -x_halfwidth , -y ], [ x_halfwidth , -y ] ] )   # negative-side gridline

    # draw the gridlines
    self.current_frame.add_lines( major_lines_accum,                 # draw major gridlines
                                         linewidth = meters_per_pixel,      # roughly 1 pixel
                                         color = "black",
                                         alpha = 0.2 )
    self.current_frame.add_lines( minor_lines_accum,                 # draw minor gridlines
                                         linewidth = meters_per_pixel,      # roughly 1 pixel
                                         color = "black",
                                         alpha = 0.1 )
    