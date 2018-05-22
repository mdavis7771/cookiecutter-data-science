# -*- coding: utf-8 -*-
import sys
import click
from dotenv import find_dotenv, load_dotenv
from sklearn.metrics import accuracy_score, precision_score, recall_score
from src.utils import config_logging, log_func, time_func
import logging
from src.features.build_features import get_features, get_label, read_feature_vector
from src.models.random_forest import RandomForestModel
import pandas as pd

@time_func
def cv_evaluate_model(model, dframe):
    X = get_features(dframe)
    y = get_label(dframe)

    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)
    precision = precision_score(y, predictions, average='macro')
    recall = recall_score(y, predictions, average='macro')

    results = {
        'params': str(model.get_params()),
        'model': model.name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
    }
    return pd.DataFrame(data=results, index=[0])


@click.command()
@click.argument('model_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('test_file', type=click.Path(writable=True, dir_okay=False))
@click.argument('eval_file', type=click.Path(writable=True, dir_okay=False))
def evaluate(model_file, test_file, eval_file):
    """ Evaluates a model using a specific test file. The Test file must be preprocessed and featurized

        :param model_file: File path to model
        :type model_file: str

        :param test_file: Filename of the pickeled feature vector test file.
        :type test_file: str

        :param eval_file: Filename where evaluation results will be saved in CSV format.
        :type eval_file: str

        :return: True if successful otherwise False
        :rtype: bool
    """
    logger = logging.getLogger(__name__)

    data = read_feature_vector(test_file)
    model = RandomForestModel()
    model.load(model_file)

    if model.clf is None:
        logger.info("Unable to load model from {}". format(model_file))
        return False

    cv_evaluate_model(model, data).to_csv(eval_file, header=True, index=False)

    return True


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not evaluate(sys.argv[1:]):
        sys.exit(1)
