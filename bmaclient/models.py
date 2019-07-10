import six


class ApiModel(object):

    @classmethod
    def object_from_dictionary(cls, entry):
        if entry is None:
            return ''
        entry_dict = dict([
            (str(key), value) for key, value in entry.items()
        ])
        return cls(**entry_dict)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        return unicode(self).encode('utf-8')


class DOAS(ApiModel):

    def __init__(self, id, timestamp, emission):
        self.id = id
        self.timestamp = timestamp
        self.emission = emission


class EDM(ApiModel):

    def __init__(self, timestamp, slope_distance):
        self.timestamp = timestamp
        self.slope_distance = slope_distance


class GasEmission(ApiModel):

    def __init__(self, timestamp, co2_min, co2_max, co2_avg, temperature_min,
                 temperature_max, temprature_avg, humidity_min, humidity_max,
                 humidity_avg, input_battery_voltage):
        self.timestamp = timestamp
        self.co2_min = co2_min
        self.co2_max = co2_max
        self.co2_avg = co2_avg
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.temprature_avg = temprature_avg
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.humidity_avg = humidity_avg
        self.input_battery_voltage = input_battery_voltage


class GasTemperture(ApiModel):

    def __init__(self, timestamp, temperature1, temperature2, temperature3,
                 temperature4, battery_voltage):
        self.timestamp = timestamp
        self.temperature1 = temperature1
        self.temperature2 = temperature2
        self.temperature3 = temperature3
        self.temperature4 = temperature4
        self.battery_voltage = battery_voltage
