from dataclasses import dataclass
from typing import List, Mapping


@dataclass
class BaseModel:
    @staticmethod
    def from_api_response(*args, **kwargs):
        raise NotImplementedError('from_api_response not implemented for this model, try using the constructor')


@dataclass
class User(BaseModel):
    credits: int = None
    joinedAt: str = None
    shipCount: int = None
    StructureCount: int = None
    username: str = None


@dataclass
class FlightPlan(BaseModel):
    arrivesAt: str = None
    createdAt: str = None
    departure: str = None
    destination: str = None
    distance: int = None
    fuelConsumed: int = None
    fuelRemaining: int = None
    id: str = None
    shipId: str = None
    terminatedAt: str = None
    timeRemainingInSeconds: int = None


@dataclass
class Loan(BaseModel):
    due: str = None
    id: str = None
    repaymentAmount: int = None
    status: str = None
    type: str = None


@dataclass
class Cargo(BaseModel):
    good: str = None
    quantity: int = None
    totalVolume: int = None


@dataclass
class Ship(BaseModel):
    cargo: List[Cargo] = None
    shipClass: str = None
    flightPlanId: str = None
    id: str = None
    location: str = None
    manufacturer: str = None
    maxCargo: int = None
    plating: int = None
    spaceAvailable: int = None
    speed: int = None
    type: str = None
    weapons: int = None
    loadingSpeed: int = None
    restrictedGoods: Mapping[str, str] = None
    x: int = None
    y: int = None

    @staticmethod
    def from_api_response(data: dict):
        data['shipClass'] = data['class']
        del data['class']
        data['cargo'] = [Cargo(**cargo) for cargo in data['cargo']]
        del data['cargo']
        return Ship(**data)


@dataclass
class Item(BaseModel):
    good: str = None
    quantity: int = None


@dataclass
class Structure(BaseModel):
    active: bool = None
    consumes: List[str] = None
    id: str = None
    inventory: List[Item] = None
    location: str = None
    ownedBy: Mapping[str, str] = None
    produces: List[str] = None
    status: str = None
    type: str = None


@dataclass
class Location(BaseModel):
    allowsConstruction: bool = None
    dockedShips: int = None
    name: str = None
    symbol: str = None
    type: str = None
    x: int = None
    y: int = None


@dataclass
class System(BaseModel):
    symbol: str = None
    name: str = None


@dataclass
class AvailableGood(BaseModel):
    name: str = None
    symbol: str = None
    volumePerUnit: int = None


@dataclass
class AvailableLoan(BaseModel):
    amount: int = None
    collateralRequired: int = None
    rate: 40 = None
    termInDays: int = None
    type: str = None


@dataclass
class AvailableStructures(BaseModel):
    allowedLocationTypes: List[str] = None
    consumes: List[str] = None
    name: str = None
    price: int = None
    produces: List[str] = None
    type: str = None

@dataclass
class PurchaseLocation(BaseModel):
    location: str = None
    price: int = None
    system: str = None


@dataclass
class AvailableShip(BaseModel):
    shipClass: str = None
    manufacturer: str = None
    maxCargo: int = None
    plating: int = None
    speed: int = None
    type: str = None
    weapons: int = None
    purchaseLocations: List[PurchaseLocation] = None

    @staticmethod
    def from_api_response(data: dict):
        data['shipClass'] = data['class']
        data['purchaseLocations'] = [PurchaseLocation(**p) for p in data['purchaseLocations']]
        del data['class']
        return AvailableShip(**data)


@dataclass
class MarketGood(BaseModel):
    pricePerUnit: int = None
    purchasePricePerUnit: int = None
    quantityAvailable: int = None
    sellPricePerUnit: int = None
    spread: int = None
    symbol: str = None
    volumePerUnit: int = None


@dataclass
class Market(BaseModel):
    goods: List[MarketGood] = None
    location: str = None

    @staticmethod
    def from_api_response(data: dict):
        data['goods'] = [MarketGood(**g) for g in data['goods']]
        return Market(**data)
