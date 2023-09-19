from src.db import Requests


def check_args_length(tuple_db):
    if len(tuple_db) != 5:
        raise Exception("Invalid length of the tuple")


class Person:
    def __init__(self):
        self.request_db = Requests()
        self.person = {
            "id": None,
            "name": None,
            "age": None,
            "address": None,
            "work": None
        }

    def convert_tuple_to_person(self, tuple_db):
        check_args_length(tuple_db)

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

        self.convert_tuple_to_person(tuple_db)
        return dict(self.person)

    def get_persons(self):
        tuple_db = self.request_db.get_persons()
        persons = list()

        if not tuple_db:
            return None

        for tmp_person in tuple_db:
            self.convert_tuple_to_person(tmp_person)
            persons.append(dict(self.person))

        return persons

    def create_new_person(self, person):
        person_id = self.request_db.add_person(person)
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return None
        return person_id

    def update_existing_person(self, new_person, person_id):
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return 1

        self.convert_tuple_to_person(tuple_db)
        self.person.update(new_person)
        person = self.request_db.update_person(self.person, person_id)
        self.convert_tuple_to_person(person)
        return 0

    def remove_person(self, person_id):
        if not self.request_db.get_person(person_id):
            return 0

        self.request_db.delete_person(person_id)
        return person_id
