import pytest
from .task import Validator, LearningTracker


@pytest.fixture(params=['John Smith jsmith@hotmail.com', 'Robert Jemison Van de Graaff robertvdgraaff@mit.edu'])
def student(request):
    return request.param


@pytest.fixture
def easy_name():
    return 'John Smith jsmith@hotmail.com'


@pytest.fixture
def complex_name():
    return 'Robert Jemison Van de Graaff robertvdgraaff@mit.edu'


def test_easy_valid_name(easy_name):
    validator = Validator(easy_name)
    data = validator.separate_fields()
    expected = {'first_name': 'John', 'last_name': 'Smith', 'email': 'jsmith@hotmail.com'}
    assert data == expected


def test_complex_valid_name(complex_name):
    validator = Validator(complex_name)
    data = validator.separate_fields()
    expected = {'first_name': 'Robert', 'last_name': 'Jemison Van de Graaff', 'email': 'robertvdgraaff@mit.edu'}
    assert data == expected


def test_valid_firstname(student):
    validator = Validator(student)
    data = validator.separate_fields()
    print(data)
    assert validator.valid_name(data['first_name']) is True


def test_valid_lastname(student):
    validator = Validator(student)
    data = validator.separate_fields()
    assert validator.valid_last_name(data['last_name']) is True


def test_valid_mail(student):
    validator = Validator(student)
    data = validator.separate_fields()
    assert validator.valid_mail((data['email']), ['hi@hotmail.com']) is True


def test_valid_student(student):
    validator = Validator(student)
    data = validator.separate_fields()
    assert validator.valid_student(data, None) is True
