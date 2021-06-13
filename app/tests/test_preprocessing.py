import pytest
import requests
from ..format import preprocess_opening_hours_data, preprocess_datetime, preprocess_time


def test_preprocess_opening_hours_data(test_data):

    input_opening_hours_data = test_data['split_sample_opening_hours_data']
    preprocessed_opening_hours_data = [[['Mon', {'openTime': ['14:30:00'], 'closeTime': ['20:00:00']}],
                                       [' Fri  ', {'openTime': ['14:30:00'],
                                                   'closeTime': ['20:00:00']}]],
                                       [[' Tues  ', {'openTime': ['11:00:00'],
                                                     'closeTime': ['14:00:00']}]],
                                       [[' Weds  ', {'openTime': ['13:15:00', '00:00:00'],
                                                     'closeTime': ['23:59:59', '03:15:00']}]],
                                       [[' Thurs  ', {'openTime': ['10:00:00', '00:00:00'],
                                                      'closeTime': ['23:59:59', '03:15:00']}]],
                                       [[' Sat  ', {'openTime': ['05:00:00'],
                                                    'closeTime': ['11:30:00']}]],
                                       [[' Sun ', {'openTime': ['10:45:00'], 'closeTime': ['17:00:00']}]]]

    for pointer in range(0, len(input_opening_hours_data)):
        assert preprocessed_opening_hours_data[pointer] == preprocess_opening_hours_data(
            input_opening_hours_data[pointer])


def test_preprocess_datetime(test_data):
    input_data = test_data['sample_datetime']
    expected_output_time = '2020-02-10 04:09:00'
    assert expected_output_time == str(preprocess_datetime(input_data))
