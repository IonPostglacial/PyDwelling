import sqlite3
import os

from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str


def items_from_name_list(name_list):
    return map(lambda e: Item(*e), enumerate(name_list))


class DwellingException(Exception):
    def __init__(self, msg: str):
        super(DwellingException, self).__init__(msg)
        self.message = msg


class Table:
    def __init__(self, table_name: str, default_records):
        self.table_name = table_name
        self.default_records = [record for record in default_records]
        self.__default_records_by_id= { record.id : record for record in self.default_records }
        self.__default_records_by_name = { record.name : record for record in self.default_records }

    def get_by_id(self, id: int):
        return self.__default_records_by_id[id]

    def get_by_name(self, name: str):
        try:
            item = self.__default_records_by_name[name]
        except KeyError:
            def recordName(record):
                return f"'{record.name}'"
            raise DwellingException("Record '" + name + "' is unknown in '" + self.table_name + "'. Should be on of " + ", ".join(map(recordName, self.default_records)))
        else:
            return item

    def create(self, db_cursor):
        db_cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id Integer PRIMARY KEY, name Text)")

    def insert_default_records(self, db_cursor):
        record_names = map(lambda r: r.name, self.default_records)
        db_cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?, ?)", enumerate(record_names))


tables = []


def define_table(table_name: str, default_record_names):
    table = Table(table_name, items_from_name_list(default_record_names))
    tables.append(table)
    return table


parts_table = define_table("Parts", ["Abri", "Case", "Couloir", "Cuisine"])
categories_table = define_table("Categories", ["Couloir", "Partie Principale"])
classes_table = define_table("Classes", ["Abrit", "Cuisine", "Maison"])
types_table = define_table("Types", ["Arbaletrier", "Arbaletrier Principal", "Chevron", "Chevron du milieu", "Chevron Extérieur", "Fenêtre", "Mur", "Mur Intérieur", "Mur Extérieur", "Panne", "Panne Faitière", "Panne Intérieure", "Pilier", "Pilier", "Pilier (d)", "Pilier dans la terre", "Pilier de télé", "Pilier de fenêtre", "Pilier intérieur", "Pilier Principal", "Sablière"])
materials_table = define_table("Materials", ["Bois", "Pétiole de Rafa"])
species_table = define_table("Species", ["Afiafy"])


def create_table_wood(db_cursor):
    db_cursor.execute("""CREATE TABLE Wood (
        id Integer PRIMARY KEY AUTOINCREMENT,
        part Integer,
        type1 Integer,
        type2 Integer,
        category Integer,
        class Integer,
        material Integer,
        specie Integer,
        circumference Real,
        length Real,
        FOREIGN KEY(part) REFERENCES Parts(id),
        FOREIGN KEY(type1) REFERENCES Types(id),
        FOREIGN KEY(type2) REFERENCES Types(id),
        FOREIGN KEY(category) REFERENCES Categories(id),
        FOREIGN KEY(class) REFERENCES Classes(id),
        FOREIGN KEY(material) REFERENCES Materials(id),
        FOREIGN KEY(specie) REFERENCES Species(id)
    )""")


@dataclass
class Wood:
    id: int
    part: Item
    type1: Item
    type2: Item
    category: Item
    the_class: Item
    material: Item
    specie: Item
    circumference: float
    length: float

    @staticmethod
    def from_db_row(db_row):
        return Wood(
            db_row[0],
            parts_table.get_by_id(db_row[1]),
            types_table.get_by_id(db_row[2]),
            types_table.get_by_id(db_row[3]),
            categories_table.get_by_id(db_row[4]),
            classes_table.get_by_id(db_row[5]),
            materials_table.get_by_id(db_row[6]),
            species_table.get_by_id(db_row[7]),
            db_row[8],
            db_row[9],
        )

    @staticmethod
    def from_text_columns(db_row):
        if len(db_row) != 10: raise DwellingException("Lines should contain exactly 10 elements.")
        trimmed_rows = list(map(lambda s: s.strip(), db_row))
        return Wood(
            int(trimmed_rows[0]),
            parts_table.get_by_name(trimmed_rows[1]),
            types_table.get_by_name(trimmed_rows[2]),
            types_table.get_by_name(trimmed_rows[3]),
            categories_table.get_by_name(trimmed_rows[4]),
            classes_table.get_by_name(trimmed_rows[5]),
            materials_table.get_by_name(trimmed_rows[6]),
            species_table.get_by_name(trimmed_rows[7]),
            float(trimmed_rows[8]),
            float(trimmed_rows[9]),
        )


db_name = "dwelling.db"
db_already_exists = os.path.isfile(db_name)


def create_database_structure():
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()

        if not db_already_exists:
            for table in tables:
                table.create(cur)
                table.insert_default_records(cur)

            create_table_wood(cur)

            cur.close()


def get_all_wood_records():
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT * from Wood")
        row = cur.fetchone()
        while row is not None:
            yield Wood.from_db_row(row)
            row = cur.fetchone()

        cur.close()


def add_wood_record(wood):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO Wood VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (wood.id, wood.part.id, wood.type1.id, wood.type2.id, wood.category.id, wood.the_class.id,
                wood.material.id, wood.specie.id, wood.circumference, wood.length))
        except sqlite3.IntegrityError as e:
            raise DwellingException(str(e))

    cur.close()
