from libarduino import pinMode,digitalWrite,analogRead
import time

class Actuator():
    def __init__(self, port):
        self.port = port
        pinMode(self.port, 'OUTPUT')

    def activate(self):
        digitalWrite(self.port, 1)

    def deactivate(self):
        digitalWrite(self.port, 0)


class Ranger():
    def __init__(self, port, drink):
        self.port = port
        self.drink = drink

    def read(self):
        return analogRead(self.port)

class Mixer():
    def __init__(self, motor, piston, rangers, valves, capacity=250, drinks=2, dist=128):
        self.motor    = motor
        self.piston   = piston
        self.rangers  = rangers
        self.valves   = valves
        self.capacity = capacity
        self.drinks   = drinks
        self.dist     = dist
 
    def mix_drink(self,recipe):
        use = [] # Use these liquids.
        for i in range(self.drinks):
            if recipe[i] > 0:
                use.append(i)

        for i in use:
            while self.rangers[i].read() > self.dist:
                self.motor.activate()
                time.sleep(0.1)
            
            self.motor.deactivate()
            start_time = time.time()
            self.valves[i].activate()
            
            const = 1 # Const is the relation between time and how much liquid which gets through the valves. TODO find proper const.
            fill_time = recipe[i] * self.capacity * const


            while (time.time() - start_time) < fill_time:
                print 'Standing still'

            self.valves[i].deactivate()

    def serve(self,piston_time=7,ranger=0):
        # Get to piston position
        while self.rangers[ranger].read() > self.dist:
            self.motor.activate()
            time.sleep(0.1)
        
        start_time = time.time()
        self.piston.activate()

        while (time.time() - start_time) < piston_time:
            print 'Serving drink'

        self.piston.deactivate()
