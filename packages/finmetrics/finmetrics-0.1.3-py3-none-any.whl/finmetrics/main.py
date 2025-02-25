import numpy as np
from typing import Sequence, Union


# Basic Return Calculations
def holding_period_return(beginning_value: float, ending_value: float, total_income: float = 0.0) -> float:
    """
    Computes the Holding period return for a period

    :param beginning_value: starting value of an underlying asset
    :type beginning_value: float

    :param ending_value: ending value of an underlying asset
    :type ending_value: float

    :param total_income:
    :type total_income: float

    :return: holding period return for a period between: time @ ending value & time @ beginning value
    :rtype: float
    """
    if beginning_value == 0:
        raise ValueError("Beginning Value must be non zero")
    return (ending_value - beginning_value + total_income) / beginning_value


def holding_period_return_multi_period(annual_returns: Union[Sequence[float], np.ndarray]) -> float:
    """
    Computes the holding period return for a series of periods given a sequence of values

    :param annual_returns: A list or numpy ndarray of annual returns for a series of periods
    :type annual_returns: list[float] or numpy ndarray

    :return: Holding Period Return for a wide range of periods
    :rtype: float
    """
    if not annual_returns:
        raise ValueError("annual_returns must contain at least 1 value")
    if not isinstance(annual_returns, (Sequence, np.ndarray)):
        raise ValueError("annual_returns must be a sequence of floats or numpy array")
    try:
        accumulator = 1
        for i in annual_returns:
            accumulator *= (1 + i)
        return accumulator - 1
    except Exception as e:
        raise Exception(f"Error with holding_period_return_multi_period: {e}")


def arithmetic_return(holding_period_returns: Union[Sequence[float], np.ndarray]) -> float:
    """
    Computes the arithmetic return given a sequence of holding period returns

    :param holding_period_returns: a list or numpy ndarray of holding periods returns
    :type holding_period_returns:  list[float] or numpy ndarray

    :return: arithmetic (mean) return of array of holding period returns
    :rtype: float
    """
    if not holding_period_returns:
        raise ValueError("holding_period_returns must contain at least 1 value")
    if not isinstance(holding_period_returns, (Sequence, np.ndarray)):
        raise ValueError("holding_period_returns must be a sequence of floats or numpy array")
    try:
        return sum(holding_period_returns) / len(holding_period_returns)
    except Exception as e:
        raise Exception(f"Error with arithmetic_return: {e}")


def geometric_return(holding_period_returns: Union[Sequence[float], np.ndarray]) -> float:
    """
    Computes the geometric_return given a series of holding period returns

    :param holding_period_returns: a list or numpy ndarray of holding period returns
    :type holding_period_returns: list[float] or numpy ndarray

    :return: geometric return of an array of holding period returns
    :rtype float
    """
    if not holding_period_returns:
        raise ValueError("holding_period_returns must contain at least 1 value")
    if not isinstance(holding_period_returns, (Sequence, np.ndarray)):
        raise ValueError("holding_period_returns must be a sequence of floats or numpy array")
    try:
        rate = 1
        count = len(holding_period_returns)
        for i in holding_period_returns:
            rate *= (1 + i)
        rate = (rate ** (1 / count)) - 1
        return rate
    except Exception as e:
        raise Exception(f"Error with geometric_return: {e}")


def harmonic_mean(values: Union[Sequence[float], np.ndarray]) -> float:
    """
    Computes the harmonic mean given a series of positive floating point values

    :param values: a sequence (list or numpy ndarray) of positive floating point values
    :type values: list[float] or numpy ndarray

    :return: harmonic mean (average) of positive values
    :rtype: float
    """
    if len(values) == 0:
        raise ValueError("values must contain at least 1 value")
    if not isinstance(values, (Sequence, np.ndarray)):
        raise ValueError("values must be a sequence of floats or numpy array")
    try:
        num_vals = len(values)
        if isinstance(values, np.ndarray):
            min_val = values.min()
        else:
            min_val = min(values)

        if min_val <= 0:
            raise ValueError("values cannot be negative")
        sum_reciprocals = 0
        for i in values:
            sum_reciprocals += (1 / i)
        return num_vals / sum_reciprocals
    except Exception as e:
        raise Exception(f"Error with harmonic_mean: {e}")


