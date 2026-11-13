"""
Test suite for SensorLab MVP functions.

Run with:
    python -m pytest test_sensorlab.py -v
"""

import pytest
import sensorlab as sl


# ============================================================
# ADC MODULE
# ============================================================

class TestAdcToVoltage:

    def test_midpoint(self):
        assert sl.adc_to_voltage(512, 10, 5.0) == pytest.approx(
            2.5024, rel=1e-3
        )

    def test_zero(self):
        assert sl.adc_to_voltage(0, 10, 5.0) == 0.0

    def test_max_value(self):
        assert sl.adc_to_voltage(1023, 10, 5.0) == 5.0

    def test_adc_value_too_high_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(1024, 10, 5.0)

    def test_negative_adc_value_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(-5, 10, 5.0)

    def test_zero_resolution_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(0, 0, 5.0)

    def test_negative_resolution_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(0, -2, 5.0)

    def test_zero_vref_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(0, 10, 0)

    def test_negative_vref_raises(self):
        with pytest.raises(ValueError):
            sl.adc_to_voltage(0, 10, -3.3)


# ============================================================
# VOLTAGE TO ADC
# ============================================================

class TestVoltageToAdc:

    def test_midpoint_roundtrip(self):
        voltage = sl.adc_to_voltage(512, 10, 5.0)

        assert sl.voltage_to_adc(
            voltage, 10, 5.0
        ) == 512

    def test_zero(self):
        assert sl.voltage_to_adc(0, 10, 5.0) == 0

    def test_max_voltage(self):
        assert sl.voltage_to_adc(5.0, 10, 5.0) == 1023

    def test_voltage_above_vref_raises(self):
        with pytest.raises(ValueError):
            sl.voltage_to_adc(6.0, 10, 5.0)

    def test_negative_voltage_raises(self):
        with pytest.raises(ValueError):
            sl.voltage_to_adc(-1.0, 10, 5.0)

    def test_invalid_resolution_raises(self):
        with pytest.raises(ValueError):
            sl.voltage_to_adc(2.5, 0, 5.0)

    def test_invalid_vref_raises(self):
        with pytest.raises(ValueError):
            sl.voltage_to_adc(2.5, 10, 0)


# ============================================================
# CALIBRATION MODULE
# ============================================================

class TestLinearCalibration:

    def test_normal_case(self):
        assert sl.linear_calibration(
            0.8, 100, -50
        ) == 30.0

    def test_zero_slope(self):
        assert sl.linear_calibration(
            0.8, 0, -50
        ) == -50

    def test_negative_slope(self):
        assert sl.linear_calibration(
            0.8, -100, -50
        ) == -130.0

    def test_negative_raw_value(self):
        assert sl.linear_calibration(
            -5, 100, -50
        ) == -550


class TestOffsetCalibration:

    def test_positive_offset(self):
        assert sl.offset_calibration(10, 5) == 15

    def test_negative_offset(self):
        assert sl.offset_calibration(10, -5) == 5

    def test_zero_offset(self):
        assert sl.offset_calibration(0, 0) == 0


# ============================================================
# MOVING AVERAGE
# ============================================================

class TestMovingAverage:

    def test_basic_window(self):
        result = sl.moving_average(
            [10, 12, 14, 16, 18], 3
        )

        assert result == [12.0, 14.0, 16.0]

    def test_window_size_one_returns_original(self):
        result = sl.moving_average(
            [1, 2, 3], 1
        )

        assert result == [1.0, 2.0, 3.0]

    def test_window_equals_data_length(self):
        result = sl.moving_average(
            [1, 2, 3], 3
        )

        assert result == [2.0]

    def test_empty_data_raises(self):
        with pytest.raises(ValueError):
            sl.moving_average([], 3)

    def test_zero_window_size_raises(self):
        with pytest.raises(ValueError):
            sl.moving_average([1, 2, 3], 0)

    def test_window_larger_than_data_raises(self):
        with pytest.raises(ValueError):
            sl.moving_average([1, 2, 3], 5)


# ============================================================
# RMS
# ============================================================

class TestRms:

    def test_symmetric_signal(self):
        assert sl.rms(
            [5, -5, 5, -5]
        ) == pytest.approx(5.0)

    def test_constant_signal(self):
        assert sl.rms(
            [3, 3, 3]
        ) == pytest.approx(3.0)

    def test_zeros(self):
        assert sl.rms(
            [0, 0, 0]
        ) == pytest.approx(0.0)

    def test_empty_data_raises(self):
        with pytest.raises(ValueError):
            sl.rms([])


# ============================================================
# NORMALIZATION
# ============================================================

class TestNormalize:

    def test_basic_range(self):
        result = sl.normalize(
            [10, 20, 30]
        )

        assert result == [0.0, 0.5, 1.0]

    def test_identical_values_returns_zeros(self):
        result = sl.normalize(
            [7, 7, 7]
        )

        assert result == [0.0, 0.0, 0.0]

    def test_negative_values(self):
        result = sl.normalize(
            [-10, 0, 10]
        )

        assert result == [0.0, 0.5, 1.0]

    def test_empty_data_raises(self):
        with pytest.raises(ValueError):
            sl.normalize([])


# ============================================================
# PERCENT ERROR
# ============================================================

class TestPercentError:

    def test_basic_case(self):
        result = sl.percent_error(
            46.5, 45.0
        )

        assert result == pytest.approx(
            3.333, rel=1e-3
        )

    def test_zero_error(self):
        assert sl.percent_error(
            45.0, 45.0
        ) == 0.0

    def test_always_positive(self):
        result = sl.percent_error(
            40.0, 45.0
        )

        assert result > 0

    def test_zero_actual_raises(self):
        with pytest.raises(ValueError):
            sl.percent_error(10, 0)


# ============================================================
# RMSE
# ============================================================

class TestRmse:

    def test_basic_case(self):
        result = sl.rmse(
            [2, 4, 6],
            [3, 4, 5]
        )

        assert result == pytest.approx(
            0.8165, rel=1e-3
        )

    def test_identical_lists_zero_error(self):
        assert sl.rmse(
            [1, 2, 3],
            [1, 2, 3]
        ) == pytest.approx(0.0)

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError):
            sl.rmse(
                [1, 2, 3],
                [1, 2]
            )

    def test_empty_lists_raise(self):
        with pytest.raises(ValueError):
            sl.rmse([], [])


# ============================================================
# CLAMP
# ============================================================

class TestClamp:

    def test_value_within_range(self):
        assert sl.clamp(
            50, 0, 100
        ) == 50

    def test_value_above_max(self):
        assert sl.clamp(
            120, 0, 100
        ) == 100

    def test_value_below_min(self):
        assert sl.clamp(
            -10, 0, 100
        ) == 0

    def test_value_equals_bound(self):
        assert sl.clamp(
            100, 0, 100
        ) == 100

    def test_min_greater_than_max_raises(self):
        with pytest.raises(ValueError):
            sl.clamp(
                50, 100, 0
            )
