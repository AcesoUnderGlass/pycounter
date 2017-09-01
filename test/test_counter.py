import counter
import sqlite3
import pytest

conn = sqlite3.connect("temp.db")

# Mock the database.
counter.get_conn = lambda: conn

TABLE_NAME = "test_table"

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


def test_check_table(test_table):
    assert counter.check_table(TABLE_NAME)


def test_delete_variable():
    conn.execute("create table x (name);")
    counter.delete_variable("x")
    assert not counter.check_table("x")


def test_create_table():
    var = "v1"
    counter.create_table(var)
    assert counter.check_table(var)
    counter.delete_variable(var)


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
