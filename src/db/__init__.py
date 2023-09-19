import psycopg2

DB_URL = 'postgresql://program:test@containers-us-west-169.railway.app:7613/persons'


class Requests:
    def __init__(self):
        self.DB_URL = DB_URL

        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        if not self.check_persons_table():
            self.create_table()

    def check_persons_table(self):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        for table in cursor.fetchall():
            if table[0] == "persons":
                cursor.close()
                connection.close()
                return True
        cursor.close()
        connection.close()
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
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(new_table)
        connection.commit()
        cursor.close()
        connection.close()



