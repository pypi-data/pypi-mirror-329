import math

CONSTANTS = {
    "B": {
        "alpha": 7.0,
        "zg": 356.76,
        "a_prime": 1 / 7,
        "b_prime": 0.84,
        "a_bar": 1 / 4,
        "b_bar": 0.45,
        "c": 0.30,
        "l": 97.54,
        "e": 1 / 3,
        "zmin": 9.14,
    },
    "C": {
        "alpha": 9.5,
        "zg": 274.32,
        "a_prime": 1 / 9.5,
        "b_prime": 1.00,
        "a_bar": 1 / 6.5,
        "b_bar": 0.65,
        "c": 0.20,
        "l": 152.40,
        "e": 1 / 5,
        "zmin": 4.57,
    },
    "D": {
        "alpha": 11.5,
        "zg": 213.36,
        "a_prime": 1 / 11.5,
        "b_prime": 1.07,
        "a_bar": 1 / 9,
        "b_bar": 0.80,
        "c": 0.15,
        "l": 198.12,
        "e": 1 / 8,
        "zmin": 2.13,
    },
}


class calculate_gust:
    """
    exposure : exposure type of wind [B,C,D] 
    wind_speed : wind speed in m/s
    b_length : milimeters
    l_length : milimeters   
    """
    def __init__(self,exposure,mean_height,wind_speed,b_length,l_length,nat_freq):
        self.exposure = exposure
        self.mean_height = mean_height
        self.constants = CONSTANTS
        self.V = wind_speed * 0.2777777778 #convert to m/s
        self.B = b_length
        self.L = l_length
        self.n1 = nat_freq
        self.type = type

    def aerodynamicHeight(self):
        zmin = self.constants[self.exposure]["zmin"]
        z_bar = max(0.6 * self.mean_height, zmin)
        units = ""
        report = '''
        \\text{ MAX}\\left( 0.6 \\times h, z_{min}\\right) <br> 

        '''
        results = {
            "value" : z_bar,
            "units" : units,
            "report" : report
        }
        return results

    def turbulenceIntensity(self):
        c = self.constants[self.exposure]["c"]
        Iz_bar = c * math.pow(10/self.aerodynamicHeight()['value'],1/ 6)
        results = {
            "value" : Iz_bar,
            # "units" : units,
            # "report" : report
        }
        return results

    def scaleOfTurbulence(self):
        l_val = self.constants[self.exposure]["l"]
        e = self.constants[self.exposure]["e"]
        Lz_bar = l_val * math.pow(self.aerodynamicHeight()['value']/10,e)
        # return Lz_bar
        results = {
            "value" : Lz_bar,
            # "units" : units,
            # "report" : report
        }
        return results


    def meanWindSpeed(self):
        a_bar = self.constants[self.exposure]["a_bar"]
        b_bar = self.constants[self.exposure]["b_bar"]
        Vz_bar = b_bar * math.pow(self.aerodynamicHeight()['value']/10,a_bar) * self.V
        results = {
            "value" : Vz_bar,
            # "units" : units,
            # "report" : report
        }
        return results

    def gustResponsePeakResponse(self):
        val = 2.0 * math.log(3600.0 * self.n1)
        gR = math.sqrt(val) + 0.577 / math.sqrt(val)
        results = {
            "value" : gR,
            # "units" : units,
            # "report" : report
        }
        return results

    def backgroundResponse(self):

        background_response_init = 1.0 + 0.63 * math.pow( (self.B + self.mean_height)/self.scaleOfTurbulence()['value'],0.63)
        background_response = math.sqrt(1.0/background_response_init)
        results = {
            "value" : background_response,
            # "units" : units,
            # "report" : report
        }
        return results

    def reducedFrequency(self):
        ni = (self.n1 * self.scaleOfTurbulence()['value']) / self.meanWindSpeed()['value']
        results = {
            "value" : ni,
            # "units" : units,
            # "report" : report
        }
        return results

    def sizeFactorEffect(self):
        dimensions = [
            {"name": "h", "value": self.mean_height, "constant": 4.6},
            {"name": "B", "value": self.B, "constant": 4.6},
            {"name": "L", "value": self.L, "constant": 15.4},
        ]
        R_values = {}

        for dim in dimensions:
            eta = dim["constant"] * self.n1 * (dim["value"] / self.meanWindSpeed()['value'])
            term_exp = math.exp(-2.0 * eta)
            Rsizefactor = (1.0 / eta) - ((1.0 / (2.0 * eta * eta)) * (1.0 - term_exp))
            R_values[f"R{dim['name']}"] = Rsizefactor

        results = {
            "rh" : {
                "value" : R_values['Rh'],
                "units" : "",
                "report" : ""
            },
            "rB" : {
                "value" : R_values['RB'],
                "units" : "",
                "report" : ""                
            },          
            "rL" : {
                "value" : R_values['RL'],
                "units" : "",
                "report" : ""                    
            }
        }
        return results

    def resonantResponseFactor(self,beta_input = 0.010):
        '''
        concrete structure = 0.015
        steel = 0.010
        '''
        r_factor = self.sizeFactorEffect()

        beta = beta_input
        rn = (7.47 * self.reducedFrequency()["value"] ) / math.pow(1 + 10.3 * self.reducedFrequency()["value"], 5 / 3)

        r_value = math.sqrt(
                (1.0 / beta)
                * rn
                * r_factor["rh"]["value"]
                * r_factor["rB"]["value"]
                * (0.53 + 0.47 * r_factor["rL"]["value"])
            )
        
        results = {
            "rn" : {
                "value" : rn,
                "units" : "",
                "report" : ""               
            },
            "r" : {
                "value" : r_value,
                "units" : "",
                "report" : ""                   
            }
        }

        return results

    def gust_factor(self):
        #CONSTANT
        GQ = 3.4
        GV = 3.4
        COEFFICIENT = 0.925

        #Factors
        Q_factor = self.backgroundResponse()["value"]
        gR = self.gustResponsePeakResponse()["value"]
        R_factor = self.resonantResponseFactor()["r"]["value"]
        Iz_bar = self.turbulenceIntensity()["value"]

        if(self.n1 <= 1):
            Gfa = (math.pow(GQ,2)*math.pow(Q_factor,2)) + (math.pow(gR,2) * math.pow(R_factor,2))
            Gf = COEFFICIENT * ((1.0 + (1.7*Iz_bar*math.sqrt(Gfa)))/ (1.0 + (1.7*GV*Iz_bar)))
            units = ""        
            results = {
                "value" : Gf,
                "units" : units,
                # "report" : report
            }            
        else:
            numerator = 1.0 + 0.7 * GQ * self.turbulenceIntensity()['value'] * self.backgroundResponse()['value'] 
            denominator = 1.0 + 0.7 * GV * self.turbulenceIntensity()['value']
            gust_factor = COEFFICIENT * (numerator / denominator)
            units = ""
            results = {
                "value" : gust_factor,
                "units" : units,
                # "report" : report
            }
        return results

# kzt =1
# kd = 0.85
# wind_speed = 240
# exposure = "D"
# mean_height = 24.50
# na_value = 0.90
# # type = "rigid"

# wind_velocity = calculate_gust(exposure,mean_height,wind_speed,100,100,na_value)
# # print(wind_velocity.aerodynamicHeight())
# # print(wind_velocity.turbulenceIntensity())
# # print(wind_velocity.scaleOfTurbulence())
# # print(wind_velocity.meanWindSpeed())
# # print(wind_velocity.gustResponsePeakResponse())
# # print(wind_velocity.backgroundResponse())
# # # print(wind_velocity.reducedFrequency())
# print(wind_velocity.sizeFactorEffect())
# print(wind_velocity.gust_factor())