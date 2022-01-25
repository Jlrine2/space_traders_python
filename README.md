# Space Traders Python

SDK for interacting with the [SpaceTraders API](https://spacetraders.io/)


## Usage:
create an instance of the api
```python
from space_traders import Api

api = Api('TOKEN')
```

check account
```python
api.info()
```