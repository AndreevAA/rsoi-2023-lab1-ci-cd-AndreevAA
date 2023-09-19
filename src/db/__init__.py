import psycopg2

DB_URL = 'postgresql://program:test@containers-us-west-169.railway.app:7613/persons'


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



