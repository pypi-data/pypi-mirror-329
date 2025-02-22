"""
Retrieve remote payload and perform extract/transform/load (ETL)
"""

from pathlib import Path
from uksic.etl.download import Downloader
from uksic.etl.extract import Extractor

# pylint: disable=line-too-long
URL = 'https://www.ons.gov.uk/file?uri=/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2007/publisheduksicsummaryofstructureworksheet.xlsx'

class App:
    """
    Main application class that coordinates downloading an extracting data.
    """

    def __init__(
        self,
        url: str = URL,
        data_dir: Path | None = None,
        out_file_name: str = 'publisheduksicsummaryofstructureworksheet.xlsx'
    ):
        self.url = url

        self.data_dir = data_dir

        self.out_file_path: Path = data_dir.joinpath(out_file_name)


    def run(self):
        """
        Run application to retrieve remote payload and perform ETL
        """

        self.download()
        self.extract()


    def download(self):
        """
        Perform download of SIC payload for extraction.
        """
        # Download file if it doesn't exist
        downloader = Downloader(src=self.url, dst=self.out_file_path)
        downloader.download()


    def extract(self):
        """
        Extract download payload for transforming into output formats.
        """
        # Extract files if they don't exist
        extractor = Extractor(src_path=self.out_file_path, dst_dir=self.data_dir)
        extractor.extract()
