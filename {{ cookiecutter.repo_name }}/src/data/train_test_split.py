# -*- coding: utf-8 -*-
import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import logging
from src.utils import config_logging, log_func, time_func
from src.features.build_features import read_feature_vector, get_features, get_label, get_label_column_name
import sys
from sklearn.model_selection import train_test_split


@click.command()
@click.argument('feature_vector_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('train_output_file', type=click.Path(writable=True, dir_okay=False))
@click.argument('test_output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--test_ratio', default=20, type=int)
@log_func
@time_func
def split(feature_vector_file, train_output_file, test_output_file, test_ratio):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).

        :param feature_vector_file: File path to feature vector dataset
        :type feature_vector_file: str

        :param train_output_file: Filename to save a copy of the split train data to.
        :type train_output_file: str

        :param test_output_file: Filename to save a copy of the split test data to.
        :type test_output_file: str

        :param test_ratio: Amount (in percent) of data to use for testing. E.g, 20
        :type test_ratio: int
    """
    logger = logging.getLogger(__name__)

    logger.info('Preprocessing {} into {} and {} at {} ratio'.format(feature_vector_file, train_output_file,
                                                                     test_output_file, test_ratio))

    dframe = read_feature_vector(feature_vector_file)
    X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(get_features(dframe), get_label(dframe),
                                                                            test_size=float(test_ratio)/100,
                                                                            random_state=31337)

    # recombine the features and labels so we can save them
    X_test_data[get_label_column_name()] = y_test_data
    X_train_data[get_label_column_name()] = y_train_data

    X_test_data.to_pickle(test_output_file)
    X_train_data.to_pickle(train_output_file)


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not split(sys.argv[1:]):
        sys.exit(1)
