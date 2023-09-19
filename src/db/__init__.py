import psycopg2

DB_URL = 'postgresql://postgres:postgres@localhost/postgresql'


class Requests:
    def __init__(self):
        self.DB_URL = DB_URL

        self.create_table_if_not_exists()

    def open_connection(self):
        self.connection = psycopg2.connect(self.DB_URL)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def create_table_if_not_exists(self):
        if not self.check_persons_table():
            self.create_table()

    def check_persons_table(self):
        self.open_connection()
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        for table in self.cursor.fetchall():
            if table[0] == "persons":
                self.close_connection()
                return True
        self.close_connection()
        return False

    def create_table(self):
        new_table = '''
                            CREATE TABLE persons
                            (
                               id serial primary key,
                               name varchar(50) not null,
                               age integer,
                               address varchar(50),
                               work varchar(50)
                            );
                            '''
        self.open_connection()
        self.cursor.execute(new_table)
        self.connection.commit()
        self.close_connection()

    def get_person(self, person_id):
        self.open_connection()
        self.cursor.execute(f"SELECT * From persons WHERE id={person_id};")
        person = self.cursor.fetchone()
        self.close_connection()
        return person

    def get_persons(self):
        self.open_connection()
        self.cursor.execute("SELECT * FROM persons;")
        persons = self.cursor.fetchall()
        self.close_connection()
        return persons

    def add_person(self, new_person):
        self.open_connection()
        self.cursor.execute(f"INSERT INTO persons (name, address, work, age) VALUES ('{new_person['name']}', "
                       f"'{new_person['address']}', '{new_person['work']}', '{new_person['age']}') RETURNING id;")
        self.connection.commit()
        person = self.cursor.fetchone()
        self.close_connection()
        return person[0]

    def update_person(self, new_info, person_id):
        self.open_connection()
        self.cursor.execute(f"UPDATE persons SET name = '{new_info['name']}', address = '{new_info['address']}', "
                       f"work = '{new_info['work']}', age = '{new_info['age']}' "
                       f"WHERE id={person_id} RETURNING id, name, age, address, work;")
        self.connection.commit()
        person = self.cursor.fetchone()
        self.close_connection()
        return person

    def delete_person(self, person_id):
        self.open_connection()
        self.cursor.execute(f"DELETE FROM persons WHERE id={person_id};")
        rows_deleted = self.cursor.rowcount
        self.connection.commit()
        self.close_connection()
        return rows_deleted
