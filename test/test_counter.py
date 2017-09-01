import counter
import sqlite3
import pytest

conn = sqlite3.connect("temp.db")

# Mock the database.
counter.get_conn = lambda: conn

TABLE_NAME = "test_table"
ENSURED_TABLE = "ensured_table"

# Clean up (for development purposes)
try:
    conn.execute("drop table {}".format(TABLE_NAME))
except sqlite3.OperationalError:
    pass


@pytest.fixture
def test_table():
    conn.execute("create table {} (timestamp);".format(TABLE_NAME))
    yield
    conn.execute("drop table {};".format(TABLE_NAME))


@pytest.fixture()
def remove_ensured():
    yield
    conn.execute("drop table {}".format(ENSURED_TABLE))


def test_check_table(test_table):
    assert counter.check_table(TABLE_NAME)


def test_delete_variable():
    conn.execute("create table x (name);")
    counter.delete_variable("x")
    assert not counter.check_table("x")


def test_create_variable():
    counter.create_variable(TABLE_NAME)
    assert counter.check_table(TABLE_NAME)
    counter.delete_variable(TABLE_NAME)


def test_increment_ensured(remove_ensured):
    counter.increment_variable(ENSURED_TABLE)
    assert counter.variable_count(ENSURED_TABLE) == 1


def test_increment_variable(test_table):
    counter.increment_variable(TABLE_NAME)
    result = conn.execute("select * from {}".format(TABLE_NAME)).fetchall()
    assert len(result) == 1
    assert len(result[0]) == 1


def test_count_variable(test_table):
    assert counter.variable_count(TABLE_NAME) == 0
    counter.increment_variable(TABLE_NAME)
    counter.increment_variable(TABLE_NAME)
    counter.increment_variable(TABLE_NAME)
    assert counter.variable_count(TABLE_NAME) == 3


def test_count_ensured(remove_ensured):
    assert counter.variable_count(ENSURED_TABLE) == 0
