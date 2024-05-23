import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import tempfile
import os

class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija servisa")
        
        self.device_rows = []

        self.create_widgets()
        self.create_table()
        self.load_revers_list()

    def create_widgets(self):
        tk.Label(self.root, text="Ime firme:").grid(row=0, column=0)
        self.ime_firme_entry = tk.Entry(self.root)
        self.ime_firme_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Lično ime:").grid(row=1, column=0)
        self.licno_ime_entry = tk.Entry(self.root)
        self.licno_ime_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Adresa:").grid(row=2, column=0)
        self.adresa_entry = tk.Entry(self.root)
        self.adresa_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Kontakt telefon:").grid(row=3, column=0)
        self.kontakt_telefon_entry = tk.Entry(self.root)
        self.kontakt_telefon_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Uređaji:").grid(row=4, column=0, columnspan=2)

        self.uredjaj_frame = tk.Frame(self.root)
        self.uredjaj_frame.grid(row=5, column=0, columnspan=2)

        self.add_device_row()

        tk.Button(self.root, text="Dodaj uređaj", command=self.add_device_row).grid(row=6, column=0, columnspan=2)

        tk.Button(self.root, text="Sačuvaj", command=self.save_data).grid(row=7, column=0, columnspan=2)
        tk.Button(self.root, text="Novi", command=self.new_revers).grid(row=8, column=0, columnspan=2)
        tk.Button(self.root, text="Štampaj", command=self.print_revers).grid(row=9, column=0, columnspan=2)

        tk.Label(self.root, text="Pretraga:").grid(row=10, column=0)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.grid(row=10, column=1)

        self.revers_tree = ttk.Treeview(self.root, columns=("id", "broj_reversa", "datum", "ime_firme", "licno_ime", "adresa", "kontakt_telefon"), show="headings")
        self.revers_tree.heading("id", text="ID")
        self.revers_tree.heading("broj_reversa", text="Broj reversa")
        self.revers_tree.heading("datum", text="Datum")
        self.revers_tree.heading("ime_firme", text="Ime firme")
        self.revers_tree.heading("licno_ime", text="Lično ime")
        self.revers_tree.heading("adresa", text="Adresa")
        self.revers_tree.heading("kontakt_telefon", text="Kontakt telefon")
        self.revers_tree.grid(row=11, column=0, columnspan=2)

        self.revers_tree.bind("<<TreeviewSelect>>", self.load_selected_revers)

        tk.Button(self.root, text="Pretraži", command=self.search_revers).grid(row=12, column=0, columnspan=2, pady=10)

    def create_table(self):
        conn = sqlite3.connect("evidencija_servisa.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS reversi (
                        id INTEGER PRIMARY KEY,
                        broj_reversa INTEGER,
                        datum TEXT,
                        ime_firme TEXT,
                        licno_ime TEXT,
                        adresa TEXT,
                        kontakt_telefon TEXT,
                        uredjaji TEXT
                    )""")
        conn.commit()
        conn.close()

    def add_device_row(self):
        device_frame = tk.Frame(self.uredjaj_frame)
        device_frame.grid(row=len(self.device_rows) + 1, column=0, columnspan=8, padx=5, pady=5)

        tk.Label(device_frame, text="Tip uređaja").grid(row=0, column=0)
        tk.Label(device_frame, text="Serijski broj").grid(row=0, column=1)
        tk.Label(device_frame, text="Osnovni podaci").grid(row=0, column=2)
        tk.Label(device_frame, text="Broj primljenih novčanica").grid(row=0, column=3)
        tk.Label(device_frame, text="Ugrađeni delovi").grid(row=0, column=4)
        tk.Label(device_frame, text="Opis").grid(row=0, column=5)
        tk.Label(device_frame, text="Obračun").grid(row=0, column=6)
        tk.Label(device_frame, text="Serviser").grid(row=0, column=7)

        tip_uredjaja_entry = tk.Entry(device_frame)
        tip_uredjaja_entry.grid(row=1, column=0, padx=5, pady=5)
        serijski_broj_entry = tk.Entry(device_frame)
        serijski_broj_entry.grid(row=1, column=1, padx=5, pady=5)
        osnovni_podaci_entry = tk.Entry(device_frame)
        osnovni_podaci_entry.grid(row=1, column=2, padx=5, pady=5)
        broj_primljenih_novcanica_entry = tk.Entry(device_frame)
        broj_primljenih_novcanica_entry.grid(row=1, column=3, padx=5, pady=5)
        ugradjeni_delovi_entry = tk.Entry(device_frame)
        ugradjeni_delovi_entry.grid(row=1, column=4, padx=5, pady=5)
        opis_entry = tk.Entry(device_frame)
        opis_entry.grid(row=1, column=5, padx=5, pady=5)
        obracun_entry = tk.Entry(device_frame)
        obracun_entry.grid(row=1, column=6, padx=5, pady=5)
        serviser_entry = tk.Entry(device_frame)
        serviser_entry.grid(row=1, column=7, padx=5, pady=5)

        self.device_rows.append({
            "tip_uredjaja": tip_uredjaja_entry,
            "serijski_broj": serijski_broj_entry,
            "osnovni_podaci": osnovni_podaci_entry,
            "broj_primljenih_novcanica": broj_primljenih_novcan
        "broj_primljenih_novcanica": broj_primljenih_novcanica_entry,
            "ugradjeni_delovi": ugradjeni_delovi_entry,
            "opis": opis_entry,
            "obracun": obracun_entry,
            "serviser": serviser_entry
        })

    def save_data(self):
        ime_firme = self.ime_firme_entry.get()
        licno_ime = self.licno_ime_entry.get()
        adresa = self.adresa_entry.get()
        kontakt_telefon = self.kontakt_telefon_entry.get()

        uredjaji = []
        for device_row in self.device_rows:
            tip_uredjaja = device_row["tip_uredjaja"].get()
            serijski_broj = device_row["serijski_broj"].get()
            osnovni_podaci = device_row["osnovni_podaci"].get()
            broj_primljenih_novcanica = device_row["broj_primljenih_novcanica"].get()
            ugradjeni_delovi = device_row["ugradjeni_delovi"].get()
            opis = device_row["opis"].get()
            obracun = device_row["obracun"].get()
            serviser = device_row["serviser"].get()
            uredjaj = f"{tip_uredjaja}, {serijski_broj}, {osnovni_podaci}, {broj_primljenih_novcanica}, {ugradjeni_delovi}, {opis}, {obracun}, {serviser}"
            uredjaji.append(uredjaj)

        conn = sqlite3.connect("evidencija_servisa.db")
        c = conn.cursor()
        datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO reversi (broj_reversa, datum, ime_firme, licno_ime, adresa, kontakt_telefon, uredjaji) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (1, datum, ime_firme, licno_ime, adresa, kontakt_telefon, ", ".join(uredjaji)))
        conn.commit()
        conn.close()

        self.load_revers_list()

    def load_revers_list(self):
        conn = sqlite3.connect("evidencija_servisa.db")
        c = conn.cursor()
        c.execute("SELECT * FROM reversi")
        reversi = c.fetchall()
        conn.close()

        self.revers_tree.delete(*self.revers_tree.get_children())

        for revers in reversi:
            self.revers_tree.insert("", "end", values=revers)

    def load_selected_revers(self, event):
        selection = self.revers_tree.selection()
        if selection:
            item = self.revers_tree.item(selection[0])
            id = item["values"][0]
            conn = sqlite3.connect("evidencija_servisa.db")
            c = conn.cursor()
            c.execute("SELECT * FROM reversi WHERE id=?", (id,))
            revers = c.fetchone()
            conn.close()

            self.ime_firme_entry.delete(0, tk.END)
            self.ime_firme_entry.insert(0, revers[3])
            self.licno_ime_entry.delete(0, tk.END)
            self.licno_ime_entry.insert(0, revers[4])
            self.adresa_entry.delete(0, tk.END)
            self.adresa_entry.insert(0, revers[5])
            self.kontakt_telefon_entry.delete(0, tk.END)
            self.kontakt_telefon_entry.insert(0, revers[6])

            self.device_rows.clear()
            for device_data in revers[7].split(","):
                tip_uredjaja, serijski_broj, osnovni_podaci, broj_primljenih_novcanica, ugradjeni_delovi, opis, obracun, serviser = device_data.split(";")
                self.add_device_row()
                row = self.device_rows[-1]
                row["tip_uredjaja"].insert(0, tip_uredjaja)
                row["serijski_broj"].insert(0, serijski_broj)
                row["osnovni_podaci"].insert(0, osnovni_podaci)
                row["broj_primljenih_novcanica"].insert(0, broj_primljenih_novcanica)
                row["ugradjeni_delovi"].insert(0, ugradjeni_delovi)
                row["opis"].insert(0, opis)
                row["obracun"].insert(0, obracun)
                row["serviser"].insert(0, serviser)

    def new_revers(self):
        self.ime_firme_entry.delete(0, tk.END)
        self.licno_ime_entry.delete(0, tk.END)
        self.adresa_entry.delete(0, tk.END)
        self.kontakt_telefon_entry.delete(0, tk.END)

        for device_row in self.device_rows:
            device_row["tip_uredjaja"].delete(0, tk.END)
            device_row["serijski_broj"].delete(0, tk.END)
            device_row["osnovni_podaci"].delete(0, tk.END)
            device_row["broj_primljenih_novcanica"].delete(0, tk.END)
            device_row["ugradjeni_delovi"].delete(0, tk.END)
            device_row["opis"].delete(0, tk.END)
            device_row["obracun"].delete(0, tk.END)
            device_row["serviser"].delete(0, tk.END)

    def search_revers(self):
        search_text = self.search_var.get()
        conn = sqlite3.connect("evidencija_servisa.db")
        c = conn.cursor()
        c.execute("SELECT * FROM reversi WHERE ime_firme LIKE ? OR licno_ime LIKE ? OR adresa LIKE ? OR kontakt_telefon LIKE ?", ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        reversi = c.fetchall()
        conn.close()

        self.revers_tree.delete(*self.revers_tree.get_children())

        for revers in reversi:
            self.revers_tree.insert("", "end", values=revers)

    def print_revers(self):
        temp_dir = tempfile.gettempdir()
        with open(os.path.join(temp_dir, "revers.txt"), "w") as f:
            for device_row in self.device_rows:
                tip_uredjaja = device_row["tip_uredjaja"].get()
                serijski_broj = device_row["serijski_broj"].get()
                osnovni_podaci = device_row["osnovni_podaci"].get()
                broj_primljenih_novcanica = device_row["broj_primljenih_novcanica"].get()
                ugradjeni_delovi = device_row["ugradjeni_delovi"].get()
                opis = device_row["opis"].get()
                obracun = device_row["obracun"].get()
                serviser = device_row["serviser"].get()
                opis = device_row["opis"].get()
                obracun = device_row["obracun"].get()
                serviser = device_row["serviser"].get()

                # Upisivanje podataka u bazu
                c.execute('''INSERT INTO uređaj (klijent_id, tip_uredjaja, serijski_broj, osnovni_podaci, broj_primljenih_novcanica, ugradjeni_delovi, opis, obracun, serviser, datum, broj_reversa)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (klijent_id, tip_uredjaja, serijski_broj, osnovni_podaci, broj_primljenih_novcanica, ugradjeni_delovi, opis, obracun, serviser, datum, broj_reversa))

        conn.commit()
        conn.close()
        messagebox.showinfo("Info", "Podaci su uspešno sačuvani")
        self.load_revers_list()
    def print_revers(self):
        if not self.revers_id:
            messagebox.showwarning("Upozorenje", "Morate prvo sačuvati revers pre štampanja.")
            return

        ime_firme = self.ime_firme_entry.get()
        licno_ime = self.licno_ime_entry.get()
        adresa = self.adresa_entry.get()
        kontakt_telefon = self.kontakt_telefon_entry.get()

        filename = f'revers_{self.revers_id}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'Broj reversa: {self.revers_id}\n')
            f.write(f'Datum: {datetime.now().strftime("%Y-%m-%d")}\n\n')
            f.write('Podaci o klijentu:\n')
            f.write(f'Ime firme: {ime_firme}\n')
            f.write(f'Lično ime: {licno_ime}\n')
            f.write(f'Adresa: {adresa}\n')
            f.write(f'Kontakt telefon: {kontakt_telefon}\n\n')
            f.write('Podaci o uređajima:\n')

            for row in self.device_rows:
                f.write('---\n')
                f.write(f'Tip uređaja: {row["tip_uredjaja"].get()}\n')
                f.write(f'Serijski broj: {row["serijski_broj"].get()}\n')
                f.write(f'Osnovni podaci: {row["osnovni_podaci"].get()}\n')
                f.write(f'Broj primljenih novčanica: {row["broj_primljenih_novcanica"].get()}\n')
                f.write(f'Ugrađeni delovi: {row["ugradjeni_delovi"].get()}\n')
                f.write(f'Opis: {row["opis"].get()}\n')
                f.write(f'Obračun: {row["obracun"].get()}\n')
                f.write(f'Serviser: {row["serviser"].get()}\n')

        messagebox.showinfo("Info", f"Revers je sačuvan kao {filename}")

    def new_revers(self):
        self.revers_id = None
        self.broj_reversa_label.config(text="Broj reversa: 0")
        self.datum_label.config(text="Datum: " + datetime.now().strftime("%Y-%m-%d"))
        
        self.ime_firme_entry.delete(0, tk.END)
        self.licno_ime_entry.delete(0, tk.END)
        self.adresa_entry.delete(0, tk.END)
        self.kontakt_telefon_entry.delete(0, tk.END)

        for row in self.device_rows:
            row["tip_uredjaja"].delete(0, tk.END)
            row["serijski_broj"].delete(0, tk.END)
            row["osnovni_podaci"].delete(0, tk.END)
            row["broj_primljenih_novcanica"].delete(0, tk.END)
            row["ugradjeni_delovi"].delete(0, tk.END)
            row["opis"].delete(0, tk.END)
            row["obracun"].delete(0, tk.END)
            row["serviser"].delete(0, tk.END)

    def create_table(self):
        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS klijent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ime_firme TEXT,
                licno_ime TEXT,
                adresa TEXT,
                kontakt_telefon TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS uređaj (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                klijent_id INTEGER,
                tip_uredjaja TEXT,
                serijski_broj TEXT,
                osnovni_podaci TEXT,
                broj_primljenih_novcanica TEXT,
                ugradjeni_delovi TEXT,
                opis TEXT,
                obracun TEXT,
                serviser TEXT,
                datum TEXT,
                broj_reversa INTEGER,
                FOREIGN KEY (klijent_id) REFERENCES klijent(id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS revers_broj (
                id INTEGER PRIMARY KEY,
                broj_reversa INTEGER
            )
        ''')

        c.execute('INSERT OR IGNORE INTO revers_broj (id, broj_reversa) VALUES (1, 0)''')
        
        conn.commit()
        conn.close()

    def load_revers_list(self):
        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        c.execute('''
            SELECT uređaj.broj_reversa, uređaj.datum, klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon
            FROM uređaj
            JOIN klijent ON uređaj.klijent_id = klijent.id
            GROUP BY uređaj.broj_reversa
        ''')

        for row in self.revers_tree.get_children():
            self.revers_tree.delete(row)

        for row in c.fetchall():
            self.revers_tree.insert("", tk.END, values=row)

        conn.close()

    def search_revers(self):
        query = self.search_var.get()

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        c.execute('''
            SELECT uređaj.broj_reversa, uređaj.datum, klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon
            FROM uređaj
            JOIN klijent ON uređaj.klijent_id = klijent.id
            WHERE klijent.ime_firme LIKE ? OR klijent.licno_ime LIKE ? OR klijent.adresa LIKE ? OR klijent.kontakt_telefon LIKE ? OR uređaj.serijski_broj LIKE ? OR uređaj.broj_reversa LIKE ?
            GROUP BY uređaj.broj_reversa
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))

        for row in self.revers_tree.get_children():
            self.revers_tree.delete(row)

        for row in c.fetchall():
            self.revers_tree.insert("", tk.END, values=row)

        conn.close()

    def load_selected_revers(self, event):
        selected_item = self.revers_tree.selection()[0]
        revers_id = self.revers_tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('evidencija.db')
        c = conn.cursor()

        c.execute('''
            SELECT klijent.ime_firme, klijent.licno_ime, klijent.adresa, klijent.kontakt_telefon, uređaj.tip_uredjaja, uređaj.serijski_broj,
                   uređaj.osnovni_podaci, uređaj.broj_primljenih_novcanica, uređaj.ugradjeni_delovi, uređaj.opis, uređaj.obracun, uređaj.serviser
            FROM uređaj
            JOIN klijent ON uređaj.klijent_id = klijent.id
            WHERE uređaj.broj_reversa=?
        ''', (revers_id,))

        revers_data = c.fetchall()
        conn.close()

        self.revers_id = revers_id
        self.broj_reversa_label.config(text=f"Broj reversa: {revers_id}")
        self.datum_label.config(text="Datum: " + datetime.now().strftime("%Y-%m-%d"))

        if revers_data:
            self.ime_firme_entry.delete(0, tk.END)
            self.ime_firme_entry.insert(0, revers_data[0][0])

            self.licno_ime_entry.delete(0, tk.END)
            self.licno_ime_entry.insert(0, revers_data[0][1])

            self.adresa_entry.delete(0, tk.END)
            self.adresa_entry.insert(0, revers_data[0][2])

            self.kontakt_telefon_entry.delete(0, tk.END)
            self.kontakt_telefon_entry.insert(0, revers_data[0][3])

            for row, data in enumerate(revers_data):
                if row < len(self.device_rows):
                    self.device_rows[row]["tip_uredjaja"].delete(0, tk.END)
                    self.device_rows[row]["tip_uredjaja"].insert(0, data[4])

                    self.device_rows[row]["serijski_broj"].delete(0, tk.END)
                    self.device_rows[row]["serijski_broj"].insert(0, data[5])

                    self.device_rows[row]["osnovni_podaci"].delete(0, tk.END)
                    self.device_rows[row]["osnovni_podaci"].insert(0, data[6])

                    self.device_rows[row]["broj_primljenih_novcanica"].delete(0, tk.END)
                    self.device_rows[row]["broj_primljenih_novcanica"].insert(0, data[7])

                    self.device_rows[row]["ugradjeni_delovi"].delete(0, tk.END)
                    self.device_rows[row]["ugradjeni_delovi"].insert(0, data[8])

                    self.device_rows[row]["opis"].delete(0, tk.END)
                    self.device_rows[row]["opis"].insert(0, data[9])

                    self.device_rows[row]["obracun"].delete(0, tk.END)
                    self.device_rows[row]["obracun"].insert(0, data[10])

                    self.device_rows[row]["serviser"].delete(0, tk.END)
                    self.device_rows[row]["serviser"].insert(0, data[11])




