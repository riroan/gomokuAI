
class Replay:
    def __init__(self):
        # it has tuple which is (s_t, pi_t, z)
        self.replay = []
        self.start = 0
        self.end = 0
    
    def initialize(self):
        self.replay = []
    
    def save(self, s_t, pi_t,z = 0):
        replay.append((s_t,pi,t_z))