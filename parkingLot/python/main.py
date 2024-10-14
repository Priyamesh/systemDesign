from abc import abstractmethod
from datetime import datetime
import time


# Vehical class
class Vehical:

    @abstractmethod
    def __init__(self, vehical_number):
        self.vehical_number = vehical_number

    def get_vehical_type(self):
        pass

    def get_vehical_number(self):
        return self.vehical_number


class Car(Vehical):

    def __init__(self, vehical_number):
        super().__init__(vehical_number)

    def get_vehical_type(self):
        return "Car"


class Bike(Vehical):

    def __init__(self, vehical_number):
        super().__init__(vehical_number)

    def get_vehical_type(self):
        return "Bike"


class Truck(Vehical):

    def __init__(self, vehical_number):
        super().__init__(vehical_number)

    def get_vehical_type(self):
        return "Truck"


# parking spot
class ParkingSpot:

    def __init__(self, id, spot_type, is_free=True):
        self.id = id
        self.spot_type = spot_type
        self.is_free = is_free

    def get_is_free(self):
        return self.is_free

    def reserve(self):
        self.is_free = False

    def release(self):
        self.is_free = True


# reservation
class Reservation:

    def __init__(self, id, vehical, spot):
        self.id = id
        self.vehical = vehical
        self.spot = spot
        self.start_time = datetime.now()
        self.end_time = None

    def get_id(self):
        return self.id

    def get_vehical(self):
        return self.vehical

    def get_spot(self):
        return self.spot

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def end_reservation(self):
        self.end_time = datetime.now()
        self.spot.release()
        return self.end_time - self.start_time


# ticket
class Ticket:

    def __init__(self, id, reservation, rate):
        self.id = id
        self.reservation = reservation
        self.rate = rate

    def get_id(self):
        return self.id

    def get_fare(self):
        # convert this to per hour calculation
        return (
            self.rate
            * (
                self.reservation.get_end_time() - self.reservation.get_start_time()
            ).total_seconds()
        )


# payment
class Payment:

    def __init__(self, id, ticket):
        self.id = id
        self.ticket = ticket
        self.amount = ticket.get_fare()

    def get_id(self):
        return self.id

    def get_ticket(self):
        return self.ticket

    def get_amount(self):
        return self.amount


class ParkingLot:

    def __init__(self, bikespots, carspots, truckspots):
        self.spots = {
            "Bike": [ParkingSpot(i, "bike") for i in range(bikespots)],
            "Car": [ParkingSpot(i, "car") for i in range(carspots)],
            "Truck": [ParkingSpot(i, "truck") for i in range(truckspots)],
        }
        self.reservations = {}
        self.tickets = {}
        self.payments = {}
        self.spot_rates = {"Car": 10, "Bike": 5, "Truck": 15}

    def get_spots(self):
        return self.spots

    def get_reservations(self):
        return self.reservations

    def get_tickets(self):
        return self.tickets

    def get_payments(self):
        return self.payments

    def add_reservation(self, reservation):
        self.reservations[reservation.id] = reservation

    def add_ticket(self, ticket):
        self.tickets[ticket.id] = ticket

    def add_payment(self, payment):
        self.payments[payment.id] = payment

    def check_availability(self, vehical):
        for spot in self.spots[vehical.get_vehical_type()]:
            if spot.get_is_free():
                return spot
        return False

    def reserve_spot(self, vehical):
        available_spot = self.check_availability(vehical)
        if available_spot:
            available_spot.reserve()
            reservation = Reservation(
                len(self.reservations) + 1, vehical, available_spot
            )
            self.add_reservation(reservation)
            return reservation
        return None

    def generate_ticket(self, reservation):
        ticket = Ticket(
            len(self.tickets) + 1,
            reservation,
            self.spot_rates[reservation.vehical.get_vehical_type()],
        )
        self.add_ticket(ticket)
        return ticket

    def release_spot(self, reservation):
        reservation.end_reservation()
        ticket = self.generate_ticket(reservation)
        payment = Payment(len(self.payments) + 1, ticket)
        self.add_payment(payment)
        return (ticket, payment)


parking_lot = ParkingLot(2, 2, 2)

vehical1 = Car("123ABCD")
reservation1 = parking_lot.reserve_spot(vehical1)
print(reservation1.__dict__)

vehical2 = Truck("987MNBV")
reservation2 = parking_lot.reserve_spot(vehical2)
print(reservation2.__dict__)

time.sleep(5)

ticket1, payment1 = parking_lot.release_spot(reservation1)
print(ticket1.__dict__)
print(payment1.__dict__)

time.sleep(3)

ticket2, payment2 = parking_lot.release_spot(reservation2)
print(ticket2.__dict__)
print(payment2.__dict__)
