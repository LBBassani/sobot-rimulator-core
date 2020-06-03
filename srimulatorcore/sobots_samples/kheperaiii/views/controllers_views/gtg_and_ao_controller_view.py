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





from .....utils import linalg2_util as linalg

VECTOR_LEN = 0.75 # length of heading vector

class GTGAndAOControllerView:

  def __init__( self, viewer, supervisor ):
    self.viewer = viewer
    self.supervisor = supervisor
    self.gtg_and_ao_controller = supervisor.gtg_and_ao_controller

  # draw a representation of the blended controller's internal state to the frame
  def draw_gtg_and_ao_controller_to_frame( self , ref_pose = [0.0, 0.0]):
    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()
    robot_pos[0] = robot_pos[0] - ref_pose[0]
    robot_pos[1] = robot_pos[1] - ref_pose[1]

    # draw the detected environment boundary (i.e. sensor readings)
    obstacle_vertexes = self.gtg_and_ao_controller.obstacle_vectors[:]
    obstacle_vertexes.append( obstacle_vertexes[0] )  # close the drawn polygon
    obstacle_vertexes = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , obstacle_vertexes ) )
    obstacle_vertexes = linalg.rotate_and_translate_vectors( obstacle_vertexes, robot_theta, robot_pos )
    self.viewer.current_frame.add_lines(  [ obstacle_vertexes ],
                                          linewidth = 0.005,
                                          color = "black",
                                          alpha = 1.0 )

    # draw the computed avoid-obstacles vector
    ao_heading_vector = linalg.scale( linalg.unit( self.gtg_and_ao_controller.ao_heading_vector ), VECTOR_LEN )
    vector_line = [ ref_pose , ao_heading_vector ]
    vector_line = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vector_line ) )
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    self.viewer.current_frame.add_lines( [ vector_line ],
                                         linewidth = 0.005,
                                         color = "red",
                                         alpha = 1.0 )

    # draw the computed go-to-goal vector
    gtg_heading_vector = linalg.scale( linalg.unit( self.gtg_and_ao_controller.gtg_heading_vector ), VECTOR_LEN )
    vector_line = [ ref_pose , gtg_heading_vector ]
    vector_line = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vector_line ) )
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )

    self.viewer.current_frame.add_lines( [ vector_line ],
                                         linewidth = 0.005,
                                         color = "dark green",
                                         alpha = 1.0 )

    # draw the computed blended vector
    blended_heading_vector = linalg.scale( linalg.unit( self.gtg_and_ao_controller.blended_heading_vector ), VECTOR_LEN )
    vector_line = [ ref_pose , blended_heading_vector ]
    vector_line = list( map( lambda x : [ x[0] - ref_pose[0], x[1] - ref_pose[1] ] , vector_line ) )
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    self.viewer.current_frame.add_lines( [ vector_line ],
                                         linewidth = 0.02,
                                         color = "blue",
                                         alpha = 1.0 )
