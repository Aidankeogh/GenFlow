# rattaca
The RATTACA project aims to use genetic prediction to identify rats to identify rats that would exhibit extreme phenotypes for addiction-related traits. This repository creates a machine learning pipeline to accelerate genome-wide association studies (GWAS) on the collected rat genotype and phenotype data. 

## Setup

The training pipeline was built to use the following technologies:

<!-- table of requirements -->

The pipeline has been tested with Python 3.X. <!-- add python versions that work -->

This repository provides files to setup either a Python venv or conda environment for running the training pipeline.

### Python venv

To use Python venv you first create the venv, activate, and install the pipeline dependencies with the requirements file.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Conda environment

To use conda environments you can create a new environment with the included yaml file.

```
conda create -n rattaca-venv -r environment.yml
conda activate rattaca-venv
```

## Running the trainer

This project uses hydra, the main entrypoint is training_pipeline.py

 To run the default example, run `python training_pipeline.py` from the root directory.

 For an example running a custom config, try `python training_pipeline.py --config-name=optuna_test`, which runs config/optuna_test.yaml
