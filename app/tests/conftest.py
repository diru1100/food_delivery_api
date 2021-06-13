import pytest


@pytest.fixture(scope="module")
def test_data():
    return {'sample_time': '06:02 PM',

            'sample_day_range': 'Wed-Mon',

            'split_sample_opening_hours_data': ['Mon, Fri 2:30 pm - 8 pm ',
                                                ' Tues 11 am - 2 pm ',
                                                ' Weds 1:15 pm - 3:15 am ',
                                                ' Thurs 10 am - 3:15 am ',
                                                ' Sat 5 am - 11:30 am ',
                                                ' Sun 10:45 am - 5 pm'],

            'sample_datetime': '02/10/2020 04:09 AM'}
