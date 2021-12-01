# compute the area for various heat exchanger geometries
class HeatExchanger:
    def __init__(self):
        # no dimension can be greater than 2 times any other dimension
        self.l = 2.5  # m - length of hx tubes
        self.x = 2  # m
        self.y = 2  # m
        self.diameter = 0.1  # meters
    def numbertubes(self):
        # given the entire dimensions, determine how many tubes can fit if aligned
        xyarea = self.x*self.y
        # let spacing btw tubes be 2 times the diameter
        St = 2*self.diameter
        
        nt  # number of tubes

    # given the hx geometries and thermal properties, determine
    def velocity(self, air):
        area = self.x * self.l  # find area external fluid flows thru

        mass_flow = 10  # kg/s  mass flow in entire system
        air_density = 1.154  # kg/m^3  density of air (external flow)
        air_viscosity = 184.5E-7  # Ns/m^2
        air_pr = 0.707

        velocity_air = mass_flow/(air_density*area)
        print(velocity_air)
