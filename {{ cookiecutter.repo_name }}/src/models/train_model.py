# -*- coding: utf-8 -*-
import click
import pickle
from dotenv import find_dotenv, load_dotenv
import logging
from src.utils import config_logging, log_func, time_func
import sys

from random_forest import RandomForestModel
from src.features.build_features import read_feature_vector


@click.command()
@click.argument('train_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('model_output', type=click.Path(writable=True, dir_okay=False))
@log_func
@time_func
def train_model(train_file, model_output):
    """ Create features from the preprocessed files (../processed) into
       a vector of data ready to be analyzed (saved in ../processed).

       :param train_file: File path to the training data that has been featurized and preprocessed.
       :type train_file: str

       :param model_output: Filename to save the pickeled model to.
       :type model_output: str

   """
    logger = logging.getLogger(__name__)

    logger.info('Training model from {} into {}'.format(train_file, model_output))

    dframe = read_feature_vector(train_file)
    model = RandomForestModel()
    model.train(dframe)
    model.save(model_output)

if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not train_model(sys.argv[1:]):
        sys.exit(1)

