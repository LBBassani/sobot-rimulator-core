

class ControllerView():

    def __init__( self, viewer, supervisor ):
        self.viewer = viewer
        self.supervisor = supervisor
  
    def draw_controller_to_frame( self , controller, ref_pose = [0.0, 0.0]):
        raise(NotImplementedError)
    

