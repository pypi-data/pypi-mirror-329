"""
Test downloader class
"""

from pathlib import Path
from pytest_httpx import HTTPXMock
from pytest import raises
from uksic.etl.download import Downloader

DATA_DIR = Path(__file__).parent.joinpath('data').joinpath('download')

def test_download_skipped_file_exists():
    """
    Verify that downloading is skipped when a matching file already exists.
    """

    downloader = Downloader(
        dst=DATA_DIR.joinpath('exists').joinpath('test.csv')
    )

    downloader.download()
    assert not downloader.downloaded


def test_download(httpx_mock: HTTPXMock):
    """
    Verify that file is downloaded when a local file does not exist.
    Removes file if it exists before assertion.
    Intercepts and mocks HTTP call with pytest fixture.
    """

    dst = DATA_DIR.joinpath('empty').joinpath('test.csv')
    dst.unlink(missing_ok=True)

    content = b"id,summary\n1,test"
    httpx_mock.add_response(content=content)

    downloader = Downloader(
        src="https://example.com/test.csv",
        dst=dst
    )

    downloader.download()

    assert downloader.downloaded
    assert dst.exists()
    with open(file=dst, mode='r', encoding='utf8') as test_file:
        assert test_file.read() == content.decode(encoding='utf8')


def test_download_error(httpx_mock: HTTPXMock):
    """
    Verify that on HTTP errors, an exception is thrown
    """

    dst = DATA_DIR.joinpath('empty').joinpath('missing.csv')
    dst.unlink(missing_ok=True)

    httpx_mock.add_response(status_code=404)

    downloader = Downloader(
        src="https://example.com/missing.csv",
        dst=dst
    )

    with raises(ValueError) :
        downloader.download()
