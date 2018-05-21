# {{cookiecutter.project_name}}
--------

{{cookiecutter.description}}

## Project Organization

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

--------

Project based on the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/)
