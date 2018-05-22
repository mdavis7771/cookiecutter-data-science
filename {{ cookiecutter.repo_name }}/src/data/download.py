# -*- coding: utf-8 -*-
import requests
import math
import click
from dotenv import find_dotenv, load_dotenv
from tqdm import tqdm
import logging
from src.utils import config_logging, log_func, time_func, TqdmToLogger
from urlparse import urlparse
import boto3
import botocore
import os
import sys


def hook(t):
    def inner(bytes_amount):
        t.update(bytes_amount)
    return inner


@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
@log_func
@time_func
def download_file(url, filename):
    """ Downloads the raw file into (../raw) so it is ready to be processed

    :param url: The HTTP, HTTPS, or S3 URL to download the file from.
    :type url: str

    :param filename: Full path and filename where to save the download data to.
    :type filename: str
    """
    logger = logging.getLogger(__name__)
    logger.info('Downloading from {} to {}'.format(url, filename))

    if len(url) > 5 and url[:5] == "s3://":
        url_info = urlparse(url)

        logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
        client = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )

        try:
            key = url_info.path[1:]
            total_size = float(client.head_object(Bucket=url_info.netloc, Key=key)['ContentLength'])
            block_size = 1024 * 1024
            logger.info("File Size: {}MB".format(round(total_size/block_size, 2)))

            tqdm_out = TqdmToLogger(logger, level=logging.INFO)
            with tqdm(file=tqdm_out, total=total_size, unit='B', unit_scale=True) as t:
                # remove slash from the front when specifying the key
                client.download_file(url_info.netloc, key, filename, Callback=hook(t))

        except botocore.exceptions.ClientError as e:
            logger.error("Unable to download file: {}".format(e.message))
            return False
    else:
        # Streaming, so we can iterate over the response.
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error("Unable to download file: {}".format(err.message))
            return False

        # Total size in bytes.
        total_size = float(r.headers.get('content-length', 0))
        block_size = 1024 * 1024
        logger.info("File Size: {}MB".format(round(total_size/block_size, 2)))
        wrote = 0
        tqdm_out = TqdmToLogger(logger, level=logging.INFO)

        with open(filename, 'wb') as f:
            for data in tqdm(r.iter_content(block_size), file=tqdm_out, total=math.ceil(total_size/block_size),
                             unit='MB', unit_scale=True):
                wrote = wrote + len(data)
                f.write(data)

        if total_size != 0 and wrote != total_size:
            logger.info("ERROR: Downloaded file is corrupt. Size mismatch. Total size {} != {}".format(total_size, wrote))
            return False

    logger.info("Download complete.")
    return True


if __name__ == '__main__':
    config_logging()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    if not download_file(sys.argv[1:]):
        sys.exit(1)
