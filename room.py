class Room:


    def __init__(self, room_number: int, room_type: str, price: float, availability: bool = True):
        self._room_number  = room_number
        self._room_type    = room_type
        self._price        = price
        self._availability = availability

    @property
    def room_number(self) -> int:
        return self._room_number

    @property
    def room_type(self) -> str:
        return self._room_type

    @property
    def price(self) -> float:
        return self._price

    @property
    def availability(self) -> bool:
        return self._availability

    @availability.setter
    def availability(self, val: bool):
        self._availability = val

    def to_dict(self) -> dict:
        return {
            "Room Number":   self._room_number,
            "Room Type":     self._room_type,
            "Price":         self._price,
            "Availability":  self._availability
        }

    def __str__(self) -> str:
        status = "Available" if self._availability else "Occupied"
        return f"Room {self._room_number} ({self._room_type}) — {status} @ ${self._price:.2f}"

    def __repr__(self) -> str:
        return str(self)
