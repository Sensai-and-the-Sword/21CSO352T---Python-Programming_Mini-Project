# SensorLab

**A Python-Based Sensor Data Processing and Analysis Toolkit**

SensorLab is a lightweight, educational Python project that implements common numerical operations used when working with sensor measurements. It demonstrates how core Python concepts can be applied to ADC conversion, calibration, signal processing, and measurement-error analysis.

## Project objectives

- Convert between ADC counts and analog voltage.
- Apply linear and offset calibration to sensor readings.
- Smooth sample sequences using a moving average.
- Calculate signal magnitude using RMS.
- Normalize datasets to the range `[0, 1]`.
- Calculate absolute percentage error and root-mean-square error (RMSE).
- Restrict values to a specified range using a clamp function.
- Practise modular programming, loops, conditionals, lists, validation, and testing.

## Features

| Area | Functions |
|---|---|
| ADC conversion | `adc_to_voltage()`, `voltage_to_adc()` |
| Calibration | `linear_calibration()`, `offset_calibration()` |
| Signal processing | `moving_average()`, `square_root()`, `rms()`, `normalize()` |
| Error analysis | `percent_error()`, `rmse()` |
| Utility | `clamp()` |

## Repository contents

```text
SensorLab/
├── sensorlab.py
├── test_sensorlab.py
├── README.md
└── screenshots/
    └── (optional source-code and test screenshots)
```

## Requirements

- Python 3.8 or later
- `pytest` (only required to run the test suite)

The implementation in `sensorlab.py` uses core Python and does not require external numerical libraries.

## Installation and execution

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install pytest:

```bash
python -m pip install pytest
```

4. Run the test suite:

```bash
python -m pytest test_sensorlab.py -v
```

To import the functions into another Python program:

```python
import sensorlab

voltage = sensorlab.adc_to_voltage(512, 10, 5.0)
print(voltage)
```

## Example calculations

### ADC count to voltage

```python
import sensorlab

print(sensorlab.adc_to_voltage(1023, 10, 5.0))
# 5.0
```

### Moving average

```python
print(sensorlab.moving_average([10, 12, 14, 16, 18], 3))
# [12.0, 14.0, 16.0]
```

### RMS

```python
print(sensorlab.rms([5, -5, 5, -5]))
# approximately 5.0
```

### Normalization

```python
print(sensorlab.normalize([10, 20, 30]))
# [0.0, 0.5, 1.0]
```

## Implementation notes

- ADC conversion uses `2 ** resolution_bits - 1` as the maximum ADC code.
- `voltage_to_adc()` implements manual round-half-up logic for non-negative ADC values.
- `square_root()` uses 20 Newton–Raphson iterations.
- Minimum, maximum, summation, and absolute-value operations are implemented manually where appropriate.
- `percent_error()` uses the absolute value of both the difference and reference value, and rejects an actual value of zero.
- `normalize()` returns zeros when all input values are identical to avoid division by zero.

## Testing

The test suite is organized into classes by function. It covers normal operation, boundary conditions, and invalid inputs. Floating-point results are checked with `pytest.approx()`, and invalid-input behaviour is checked with `pytest.raises(ValueError)`.

The updated test suite should contain **51 test cases**, including a test for a negative reference value in `percent_error()`. Run the command above to verify the code in your environment.

## Scope and limitations

SensorLab processes numerical values supplied by the caller. It does not currently acquire live data from physical sensors, communicate with microcontrollers, read external datasets, or generate charts. The moving average and fixed-iteration square-root implementation are intentionally simple educational algorithms.

## Author

**Shreya Muthukaruppan**  
Roll Number: `RA2411074010011`  
B.Tech – Mechatronics Engineering  
SRM Institute of Science and Technology  
Course: Python Programming

## License

This project was developed as an academic course submission. No separate open-source license is specified.
