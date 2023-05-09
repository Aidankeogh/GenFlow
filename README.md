# rattaca
Machine learning on rat genes

## Setup

 connect to https://narrows-gpu.sdsc.edu

 run `conda activate capstone-base`

## Running the trainer

This project uses hydra, the main entrypoint is training_pipeline.py

 To run the default example, run `python training_pipeline.py` from the root directory.

 For an example running a custom config, try `python training_pipeline.py --config-name=optuna_test`, which runs config/optuna_test.yaml