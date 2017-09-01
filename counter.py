"""
A simply utility for incrementing counters stored in sqlite tables.
For god's sake don't put this on a server.
"""
import click
import sqlite3
import os.path as op


def get_conn():
    """Returns connection to the database."""
    loc = op.join(op.expanduser("~"), ".counter.db")
    conn = sqlite3.connect(loc)
    return conn


def check_table(variable_name: str) -> bool:
    """Checks if the specified table exists"""
    fetch_table = "select name from sqlite_master where type='table' and name=:variable;"
    result = get_conn().execute(fetch_table, {"variable": variable_name}).fetchall()
    exists = len(result) > 0
    return exists


def ensure_table(variable_name: str):
    """Ensures the table exists"""
    if check_table(variable_name):
        return
    else:
        return create_table(variable_name)


def create_table(variable_name: str):
    """Creates the required sqlite table."""
    get_conn().execute("create table {}(timestamp integer)".format(variable_name))


def delete_variable(variable_name: str):
    """Deletes a variable"""
    get_conn().execute("drop table {}".format(variable_name))


def increment_variable(variable_name: str):
    """Increments the count for the variable."""
    get_conn().execute("insert into {} values(strftime('%s','now'))".format(variable_name))


def variable_count(variable_name: str):
    """Counts the variable"""
    ensure_table(variable_name)
    result = get_conn().execute("select count(timestamp) from {}".format(variable_name))
    return result.fetchall()[0][0]



def dump_to_json():
    """Stores all data as a JSON file."""


def main():
    print("Executed")


if __name__ == "__main__":
    main()
