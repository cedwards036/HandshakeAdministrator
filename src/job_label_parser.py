import csv
from typing import List

from autohandshake import HandshakeBrowser

from src.utils import to_csv, create_filepath_in_download_dir, get_datestamped_filename


def run_job_labels_report(browser: HandshakeBrowser) -> str:
    input_filepath = input('Please enter the filepath of the input jobs file: ')
    return create_job_labels_report(input_filepath)


def create_job_labels_report(input_filepath: str) -> str:
    """
    Given a valid filepath to a downloaded jobs file, create a report csv detailing which jobs have qualification labels

    :param input_filepath: the filepath of the raw jobs data
    :return: the output filepath
    """
    output_filepath = _create_csv_filepath('jobs_qual_labels')
    to_csv(parse_job_file(input_filepath), output_filepath)
    return output_filepath


def parse_job_file(filepath: str) -> List[dict]:
    """
    Given a valid filepath to a downloaded jobs file, parse it for qualification labels

    :param filepath: the filepath to the raw jobs data file
    :return: a list of dicts containing job id and labels for all jobs with qualification labels
    """
    ID_COL_NAME = 'Job Id'
    LABELS_COL_NAME = 'Qualification Labels'
    result = []
    with open(filepath, encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        for row in reader:
            if row[LABELS_COL_NAME].strip() != '':
                result.append({
                    'job_id': row[ID_COL_NAME],
                    'job_url': f'https://jhu.joinhandshake.com/jobs/{row[ID_COL_NAME]}',
                    'qualification_labels': [label.strip() for label in row[LABELS_COL_NAME].split(', ')]
                })
    return result


def _create_csv_filepath(filename: str):
    return create_filepath_in_download_dir(f'{get_datestamped_filename(filename)}.csv')
