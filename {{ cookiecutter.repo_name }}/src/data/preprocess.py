# -*- coding: utf-8 -*-
import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import logging
from src.utils import config_logging, log_func, time_func
import sys


def read_raw_data(fname):
    dframe = pd.read_csv(fname, header=None)
    return dframe


def preprocess_data(dframe):
    dframe = dframe.copy()  # I want to avoid inplace modifications
    # cleanup some stuff, remove duplicates, etc
    #
    return dframe


def read_processed_data(fname):
    dframe = pd.read_pickle(fname)
    return dframe


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel_file', type=click.Path(writable=True, dir_okay=False), default=None)
@log_func
@time_func
def preprocess_file(input_file, output_file, excel_file):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).

        :param input_file: File path to raw data file
        :type input_file: str

        :param output_file: Filename to save the pickedled preprocessed data file.
        :type output_file: str

        :param excel_file: Filename to save a copy of the preprocessed data in XLSX format.
        :type excel_file: str
    """
    logger = logging.getLogger(__name__)

    logger.info('Preprocessing {} into {}'.format(input_file, output_file))

    dframe = read_raw_data(input_file)
    dframe = preprocess_data(dframe)

    dframe.to_pickle(output_file)
    if excel_file is not None:
        dframe.to_excel(excel_file)


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not preprocess_file(sys.argv[1:]):
        sys.exit(1)
