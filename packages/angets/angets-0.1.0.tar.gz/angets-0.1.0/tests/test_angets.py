"""Unit tests for Angets."""
# Built-ins
from datetime import date

# Angets
import angets

# Third-party
import pytest

err = angets.exceptions


class TestGetNonEmptyStr:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.EmptyStringError):
            angets.get_non_empty_str()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: ' ')
        with pytest.raises(err.EmptyStringError):
            angets.get_non_empty_str()

    def test_exception2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Test')
        with pytest.raises(err.InvalidAttemptsValueError):
            angets.get_non_empty_str(attempts=0)

    def test_exception3(self, monkeypatch):
        inputs = iter(['', '', ''])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(err.AttemptsExceededError):
            angets.get_non_empty_str(attempts=3)

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Bob')
        result = angets.get_non_empty_str()
        assert result == 'Bob'

    def test_returned_value1(self, monkeypatch):
        inputs = iter(['', 'Java', 'Bob'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        result = angets.get_non_empty_str(attempts=3)
        assert result == 'Java'


class TestFloat:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.NonFloatingPointError):
            angets.get_float()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'テスト用')
        with pytest.raises(err.AttemptsExceededError):
            angets.get_float(attempts=100)

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '10')
        result = angets.get_float()
        assert result == 10.0

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: ' 1991.12 ')
        result = angets.get_float()
        assert result == 1991.12

    def test_normalization0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '４２０．０２４')
        result = angets.get_float()
        assert result == 420.024

    def test_normalization1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'ー3．1４')
        result = angets.get_float()
        assert result == -3.14


class TestConstrainedFloat:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '5')
        with pytest.raises(err.OutOfBoundsError):
            angets.get_constrained_float(within=(1, 4), interval='[]')

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '4')
        with pytest.raises(err.OutOfBoundsError):
            angets.get_constrained_float(within=(1, 4), interval='[)')

    def test_exception2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2')
        with pytest.raises(err.OutOfBoundsError):
            angets.get_constrained_float(within=(2, 1), interval='[]')

    def test_exception3(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '-2.71')
        with pytest.raises(err.OutOfBoundsError):
            angets.get_positive_float()

    def test_exception4(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '5')
        with pytest.raises(err.InvalidIntervalError):
            angets.get_constrained_float(within=(1, 4), interval='])')

    def test_exception5(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '5')
        with pytest.raises(err.InvalidIntervalError):
            angets.get_constrained_float(within=(1, 4), interval='{}')

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '4')
        result = angets.get_constrained_float(within=(1, 4), interval='[]')
        assert result == 4

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '-0.34')
        result = angets.get_constrained_float(within=(-1, 0), interval='()')
        assert result == -0.34

    def test_returned_value2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2.71')
        result = angets.get_positive_float()
        assert result == 2.71

    def test_returned_value3(self, monkeypatch):
        inputs = iter(['Orgil', '3.14', '-6.28'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        result = angets.get_non_negative_float(attempts=3)
        assert result == 3.14


class TestInt:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.NonIntegerError):
            angets.get_int()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '1.01')
        with pytest.raises(err.NonIntegerError):
            angets.get_int()

    # Huh, I suppose tests are important after all!
    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '1.0')
        result = angets.get_int()
        assert result == 1

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '４２０')
        result = angets.get_int()
        assert result == 420


class TestConstrainedInt:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.NonIntegerError):
            angets.get_constrained_int(within=(1, 4), interval='[]')

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2.5')
        with pytest.raises(err.NonIntegerError):
            angets.get_constrained_int(within=(1, 4), interval='[]')

    def test_exception2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '0')
        with pytest.raises(err.OutOfBoundsError):
            angets.get_positive_int()

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '1.0')
        result = angets.get_constrained_int(within=(1, 4), interval='[]')
        assert result == 1

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '5')
        result = angets.get_positive_int()
        assert result == 5


class TestDate:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.InvalidISOFormatError):
            angets.get_date()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2024/2/22')
        with pytest.raises(err.InvalidISOFormatError):
            angets.get_date()

    def test_exception2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2024年2月22日')
        with pytest.raises(err.InvalidISOFormatError):
            angets.get_date()

    def test_exception3(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '   2022/02/22 ')
        with pytest.raises(err.InvalidISOFormatError):
            angets.get_date()

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2024-02-22')
        result = angets.get_date()
        assert result == date(2024, 2, 22)

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '２０２４０２２２')
        result = angets.get_date()
        assert result == date(2024, 2, 22)


class TestConfirmation:
    def test_exception0(self, monkeypatch):
        inputs = iter(['', '', ''])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(err.AttemptsExceededError):
            angets.get_confirmation(attempts=3)

    # Its little details that come to haunt you...
    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Q')
        with pytest.raises(err.InvalidConfirmationError):
            angets.get_confirmation()

    def test_return_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = angets.get_confirmation()
        assert result == True

    def test_return_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'N')
        result = angets.get_confirmation()
        assert result == False

    def test_return_value2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Kay')
        result = angets.get_confirmation(selection={'k': True, 'kay': True, 'n': False, 'nay': False})
        assert result == True
