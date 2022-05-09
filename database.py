import sqlite3


class sql_database:
    def data_inserter(self, barcode, name, price):
        con = sqlite3.connect("product_database.db")
        cur = con.cursor()
        data = [barcode, name, price]
        cur.execute(
            """CREATE TABLE IF NOT EXISTS grocery (barcode text PRIMARY KEY, name text, price real)"""
        )
        cur.execute("INSERT OR IGNORE INTO grocery VALUES (?,?,?)", data)
        con.commit()

    def data_remover(self, barcode):
        con = sqlite3.connect("product_database.db")
        cur = con.cursor()
        data = [barcode]
        cur.execute("DELETE FROM grocery WHERE barcode = (?)", data)
        con.commit()

    def realtime_data_uploader(self, barcode, db_name):
        self.barcode = barcode
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS grocery (barcode text PRIMARY KEY)""")
        cur.execute("""INSERT OR IGNORE INTO grocery VALUES (?)""", [self.barcode])
        con.commit()

    def get_data(self):
        list_data = []
        dict_data = {}
        con = sqlite3.connect("product_database.db")
        cur = con.cursor()
        for row in cur.execute("""SELECT * FROM grocery """):
            list_data.append(row)

        for x in range(len(list_data)):
            dict_data[list_data[x][0]] = [list_data[x][1], list_data[x][2]]

        return dict_data

    def realtime_get_data(self, db_name):
        selected_product = []
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        for row in cur.execute("""SELECT * FROM grocery """):
            selected_product.append(row[0])
        return selected_product
