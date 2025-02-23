from mfp.mfp_sub.times_config import TWO
from mfp.utils import check_units


def times_two(x):
    check_units(x)
    return x * TWO
