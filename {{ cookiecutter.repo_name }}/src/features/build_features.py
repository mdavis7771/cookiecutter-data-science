# -*- coding: utf-8 -*-
import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import logging
from src.utils import config_logging, log_func, time_func, TqdmToLogger
from src.data.preprocess import read_processed_data
import sys


def read_feature_vector(fname, with_label=True):
    """ Return just feature vector

        :param fname: Filename to read the feature vector from
        :type fname: str

        :param with_label: Whether to return the label with the data or not.
        :type with_label: bool

        :return: Dataframe of just the feature columns
        :rtype: pandas.DataFrame
    """
    dframe = pd.read_pickle(fname)
    """ :type: pandas.DataFrame """

    if not with_label:  # remove the label column
        dframe.drop(labels=get_label_column_name(), axis=1, inplace=True)

    return dframe


def get_feature_names():
    """ Return just the names of the column feature

        :return: List of just the feature column names
        :rtype: list
    """
    return ['x0', 'x1', 'x2', 'x3']


def get_features(dframe):
    """ Return just the features for the dframe

        :param dframe: Dataframe to return features from
        :type dframe: pandas.DataFrame

        :return: Dataframe of just the feature columns
        :rtype: pandas.DataFrame
    """
    return dframe[get_feature_names()]


def get_label_column_name():
    return ['y']


def get_label(dframe):
    return dframe[get_label_column_name()]


def build_feature_vector(dframe):
    """ Create features for the dframe and returns a new dframe with the features

        :param dframe: Dataframe to build features from
        :type dframe: pandas.DataFrame
    """

    dframe = dframe.copy()  # Avoid inplace modifications
    dframe.columns = get_feature_names() + get_label_column_name()
    return dframe


@click.command()
@click.argument('processed_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('feature_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel_file', type=click.Path(writable=True, dir_okay=False), default=None)
@log_func
@time_func
def build_features_file(processed_file, feature_file, excel_file):
    """ Create features from the preprocessed files (../processed) into
        a vector of data ready to be analyzed (saved in ../processed).

        :param processed_file: File path to raw data file
        :type processed_file: str

        :param feature_file: Filename to save the pickeled feature vector to.
        :type feature_file: str

        :param excel_file: Filename to save a copy of the preprocessed data in XLSX format.
        :type excel_file: str
    """
    logger = logging.getLogger(__name__)

    logger.info('Creating features from {} into {}'.format(processed_file, feature_file))

    dframe = read_processed_data(processed_file)
    dframe = build_feature_vector(dframe)

    dframe.to_pickle(feature_file)
    if excel_file is not None:
        dframe.to_excel(excel_file)


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not build_features_file(sys.argv[1:]):
        sys.exit(1)
