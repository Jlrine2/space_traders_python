from typing import List, Mapping


class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


class User(BaseModel):
    credits: int = None
    joinedAt: str = None
    shipCount: int = None
    structureCount: int = None
    username: str = None

    def __init__(
            self,
            credits: int = None,
            joinedAt: str = None,
            shipCount: int = None,
            structureCount: int = None,
            username: str = None
    ):
        super().__init__(
            credits=credits,
            joinedAt=joinedAt,
            shipCount=shipCount,
            StructureCount=structureCount,
            username=username
        )


class FlightPlan(BaseModel):
    arriveAt: str = None
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

    def __init__(
            self,
            arrivesAt: str = None,
            createdAt: str = None,
            departure: str = None,
            destination: str = None,
            distance: int = None,
            fuelConsumed: int = None,
            fuelRemaining: int = None,
            id: str = None,
            shipId: str = None,
            terminatedAt: str = None,
            timeRemainingInSeconds: int = None,
    ):
        super().__init__(
            arrivesAt=arrivesAt,
            createdAt=createdAt,
            departure=departure,
            destination=destination,
            distance=distance,
            fuelConsumed=fuelConsumed,
            fuelRemaining=fuelRemaining,
            id=id,
            shipId=shipId,
            terminatedAt=terminatedAt,
            timeRemainingInSeconds=timeRemainingInSeconds,
        )


class Loan(BaseModel):
    due: str = None
    id: str = None
    repaymentAmount: int = None
    status: str = None
    type: str = None

    def __init__(
            self,
            due: str = None,
            id: str = None,
            repaymentAmount: int = None,
            status: str = None,
            type: str = None,
    ):
        super().__init__(
            due=due,
            id=id,
            repaymentAmount=repaymentAmount,
            status=status,
            type=type,
        )


class Cargo(BaseModel):
    good: str = None
    quantity: int = None
    totalVolume: int = None

    def __init__(
            self,
            good: str = None,
            quantity: int = None,
            totalVolume: int = None,
    ):
        super().__init__(
            good=good,
            quantity=quantity,
            totalVolume=totalVolume,
        )


class Ship(BaseModel):
    cargo: List[Mapping[str, str]] = None
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
    restrictedGoods: list[str] = None
    x: int = None
    y: int = None

    def __init__(
            self,
            cargo: List[Mapping[str, str]] = None,
            shipClass: str = None,
            flightPlanId: str = None,
            id: str = None,
            location: str = None,
            manufacturer: str = None,
            maxCargo: int = None,
            plating: int = None,
            spaceAvailable: int = None,
            speed: int = None,
            type: str = None,
            weapons: int = None,
            loadingSpeed: int = None,
            restrictedGoods: list[str]= None,
            x: int = None,
            y: int = None,
    ):
        super().__init__(
            cargo=[Cargo(**cargo) for cargo in cargo],
            shipClass=shipClass,
            flightPlanId=flightPlanId,
            id=id,
            location=location,
            manufacturer=manufacturer,
            maxCargo=maxCargo,
            plating=plating,
            spaceAvailable=spaceAvailable,
            speed=speed,
            type=type,
            weapons=weapons,
            loadingSpeed=loadingSpeed,
            restrictedGoods=restrictedGoods,
            x=x,
            y=y,
        )


class Item(BaseModel):
    good: str = None
    quantity: int = None
    def __init__(
            self,
            good: str = None,
            quantity: int = None,
    ):
        super().__init__(
            good=good,
            quantity=quantity,
        )


class Structure(BaseModel):
    active: bool = None
    consumes: List[str] = None,
    id: str = None,
    inventory: List[Item] = None,
    location: str = None,
    ownedBy: Mapping[str, str] = None,
    produces: List[str] = None,
    status: str = None,
    type: str = None,
    def __init__(
            self,
            active: bool = None,
            consumes: List[str] = None,
            id: str = None,
            inventory: List[Item] = None,
            location: str = None,
            ownedBy: Mapping[str, str] = None,
            produces: List[str] = None,
            status: str = None,
            type: str = None,
    ):
        super().__init__(
            active=active,
            consumes=consumes,
            id=id,
            inventory=[Item(**item) for item in inventory],
            location=location,
            ownedBy=ownedBy,
            produces=produces,
            status=status,
            type=type,
        )


class Location(BaseModel):
    allowsConstruction: bool = None
    dockedShips: int = None
    name: str = None
    symbol: str = None
    type: str = None
    x: int = None
    y: int = None

    def __init__(
            self,
            allowsConstruction: bool = None,
            dockedShips: int = None,
            name: str = None,
            symbol: str = None,
            type: str = None,
            x: int = None,
            y: int = None,
    ):
        super().__init__(
            allowsConstruction=allowsConstruction,
            dockedShips=dockedShips,
            name=name,
            symbol=symbol,
            type=type,
            x=x,
            y=y,
        )


class System(BaseModel):
    symbol: str = None
    name: str = None

    def __init__(
            self,
            symbol: str = None,
            name: str = None,
    ):
        super().__init__(
            symbol=symbol,
            name=name,
        )


class AvailableGood(BaseModel):
    name: str = None
    symbol: str = None
    volumePerUnit: int = None

    def __init__(
            self,
            name: str = None,
            symbol: str = None,
            volumePerUnit: int = None
    ):
        super().__init__(
            name=name,
            symbol=symbol,
            volumePerUnit=volumePerUnit,
        )


class AvailableLoan(BaseModel):
    amount: int = None
    collateralRequired: int = None
    rate: 40 = None
    termInDays: int = None
    type: str = None

    def __init__(
            self,
            amount: int = None,
            collateralRequired: int = None,
            rate: 40 = None,
            termInDays: int = None,
            type: str = None,
    ):
        super().__init__(
            amount=amount,
            collateralRequired=collateralRequired,
            rate=rate,
            termInDays=termInDays,
            type=type,
        )


class AvailableStructures(BaseModel):
    allowedLocationTypes: List[str] = None
    consumes: List[str] = None
    name: str = None
    price: int = None
    produces: List[str] = None
    type: str = None

    def __init__(
            self,
            allowedLocationTypes: List[str] = None,
            consumes: List[str] = None,
            name: str = None,
            price: int = None,
            produces: List[str] = None,
            type: str = None,
    ):
        super().__init__(
            allowedLocationTypes=allowedLocationTypes,
            consumes=consumes,
            name=name,
            price=price,
            produces=produces,
            type=type,
        )


class PurchaseLocation(BaseModel):
    location: str = None
    price: int = None
    system: str = None

    def __init__(
            self,
            location: str = None,
            price: int = None,
            system: str = None,
    ):
        super().__init__(
            location=location,
            price=price,
            system=system,
        )


class AvailableShip(BaseModel):
    shipClass: str = None
    manufacturer: str = None
    maxCargo: int = None
    plating: int = None
    speed: int = None
    type: str = None
    weapons: int = None
    purchaseLocations: List[PurchaseLocation] = None

    def __init__(
            self,
            shipClass: str = None,
            manufacturer: str = None,
            maxCargo: int = None,
            plating: int = None,
            speed: int = None,
            type: str = None,
            weapons: int = None,
            purchaseLocations: List[PurchaseLocation] = None,
    ):
        super().__init__(
            shipClass=shipClass,
            manufacturer=manufacturer,
            maxCargo=maxCargo,
            plating=plating,
            speed=speed,
            type=type,
            weapons=weapons,
            purchaseLocations=[PurchaseLocation(**purchaseLocation) for purchaseLocation in purchaseLocations],
        )


class MarketGood(BaseModel):
    pricePerUnit: int = None
    purchasePricePerUnit: int = None
    quantityAvailable: int = None
    sellPricePerUnit: int = None
    spread: int = None
    symbol: str = None
    volumePerUnit: int = None

    def __init__(
            self,
            pricePerUnit: int = None,
            purchasePricePerUnit: int = None,
            quantityAvailable: int = None,
            sellPricePerUnit: int = None,
            spread: int = None,
            symbol: str = None,
            volumePerUnit: int = None,
    ):
        super().__init__(
            pricePerUnit=pricePerUnit,
            purchasePricePerUnit=purchasePricePerUnit,
            quantityAvailable=quantityAvailable,
            sellPricePerUnit=sellPricePerUnit,
            spread=spread,
            symbol=symbol,
            volumePerUnit=volumePerUnit,
        )


class Market(BaseModel):
    goods: List[MarketGood] = None
    location: str = None

    def __init__(
            self,
            goods: List[MarketGood] = None,
            location: str = None,
    ):
        super().__init__(
            goods=[MarketGood(**marketGood) for marketGood in goods],
            location=location,
        )
