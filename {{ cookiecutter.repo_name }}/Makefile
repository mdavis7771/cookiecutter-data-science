.PHONY: clean download preprocess train evaluate visualize lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DATA_RAW_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
DATA_RAW_FILENAME = "data/raw/data.csv"
DATA_PREPROCESSED_FILENAME = "data/processed/processed.pkl"
DATA_FEATUREVECTOR_FILENAME = "data/interim/feature_vector.pkl"
MODEL_FILENAME = "results/models/output.model"
TRAIN_FILE = "data/interim/train.pkl"
TEST_FILE = "data/interim/test.pkl"
EVAL_FILENAME = "results/reports/eval.csv"
FIGURES_FOLDER = "results/reports/figures"
BUCKET = {{ cookiecutter.s3_bucket }}
PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}
ENFILE = .env

# This reads our.env file and preserves and overwrites from command line
export $(shell [ ! -n "$(ENVFILE)" ] || cat $(ENVFILE) | grep -v \
    --perl-regexp '^('$$(env | sed 's/=.*//'g | tr '\n' '|')')\=')

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Download, preprocess, featurize, split, train, evaluate
all: $(DATA_RAW_FILENAME) $(DATA_PREPROCESSED_FILENAME) $(DATA_FEATUREVECTOR_FILENAME) $(MODEL_FILENAME) $(TRAIN_FILE) $(TEST_FILE) $(EVAL_FILENAME)

## Install Python Dependencies
requirements: test_environment
	pip install -U pip setuptools wheel
	pip install -r requirements.txt

$(DATA_RAW_FILENAME):
	$(PYTHON_INTERPRETER) src/data/download.py $(DATA_RAW_URL) $@

## Download raw Data from $(DATA_RAW_URL)
download: $(DATA_RAW_FILENAME)

$(DATA_PREPROCESSED_FILENAME): $(DATA_RAW_FILENAME)
	$(PYTHON_INTERPRETER) src/data/preprocess.py $< $@

## Preprocess the data
preprocess: $(DATA_PREPROCESSED_FILENAME)

build_features $(DATA_FEATUREVECTOR_FILENAME): $(DATA_PREPROCESSED_FILENAME)
	$(PYTHON_INTERPRETER) src/features/build_features.py $< $@

## Build Feature Vector from Preprocessed file
build_features: $(DATA_FEATUREVECTOR_FILENAME)

$(TRAIN_FILE): $(DATA_FEATUREVECTOR_FILENAME)
	$(PYTHON_INTERPRETER) src/data/train_test_split.py $(DATA_FEATUREVECTOR_FILENAME) $(TRAIN_FILE) $(TEST_FILE)

$(TEST_FILE): $(DATA_FEATUREVECTOR_FILENAME)
	$(PYTHON_INTERPRETER) src/data/train_test_split.py $(DATA_FEATUREVECTOR_FILENAME) $(TRAIN_FILE) $(TEST_FILE)

## Split feature vector file into train and test files
split: $(TRAIN_FILE)

$(MODEL_FILENAME): split
	$(PYTHON_INTERPRETER) src/models/train_model.py $(TRAIN_FILE) $@

## Train the model and output a model file.
train: $(MODEL_FILENAME)

$(EVAL_FILENAME): $(MODEL_FILENAME)
	$(PYTHON_INTERPRETER) src/evaluation/evaluate.py $(MODEL_FILENAME) $(TEST_FILE) $@

## Evaluate the model using test and output evaluation metrics
eval: $(EVAL_FILENAME)

## Generate Figures from the evaluation file
visualize: $(EVAL_FILENAME)
	$(PYTHON_INTERPRETER) src/visualize/visualize.py $(EVAL_FILENAME) $(FIGURES_FOLDER)

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -f data/raw/*.*
	rm -f data/processed/*.*
	rm -f data/interim/*.*
	rm -f data/external/*.*
	rm -f results/reports/*.*
	rm -f results/reports/figures/*.*
	rm -f results/models/*.*

## Lint using flake8
lint:
	flake8 src

## Upload Data to S3
sync_data_to_s3:
	aws s3 sync data/ s3://$(BUCKET)/data/

## Download Data from S3 - Should be used when sharing a specific versioned run and not starting from scratch
sync_data_from_s3:
	aws s3 sync s3://$(BUCKET)/data/ data/

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) -f environment.yml python=3
else
	conda create --name $(PROJECT_NAME) -f environment.yml python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	@pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already intalled.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20
show-help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
