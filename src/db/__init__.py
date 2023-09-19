import psycopg2

DB_URL = 'postgresql://program:test@containers-us-west-169.railway.app:7613/persons'


class Requests:
    def __init__(self):
        self.DB_URL = DB_URL

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


