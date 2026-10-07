import tkinter as tk


class DriverLogin:

    def __init__(self):

        self.driver_name = ""
        self.driver_id = ""
        self.vehicle_number = ""

    def show(self):

        root = tk.Tk()

        root.title("NeuroGuard X Driver Login")

        root.geometry("400x300")
        root.resizable(False, False)

        tk.Label(
            root,
            text="NeuroGuard X",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(root, text="Driver Name").pack()

        name_entry = tk.Entry(root, width=35)
        name_entry.pack()

        tk.Label(root, text="Driver ID").pack()

        id_entry = tk.Entry(root, width=35)
        id_entry.pack()

        tk.Label(root, text="Vehicle Number").pack()

        vehicle_entry = tk.Entry(root, width=35)
        vehicle_entry.pack()

        def start():

            self.driver_name = name_entry.get()
            self.driver_id = id_entry.get()
            self.vehicle_number = vehicle_entry.get()

            root.destroy()

        tk.Button(
            root,
            text="Start Trip",
            command=start,
            bg="green",
            fg="white",
            width=20
        ).pack(pady=20)

        root.mainloop()

        return {
            "driver_name": self.driver_name,
            "driver_id": self.driver_id,
            "vehicle_number": self.vehicle_number
        }