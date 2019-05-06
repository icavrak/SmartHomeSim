import datetime
from PricingProfile import PricingProfile

class PricingProfile_Dual(PricingProfile):

    def __init__(self):
        self.low_price = 1.0
        self.high_price = 2.0

    def __init__(self, init_arguments):
        arg_list = init_arguments.split(", ")
        self.low_price = float(arg_list[0])
        self.high_price = float(arg_list[1])

        self.low_to_high = datetime.datetime.strptime("07:00:00", "%H:%M:%S").time()
        self.high_to_low = datetime.datetime.strptime("21:00:00", "%H:%M:%S").time()


    def getCurrentPrice(self, time):

        current_time = time.time()
        if current_time < self.low_to_high:
            return self.low_price

        if current_time > self.high_to_low:
            return self.low_price

        return self.high_price
