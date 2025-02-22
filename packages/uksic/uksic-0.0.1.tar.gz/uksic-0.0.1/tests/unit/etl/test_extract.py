"""
Test extractor class
"""

from pathlib import Path
from pytest import raises
from uksic.etl.extract import Extractor
from tests.unit.etl.utils import assert_csvs_are_correct

DATA_DIR = Path(__file__).parent.joinpath('data')
SRC_PATH = DATA_DIR.joinpath('ons').joinpath('publisheduksicsummaryofstructureworksheet.xlsx')

def test_no_id_column():
    """
    Verify that an exception is thrown if an id column is not specified
    """
    extractor = Extractor()
    with raises(ValueError):
        extractor.extract_rows(level='abc', columns={'no_id': 'abc'}, filename='test.csv')


def test_extract_files():
    """
    Test extracting expected XLSX into CSVs. Verify extracted CSVs contain the expected columns
    """

    dst_dir = DATA_DIR.joinpath('extract').joinpath('empty')

    # Delete any files before running tests
    for item in dst_dir.iterdir():
        if item.is_file() and str(item).endswith('.csv'):
            item.unlink()

    extractor = Extractor(
        src_path=SRC_PATH,
        dst_dir=dst_dir
    )

    extractor.extract()

    assert_csvs_are_correct(data_dir=dst_dir)
