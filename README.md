# RATTACA: A Streamlined Workflow to Facilitate Genome-Scale AI
The RATTACA project aims to use Whole Genome Sequencing data from a heterogenius stock of rats to identify variants that are linked to extreme phenotypes primarily related to physciatric behavior and addiction. The goal of this work is to provide a pipeline that accelerates the use of Machine Learning in Genome-Wide Association Studies (GWAS) by integrating the standard Genomics toolkits of Sgkit and Plink with the standard Machine Learning training toolkits of Sklearn, Hydra, MLFlow, and Optuna.  With this combination of toolkits from Genomics and Machine Learning, this repository offers a streamlined workflow for repetative training and evaluation of Machine Learning methods that aim to predict phenotypes from genotypes.  The results from various training runs can then be interactively visualized and assesed via the MLFlow user dashboard.

## Setup

The training pipeline was built to use the following technologies:

<!-- table of requirements -->

The pipeline has been tested with Python 3.X. <!-- add python versions that work -->

This repository provides an environment file to setup a conda environment for running the training pipeline.

```
conda env create -f environment.yml
conda activate rattaca-venv
```

## Running the Trainer

This project uses hydra, the main entrypoint is training_pipeline.py

To run the default example run the following from the root directory

```
python training_pipeline.py
```

For an example running a custom config, try 

```
python training_pipeline.py --config-name=optuna_test
```
This runs config/optuna_test.yaml, an experiment using a Ridge Regression model.

See the folder `config/` for the list of our modeling experiment files. New experiments for new models can be run by creating a new config files and altering the parameter in the `--config-name` option.  The following describes how to go about configuring a specific trainining run.

### Step 1: Configuring the Data

To configure a training run that models on a specific version of Linkage Disequillibrium pruned data to a specific phenotypes dataset, one will need to write a conifg file in the `config/dataset` folder.  Adjust `geno_bed`, `geno_bim`, and `geno_fam` to call the specific genotypes dataset and adjust `phenotypes` to call the specific phenotypes dataset.  Adjusting `select_traits` will limit to certain phenotypes. The `gwas_p_value` will adjust the variant reduction based on GWAS statistical association p-value to the input phenotypes, but this parameter can be swept when configuring an experiment.

![Alt text](screenshots/data_configure.png?raw=true)

### Step 2: Configuring the Model

To configure a training run that calls a specific type of Machine Learning model, such as an XGBoost, one will need to write a config file in the `config/models` folder and establish the default hyperparameters that can be called or adjusted when configuring an experiment.  Adjust the `import_module` to call the python Machine Learning module.  Custom use defined models are permitted so long they have .fit and .predict.  Adujust `name` to call the specific model from the module, such as XGBRegressor from the xgboost python module.  Adjsut `params` according to the authorized hyperparameters of the model.

![Alt text](screenshots/model_configure.png?raw=true)

### Step 3: Configuring the Experiment

<!-- To do -->





