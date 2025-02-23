"""Basic backend utility functions"""


def check_units(check):
    """Check if unit is ok"""

    valid_units = [1, 2, 3, 4]

    if check not in valid_units:
        raise ValueError(f"Unit {check} not in {valid_units}")
