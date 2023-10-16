from dataclasses import dataclass
from enum import Enum

import pytest
from domain_models.validation import validate_request


class FakeEnum(Enum):
    YES = 'yes'
    NO = 'no'


@dataclass
class FakeType:
    one: str
    two: int
    three: FakeEnum


@pytest.fixture
def req():
    return {'one': 'one', 'two': 2, 'three': 'yes'}


def test_it_doesnt_error_if_valid(req):
    response = validate_request(req, FakeType)
    assert response == []


def test_it_errors_when_missing_a_key(req):
    del req['two']
    response = validate_request(req, FakeType)
    assert len(response) == 1
    assert response[0] == "Missing fields: ['two']"


def test_it_errors_when_missing_two_keys(req):
    del req['one']
    del req['two']
    response = validate_request(req, FakeType)
    assert len(response) == 1
    assert response[0] == "Missing fields: ['one', 'two']"


def test_it_errors_when_adding_extra_field(req):
    req['four'] = 'four'
    response = validate_request(req, FakeType)
    assert len(response) == 1
    assert response[0] == "Unrecognised fields: ['four']"


def test_it_errors_when_field_has_incorrect_name(req):
    req['too'] = req.pop('two')
    response = validate_request(req, FakeType)
    assert len(response) == 2
    assert response[0] == "Missing fields: ['two']"
    assert response[1] == "Unrecognised fields: ['too']"


def test_it_errors_when_field_has_incorrect_type(req):
    req['two'] = 'two'
    response = validate_request(req, FakeType)
    assert len(response) == 1
    assert response[0] == "Expected types: [{'two': int}]"


def test_it_errors_when_enum_isnt_recognised(req):
    req['three'] = 'bad'
    response = validate_request(req, FakeType)
    assert len(response) == 1
    assert response[0] == "Expected values: [{'three': [yes,no]}]"
