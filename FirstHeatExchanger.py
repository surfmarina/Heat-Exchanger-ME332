# compute the area for various heat exchanger geometries
import math

# TODO Put values for air in the tables below given temp- some global variables
mass_flow = 10  # kg/s  mass flow in entire system
air_density = 1.154  # kg/m^3  density of air (external flow)
air_viscosity = 184.5E-7  # Ns/m^2
air_pr = 0.707


class HeatExchanger:

    def __init__(self):
        # Todo change the dimensions of the heat exchanger below
        # no dimension can be greater than 2 times any other dimension
        self.length = 2.5  # m - length of hx tubes
        self.x = 2  # m
        self.y = 2  # m
        self.diameter = 0.1  # meters

    def number_tubes(self):
        # given diameter and dimensions of hx
        # find max number of tubes and update spacing to make it even
        St = 2 * self.diameter  # initialise spacing as 2 times the diameter
        Nx = math.floor(self.x / (2 * self.diameter))  # round down to nearest int.
        Ny = math.floor(self.y / (2 * self.diameter))
        # update spacing to make it even
        Sx = self.x / (Nx * 2)
        Sy = self.y / (Ny * 2)
        spacing = [Nx, Ny, Sx, Sy]
        return spacing

    # given the hx geometries and thermal properties, determine v and vmax of external air flow
    def velocity(self, spacing):
        area = self.x * self.length  # find area external fluid flows thru
        v = mass_flow / (air_density * area)
        sx = spacing(2)
        vmax = sx*v/(sx-self.diameter)
        # if either velocity is above 100 m/s give a warning for compressible flow

        def is_zero(vmax):
            if vmax >= 100:
                print
                "WARNING: Air is travelling faster than 100 m/s"
            return vmax
