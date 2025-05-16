import csv
from datetime import date
from room import Room
from guest import Guest
from reservation import Reservation

class HotelManagement:
    ROOMS_FILE        = "rooms.csv"
    GUESTS_FILE       = "guests.csv"
    RESERVATIONS_FILE = "reservations.csv"

    def __init__(self):
        self.rooms        : dict[int,Room]        = {}
        self.guests       : dict[str,Guest]       = {}
        self.reservations : list[Reservation]      = []

    # ─── Loading ───────────────────────────────────────────────────────

    def load_data(self) -> None:
        self._load_rooms()
        self._load_guests()
        self._load_reservations()

    def _load_rooms(self) -> None:
        try:
            with open(self.ROOMS_FILE, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    num = int(row["Room Number"])
                    room = Room(
                        room_number = num,
                        room_type   = row["Room Type"],
                        price       = float(row["Price"]),
                        availability= row["Availability"].lower()=="true"
                    )
                    self.rooms[num] = room
        except FileNotFoundError:
            pass

    def _load_guests(self) -> None:
        try:
            with open(self.GUESTS_FILE, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    guest = Guest(
                        name         = row["Name"],
                        contact_info = row["Contact Info"],
                        guest_id     = row["Guest ID"]
                    )
                    self.guests[guest.guest_id] = guest
        except FileNotFoundError:
            pass

    def _load_reservations(self) -> None:
        try:
            with open(self.RESERVATIONS_FILE, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    gid = row["Guest ID"]
                    rid = int(row["Room Number"])
                    ci  = date.fromisoformat(row["Check In Date"])
                    co  = date.fromisoformat(row["Check Out Date"])
                    guest = self.guests.get(gid)
                    room  = self.rooms.get(rid)
                    if not guest or not room:
                        continue
                    res = Reservation(
                        guest          = guest,
                        room           = room,
                        check_in_date  = ci,
                        check_out_date = co
                    )
                    if row["Is Active"].lower() == "true":
                        res._is_active = True
                        res.room.availability = False
                    self.reservations.append(res)
        except FileNotFoundError:
            pass

    # ─── Saving ────────────────────────────────────────────────────────

    def save_data(self) -> None:
        # Rooms
        with open(self.ROOMS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Room Number","Room Type","Price","Availability"]
            )
            writer.writeheader()
            for r in self.rooms.values():
                writer.writerow(r.to_dict())

        # Guests
        with open(self.GUESTS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Guest ID","Name","Contact Info"]
            )
            writer.writeheader()
            for g in self.guests.values():
                writer.writerow(g.to_dict())

        # Reservations
        with open(self.RESERVATIONS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "Guest ID","Guest Name",
                    "Room Number","Check In Date","Check Out Date","Is Active"
                ]
            )
            writer.writeheader()
            for res in self.reservations:
                # only active or we want to keep history?
                writer.writerow(res.to_dict())

    # ─── Guest Operations ─────────────────────────────────────────────

    def add_guest(self, guest: Guest) -> None:
        self.guests[guest.guest_id] = guest
        self.save_data()

    # ─── Reservation Operations ────────────────────────────────────────

    def make_reservation(
        self,guest: Guest,room_number: int,stay_duration_days: int
        ) -> Reservation:
        if room_number not in self.rooms:
            raise KeyError(f"Room {room_number} does not exist.")
        # prevent double-booking of same room:
        room = self.rooms[room_number]
        if not room.availability:
            raise RuntimeError("Room is not available.")

        res = Reservation(guest, room, stay_duration_days=stay_duration_days)
        res.book()
        self.reservations.append(res)
        self.save_data()
        return res

    def modify_reservation(self, reservation: Reservation, new_days: int) -> None:
        reservation.update_stay_duration(new_days)
        self.save_data()

    def cancel_reservation(self, reservation: Reservation) -> None:
        reservation.cancel()
        # remove it from our list
        self.reservations = [r for r in self.reservations if r is not reservation]
        self.save_data()
