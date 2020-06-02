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


class GoToGoalController:

  def __init__( self, supervisor ):
    raise NotImplementedError

  def update_heading( self ):
    raise NotImplementedError

  def execute( self ):
    raise NotImplementedError

  # return a go-to-goal heading vector in the robot's reference frame
  def calculate_gtg_heading_vector( self ):
    raise NotImplementedError

  def _print_vars( self, eP, eI, eD, v, omega ):
    raise NotImplementedError
