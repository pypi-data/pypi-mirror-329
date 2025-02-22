import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class calculate_velocity_pressure:
    def __init__(self, kzt, kd, wind_speed, exposure, mean_height):
        self.kzt = kzt
        self.kd = kd
        self.wind_speed = wind_speed * 0.2777777778  # Convert to m/s
        self.exposure = exposure
        self.mean_height = mean_height
        self.constants = {
            "B": {"zg": 365.76, "alpha": 7},
            "C": {"zg": 274.32, "alpha": 9.5},
            "D": {"zg": 213.36, "alpha": 11.5}
        }
        self.zg = self.constants[exposure]["zg"]
        self.alpha = self.constants[exposure]["alpha"]
        self.qzkz = 0.613 * self.kzt * self.kd * self.wind_speed ** 2
        self.height_data = [4.5, 6, 7.5, 9, 12, 15, 18, 21, 24, 27, 30, 36, 42, 48, 54, 60, 75, 90, 105, 120, 135, 150]
        self.height_index = self._filter_height_data()

    def _filter_height_data(self):
        height_index = [index for index in self.height_data if index < self.mean_height]
        height_index.append(self.mean_height)
        return height_index
    def calculate_qzkzvalue(self):
        qzkz = 0.613 * self.kzt * self.kd * math.pow(self.wind_speed,2)
        return qzkz
  
    def generate_qzkzdata(self):

        height_index = []
        kzi_arr = [] #store kzi value
        qzi_arr = [] #store the qzi value 
        
        height_data = [0,4.5, 6, 7.5, 9, 12, 15, 18, 21, 24, 27, 30, 36, 42, 48, 54, 60, 75, 90, 105, 120, 135, 150]
        for i in height_data:
            if i < self.mean_height:
                height_index.append(i)

        height_index.append(self.mean_height)

        for height in height_index:
            alpha_power = 2 / self.alpha
            Kz_part_one = height / self.zg
            if height == 0:
                Kz_part_one = 4.5 / self.zg
                Kzi = 2.01 * math.pow(Kz_part_one,alpha_power)
            else:
                # Kz_part_one = 4.5 / self.zg
                Kzi = 2.01 * math.pow(Kz_part_one,alpha_power)
            qzi = Kzi * self.calculate_qzkzvalue()
            kzi_arr.append(Kzi)
            qzi_arr.append(qzi)
        final_data = [height_index,kzi_arr,qzi_arr] 
        return final_data
    
    def report(self):
        '''
        Generate the report using the wind velocity
        '''
        ##For qzkz
        report = ""
        report += "<h2>Velocity Pressure</h2>"
        report += "<center> \\( q_{z } = 0.613 \\times K_{ z } \\times K_{ zt } \\times K_{ d } \\times \\left( V \\right)^{2} \\) </center>"
        report += f"<center> \\( q_{{z}} = 0.613 \\times K_{{z}} \\times {self.kzt:.2f} \\times {self.kd:.2f} \\times \\left( {self.wind_speed:.2f} \\frac{{m}}{{s}} \\right)^{2} \\) </center>"
        report += f"<center> \\( q_{{z}} = {self.calculate_qzkzvalue():.2f} \\times K_{{ z }} \\text{{  }} \\frac{{N}}{{m^{2}}} \\text{{ or }} P_{{a}}  \\) </center>"

        return report


    def plot(self):
        """
        Generate three arrays (Height, Kzi, Qzi) from self.generate_qzkzdata(),
        and create a Matplotlib Figure without using Seaborn.
        """

        # Retrieve data
        data = self.generate_qzkzdata()
        ht_arr = data[0]  # Array of Heights (Y-axis)
        qzi_arr = data[2]  # Array of Wind Velocity Pressures (X-axis)

        # Create figure and axis with improved size
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

        # Plot with improved styling
        ax.plot(qzi_arr, ht_arr, color='black', linewidth=2.5, linestyle='-')

        # Label axes and title with enhanced visibility
        ax.set_xlabel('Wind Velocity Pressure (Pa)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Height (m)', fontsize=14, fontweight='bold')
        ax.set_title('Wind Pressure vs. Height Profile', fontsize=16, fontweight='bold')

        # Customize tick labels for readability
        ax.tick_params(axis='both', labelsize=12)

        # Set x-axis to start at 0
        ax.set_xlim(left=0)

        # Enable professional grid style
        ax.grid(True, linestyle='--', alpha=0.6, linewidth=0.8)

        # Improve layout
        plt.tight_layout()

        # Return figure for further use
        return fig
        # return fig


# kzt =1
# kd = 0.85
# wind_speed = 240
# exposure = "B"
# mean_height = 24

# wind_velocity = calculate_velocity_pressure(kzt,kd,wind_speed,exposure,mean_height)
# print(wind_velocity.calculate_qzkzvalue())
# print(wind_velocity.generate_qzkzdata())
# print(wind_velocity.plot())