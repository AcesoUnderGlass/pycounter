"""
A simply utility for incrementing counters stored in sqlite tables.
For god's sake don't put this on a server.
"""
from __future__ import print_function
import sqlite3
import os.path as op
import sys


def get_conn():
    """Returns connection to the database."""
    loc = op.join(op.expanduser("~"), ".counter.db")
    conn = sqlite3.connect(loc, timeout=10)
    return conn


def check_table(variable_name):
    """Checks if the specified table exists"""
    fetch_table = "select name from sqlite_master where type='table' and name=:variable;"
    result = get_conn().execute(fetch_table, {"variable": variable_name}).fetchall()
    exists = len(result) > 0
    return exists


def ensure_table(variable_name):
    """Ensures the table exists"""
    if not check_table(variable_name):
        return create_variable(variable_name)


def create_variable(variable_name):
    """Creates the required sqlite table."""
    get_conn().execute("create table {}(timestamp integer)".format(variable_name))


def delete_variable(variable_name):
    """Deletes a variable"""
    try:
        get_conn().execute("drop table {}".format(variable_name))
    except sqlite3.OperationalError:
        print("Variable does not exist.")
        pass


def increment_variable(variable_name):
    """Increments the count for the variable."""
    ensure_table(variable_name)
    conn = get_conn()
    conn.execute("insert into {} values(strftime('%s','now'))".format(variable_name))
    conn.commit()




def variable_count(variable_name):
    """Counts the variable"""
    ensure_table(variable_name)
    conn = get_conn()
    result = conn.execute("select count(timestamp) from {}".format(variable_name))

    return result.fetchall()[0][0]


def dump_to_json():
    """Stores all data as a JSON file."""
    raise NotImplementedError

if __name__ == "__main__":
    command = sys.argv[1]
    variable = sys.argv[2]

    if command == 'increment':
        print('incrementing ' + variable)
        increment_variable(variable)
    print(variable_count(variable))

