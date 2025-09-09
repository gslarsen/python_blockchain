class Car:
    top_speed = 100

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Car Information: {self.year} {self.make} {self.model}")

    def drive(self):
        print(f"I'm driving, but certainly not faster than {self.top_speed} km/h")


car1 = Car("Toyota", "Corolla", 2020)
car1.display_info()
car1.drive()
