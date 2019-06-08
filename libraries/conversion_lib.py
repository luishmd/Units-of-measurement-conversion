__author__ = 'Luis Domingues'

def init():

    # Ref unit is 1 bar
    dic_pressure = {"pascal":1e-5,
                    "kilopascal":1e-2,
                    "megapascal":10.0,
                    "centipascal":1e-7,
                    "milipascal":1e-8,
                    "atmosphere":1.01325,
                    "cm H2O @4 degC": 0.000980665,
                    "centitorr":0.000013332237,
                    "mm Hg @0 degC":0.0013332239,
                    "in Hg 32 degF":0.0338638,
                    "cm H2O @ 4 degC":0.000980638,
                    "mm H2O @ 4 degC":0.0000980638,
                    "m H2O @ 4 degC":0.0980638,
                    "bar":1.0,
                    "milibar":1e-3,
                    "dyne/cm2":1e-6,
                    "kilogram-force/m2":0.000098066,
                    "psi":0.068947573,
                    "torr":0.0013332239}

    # Ref unit is 0 degC
    # unit_to = f[0] + f[1]*unit_from
    dic_temperature_to_celsius = {"Kelvin":[-273.15, 1],
                                  "Fahrenheit":[-32*5.0/9.0, 5.0/9.0],
                                  "Rankine":[-491.67*5.0/9.0, 5.0/9.0],
                                  "Celsius":[0, 1]}
    dic_temperature_from_celsius = {"Kelvin":[273.15, 1],
                                    "Fahrenheit":[32, 9.0/5.0],
                                    "Rankine":[273.15*9.0/5.0, 9.0/5.0],
                                    "Celsius":[0, 1]}

    # Ref unit is 1 m
    dic_length = {"picometre":1e-12,
                  "angstrom":1e-10,
                  "nanometre":1e-9,
                  "micrometre":1e-6,
                  "milimetre":1e-3,
                  "centimetre":1e-2,
                  "metre":1.0,
                  "decametre":10,
                  "hectometre":100,
                  "kilometre":1000,
                  "yard":0.9144,
                  "mile":1609.35,
                  "foot":0.3048,
                  "inch":2.54e-2,
                  "lightyear":9460660000000000}

    # Ref unit is 1 kg
    dic_weight = {"kilogram":1,
                  "gram":1e-3,
                  "miligram":1e-6,
                  "metric ton":1000,
                  "pound":0.453592,
                  "ounce":0.0283495,
                  "carrat":0.0002,
                  "atomic mass unit":1.660540199e-27}

    # Ref unit is 1 second
    dic_time = {"month":30.5*24*3600,
                "day":24*3600,
                "hour":3600,
                "minute":60,
                "second":1}

    dic_units_conversion = {"pressure":dic_pressure,
                            "temperature":[dic_temperature_to_celsius, dic_temperature_from_celsius],
                            "length":dic_length,
                            "weight":dic_weight,
                            "time": dic_time,
                            "speed":[dic_length, dic_time],
                            "pace": [dic_time, dic_length]}

    return dic_units_conversion


def get_default_units():
    defaults_dic = {"pressure":"bar",
                    "temperature":"Celsius",
                    "length":"centimetre",
                    "weight":"kilogram",
                    "time":"second"}
    return defaults_dic


def conv_temperature(N_from, unit_from, unit_to, dic_list):
    """
    For temperature conversions
    """
    dic_t_to_celsius = dic_list[0]
    dic_celsius_to_t = dic_list[1]
    temp_celsius = dic_t_to_celsius[unit_from][0] + dic_t_to_celsius[unit_from][1]*N_from
    N_to = dic_celsius_to_t[unit_to][0] + dic_celsius_to_t[unit_to][1]*temp_celsius
    return N_to


def conv_simple(N_from, unit_from, unit_to, dic):
    """
    For simple conversions
    """
    f_from = dic[unit_from]
    f_to = dic[unit_to]
    N_to = float(N_from) * f_from / f_to
    return N_to


def conv_composite(N_from, unit_from, unit_to, dic_list):
    """
    For units of the type m/s
    """
    [unit_from_num, unit_from_den] = unit_from.split("/")
    [unit_to_num, unit_to_den] = unit_to.split("/")
    N_to_num = conv_simple(1, unit_from_num, unit_to_num, dic_list[0])
    N_to_den = conv_simple(1, unit_from_den, unit_to_den, dic_list[1])
    N_to = float(N_from) * N_to_num / N_to_den
    return N_to


def conv(N_from, unit_type, unit_from, unit_to, dic):
    """
    Main function to be used. Should use all other functions
    """
    if unit_type == "temperature":
        N_to = conv_temperature(N_from, unit_from, unit_to, dic["temperature"])
    else:
        if unit_type == "speed":
            N_to = conv_composite(N_from, unit_from, unit_to, dic["speed"])
        else:
            if unit_type == "pace":
                N_to = conv_composite(N_from, unit_from, unit_to, dic["pace"])
            else:
                N_to = conv_simple(N_from, unit_from, unit_to, dic[unit_type])
    return N_to


def get_options(dic):
    options = dic.keys()
    return options


if __name__ == "__main__":
# Testing
    dic_main = init()
    N = conv(100,"length", "milimetre","milimetre",dic_main)
    print(N)

    speed = 4.2530

    dic_main = init()
    N = conv(speed, "speed", "metre/second", "kilometre/hour", dic_main)
    print(N)

    dic_main = init()
    N = conv(1/speed, "pace", "second/metre", "minute/kilometre", dic_main)
    print(N)