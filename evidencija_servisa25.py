import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija Servisa")
        
        self.revers_id = None
        self.create_table()
        self.create_widgets()
        self.load_revers_list()

    def create_widgets(self):
        # Dodavanje Label-a za prikaz broja reversa i datuma
        self.broj_reversa_label = tk.Label(self.root, text="Broj reversa: 0")
        self.broj_reversa_label.grid(row=0, column=0, padx=10, pady=5)

        self.datum_label = tk.Label(self.root, text="Datum: " + datetime.now().strftime("%Y-%m-%d"))
        self.datum_label.grid(row=0, column=1, padx=10, pady=5)

        # Podaci o klijentu
        tk.Label(self.root, text="Ime firme:").grid(row=1, column=0, padx=10, pady=5)
        self.ime_firme_combobox = ttk.Combobox(self.root)
        self.ime_firme_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.ime_firme_combobox.bind('<KeyRelease>', self.update_combobox_values)

        tk.Label(self.root, text="Lično ime:").grid(row=2, column=0, padx=10, pady=5)
        self.licno_ime_entry = tk.Entry(self.root)
        self.licno_ime_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Adresa:").grid(row=3, column=0, padx=10, pady=5)
        self.adresa_entry = tk.Entry(self.root)
        self.adresa_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Kontakt telefon:").grid(row=4, column=0, padx=10, pady=5)
        self.kontakt_telefon_combobox = ttk.Combobox(self.root)
        self.kontakt_telefon_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.kontakt_telefon_combobox.bind('<KeyRelease>', self.update_combobox_values)

        # Podaci o uređaju
        self.uredjaj_frame = tk.Frame(self.root)
        self.uredjaj_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Dodavanje naslova za kolone
        headers = ["Tip uređaja", "Serijski broj", "Osnovni podaci", "Broj primljenih novčanica", "Ugrađeni delovi", "Opis", "Obračun", "Serviser"]
        for col, header in enumerate(headers):
            tk.Label(self.uredjaj_frame, text=header, bg="lightgreen").grid(row=0, column=col, padx=5, pady=5)

        self.device_rows = []
        self.add_device_row()

        tk.Button(self.root, text="Dodaj još jedan uređaj", command=self.add_device_row).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Sačuvaj", command=self.save_data).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Štampaj", command=self.print_revers).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Novi revers", command=self.new_revers).grid(row=9, column=0, columnspan=2, pady=10)

        # Tabela sa postojećim reversima
        self.revers_tree = ttk.Treeview(self.root, columns=("broj_reversa", "datum", "ime_firme", "licno_ime", "adresa", "kontakt_telefon"), show='headings')
        self.revers_tree.heading("broj_reversa", text="Broj reversa")
        self.revers_tree.heading("datum", text="Datum")
        self.revers_tree.heading("ime_firme", text="Ime firme")
        self.revers_tree.heading("licno_ime", text="Lično ime")
        self.revers_tree.heading("adresa", text="Adresa")
        self.revers_tree.heading("kontakt_telefon", text="Kontakt telefon")
        self.revers_tree.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        self.revers_tree.bind("<Double-1>", self.load_selected_revers)

        # Polje za pretragu
        self.search_var = tk.StringVar()
        tk.Label(self.root, text="Pretraga:").grid(row=11, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.grid(row=11, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_revers())

    def update_combobox_values(self, event):
        widget = event.widget
        input_value = widget.get()

        if isinstance(widget, ttk.Combobox):
            if widget == self.ime_firme_combobox:
                query = "SELECT DISTINCT ime_firme FROM klijent WHERE ime_firme LIKE ?"
            elif widget == self.kontakt_telefon_combobox:
                query = "SELECT DISTINCT kontakt_telefon FROM klijent WHERE kontakt_telefon LIKE ?"
            else:
                return

            conn = sqlite3.connect('evidencija.db')
            c = conn.cursor()
            c.execute(query, (f'{input_value}%',))
            values = [row[0] for row in c.fetchall()]
            conn.close()

            widget['values'] = values

    def add_device_row(self):
        row = len(self.device_rows) + 1
        device_row = {
            "tip_uredjaja": tk.Entry(self.uredjaj_frame),
            "serijski_broj": tk.Entry(self.uredjaj_frame),
            "osnovni_podaci": tk.Entry(self.uredjaj_frame, width=20),
            "broj_primljenih_novcanica": tk.Entry(self.uredjaj_frame),
            "ugradjeni_delovi": tk.Entry(self.uredjaj_frame),
            "opis": tk.Entry(self.uredjaj_frame, width=20),
            "obracun": tk.Entry(self.uredjaj_frame),
            "serviser": tk.Entry(self.uredjaj_frame)
        }
        self.device_rows.append(device_row)

        device_row["tip_uredjaja"].grid(row=row, column=0, padx=5, pady=5)
        device_row["serijski_broj"].grid(row=row, column=1, padx=5, pady=5)
        device_row["osnovni_podaci"].grid(row=row, column=2, padx=5, pady=5)
        device_row["broj_primljenih_novcanica"].grid(row=row, column=3, padx=5, pady=5)
        device_row["ugradjeni_delovi"].grid(row=row, column=4, padx=5, pady=5)
        device_row["opis"].grid(row=row, column=5, padx=5, pady=5)
        device_row["obracun"].grid(row=row, column=6, padx=5, pady=5)
        device_row["serviser"].grid(row=row, column=7, padx=5, pady=5)

    def save_data(self):
        ime_firme = self.ime_firme_combobox.get()
        licno_ime = self.licno_ime_entry.get()
        adresa = self.adresa_entry.get()
        kontakt_telefon = self.kontakt_telefon_combobox.get()

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        # Proveravamo da li klijent već postoji u bazi
        c.execute('SELECT id FROM klijent WHERE ime_firme=? AND licno_ime=? AND adresa=? AND kontakt_telefon=?', (ime_firme, licno_ime, adresa, kontakt_telefon))
        klijent = c.fetchone()
        if klijent:
            klijent_id = klijent[0]
        else:
            c.execute('INSERT INTO klijent (ime_firme, licno_ime, adresa, kontakt_telefon) VALUES (?, ?, ?, ?)', (ime_firme, licno_ime, adresa, kontakt_telefon))
            klijent_id = c.lastrowid

        if self.revers_id:
            c.execute('DELETE FROM uredjaj WHERE revers_id=?', (self.revers_id,))
        else:
            c.execute('INSERT INTO revers (klijent_id, datum) VALUES (?, ?)', (klijent_id, datetime.now().strftime("%Y-%m-%d")))
            self.revers_id = c.lastrowid

        for device_row in self.device_rows:
            c.execute('''INSERT INTO uredjaj (revers_id, tip_uredjaja, serijski_broj, osnovni_podaci, broj_primljenih_novcanica, ugradjeni_delovi, opis, obracun, serviser) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                self.revers_id,
                device_row["tip_uredjaja"].get(),
                device_row["serijski_broj"].get(),
                device_row["osnovni_podaci"].get(),
                device_row["broj_primljenih_novcanica"].get(),
                device_row["ugradjeni_delovi"].get(),
                device_row["opis"].get(),
                device_row["obracun"].get(),
                device_row["serviser"].get()
            ))

        conn.commit()
        conn.close()

        self.load_revers_list()
        messagebox.showinfo("Uspeh", "Podaci su sačuvani uspešno!")

    def load_revers_list(self):
        for item in self.revers_tree.get_children():
            self.revers_tree.delete(item)

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()
        c.execute('''SELECT revers.id, revers.datum, klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon 
                     FROM revers 
                     JOIN klijent ON revers.klijent_id = klijent.id 
                     ORDER BY revers.id DESC''')
        for row in c.fetchall():
            self.revers_tree.insert('', 'end', values=row)
        conn.close()

    def load_selected_revers(self, event):
        selected_item = self.revers_tree.selection()[0]
        revers_id = self.revers_tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()
        c.execute('''SELECT revers.id, revers.datum, klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon 
                     FROM revers 
                     JOIN klijent ON revers.klijent_id = klijent.id 
                     WHERE revers.id=?''', (revers_id,))
        revers = c.fetchone()

        self.revers_id = revers[0]
        self.broj_reversa_label.config(text="Broj reversa: " + str(revers[0]))
        self.datum_label.config(text="Datum: " + revers[1])
        self.ime_firme_combobox.set(revers[2])
        self.licno_ime_entry.delete(0, tk.END)
        self.licno_ime_entry.insert(0, revers[3])
        self.adresa_entry.delete(0, tk.END)
        self.adresa_entry.insert(0, revers[4])
        self.kontakt_telefon_combobox.set(revers[5])

        for row in self.device_rows:
            for widget in row.values():
                widget.grid_forget()
        self.device_rows.clear()

        c.execute('SELECT tip_uredjaja, serijski_broj, osnovni_podaci, broj_primljenih_novcanica, ugradjeni_delovi, opis, obracun, serviser FROM uredjaj WHERE revers_id=?', (revers_id,))
        for device in c.fetchall():
            self.add_device_row()
            device_row = self.device_rows[-1]
            device_row["tip_uredjaja"].insert(0, device[0])
            device_row["serijski_broj"].insert(0, device[1])
            device_row["osnovni_podaci"].insert(0, device[2])
            device_row["broj_primljenih_novcanica"].insert(0, device[3])
            device_row["ugradjeni_delovi"].insert(0, device[4])
            device_row["opis"].insert(0, device[5])
            device_row["obracun"].insert(0, device[6])
            device_row["serviser"].insert(0, device[7])

        conn.close()

    def search_revers(self):
        search_term = self.search_var.get()

        for item in self.revers_tree.get_children():
            self.revers_tree.delete(item)

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()
        c.execute('''SELECT revers.id, revers.datum, klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon 
                     FROM revers 
                     JOIN klijent ON revers.klijent_id = klijent.id 
                     WHERE klijent.ime_firme LIKE ? OR klijent.licno_ime LIKE ? OR klijent.adresa LIKE ? OR klijent.kontakt_telefon LIKE ? 
                     ORDER BY revers.id DESC''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        for row in c.fetchall():
            self.revers_tree.insert('', 'end', values=row)
        conn.close()

    def new_revers(self):
        self.revers_id = None
        self.broj_reversa_label.config(text="Broj reversa: 0")
        self.datum_label.config(text="Datum: " + datetime.now().strftime("%Y-%m-%d"))
        self.ime_firme_combobox.set("")
        self.licno_ime_entry.delete(0, tk.END)
        self.adresa_entry.delete(0, tk.END)
        self.kontakt_telefon_combobox.set("")
        for row in self.device_rows:
            for widget in row.values():
                widget.grid_forget()
        self.device_rows.clear()
        self.add_device_row()

    def print_revers(self):
        messagebox.showinfo("Štampanje", "Štampanje reversa...")

    def create_table(self):
        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS klijent (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ime_firme TEXT,
                        licno_ime TEXT,
                        adresa TEXT,
                        kontakt_telefon TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS revers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        klijent_id INTEGER,
                        datum TEXT,
                        FOREIGN KEY (klijent_id) REFERENCES klijent (id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS uredjaj (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        revers_id INTEGER,
                        tip_uredjaja TEXT,
                        serijski_broj TEXT,
                        osnovni_podaci TEXT,
                        broj_primljenih_novcanica INTEGER,
                        ugradjeni_delovi TEXT,
                        opis TEXT,
                        obracun TEXT,
                        serviser TEXT,
                        FOREIGN KEY (revers_id) REFERENCES revers (id)
                    )''')

        conn.commit()
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
