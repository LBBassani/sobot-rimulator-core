class Controller:
    def __init__(self, controllerView):
        self.controllerView = controllerView
    
    def update_heading( self ):
        raise(NotImplementedError)
    
    def execute( self ):
        raise(NotImplementedError)