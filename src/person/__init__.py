class Person:
    def __init__(self):
        self.request_db = None
        self.person = {
            "id": None,
            "name": None,
            "age": None,
            "address": None,
            "work": None
        }

    def person_from_tuple(self, tuple_db):
        if len(tuple_db) != 5:
            raise Exception("tuple's length isn't five")

        self.person = {
            "id": int(tuple_db[0]),
            "name": str(tuple_db[1]),
            "age": int(tuple_db[2]),
            "address": str(tuple_db[3]),
            "work": str(tuple_db[4])
        }

    def get_person(self, person_id):
        tuple_db = self.request_db.get_person(person_id)

        if not tuple_db:
            return None

        self.person_from_tuple(tuple_db)
        return self.person