class ServoConveyor:
    def __init__(self, conveyor_length, belt_length, speed, rpm_max, pulley_rad):
        self.conveyor_length = conveyor_length
        self.belt_length = belt_length
        self.speed = speed
        self.rpm_max = rpm_max
        self.pulley_radius = pulley_rad
    
    def __str__(self):
        return f'Servo Motor Conveyor.\
            \nConveyor Length[mm]: {self.conveyor_length}\
            \nBelt Length [mm]: {self.belt_length}\
            \nSpeed [%]: {self.speed}\
            \nMax Speed [RPM]: {self.rpm_max}\
            \nPulley Radius [mm]: {self.pulley_radius}'

    # Edit once working with the servo motor
    def run_forwards(self):
        print('set conveyor to run forwards')

    def run_backwards(self):
        print('set conveyor to run backwards')

    def move_dis_rel(self, distance):
        print('move a specific distance forwards or backwards, set negative value to "backwards"')