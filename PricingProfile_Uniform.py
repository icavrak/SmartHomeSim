from PricingProfile import PricingProfile

class PricingProfile_Uniform(PricingProfile):

    def __init__(self):
        self.current_price = 1.0

    def __init__(self, init_arguments):
        self.current_price = float(init_arguments)

