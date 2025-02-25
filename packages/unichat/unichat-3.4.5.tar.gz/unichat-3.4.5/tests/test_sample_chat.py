"""Test suite for the chat application."""

import pytest
from unichat.utils.calculator import process_calculation, CalculatorError
from sample_chat import validate_inputs


def test_validate_inputs():
    """Test input validation function."""
    with pytest.raises(ValueError):
        validate_inputs("", "gpt-4")
    with pytest.raises(ValueError):
        validate_inputs("key", "invalid-model")
    with pytest.raises(TypeError):
        validate_inputs(None, "gpt-4")


def test_calculator_valid_operations():
    """Test calculator with valid operations."""
    test_cases = [
        {
            'input': {
                'id': 'test1',
                'function': {
                    'arguments': '{"operation": "add", "operand1": 5, "operand2": 3}'
                }
            },
            'expected': "8"
        },
        {
            'input': {
                'id': 'test2',
                'function': {
                    'arguments': '{"operation": "multiply", "operand1": 4, "operand2": 2}'
                }
            },
            'expected': "8"
        },
        {
            'input': {
                'id': 'test3',
                'function': {
                    'arguments': '{"operation": "divide", "operand1": 10, "operand2": 2}'
                }
            },
            'expected': "5.0"
        }
    ]

    for case in test_cases:
        result = process_calculation(case['input'])
        assert result['content'] == case['expected']


def test_calculator_invalid_operations():
    """Test calculator with invalid operations."""
    invalid_cases = [
        {
            'id': 'test4',
            'function': {
                'arguments': '{"operation": "invalid", "operand1": 5, "operand2": 3}'
            }
        },
        {
            'id': 'test5',
            'function': {
                'arguments': '{"operation": "add", "operand1": "invalid", "operand2": 3}'
            }
        },
        {
            'id': 'test6',
            'function': {
                'arguments': '{"operation": "divide", "operand1": 5, "operand2": 0}'
            }
        }
    ]

    for case in invalid_cases:
        with pytest.raises((CalculatorError, ValueError)):
            process_calculation(case)