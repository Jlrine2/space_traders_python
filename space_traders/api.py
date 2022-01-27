import time
from typing import Optional, Type, Union

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

    @staticmethod
    def _handle_request_response(response):
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
        response = self.session.put(f'{BASE_URL}{url_path}', params={'token': self.token, **params})
        return self._handle_request_response(response)

    def delete(self, url_path, params: Optional[dict] = None):
        if params is None:
            params = {}
        response = self.session.delete(f'{BASE_URL}{url_path}', params={'token': self.token, **params})
        return self._handle_request_response(response)

    def _do_return(self, model: Type[models.BaseModel], response: Union[dict, list]):
        if isinstance(response, list):
            return [self._do_return(model, item) for item in response]
        if 'class' in response:
            response['shipClass'] = response['class']
            del response['class']
        return model(**response)


class Loans(Client):
    def __init__(self, token):
        super().__init__(token)

    def available_loans(self):
        response = self.get('types/loans')
        return self._do_return(models.Loan, response['loans'])

    def take_loan(self, loan):
        response = self.post('my/loans', params={'type': loan.type})
        return self._do_return(models.Loan, response['loan'])

    def my_loans(self):
        response = self.get('my/loans')
        return self._do_return(models.Loan, response['loans'])

    def pay_loan(self, loan_id):
        response = self.put(f'my/loans/{loan_id}')
        loans = response['loans']
        return self._do_return(models.Loan, response['loans'])


class Ships(Client):
    def __init__(self, token):
        super().__init__(token)

    def available_ships(self, system_symbol, ship_class: str):
        response = self.get(f'systems/{system_symbol}/ship-listings', params={'class': ship_class})
        return self._do_return(models.Ship, response['ships'])

    def purchase(self, listing: models.AvailableShip, location_symbol):
        params = {'location': location_symbol, 'type': listing.type}
        response = self.post('my/ships', params=params)
        return self._do_return(models.Ship, response['ship'])

    def refuel(self, ship, quantity):
        params = {'shipId': ship.id, 'good': 'FUEL', 'quantity': quantity}
        response = self.post('my/purchase-orders', params=params)
        return self._do_return(models.Ship, response['ship'])

    def view_ship(self, ship_id):
        response = self.get(f'my/ships/{ship_id}')
        return self._do_return(models.Ship, response['ship'])

    def view_all_ships(self):
        response = self.get('my/ships')
        return self._do_return(models.Ship, response['ships'])

    def create_flight_plan(self, ship: models.Ship, desination_symbol: models.Location):
        params = {'shipId': ship.id, 'destination': desination_symbol}
        response = self.post('my/flight-plans', params=params)
        return self._do_return(models.FlightPlan, response['flightPlan'])

    def view_flight_plan(self, flight_plan_id):
        response = self.get(f'my/flight-plans/{flight_plan_id}')
        return self._do_return(models.FlightPlan, response['flightPlan'])

    def jettison_cargo(self, ship: models.Ship, good_symobol: str, quantity: int):
        params = {'good': good_symobol, 'quantity': quantity}
        response = self.post(f'my/ships/{ship.id}/jettison', params=params)
        return response

    def scrap(self, ship: models.Ship):
        params = {'shipId': ship.id}
        response = self.delete(f'my/ships/{ship.id}/scrap', params=params)
        return response

    def transfer(self, from_ship: models.Ship, to_ship: models.Ship, good_symobol: str, quantity: int):
        params = {'toShipId': to_ship.id, 'good': good_symobol, 'quantity': quantity}
        response = self.post(f'my/ships/{from_ship.id}/transfer', params=params)
        return self._do_return(models.Ship, response['fromShip']), self._do_return(models.Ship, response['toShip'])


class Location(Client):
    def __init__(self, token):
        super().__init__(token)

    def view(self, location_symbol):
        response = self.get(f'locations/{location_symbol}')
        return self._do_return(models.Location, response['location'])

    def ships(self, location_symbol):
        response = self.get(f'locations/{location_symbol}/ships')
        return self._do_return(models.Ship, response['ships'])

    def view_all_locations(self, system_symbol):
        response = self.get(f'systems/{system_symbol}/locations')
        return self._do_return(models.Location, response['locations'])

    def marketplace(self, location_symbol):
        response = self.get(f'locations/{location_symbol}/marketplace')
        return models.Market(goods=self._do_return(models.MarketGood, response['marketplace']), location=location_symbol)


class Structures(Client):
    def __init__(self, token):
        super().__init__(token)

    def create(self, location_symbol, structure_type: str):
        params = {'type': structure_type, 'location': location_symbol}
        response = self.post('my/structures', params=params)
        return self._do_return(models.Structure, response['structures'])

    def deposit(self, structure_id, ship_id, good_symbol: str, quantity: int):
        params = {'shipId': ship_id, 'good': good_symbol, 'quantity': quantity}
        response = self.post(f'my/structures/{structure_id}/deposit', params=params)
        return self._do_return(models.Ship, response['ship']), self._do_return(models.Structure, response['structures'])

    def view(self, structure_id):
        response = self.get(f'my/structures/{structure_id}')
        return self._do_return(models.Structure, response['structure'])

    def view_all(self):
        response = self.get('my/structures')
        return self._do_return(models.Structure, response['structures'])

    def transfer(self, structure_id, ship_id, good_symbol: str, quantity: int):
        params = {'shipId': ship_id, 'good': good_symbol, 'quantity': quantity}
        response = self.post(f'my/structures/{structure_id}/transfer', params=params)
        return self._do_return(models.Structure, response['structures']), self._do_return(models.Ship, response['ship'])


class Api(Client):
    def __init__(self, token):
        super().__init__(token)
        self.loans = Loans(token)
        self.ships = Ships(token)
        self.location = Location(token)

    def purchase(self, ship: models.Ship, good: models.MarketGood, quantity: int):
        params = {'shipId': ship.id, 'good': good.symbol, 'quantity': quantity}
        response = self.post('my/purchase-orders', params=params)
        return self._do_return(models.Ship, response['ship'])

    def sell(self, ship: models.Ship, cargo: models.Cargo, quantity: int):
        params = {'shipId': ship.id, 'good': cargo.good, 'quantity': quantity}
        response = self.post('my/sell-orders', params=params)
        return self._do_return(models.Ship, response['ship'])

    def all_systems(self):
        response = self.get('game/systems')
        return self._do_return(models.System, response['systems'])

    def status(self):
        response = self.get('games/status')
        return response['status']

    def info(self):
        response = self.get('my/account')
        return self._do_return(models.User, response['user'])
