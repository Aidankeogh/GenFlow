# rattaca: A Streamlined Workflow to Facilitate Genome-Scale AI
The RATTACA project aims to use Whole Genome Sequencing data from a heterogenius stock of rats to identify variants that are linked to extreme phenotypes primarily related to physciatric behavior and addiction. The goal of this work is to provide a pipeline that accelerates the use of Machine Learning in Genome-Wide Association Studies (GWAS) by integrating the standard Genomics toolkits of Sgkit and Plink with the standard Machine Learning training toolkits of Sklearn, Hydra, MLFlow, and Optuna.  With this combination of toolkits from Genomics and Machine Learning, this repository offers a streamlined workflow for repetative training and evaluation of Machine Learning methods that aim to predicit phenotypes from genotypes.

## Setup

The training pipeline was built to use the following technologies:

<!-- table of requirements -->

The pipeline has been tested with Python 3.X. <!-- add python versions that work -->

This repository provides an environment file to setup a conda environment for running the training pipeline.

```
conda env create -f environment.yml
conda activate rattaca-venv
```

## Running the trainer

This project uses hydra, the main entrypoint is training_pipeline.py

 To run the default example, run `python training_pipeline.py` from the root directory.

 For an example running a custom config, try `python training_pipeline.py --config-name=optuna_test`, which runs config/optuna_test.yaml, an experiment using a Ridge Regression model.

 See the folder `config/` for the list of our modeling experiment files. New experiments for new models can be run by creating a new config files and alterig the parameter in the `--config-name` option.
