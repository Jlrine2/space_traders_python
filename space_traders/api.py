import time
from typing import Optional

import requests

from space_traders import models

BASE_URL = 'https://api.spacetraders.io/'


class ApiError(Exception):
    pass


def register(username):
    url = f'{BASE_URL}/users/{username}/claim'
    response = requests.post(url)
    return response.json()


class Client:
    def __init__(self, token=None):
        if token is None:
            raise ValueError('Must provide token')
        self.token = token
        self.session = requests.session()

    def _handle_request_response(self, response):
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ApiError(f'Error {response.status_code}, {response.json()}')
        if int(response.headers.get('x-ratelimit-remaining')) == 0:
            time.sleep(1)
        return response.json()

    def get(self, url_path, params: Optional[dict] = None):
        if params is None:
            params = {}
        response = self.session.get(f'{BASE_URL}{url_path}', params={'token': self.token, **params})
        return self._handle_request_response(response)

    def post(self, url_path, params: Optional[dict] = None):
        if params is None:
            params = {}
        response = self.session.post(f'{BASE_URL}{url_path}', params={'token': self.token, **params})
        return self._handle_request_response(response)

    def put(self, url_path, params: Optional[dict] = None):
        if params is None:
            params = {}
        response = self.session.post(f'{BASE_URL}{url_path}', params={'token': self.token, **params})
        return self._handle_request_response(response)

    def status(self):
        response = self.get('games/status')
        return response['status']

    def info(self):
        response = self.get('my/account')
        return models.get_player(response['user'])


class Loans(Client):
    def __init__(self, token):
        super().__init__(token)

    def available_loans(self):
        response = self.get('types/loans')
        return [models.get_available_loan(loan) for loan in response['loans']]

    def take_loan(self, loan):
        response = self.post('my/loans', params={'type': loan.type})
        return models.get_loan(response['loan'])

    def my_loans(self):
        response = self.get('my/loans')
        return [models.get_loan(loan) for loan in response['loans']]

    def pay_loan(self, loan_id):
        response = self.put(f'my/loans/{loan_id}')
        loans = response.json()['loans']
        return [models.get_loan(loan) for loan in loans]


class Ships(Client):
    def __init__(self, token):
        super().__init__(token)

    def available_ships(self, system_symbol, ship_class: str):
        response = self.get(f'systems/{system_symbol}/ship-listings', params={'class': ship_class})
        return [models.get_ship_listing(ship) for ship in response['shipListings']]

    def purchase_ship(self, listing: models.ShipListing, location_symbol):
        params = {'location': location_symbol, 'type': listing.type}
        response = self.post('my/ships', params=params)
        return models.get_ship(response['ship'])

    def purchase_fuel(self, ship, quantity):
        params = {'shipId': ship.ship_id, 'good': 'FUEL', 'quantity': quantity}
        response = self.post('my/purchase-orders', params=params)
        return models.get_ship(response['ship'])

    def my_ships(self):
        response = self.get('my/ships')
        return [models.get_ship(ship) for ship in response['ships']]

    def create_flight_plan(self, ship: models.Ship, desination_symbol: models.Location):
        params = {'shipId': ship.ship_id, 'destination': desination_symbol}
        response = self.post('my/flight-plans', params=params)
        return models.get_flight_plan(response['flightPlan'])

    def view_flight_plan(self, flight_plan_id):
        response = self.get(f'my/flight-plans/{flight_plan_id}')
        return models.get_flight_plan(response['flightPlan'])


class Location(Client):
    def __init__(self, token):
        super().__init__(token)

    def location_info(self, location_symbol):
        response = self.get(f'locations/{location_symbol}')
        return models.get_location(response['location'])


class Api(Client):
    def __init__(self, token):
        super().__init__(token)
        self.loans = Loans(token)
        self.ships = Ships(token)
        self.location = Location(token)

    def purchase(self, ship: models.Ship, good: models.Good, quantity: int):
        params = {'shipId': ship.ship_id, 'good': good.symbol, 'quantity': quantity}
        response = self.post('my/purchase-orders', params=params)
        return models.get_ship(response['ship'])

    def sell(self, ship: models.Ship, cargo: models.Cargo, quantity: int):
        params = {'shipId': ship.ship_id, 'good': cargo.good, 'quantity': quantity}
        response = self.post('my/sell-orders', params=params)
        return models.get_ship(response['ship'])

    def all_systems(self):
        response = self.get('game/systems')
        return [models.get_system(system) for system in response['systems']]

    def marketplace(self, location_symbol):
        response = self.get(f'locations/{location_symbol}/marketplace')
        return [models.get_good(good) for good in response['marketplace']]