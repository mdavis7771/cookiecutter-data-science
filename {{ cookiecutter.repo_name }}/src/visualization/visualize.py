# -*- coding: utf-8 -*-
import click
from dotenv import find_dotenv, load_dotenv
from src.utils import config_logging, time_func
from src.features.build_features import read_feature_vector, get_feature_names, get_label_column_name
import logging
import matplotlib
matplotlib.use('agg')
import seaborn as sns
import sys


def exploratory_visualization(dframe):
    return sns.pairplot(dframe, diag_kind='kde', vars=get_feature_names(), hue=get_label_column_name()[0])


@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
def create_figures(input_file, output_file):
    """ Evaluates a model using a specific test file. The Test file must be preprocessed and featurized

        :param input_file: File path to featurized vector of all data
        :type input_file: str

        :param output_file: Filename to save the visualization to.
        :type output_file: str

    """
    logger = logging.getLogger(__name__)
    logger.info('Plotting pairwise distribution...')

    dframe = read_feature_vector(input_file)
    plot = exploratory_visualization(dframe)
    plot.savefig(output_file)


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not create_figures(sys.argv[1:]):
        sys.exit(1)
