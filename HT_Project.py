# Heat Transfer Final Project

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class heat_exchanger:
    def __init__(self):
        # Givens
        self.cp = 1e3  # J/(kg*K)
        self.t_c_in = 25  # C
        self.t_c_out = 225  # C
        self.t_h_in = 425  # C
        self.m_dot = 10  # kg/s
        self.h_given = 150  # W/(m^2*K)

        self.c_c = self.m_dot*self.cp
        self.c_h = self.m_dot*self.cp
        self.c_min = min(self.c_c,self.c_h)
        self.c_max = max(self.c_c,self.c_h)
        self.c_r = self.c_min/self.c_max
        self.q = self.c_c*(self.t_c_out-self.t_c_in)
        self.q_max = self.c_min*(self.t_h_in-self.t_c_in)
        self.e = self.q/self.q_max
        self.ntu = -np.log(1+(1/self.c_r)*np.log(1-self.e*self.c_r))
        self.ua = self.c_min*self.ntu
        self.a_req = self.ua/self.h_given

        # Properties cold
        self.k_c = 26.3e-3
        self.c_1 = .229
        self.c_2 = .97
        self.m = .632
        self.rho_c = 1.1614
        self.mu_c = 184.6e-7
        self.pr = .707

        # Properties hot, air at 700K
        self.k_h = 52.4e-3
        self.rho_h = .4975
        self.mu_h = 338.8e-7
        self.pr_h = .695

        # Initial spacing, we loop through all of these values
        self.diam = [.01, .03, .05, .07, .1, .15, .2]
        self.num_tubes_x = [5, 10, 15, 20, 25, 30, 35, 100, 500, 1000]
        self.num_tubes_y = [5, 10, 15, 20, 25, 30, 35, 100, 500, 1000]
        self.lll = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 10, 15, 20]

    def update_spacing(self, i, j, k, q):
        st = 2*self.diam[i]
        sl = 2*self.diam[i]
        x = self.num_tubes_x[j]*st
        y = self.num_tubes_y[k]*sl
        return [st, sl, x, y]

    def cold_calculations(self, length, i, q):
        v = self.m_dot/(self.rho_c*length[2]*self.lll[q])
        v_max = length[0]*v/(length[0]-self.diam[i])
        re_d = self.rho_c*v_max*self.diam[i]/self.mu_c
        nu_d = 1.13*self.c_1*self.c_2*re_d**self.m*self.pr**(1/3)
        h_bar = nu_d*self.k_c/self.diam[i]
        return h_bar

    def hot_calculations(self, i, j, k):
        v_t = self.m_dot*4/(self.diam[i]**2*np.pi*self.rho_h*self.num_tubes_x[j]*self.num_tubes_y[k])
        re_d = self.rho_h*v_t*self.diam[i]/self.mu_h
        nu_d = .023*re_d**(4/5)*self.pr_h**.3
        h_bar = nu_d * self.k_h/self.diam[i]
        return h_bar

    def check_valid(self, i, j, k, q):
        retu = False
        spacin = self.update_spacing(i,j,k,q)
        if spacin[2] <= 2*spacin[3] and spacin[3] <= 2*spacin[2]:
            if self.lll[q] <= 2*spacin[3] and spacin[3] <= 2*self.lll[q]:
                if self.lll[q] <= 2*spacin[2] and spacin[2] <= 2*self.lll[q]:
                    retu = True
        return retu

    def new_area(self, min_h):
        return self.ua/min_h




if __name__ == "__main__":
    heater = heat_exchanger()
  #  lengths = heater.update_spacing()
  #  h_bar_cold = heater.cold_calculations(lengths)
  #  h_bar_hot = heater.hot_calculations()
    good_c = []
    good_h = []
    new_are = []
    min_h_array = []
    is_array = []
    js_array = []
    ks_array = []
    qs_array = []

    for i, diam in enumerate(heater.diam):
        for j, num_x in enumerate(heater.num_tubes_x):
            for k, num_y in enumerate(heater.num_tubes_y):
                for q, ll in enumerate(heater.lll):
                    if heater.check_valid(i, j, k, q):
                        lengths = heater.update_spacing(i, j, k, q)
                        h_bar_cold = heater.cold_calculations(lengths, i, q)
                        h_bar_hot = heater.hot_calculations(i, j, k)
                        # Check that area is in the range of 50-100 (remove extremes)
                        are = heater.new_area(min(h_bar_hot, h_bar_cold))
                        if 50 < are < 100:
                            is_array.append(diam)
                            js_array.append(num_x)
                            ks_array.append(num_y)
                            qs_array.append(ll)
                            good_c.append(h_bar_cold)
                            good_h.append(h_bar_hot)
                            min_h_array.append(min(h_bar_hot, h_bar_cold))
                            new_are.append(are)


    plt.scatter(min_h_array,new_are)
    plt.xlabel("Minimum h_bar")
    plt.ylabel("Area Required")
    plt.show()

    #table = [{'Area', 'Min h_bar', 'Diameter', 'Num T', 'Num L', 'L'}]
    #for i in range(len(min_h_array)):
    #    table.append({new_are[i], min_h_array[i], is_array[i], js_array[i], ks_array[i], qs_array[i]})

    #print(tabulate(table))

    fig = go.Figure(data=[go.Table(
        header=dict(values=['Area', 'Min h_bar', 'Diameter', 'Num T', 'Num L', 'L'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[new_are, min_h_array, is_array, js_array,ks_array,qs_array],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])

    fig.update_layout(width=700, height=2000)
    fig.show()



