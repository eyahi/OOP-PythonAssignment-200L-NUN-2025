=============================================================
HOTEL MANAGEMENT SYSTEM  –  Python 3 + Tkinter
=============================================================

A phone-sized desktop app (360 x 640 window) for front-desk staff.

 • Register or log-in guests (fixed 8-character IDs).
 • Search available rooms and create new bookings.
 • View current bookings for the logged-in guest.
 • Modify a booking’s stay length or cancel it.
 • Data is persisted in three CSV files (rooms / guests / reservations).
 • No external libraries required – just Python 3 and the Tkinter that ships
   with CPython.

-------------------------------------------------------------
1.  PROJECT STRUCTURE
-------------------------------------------------------------
 hotel-management/
 ├── GUI.py                Tkinter front-end (5 stacked frames)
 ├── hotel_management.py   Data manager
 ├── room.py               Room entity
 ├── guest.py              Guest entity
 ├── reservation.py        Reservation entity
 ├── rooms.csv             Seeded list of 50 rooms
 ├── guests.csv            Starts with header only
 └── reservations.csv      Starts with header only

-------------------------------------------------------------
2.  CSV LAYOUTS
-------------------------------------------------------------
 rooms.csv
   Room Number , Room Type , Price , Availability (True/False)

 guests.csv
   Guest ID , Name , Contact Info

 reservations.csv
   Guest ID , Guest Name , Room Number ,
   Check In Date , Check Out Date , Is Active (True/False)

 All dates are stored in ISO format  YYYY-MM-DD.

-------------------------------------------------------------
3.  HOW TO RUN
-------------------------------------------------------------
 1.  Install Python 3.10+ (Tkinter is included on Windows/macOS.
     On Debian/Ubuntu:  sudo apt install python3-tk)

 2.  From the project folder:
        python GUI.py

 3.  A 360 x 640 sky-blue window appears.

     • Select an existing guest OR enter Name + Contact and click
       “Register & Log In”.
     • Main menu shows:
          – Search and Book
          – View Bookings
          – Generate Receipt  (modify / cancel booking)
          – Logout
     • All changes are saved immediately back to the CSV files.

-------------------------------------------------------------
4.  SCREEN SUMMARY
-------------------------------------------------------------
 LOGIN
   Choose existing guest or register a new one.

 MAIN MENU
   Search and Book   /   View Bookings   /   Generate Receipt   /   Logout

 SEARCH & BOOK
   Room Type  ->  Room #  ->  Stay days   ->  Book

 VIEW BOOKINGS
   Table shows Room, Check-in, Check-out for current guest.

 MODIFY BOOKINGS
   Same table + “Modify” button.
   • Modify   – change stay length.
   • Cancel   – delete booking and free room.

-------------------------------------------------------------
5.  CODE OVERVIEW
-------------------------------------------------------------
 room.py            Room(number, type, price, availability)
 guest.py           Guest(id, name, contact_info)
 reservation.py     Reservation(book, cancel, update)
 hotel_management.py
   – loads/saves CSV
   – add_guest / make_reservation / modify_reservation / cancel_reservation
 GUI.py
   – five Tkinter frames (login, menu, book, view, modify)
   – phone portrait size, grey theme, styled Treeview grids

-------------------------------------------------------------
