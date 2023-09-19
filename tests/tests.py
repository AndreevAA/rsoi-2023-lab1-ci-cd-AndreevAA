import requests
import pytest


person1 = {
    "name": "Ivanov",
    "address": "Moscow",
    "work": "IBM",
    "age": 32
}

person2 = {
    "name": "Smirnov",
    "address": "Parish",
    "work": "Google",
    "age": 20
}

person3 = {
    "name": "Petrov",
    "address": "New York",
    "work": "Microsoft",
    "age": 25
}

patch_name = {"name": "Alex"}
patch_address = {"address": "London"}
patch_work = {"work": "Architector"}
patch_age = {"age": 21}


@pytest.mark.parametrize("persons", [person1, person2, person3])
def test_post_get(persons):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    assert r.status_code == 201
    redirected_urd = r.headers['Location']
    person_id_dict = {"id": int(redirected_urd.split("/")[-1])}
    r = requests.get(redirected_urd)
    assert r.status_code == 200
    assert r.json() == persons | person_id_dict


@pytest.mark.parametrize("persons, patch_var", [(person1, patch_name), (person1, patch_address),
                                                (person2, patch_work), (person2, patch_age),
                                                (person3, patch_name), (person3, patch_address)])
def test_post_patch(persons, patch_var):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    redirected_urd = r.headers['Location']
    r = requests.patch(url=redirected_urd, json=patch_var)
    assert r.status_code == 200
    assert patch_var.items() <= r.json().items()


@pytest.mark.parametrize("persons", [person1, person2, person3])
def test_post_delete(persons):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    redirected_urd = r.headers['Location']
    r = requests.delete(redirected_urd)
    assert r.status_code == 204
    r = requests.get(redirected_urd)
    assert r.status_code == 400


def test_get_all_persons():
    r = requests.get(url="http://127.0.0.1:8080/api/v1/persons")
    assert r.status_code == 200
    assert len(r.json()) > 0


def test_get_person_not_found():
    r = requests.get(url="http://127.0.0.1:8080/api/v1/persons/100")
    assert r.status_code == 400
    assert r.text == "Not found Person for ID 100"


def test_post_invalid_data():
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json={})
    assert r.status_code == 400
    assert r.text == "Invalid data"


def test_patch_person_not_found():
    r = requests.patch(url="http://127.0.0.1:8080/api/v1/persons/100", json=patch_name)
    assert r.status_code == 404
    assert r.text == "Not found Person for ID 100"


def test_delete_person_not_found():
    r = requests.delete(url="http://127.0.0.1:8080/api/v1/persons/100")
    assert r.status_code == 404
    assert r.text == "Person for ID 100 not found"


def test_post_get_many():
    for i in range(100):
        r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person1)
        assert r.status_code == 201
        redirected_urd = r.headers['Location']
        r = requests.get(redirected_urd)
        assert r.status_code == 200
        assert r.json() == person1


def test_post_patch_many():
    for i in range(100):
        r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person1)
        redirected_urd = r.headers['Location']
        r = requests.patch(url=redirected_urd, json=patch_name)
        assert r.status_code == 200
        assert patch_name.items() <= r.json().items()


def test_post_delete_many():
    for i in range(100):
        r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person1)
        redirected_urd = r.headers['Location']
        r = requests.delete(redirected_urd)
        assert r.status_code == 204
        r = requests.get(redirected_urd)