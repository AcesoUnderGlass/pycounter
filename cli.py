#!/usr/bin/python3
"""
CLI wrapper around counter.
This is probably unnecessary boilerplate but eh.
"""
import counter
import click


@click.command()
def new_variable(variable_name):
    """Creates a new variable to track"""
    raise NotImplementedError


@click.command()
def increment_variable(variable_name):
    """Increment a variable."""
    raise NotImplementedError


def count_variable(variable_name):
    """Return the count of a variable"""
    raise NotImplementedError


@click.command()
def list_variables():
    """Lists all variables"""
    raise NotImplementedError
