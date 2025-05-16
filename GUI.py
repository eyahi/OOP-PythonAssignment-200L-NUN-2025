import tkinter as tk
from tkinter import ttk, messagebox
from hotel_management import HotelManagement
from guest import Guest

class HotelApp:
    def __init__(self, root):
        self.root = root
        root.title("Hotel Management")
        root.geometry("360x640")
        root.resizable(False, False)
        root.configure(bg="skyblue")

        # ─── Styles ───────────────────────────────────────────────────
        self.style = ttk.Style(root)
        self.style.theme_use('default')

        # Accent button style (bright blue, white text, padded)
        self.style.configure(
            'Accent.TButton',
            background='#4eb5f1',
            foreground='white',
            font=('Helvetica', 16),
            padding=10,
            borderwidth=0
        )
        self.style.map(
            'Accent.TButton',
            background=[('active', '#66c3ff')]
        )

        # Treeview style (taller rows, bold headings, light header bg)
        self.style.configure(
            'Custom.Treeview',
            rowheight=28,
            font=('Helvetica', 12),
            fieldbackground='white'
        )
        self.style.configure(
            'Custom.Treeview.Heading',
            font=('Helvetica', 13, 'bold'),
            background='#e0e0e0'
        )
        self.style.layout('Custom.Treeview', self.style.layout('Treeview'))

        # ─── Backend ──────────────────────────────────────────────────
        self.hm = HotelManagement()
        self.hm.load_data()
        self.current_guest = None

        # ─── Frames ───────────────────────────────────────────────────
        self.login_frame  = tk.Frame(root, bg="gray")
        self.menu_frame   = tk.Frame(root, bg="gray")
        self.book_frame   = tk.Frame(root, bg="gray")
        self.view_frame   = tk.Frame(root, bg="gray")
        self.modify_frame = tk.Frame(root, bg="gray")
        for f in (
            self.login_frame,
            self.menu_frame,
            self.book_frame,
            self.view_frame,
            self.modify_frame
        ):
            f.place(relwidth=1, relheight=1)

        # ─── Build UI ─────────────────────────────────────────────────
        self._build_login()
        self._build_menu()
        self._build_book()
        self._build_view()
        self._build_modify()

        # start on login
        self._show(self.login_frame)

    def _show(self, frame):
        frame.tkraise()

    # ─── Login Screen ───────────────────────────────────────────────

    def _build_login(self):
        frm = self.login_frame
        frm.columnconfigure(0, weight=1)

        ttk.Label(frm, text="Select Existing Guest:", background="gray",
                  font=('Helvetica',12)).grid(row=0, column=0, pady=(30,5))
        self.cb_guest = ttk.Combobox(frm, state="readonly")
        self.cb_guest.grid(row=1, column=0, sticky="we", padx=30)

        ttk.Button(frm, text="Log In", style='Accent.TButton',
                   command=self._on_login).grid(row=2, column=0, pady=15, padx=50)

        ttk.Separator(frm, orient="horizontal")\
            .grid(row=3, column=0, sticky="ew", padx=30, pady=15)

        ttk.Label(frm, text="Name:", background="gray").grid(
            row=4, column=0, sticky="w", padx=30
        )
        self.e_name = ttk.Entry(frm)
        self.e_name.grid(row=5, column=0, sticky="we", padx=30, pady=5)

        ttk.Label(frm, text="Contact Info:", background="gray").grid(
            row=6, column=0, sticky="w", padx=30, pady=(10,0)
        )
        self.e_contact = ttk.Entry(frm)
        self.e_contact.grid(row=7, column=0, sticky="we", padx=30, pady=5)

        ttk.Button(frm, text="Register & Log In", style='Accent.TButton',
                   command=self._on_register).grid(row=8, column=0, pady=25, padx=50)

        self._reload_guest_list()

    def _reload_guest_list(self):
        self._guest_map = {
            f"{g.name} — {g.contact_info}": g.guest_id
            for g in self.hm.guests.values()
        }
        self.cb_guest['values'] = list(self._guest_map)
        self.cb_guest.set("")

    def _on_login(self):
        sel = self.cb_guest.get()
        gid = self._guest_map.get(sel)
        if not gid:
            messagebox.showwarning("Login Error", "Please select a guest.")
            return
        self.current_guest = self.hm.guests[gid]
        self._enter_menu()

    def _on_register(self):
        name    = self.e_name.get().strip()
        contact = self.e_contact.get().strip()
        if not name or not contact:
            messagebox.showwarning("Input Error", "Name & Contact required.")
            return
        guest = Guest(name=name, contact_info=contact)
        self.hm.add_guest(guest)
        self.current_guest = guest
        self._reload_guest_list()
        self._enter_menu()


    # ─── Main Menu ──────────────────────────────────────────────────

    def _build_menu(self):
        frm = self.menu_frame
        frm.columnconfigure(0, weight=1)

        self.lbl_welcome = ttk.Label(
            frm, text="", background="gray",
            font=('Helvetica', 16, 'bold')
        )
        self.lbl_welcome.grid(row=0, column=0, pady=40)

        ttk.Button(frm, text="Make New Booking", style='Accent.TButton',
                   command=self._enter_book).grid(row=1, column=0, pady=8, padx=60)
        ttk.Button(frm, text="View Bookings", style='Accent.TButton',
                   command=self._enter_view).grid(row=2, column=0, pady=8, padx=60)
        ttk.Button(frm, text="Modify Bookings", style='Accent.TButton',
                   command=self._enter_modify).grid(row=3, column=0, pady=8, padx=60)
        ttk.Button(frm, text="Logout", style='Accent.TButton',
                   command=self._logout).grid(row=4, column=0, pady=30, padx=60)

    def _enter_menu(self):
        self.lbl_welcome.config(
            text=f"Hello, {self.current_guest.name} ({self.current_guest.guest_id})"
        )
        self._show(self.menu_frame)

    def _logout(self):
        self.current_guest = None
        self.e_name.delete(0, 'end')
        self.e_contact.delete(0, 'end')
        self._reload_guest_list()
        self._show(self.login_frame)


    # ─── Search & Book Screen ───────────────────────────────────────

    def _build_book(self):
        frm = self.book_frame
        frm.columnconfigure(0, weight=1)

        ttk.Label(frm, text="Room Type:", background="gray").grid(
            row=0, column=0, sticky="w", padx=30, pady=(30,5)
        )
        self.cb_type = ttk.Combobox(frm, state="readonly")
        self.cb_type.grid(row=1, column=0, padx=30, sticky="we")
        self.cb_type.bind("<<ComboboxSelected>>", lambda e: self._refresh_rooms())

        ttk.Label(frm, text="Room #:", background="gray").grid(
            row=2, column=0, sticky="w", padx=30, pady=(20,5)
        )
        self.cb_rooms = ttk.Combobox(frm, state="readonly")
        self.cb_rooms.grid(row=3, column=0, padx=30, sticky="we")

        ttk.Label(frm, text="Stay (days):", background="gray").grid(
            row=4, column=0, sticky="w", padx=30, pady=(20,5)
        )
        self.e_days = ttk.Entry(frm)
        self.e_days.grid(row=5, column=0, padx=30, sticky="we")

        ttk.Button(frm, text="Book", style='Accent.TButton',
                   command=self._on_book).grid(
            row=6, column=0, pady=20, padx=80
        )
        ttk.Button(frm, text="Logout", style='Accent.TButton',
                   command=self._logout).grid(
            row=7, column=0, pady=10, padx=80
        )

    def _enter_book(self):
        types = sorted({r.room_type for r in self.hm.rooms.values()})
        self.cb_type['values'] = types
        self.cb_type.set('')
        self.cb_rooms.set('')
        self.e_days.delete(0, 'end')
        self._show(self.book_frame)

    def _refresh_rooms(self):
        sel = self.cb_type.get().lower().strip()
        avail = [
            r.room_number for r in self.hm.rooms.values()
            if r.room_type.lower()==sel and r.availability
        ]
        self.cb_rooms['values'] = avail
        self.cb_rooms.set('')

    def _on_book(self):
        try:
            room_no = int(self.cb_rooms.get())
            days    = int(self.e_days.get())
            if days<1: raise ValueError
        except:
            messagebox.showwarning(
                "Input Error",
                "Pick a room and enter a positive number of days."
            )
            return
        try:
            self.hm.make_reservation(self.current_guest, room_no, days)
            messagebox.showinfo("Success", f"Booked room {room_no} for {days} days.")
        except Exception as e:
            messagebox.showerror("Booking Failed", str(e))
            return
        self._refresh_rooms()


    # ─── View Bookings Screen ───────────────────────────────────────

    def _build_view(self):
        frm = self.view_frame
        frm.columnconfigure(0, weight=1)

        cols = ("Room","Check-in","Check-out")
        self.tv_view = ttk.Treeview(
            frm, columns=cols, show="headings",
            style='Custom.Treeview', height=10
        )
        for c in cols:
            self.tv_view.heading(c, text=c)
            self.tv_view.column(c, width=100, anchor="center")
        self.tv_view.grid(row=0, column=0, pady=(30,10), padx=10)

        ttk.Button(frm, text="Back", style='Accent.TButton',
                   command=self._enter_menu).grid(row=1, column=0, pady=20, padx=100)

    def _enter_view(self):
        self.tv_view.delete(*self.tv_view.get_children())
        for res in self.hm.reservations:
            if res.guest.guest_id == self.current_guest.guest_id and res.is_active:
                self.tv_view.insert("", "end", values=(
                    res.room.room_number,
                    res.check_in_date.strftime("%d/%m/%Y"),
                    res.check_out_date.strftime("%d/%m/%Y")
                ))
        self._show(self.view_frame)


    # ─── Modify Bookings Screen ────────────────────────────────────

    def _build_modify(self):
        frm = self.modify_frame
        frm.columnconfigure(0, weight=1)

        cols = ("Room","Check-in","Check-out")
        self.tv_mod = ttk.Treeview(
            frm, columns=cols, show="headings",
            style='Custom.Treeview', height=8
        )
        for c in cols:
            self.tv_mod.heading(c, text=c)
            self.tv_mod.column(c, width=100, anchor="center")
        self.tv_mod.grid(row=0, column=0, pady=(30,10), padx=10)

        btn_frame = tk.Frame(frm, bg="gray")
        btn_frame.grid(row=1, column=0, pady=20)
        ttk.Button(btn_frame, text="Back",     style='Accent.TButton',
                   command=self._enter_menu).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Modify",   style='Accent.TButton',
                   command=self._on_modify_popup).grid(row=0, column=1, padx=5)

    def _enter_modify(self):
        self.tv_mod.delete(*self.tv_mod.get_children())
        for idx, res in enumerate(self.hm.reservations):
            if res.guest.guest_id == self.current_guest.guest_id and res.is_active:
                self.tv_mod.insert("", "end", iid=str(idx), values=(
                    res.room.room_number,
                    res.check_in_date.strftime("%d/%m/%Y"),
                    res.check_out_date.strftime("%d/%m/%Y")
                ))
        self._show(self.modify_frame)

    def _on_modify_popup(self):
        sel = self.tv_mod.selection()
        if not sel:
            messagebox.showwarning("Select Reservation", "Please select one.")
            return
        idx = int(sel[0])
        res = self.hm.reservations[idx]

        win = tk.Toplevel(self.root)
        win.title("Modify Reservation")
        win.geometry("280x200")
        win.resizable(False, False)
        win.configure(bg="gray")

        ttk.Label(win, text=f"Room {res.room.room_number}",
                  background="gray", font=('Helvetica',14))\
            .grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(win, text="New Stay (days):",
                  background="gray")\
            .grid(row=1, column=0, sticky="e", padx=10)
        e_days = ttk.Entry(win)
        e_days.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(win, text="Update", style='Accent.TButton',
                   command=lambda: self._modify_confirm(res, e_days, win))\
            .grid(row=2, column=0, pady=15, padx=5)
        ttk.Button(win, text="Cancel Reservation", style='Accent.TButton',
                   command=lambda: self._cancel_confirm(res, win))\
            .grid(row=2, column=1, pady=15, padx=5)

    def _modify_confirm(self, res, e_days, win):
        try:
            newd = int(e_days.get())
            if newd < 1:
                raise ValueError
        except:
            messagebox.showwarning("Input Error", "Enter a positive number.")
            return
        try:
            self.hm.modify_reservation(res, newd)
            messagebox.showinfo("Updated", "Reservation updated.")
            win.destroy()
            self._enter_modify()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cancel_confirm(self, res, win):
        if messagebox.askyesno("Confirm Cancel",
                               "Are you sure you want to cancel?"):
            try:
                self.hm.cancel_reservation(res)
                messagebox.showinfo("Canceled", "Reservation canceled.")
                win.destroy()
                self._enter_modify()
            except Exception as e:
                messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
