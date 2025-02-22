"""
Test utilities for re-use across tests.
"""

from pathlib import Path
from pandas import DataFrame, read_csv
from pandas.testing import assert_series_equal

def assert_csvs_are_correct(data_dir: Path):
    """
    Given a directory, assert that the expected CSVs exist and contain expected first and
    last rows
    """

    expected = {
        'sections': {
            'row_count': 21,
            'data': {
                'id': ['A', 'U'],
                'summary': [
                    'Agriculture, forestry and fishing',
                    'Activities of extraterritorial organisations and bodies',
                ]
            },
        },
        'divisions': {
            'columns': ['id', 'section_id', 'summary'],
            'row_count': 88,
            'data': {
                'id': ['01', '99'],
                'section_id': ['A', 'U'],
                'summary': [
                    'Crop and animal production, hunting and related service activities',
                    'Activities of extraterritorial organisations and bodies'
                ]
            },
        },
        'groups': {
            'columns': ['id', 'division_id', 'summary'],
            'row_count': 272,
            'data': {
                'id': ['011', '990'],
                'division_id': ['01', '99'],
                'summary': [
                    'Growing of non-perennial crops',
                    'Activities of extraterritorial organisations and bodies',
                ]
            },
        },
        'classes': {
            'columns': ['id', 'group_id', 'summary'],
            'row_count': 615,
            'data': {
                'id': ['0111', '9900'],
                'group_id': ['011','990'],
                'summary': [
                    'Growing of cereals (except rice), leguminous crops and oil seeds',
                    'Activities of extraterritorial organisations and bodies',
                ]
            },
        },
        'subclasses': {
            'columns': ['id', 'class_id', 'summary'],
            'row_count': 191,
            'data': {
                'id': ['01621', '93199'],
                'class_id': ['0162', '9319'],
                'summary': [
                    'Farm animal boarding and care',
                    'Other sports activities (not including activities of racehorse owners) nec',
                ]
            },
        }
    }

    for csv_name, expected_data in expected.items():
        csv_path = data_dir.joinpath(f'{csv_name}.csv')
        df = read_csv(filepath_or_buffer=csv_path, dtype='string')
        assert list(df) == list(dict(expected_data['data']).keys())
        assert len(df) == expected_data['row_count']

        actual_series = df.iloc[0]
        expected_series =  DataFrame(data=expected_data['data'], dtype='string').iloc[0]

        assert_series_equal(expected_series, actual_series)
