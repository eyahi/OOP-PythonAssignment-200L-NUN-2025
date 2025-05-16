from datetime import date, timedelta
from typing import Any
from room import Room
from guest import Guest

class Reservation:


    def __init__(
        self,
        guest: Guest,room: Room,stay_duration_days: int | None = None,
        check_in_date: date | None = None,check_out_date: date | None = None):
        if check_in_date and check_out_date:
            # loaded from CSV
            self._check_in_date  = check_in_date
            self._check_out_date = check_out_date
        elif stay_duration_days is not None:
            today = date.today()
            self._check_in_date  = today
            self._check_out_date = today + timedelta(days=stay_duration_days)
        else:
            raise ValueError("Must supply either stay_duration_days or explicit dates")

        self._guest     = guest
        self._room      = room
        self._is_active = False

    @property
    def guest(self) -> Guest:
        return self._guest

    @property
    def room(self) -> Room:
        return self._room

    @property
    def check_in_date(self) -> date:
        return self._check_in_date

    @property
    def check_out_date(self) -> date:
        return self._check_out_date

    @property
    def is_active(self) -> bool:
        return self._is_active

    def book(self) -> None:
        if not self._room.availability:
            raise RuntimeError(f"Room {self._room.room_number} is not available.")
        self._room.availability = False
        self._is_active         = True

    def cancel(self) -> None:
        if not self._is_active:
            raise RuntimeError("Cannot cancel an inactive reservation.")
        self._room.availability = True
        self._is_active         = False

    def update_stay_duration(self, new_days: int) -> None:
        if not self._is_active:
            raise RuntimeError("Cannot modify an inactive reservation.")
        self._check_out_date = self._check_in_date + timedelta(days=new_days)

    def to_dict(self) -> dict[str, Any]:
        return {
            "Guest ID":       self._guest.guest_id,
            "Guest Name":     self._guest.name,
            "Room Number":    self._room.room_number,
            "Check In Date":  self._check_in_date.isoformat(),
            "Check Out Date": self._check_out_date.isoformat(),
            "Is Active":      self._is_active
        }

    def __str__(self) -> str:
        ci = self._check_in_date.strftime("%d/%m/%Y")
        co = self._check_out_date.strftime("%d/%m/%Y")
        status = "Active" if self._is_active else "Inactive"
        return (
            f"Reservation[{self._guest.guest_id}→{self._room.room_number}] "
            f"{ci} to {co} ({status})"
        )

    def __repr__(self) -> str:
        return str(self)
