"""
Open downloaded payload
"""

from csv import QUOTE_ALL
import logging
from pathlib import Path
from pandas import DataFrame, read_excel

class Extractor:
    """
    ETL extractor using pandas data frames
    """

    def __init__(
        self,
        src_path: Path | None = None,
        dst_dir: Path | None = None,
        df: DataFrame | None = None
    ):
        self.src_path = src_path
        self.dst_dir = dst_dir
        self.df = df

        self.load_df()


    def load_df(self):
        """
        Load dataframe, either from instance variable, or from disk
        """
        if self.df is None and self.src_path:
            self.df = read_excel(io=self.src_path)


    def write_csv(self, df: DataFrame, dst_path: Path):
        """
        Write a dataframe to a local CSV
        """

        print('*********')
        print(dst_path)
        print('*********')
        logging.info('Writing to CSV: %s', dst_path)
        df.to_csv(path_or_buf=dst_path, index=False, quoting=QUOTE_ALL)


    def extract(self):
        """
        Use pandas to extract rows
        """

        self.load_df()

        # Extract each level into separate CSVs
        self.extract_sections()
        self.extract_divisions()
        self.extract_groups()
        self.extract_classes()
        self.extract_subclasses()


    def extract_rows(self, level: str, columns: dict, filename: str):
        """
        Given column configuration, extract rows. Description column is always extracted.
        Applies text formatting. Writes rows to CSV.
        """

        columns['Description'] = 'summary'
        if 'id' not in columns.values():
            raise ValueError('mapped id column must be specified')

        rows = self.df[self.df['Level headings'] == level].rename(
            columns=columns
        )[columns.values()]


        for column in columns.values():
            rows[column] = [str(i).strip() for i in rows[column]]

        rows['summary'] = [str(i).capitalize() for i in rows['summary']]

        # Write to CSV
        self.write_csv(df=rows, dst_path=self.dst_dir.joinpath(filename))

        return rows


    def extract_sections(self):
        """
        Extract sections from raw dataframe
        """

        self.extract_rows(
            level='SECTION',
            columns={'SECTION': 'id'},
            filename='sections.csv'
        )


    def extract_divisions(self):
        """
        Extract divisions from raw dataframe
        """

        self.extract_rows(
            level='Division',
            columns={'Division': 'id', 'SECTION': 'section_id'},
            filename='divisions.csv'
        )


    def extract_groups(self):
        """
        Extract groups from raw dataframe
        """

        self.extract_rows(
            level='Group',
            columns={'Group': 'id', 'Division': 'division_id'},
            filename='groups.csv'
        )


    def extract_classes(self):
        """
        Extract classes from raw dataframe
        """

        self.extract_rows(
            level='Class',
            columns={'Class': 'id', 'Group': 'group_id'},
            filename='classes.csv'
        )


    def extract_subclasses(self):
        """
        Extract subclasses from raw dataframe
        """

        self.extract_rows(
            level='Sub Class',
            columns={'Sub Class': 'id', 'Class': 'class_id'},
            filename='subclasses.csv'
        )
