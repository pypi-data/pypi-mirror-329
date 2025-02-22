"""
Download remote ONS spreadsheet
"""

import logging
from pathlib import Path
import httpx

class Downloader:
    """
    ETL Downloader
    """

    def __init__(self, src: str | None = None, dst: Path | None = None):
        self.src: str | None = src
        self.dst: Path | None = dst
        self.downloaded: bool = False

    def does_dst_exist(self):
        """
        Checks whether local file exists
        """

        logging.info('Checking local path: %s', self.dst)
        return self.dst.exists()


    def download(self):
        """
        Download remote resource locally
        """

        logging.info('Remote source: %s', self.src)
        if self.does_dst_exist():
            logging.info('File exists locally, not downloading.')
            return self

        with open(file=self.dst, mode="wb") as dst_file:
            with httpx.stream("GET", self.src) as response:
                if response.status_code != 200:
                    raise ValueError(f'HTTP Status code: {response.status_code}')

                for data in response.iter_bytes():
                    dst_file.write(data)

                self.downloaded = True
        return self
