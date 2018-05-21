# MAD Cookiecutter Data Science

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work including reproducability and data versioning._


#### [Project homepage](http://drivendata.github.io/cookiecutter-data-science/)


### Requirements to use the cookiecutter template:
-----------
 - Python 2.7 or 3.5
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```

or

``` bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```


### To start a new project, run:
------------

    cookiecutter https://github.com/mdavis7771/cookiecutter-data-science


### The resulting directory structure
------------

The directory structure of your new project looks like this: 


```
    +-- .env               <- Environment specific details such as AWS secrets. DO NOT STORE IN GIT
    +-- LICENSE
    +-- Makefile           <- Makefile with commands like 'make train'
    +-- README.md          <- The top-level README for developers using this project.
    +-- api.py             <- A flask JSON API Server that performs predictions
    +-- Dockerfile         <- A Dockerfile to house the project. Optional.
    +-- environment.yml    <- An Anaconda environment file
    +-- data
    |   +-- external       <- Data from third party sources.
    |   +-- interim        <- Intermediate data that has been transformed.
    |   +-- processed      <- The final, canonical data sets for modeling.
    |   +-- raw            <- The original, immutable data dump.
    |
    +-- docs               <- A default Sphinx project; see sphinx-doc.org for details
    |
    +-- notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    |                         the creator's initials, and a short `-` delimited description, e.g.
    |                         '1.0-jqp-initial-data-exploration'.
    |
    +-- references         <- Data dictionaries, manuals, and all other explanatory materials.
    |
    +-- results            <- Generated analysis as HTML, PDF, LaTeX, etc.
    |   +-- reports
    |   |  +-- figures     <- Generated graphics and figures to be used in reporting
    |   +-- models         <- Trained and serialized models, model predictions, or model summaries
    |
    +-- requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    |                         generated with 'pip freeze > requirements.txt'
    |
    +-- setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    +-- src                <- Source code for use in this project.
    |   +-- __init__.py    <- Makes src a Python module
    |   |
    |   +-- data           <- Scripts to download or generate data
    |   | +-- make_dataset.py
    |   |
    |   +-- evaluation       <- Scripts to evaluate models, prediction outsuts, etc
    |   | +-- evaluate.py
    |   |
    |   +-- features       <- Scripts to turn raw data into features for modeling
    |   | +-- build_features.py <- Transforms a preprocessed file by adding features
    |   |
    |   +-- models         <- Scripts to train models and then use trained models to make predictions
    |   | +-- predict_model.py  <- Script to generate a prediction file from an input using the model
    |   | +-- train_model.py    <- Trains a model and saves it for reuse
    |   +-- tests          <- Scripts to test data loading, feature transformations, models, etc
    | +-- visualization    <- Scripts to create exploratory and results oriented visualizations
    |     +-- visualize.py
    |
    +-- tox.ini            <- tox file with settings for running tox; see tox.testrun.org
```

### Installing development requirements
------------

    pip install -r requirements.txt

### Running the tests
------------

    py.test tests
