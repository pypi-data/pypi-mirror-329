"""
Test ETP app run
"""

from pathlib import Path
from pytest_httpx import HTTPXMock
from uksic.etl.app import App
from tests.unit.etl.utils import assert_csvs_are_correct

DATA_DIR = Path(__file__).parent.joinpath('data')
EMPTY_DIR = DATA_DIR.joinpath('app').joinpath('empty')
SIC_SOURCE = DATA_DIR.joinpath('ons').joinpath('publisheduksicsummaryofstructureworksheet.xlsx')


def test_download_and_extract(httpx_mock: HTTPXMock):
    """
    Verify app correctly executes
    """
    # Clear downloaded file if it exists
    filename = 'test_app.xlsx'
    EMPTY_DIR.joinpath(filename).unlink(missing_ok=True)

    # Prepare mocked HTTP response
    content = None
    with open(file=SIC_SOURCE, mode='rb') as source_file:
        content = source_file.read()

    httpx_mock.add_response(content=content)
    url = 'https://example.com/sic.xslx'

    # Initialise app
    app = App(
        url=url,
        data_dir=EMPTY_DIR,
        out_file_name=filename
    )

    assert app.url == url

    # Run and verify downloaded file and extracted resources
    app.run()
    downloaded_content = None
    download_path = EMPTY_DIR.joinpath(filename)
    with open(file=download_path, mode='rb') as downloaded_file:
        downloaded_content = downloaded_file.read()

    assert downloaded_content == content

    # Verify extracted csvs
    assert_csvs_are_correct(data_dir=EMPTY_DIR)
