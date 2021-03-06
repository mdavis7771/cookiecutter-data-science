# -*- coding: utf-8 -*-
import sys
import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.metrics import accuracy_score, precision_score, recall_score
from src.utils import config_logging, time_func
import logging
from src.features.build_features import get_features, get_label, read_feature_vector
from src.models.random_forest import RandomForestModel


@time_func
def predict(model, dframe):
    X = get_features(dframe)

    pred_df = pd.DataFrame(index=X.index.values, columns=['probability', 'prediction'])
    pred_df.index.name = 'index'
    pred_df['probability'] = model.predict_proba(X)
    pred_df['prediction'] = model.predict(X)

    return pred_df


@click.command()
@click.argument('model_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('test_file', type=click.Path(writable=True, dir_okay=False))
@click.argument('predictions_file', type=click.Path(writable=True, dir_okay=False))
def predict_model(model_file, test_file, predictions_file):
    """ Evaluates a model using a specific test file. The Test file must be preprocessed and featurized

        :param model_file: File path to model
        :type model_file: str

        :param test_file: Filename of the pickeled feature vector test file.
        :type test_file: str

        :param predictions_file: Filename where the predictions will be saved to in CSV format.
        :type predictions_file: str
    """
    logger = logging.getLogger(__name__)

    data = read_feature_vector(test_file, with_label=False)
    model = RandomForestModel()
    model.load(model_file)

    if model.clf is None:
        logger.info("Unable to load model from {}". format(model_file))
        return False

    predict(model, data).to_csv(predictions_file, header=True)

    return True


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not predict_model(sys.argv[1:]):
        sys.exit(1)
