def adc_to_voltage(adc_val, res_bit, vref):
    """
    Convert a raw ADC count to an analog voltage.
    """

    if vref <= 0:
        raise ValueError("Invalid Reference Voltage")

    if res_bit <= 0:
        raise ValueError("Invalid Resolution bit")

    max_adc = 2 ** res_bit - 1

    if adc_val < 0 or adc_val > max_adc:
        raise ValueError("ADC value not in range")

    voltage = (adc_val / max_adc) * vref

    return voltage


def voltage_to_adc(voltage, res_bit, vref):
    """
    Convert an analog voltage to an ADC count.
    Uses manual rounding instead of round().
    """

    if vref <= 0:
        raise ValueError("Incorrect reference Voltage Value")

    if res_bit <= 0:
        raise ValueError("Incorrect Resolution Bit Value")

    if voltage > vref or voltage < 0:
        raise ValueError("Invalid voltage level")

    max_adc = 2 ** res_bit - 1

    adc_val = (voltage / vref) * max_adc

    # Manual rounding
    integer_part = int(adc_val)
    fractional_part = adc_val - integer_part

    if fractional_part < 0.5:
        return integer_part
    else:
        return integer_part + 1


def linear_calibration(sensor_val, slope, offset):
    """
    Apply a linear calibration to a raw sensor reading.
    """

    return slope * sensor_val + offset


def offset_calibration(sensor_val, offset):
    """
    Apply an offset correction to a raw sensor reading.
    """

    return sensor_val + offset


def moving_average(data, window_size):
    """
    Calculate a simple moving average.
    """

    if len(data) == 0:
        raise ValueError("data must not be empty")

    if window_size <= 0:
        raise ValueError("window_size must be positive")

    if window_size > len(data):
        raise ValueError("window_size cannot be larger than data length")

    result = []

    for i in range(len(data) - window_size + 1):

        total = 0

        for j in range(window_size):
            total = total + data[i + j]

        average = total / window_size

        result.append(average)

    return result


def square_root(number):
    """
    Calculate square root using Newton-Raphson iteration.
    """

    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")

    if number == 0:
        return 0.0

    guess = number

    for i in range(20):
        guess = (guess + number / guess) / 2

    return guess


def rms(data):
    """
    Compute the root-mean-square value of a dataset.
    """

    if len(data) == 0:
        raise ValueError("data must not be empty")

    sum_of_squares = 0

    for x in data:
        sum_of_squares = sum_of_squares + (x ** 2)

    mean_square = sum_of_squares / len(data)

    return square_root(mean_square)


def normalize(data):
    """
    Rescale a dataset to the range [0, 1].
    """

    if len(data) == 0:
        raise ValueError("data must not be empty")

    # Find minimum manually
    data_min = data[0]

    for x in data:
        if x < data_min:
            data_min = x

    # Find maximum manually
    data_max = data[0]

    for x in data:
        if x > data_max:
            data_max = x

    data_range = data_max - data_min

    if data_range == 0:

        result = []

        for x in data:
            result.append(0.0)

        return result

    result = []

    for x in data:

        normalized_value = (
            (x - data_min) / data_range
        )

        result.append(normalized_value)

    return result


def percent_error(measured, actual):
    """
    Compute the absolute percentage error.
    """

    if actual == 0:
        raise ValueError("actual value cannot be zero")

    difference = measured - actual

    # Manual absolute value
    if difference < 0:
        difference = -difference

    return (difference / actual) * 100


def rmse(predicted, actual):
    """
    Compute the root-mean-square error.
    """

    if len(predicted) == 0 or len(actual) == 0:
        raise ValueError(
            "predicted and actual must not be empty"
        )

    if len(predicted) != len(actual):
        raise ValueError(
            "predicted and actual must be the same length"
        )

    squared_diffs = []

    for i in range(len(predicted)):

        difference = predicted[i] - actual[i]

        squared_difference = difference ** 2

        squared_diffs.append(squared_difference)

    total = 0

    for value in squared_diffs:
        total = total + value

    mean_squared_error = total / len(squared_diffs)

    return square_root(mean_squared_error)


def clamp(value, min_val, max_val):
    """
    Restrict a value to lie within a specified range.
    """

    if min_val > max_val:
        raise ValueError(
            "min_val cannot be greater than max_val"
        )

    if value < min_val:
        return min_val

    if value > max_val:
        return max_val

    return value
