class Property:
    def __init__(self, square_meter='', num_bedrooms='', num_bathrooms='', **kwargs):
        super().__init__(**kwargs)
        self.square_meter = square_meter
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms

    @property
    def display(self):
        print("Property Details")
        print("-" * 15)
        print("square_meter : {}".format(self.square_meter))
        print("num_bedrooms : {}".format(self.num_bedrooms))
        print("num_bathrooms : {}".format(self.num_bathrooms))
        print("-" * 15)

    @staticmethod
    def prompt_init():
        return dict(square_meter=input("Enter Square Meter : "),
                    num_bedrooms=input("Enter Num Bedrooms : "),
                    num_bathrooms=input("Enter Num Bathrooms : "))


class House(Property):
    valid_fenced_yard = ("y", "n")

    # valid_garage = ("1", "2", "3", "4", "5", "n")
    def __init__(self, garage='', fenced_yard='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced_yard = fenced_yard

    def display(self):
        super().display()
        print("House Details")
        print("-" * 15)
        print("garage : {}".format(self.garage))
        print("fenced_yard : {}".format(self.fenced_yard))
        print("-" * 15)

    @staticmethod
    def prompt_init():
        data_init = Property.prompt_init()
        fenced = get_convert_input_lowercase("Is the fenced yard? : ", House.valid_fenced_yard)
        garage = input("How many cars can the garage? : ")

        data_init.update({
            "fenced": fenced,
            "garage": garage,
        })
        return data_init


class Apartment(Property):
    valid_balcony = ("y", "n")
    valid_laundry = ("y", "n")

    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        super().display()
        print("Apartment Details")
        print("-" * 15)
        print("balcony: {}".format(self.balcony))
        print("laundry: {}".format(self.laundry))
        print("-" * 15)

    @staticmethod
    def prompt_init():
        data_init = Property.prompt_init()

        laundry = get_convert_input_lowercase("Is the laundry? ", Apartment.valid_laundry)
        balcony = get_convert_input_lowercase("Is the balcony?", Apartment.valid_balcony)

        data_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return data_init


class Purchase(Property):
    def __init__(self, price='', **kwargs):
        super().__init__(**kwargs)
        self.price = price

    def display(self):
        super().display()
        print("Purchase Details")
        print("-" * 15)
        print("price: {}".format(self.price))
        print("-" * 15)

    @staticmethod
    def prompt_init():
        return dict(
            price=input("What is the selling price? "))


class Rental(Property):
    def __init__(self, furnished='', rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent

    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("furnished: {}".format(self.furnished))

    @staticmethod
    def prompt_init():
        return dict(
            rent=input("How many the month rent? "),
            furnished=get_convert_input_lowercase("Is the property furnished? ", ("y", "n")))


class HouseRental(Rental, House):
    @staticmethod
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init


class ApartmentRental(Rental, Apartment):
    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init


class ApartmentPurchase(Purchase, Apartment):
    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init


class HousePurchase(Purchase, House):
    @staticmethod
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init


class Agent:
    type_map = {("house", "purchase"): HousePurchase,
                ("house", "rental"): HouseRental,
                ("apartment", "purchase"): ApartmentPurchase,
                ("apartment", "rental"): ApartmentRental}

    def __init__(self):
        self._property_list = []

    def list_property(self):
        # print(self.property_list)
        for property in self._property_list:
            property.display()

    def add_property(self):
        property_type = get_convert_input_lowercase("select type? ", ("house", "apartment"))
        payment_type = get_convert_input_lowercase("select payment type? ", ("purchase", "rental"))

        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass)
        print(self.property_list)


def get_convert_input_lowercase(input_str, valid_options):
    input_str += " ({}) ".format((", ".join(valid_options)))
    response = input(input_str)
    while response.lower() not in valid_options:
        response = input(input_str)
    return response


agent_a = Agent()
agent_a.add_property()
agent_a.list_property()
