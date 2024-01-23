class Motor():
    # The translator is the attachment to the motor, example a timing pully has 20 teeth per rotation
    # each spaced 2 mm. So the translator is 20 teeth/rotation * 2 mm/tooth = 40 mm/rotation
    def __init__(self, steps_per_rotation, transalor):
        self.distance_per_step = transalor / steps_per_rotation # mm/step
        self.current_cartisan = 0.0
    
    def move_to(self, value):
        steps = self.position_to_steps(value)
        
        # Owen's Motor Control Code
        
        self._set_current_cartisan(value)
        
    def position_to_steps(self, coordinate):
        return (coordinate - self.current_cartisan) / self.distance_per_step # steps
    
    def _set_current_cartisan(self, value):
        self.current_cartisan = value