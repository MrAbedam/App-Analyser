from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud

class MockApplication:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category


def test_create_application():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = None
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    app_data = schemas.ApplicationCreate(name="Test App", category="Test Category")
    result = crud.create_application(db, app_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.name == "Test App"
    assert result.category == "Test Category"


def test_create_application_duplicate():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = MockApplication(id=1, name="Test App",
                                                                                   category="Test Category")
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    app_data = schemas.ApplicationCreate(name="Test App", category="Test Category")
    with pytest.raises(HTTPException):
        crud.create_application(db, app_data)


def test_get_application():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = MockApplication(id=1, name="Test App",
                                                                                   category="Test Category")
    result = crud.get_application(db, 1)
    assert result.id == 1
    assert result.name == "Test App"
    assert result.category == "Test Category"


def test_get_applications():
    db = MagicMock(Session)
    db.query.return_value.all.return_value = [MockApplication(id=1, name="Test App", category="Test Category")]
    result = crud.get_applications(db)

    assert len(result) == 1
    assert result[0].name == "Test App"


def test_update_application():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = MockApplication(id=1, name="Old Name",                                                                           category="Old Category")
    db.commit = MagicMock()
    db.refresh = MagicMock()
    app_data = schemas.ApplicationCreate(name="Updated App", category="Productivity")
    result = crud.update_application(db, 1, app_data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.name == "Updated App"
    assert result.category == "Productivity"


def test_delete_application():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = MockApplication(id=1, name="Test App",                                                                     category="Test Category")
    db.delete = MagicMock()
    db.commit = MagicMock()
    result = crud.delete_application(db, 1)

    db.delete.assert_called_once()
    db.commit.assert_called_once()
    assert result.id == 1
    assert result.name == "Test App"

def test_get_names():
    db = MagicMock(Session)
    db.query.return_value.all.return_value = [('Test App',)]
    result = crud.get_names(db)

    assert result == [('Test App',)]
