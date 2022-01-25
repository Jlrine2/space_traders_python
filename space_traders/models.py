from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, TypedDict

import dateutil.parser


@dataclass
class Player:
    username: str
    credit_balence: int
    joined_at: datetime
    ship_count: int
    structure_count: int


def get_player(input_dict):
    return Player(
        username=input_dict.get('username'),
        credit_balence=input_dict.get('credits'),
        joined_at=dateutil.parser.parse(input_dict.get('joinedAt')),
        ship_count=input_dict.get('shipCount'),
        structure_count=input_dict.get('structureCount'),
    )


@dataclass
class AvailableLoan:
    amount: int
    collateral_required: bool
    rate: int
    term_in_days: int
    type: str


def get_available_loan(input_dict):
    return AvailableLoan(
        amount=input_dict.get('amount'),
        collateral_required=input_dict.get('collateralRequired'),
        rate=input_dict.get('rate'),
        term_in_days=input_dict.get('termInDays'),
        type=input_dict.get('type'),
    )


@dataclass
class Loan:
    loan_id: str
    due: datetime
    repayment_amount: int
    status: str
    type: str


def get_loan(input_dict):
    return Loan(
        loan_id=input_dict.get('id'),
        due=dateutil.parser.parse(input_dict.get('due')),
        repayment_amount=input_dict.get('repaymentAmount'),
        status=input_dict.get('status'),
        type=input_dict.get('type'),
    )


@dataclass
class Location:
    allows_construction: bool
    docked_ships: int
    name: str
    symbol: str
    type: str
    x: int
    y: int


def get_location(input_dict):
    return Location(
        allows_construction=input_dict.get('allowsConstruction'),
        docked_ships=input_dict.get('dockedShips'),
        name=input_dict.get('name'),
        symbol=input_dict.get('symbol'),
        type=input_dict.get('type'),
        x=input_dict.get('x'),
        y=input_dict.get('y'),
    )


@dataclass
class System:
    name: str
    symbol: str
    locations: List[Location]


def get_system(input_dict):
    return System(
        name=input_dict.get('name'),
        symbol=input_dict.get('symbol'),
        locations=[get_location(location) for location in input_dict.get('locations')]
    )


@dataclass
class Good:
    price_per_unit: int
    quantity_available: int
    symbol: str
    volume_per_unit: int


def get_good(input_dict):
    return Good(
        price_per_unit=input_dict.get('pricePerUnit'),
        quantity_available=input_dict.get('quantityAvailable'),
        symbol=input_dict.get('symbol'),
        volume_per_unit=input_dict.get('volumePerUnit')
    )


@dataclass
class Cargo:
    good: str
    quantity: int
    total_volume: int


def get_cargo(input_dict):
    return Cargo(
        good=input_dict.get('good'),
        quantity=input_dict.get('quantity'),
        total_volume=input_dict.get('totalVolume'),
    )


@dataclass
class PurchaseLocation:
    location: str
    price: int


def get_purchase_location(input_dict):
    return PurchaseLocation(
        location=input_dict.get('location'),
        price=input_dict.get('price')
    )


@dataclass
class ShipListing:
    ship_class: str
    manufacturer: str
    max_cargo: str
    plating: int
    speed: int
    type: str
    weapons: int
    purchase_locations: List[PurchaseLocation]


def get_ship_listing(input_dict):
    return ShipListing(
        ship_class=input_dict.get('class'),
        manufacturer=input_dict.get('manufacturer'),
        max_cargo=input_dict.get('maxCargo'),
        plating=input_dict.get('plating'),
        speed=input_dict.get('speed'),
        type=input_dict.get('type'),
        weapons=input_dict.get('weapons'),
        purchase_locations=[get_purchase_location(loc) for loc in input_dict.get('purchaseLocations')]
    )


@dataclass
class Ship:
    cargo: List[Cargo]
    ship_class: str
    flight_plan_id: str
    ship_id: str
    location: str
    manufacturer: str
    max_cargo: str
    plating: int
    space_available: int
    speed: int
    type: str
    weapons: int
    x: int
    y: int


def get_ship(input_dict):
    return Ship(
        cargo=[get_cargo(cargo) for cargo in input_dict.get('cargo')],
        ship_class=input_dict.get('class'),
        flight_plan_id=input_dict.get('flightPlanId'),
        ship_id=input_dict.get('id'),
        location=input_dict.get('location'),
        manufacturer=input_dict.get('manufacturer'),
        max_cargo=input_dict.get('maxCargo'),
        plating=input_dict.get('plating'),
        space_available=input_dict.get('spaceAvailable'),
        speed=input_dict.get('speed'),
        type=input_dict.get('type'),
        weapons=input_dict.get('weapons'),
        x=input_dict.get('x'),
        y=input_dict.get('y'),
    )


@dataclass
class FlightPlan:
    arrive_at: datetime
    departure: str
    destination: str
    distance: int
    fuel_consumed: int
    fuel_remaining: int
    flight_plan_id: str
    ship_id: Ship
    terminated_at: datetime
    time_remaining: timedelta


def get_flight_plan(input_dict):
    terminated_at = input_dict.get('terminatedAt')
    if terminated_at:
        terminated_at = dateutil.parser.parse(terminated_at)
    return FlightPlan(
        arrive_at=dateutil.parser.parse(input_dict.get('arrivesAt')),
        departure=input_dict.get('departure'),
        destination=input_dict.get('destination'),
        distance=input_dict.get('distance'),
        fuel_consumed=input_dict.get('fuelConsumed'),
        fuel_remaining=input_dict.get('fuelRemaining'),
        flight_plan_id=input_dict.get('id'),
        ship_id=input_dict.get('shipId'),
        terminated_at=terminated_at,
        time_remaining=timedelta(seconds=input_dict.get('timeRemainingInSeconds')),
    )


@dataclass
class Inventory:
    good: str
    quantity: int


def get_inventory(input_dict):
    return Inventory(
        good=input_dict.get('good'),
        quantity=input_dict.get('quantity'),
    )


@dataclass
class Structure:
    active: bool
    consumes: List[str]
    id: str
    inventory: List[Inventory]
    location: str
    owner: str
    produces: List[str]
    status: str
    type: str


def get_structure(input_dict):
    return Structure(
        active=input_dict.get('active'),
        consumes=input_dict.get('consumes'),
        id=input_dict.get('id'),
        inventory=[get_inventory(item) for item in input_dict.get('inventory')],
        location=input_dict.get('location'),
        owner=input_dict.get('ownedBy'),
        produces=input_dict.get('produces'),
        status=input_dict.get('status'),
        type=input_dict.get('type'),
    )


