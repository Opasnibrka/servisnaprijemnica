from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv

class EvidencijaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Evidencija servisa")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.uredjaj_frame = Frame(self.master)
        self.uredjaj_frame.grid(row=5, column=0, columnspan=2)

        self.add_device_row()

    def add_device_row(self):
        device_row = Frame(self.uredjaj_frame)
        device_row.grid(row=0, column=0, sticky="ew")

        device_label = Label(device_row, text="Uredjaj:")
        device_label.grid(row=0, column=0, padx=5, pady=5)

        device_entry = Entry(device_row)
        device_entry.grid(row=0, column=1, padx=5, pady=5)

        description_label = Label(device_row, text="Opis:")
        description_label.grid(row=0, column=2, padx=5, pady=5)

        description_entry = Entry(device_row)
        description_entry.grid(row=0, column=3, padx=5, pady=5)

        components_label = Label(device_row, text="Ugradjeni delovi:")
        components_label.grid(row=0, column=4, padx=5, pady=5)

        components_entry = Entry(device_row)
        components_entry.grid(row=0, column=5, padx=5, pady=5)

        basic_info_label = Label(device_row, text="Osnovni podaci:")
        basic_info_label.grid(row=0, column=6, padx=5, pady=5)

        basic_info_entry = Entry(device_row)
        basic_info_entry.grid(row=0, column=7, padx=5, pady=5)
        receipt_number_label = Label(device_row, text="Broj prijemnice:")
        receipt_number_label.grid(row=0, column=8, padx=5, pady=5)

        receipt_number_entry = Entry(device_row)
        receipt_number_entry.grid(row=0, column=9, padx=5, pady=5)

        receive_date_label = Label(device_row, text="Datum prijema:")
        receive_date_label.grid(row=0, column=10, padx=5, pady=5)

        receive_date_entry = Entry(device_row)
        receive_date_entry.grid(row=0, column=11, padx=5, pady=5)

        serial_number_label = Label(device_row, text="Serijski broj:")
        serial_number_label.grid(row=0, column=12, padx=5, pady=5)

        serial_number_entry = Entry(device_row)
        serial_number_entry.grid(row=0, column=13, padx=5, pady=5)

        device_row.grid_columnconfigure((0, 2, 4, 6, 8, 10, 12), weight=1)
        self.add_device_button = Button(self.master, text="Dodaj uredjaj", command=self.add_device_row)
        self.add_device_button.grid(row=6, column=0, sticky="ew")

        self.search_label = Label(self.master, text="Pretraga po serijskom broju:")
        self.search_label.grid(row=7, column=0, padx=5, pady=5)

        self.search_entry = Entry(self.master)
        self.search_entry.grid(row=7, column=1, padx=5, pady=5)

        self.search_button = Button(self.master, text="Pretrazi", command=self.search)
        self.search_button.grid(row=7, column=2, sticky="ew")

        self.devices_tree = ttk.Treeview(self.master)
        self.devices_tree["columns"] = ("Device", "Description", "Components", "BasicInfo", "ReceiptNumber", "ReceiveDate", "SerialNumber")

        self.devices_tree.column("#0", width=0, stretch=NO)
        self.devices_tree.column("Device", width=100, anchor=CENTER)
        self.devices_tree.column("Description", width=100, anchor=CENTER)
        self.devices_tree.column("Components", width=100, anchor=CENTER)
        self.devices_tree.column("BasicInfo", width=100, anchor=CENTER)
        self.devices_tree.column("ReceiptNumber", width=100, anchor=CENTER)
        self.devices_tree.column("ReceiveDate", width=100, anchor=CENTER)
        self.devices_tree.column("SerialNumber", width=100, anchor=CENTER)

        self.devices_tree.heading("#0", text="", anchor=CENTER)
        self.devices_tree.heading("Device", text="Uredjaj", anchor=CENTER)
        self.devices_tree.heading("Description", text="Opis", anchor=CENTER)
        self.devices_tree.heading("Components", text="Ugradjeni delovi", anchor=CENTER)
        self.devices_tree.heading("BasicInfo", text="Osnovni podaci", anchor=CENTER)
        self.devices_tree.heading("ReceiptNumber", text="Broj prijemnice", anchor=CENTER)
        self.devices_tree.heading("ReceiveDate", text="Datum prijema", anchor=CENTER)
        self.devices_tree.heading("SerialNumber", text="Serijski broj", anchor=CENTER)

        self.devices_tree.grid(row=8, column=0, columnspan=2)
