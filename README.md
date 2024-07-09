# cookiecutter_forecast_model
Template codebase for forecasting models, including support for bayesian (stan, pymc) and traditional machine learning (sklearn) frameworks. 


## Poetry installation

You can install `poetry` via the new recommended installer :

```
curl -sSL https://install.python-poetry.org | python3 -
```

In some cases (e.g. on MacOS) python is not configured with the right permissions to create symlinks.
If this issue appears, try installing poetry with following command:

```
curl -sSL https://install.python-poetry.org | sed 's/symlinks=False/symlinks=True/' | python3 -
```

You may also need to add `~/.local/bin` to your path, to do so add the following to your *shrc file
```
export PATH="$HOME/.local/bin:$PATH"
```

Since we are using Python's venv, it’s useful to configure poetry to not create its own virtual environments :

```
poetry config virtualenvs.create false
```


## Getting Started

A Makefile serves as the primary entrypoint of all important commands: `setup`, `test`, `docs`, `test`, as well as launching the pipelines themselves.

To set up the development environment run :

```
make setup
```

The script will create a virtual environment, install all dependencies and pre-commit hooks.

<!-- To test the setup has worked as expected, it is helpful to run the pytest framework :

```
make test
```` -->

That's it, you are ready to go! 🚀


## Troubleshooting

The following details workarounds for known project issues:

- **Python installed from Conda** : instead of running `make setup` , try the following seqauence of commands.
  
  ```
  # create and activate new python environment
  python3.11 -m venv venv
  . venv/bin/activate 
  pip install --upgrade poetry pre-commit

  # deactivate conda base env
  conda deactivate base

  # select venv python interpreter in ide
  # run install commands for poetry and pre-commit
  poetry install
  pre-commit install
  ```
   

## Running project pipelines

To run your project end-to-end :

1. Unzip `artefacts` data folder and place at top-level directory (alongside `source`, `confgs`, etc.)
2. Set configurations using `configs/[config].yml` files
3. Run `make data_processing` and check `artefacts/input/processed_data/testing` folder is populated with processed data outputs
4. Run `make forecast_model` and check `artefacts/output/forecast_model` is populated with forecasting outputs and fit metrics
5. [*COMING SOON*] Run `make optimisation` and check `artefacts/output/optimisation` is populated with optimisation outputs

By default, the make commands will output and pull from "testing" folders in the `artefacts` data directory. Feel free to create additional make commands or copy and paste script into the terminal to customize output versioning.


## Interacting with the debugger

Instead of running project pipelines in the terminal, developers might prefer to work in the debugger. The following is an example vscode launch configurations for the `data_processing` pipeline.

Data processing configuration :
```
{
    "name": "data processing",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/source/run.py",
    "console": "integratedTerminal",
    "justMyCode": true,
    "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "PYDEVD_DISABLE_FILE_VALIDATION": "1"
    },
    "args": [
        "--pipeline", "data_processing",
        "--config", "configs/run_details.yml",
        "--config", "configs/directories.yml",
        "--config", "configs/pipelines.yml",
        "--config", "configs/data_processing.yml",
        "--config", "configs/forecast_model.yml",
        "--raw-data-version", "testing",
        "--processed-data-version", "testing",  // comment to timestamp output
    ]
}
```

A complete working version of the `launch.json` is committed to the GitHub repo for reference.


## How to add a pipeline task?

Step-by-step approach for adding a new task to the `data_processing` pipeline to compute an additional commercial effectiveness metric (e.g. segmentation).

1. Duplicate `process_data.py` within `source/tasks/data_processing` and rename the file and class appropriately (e.g. `process_data.py` becomes `merge_time_data.py` and `ProcessDataset` becomes `MergeTimeSeriesDatasets`). Also update the class name attribute to "evaluate_segmentation_metric".
   
2. Create config for our new segmentation metric. To do this, we need to update `pipelines.yml` with our new task name, update `directories.yml` with output files we expect to generate, and update `data_processing.yml` with any user input variables we want to make available to the task (e.g. lags for correlations).
   
3. Add our new metric task to the `data_processing_pipeline.py` pipeline within `source/pipelines/core`. To do this you need to both import the class EvaluateSegmentation and include in the `get_tasks` method logic at the bottom of the file.

4. You should now be able to run the `data_processing` pipeline and it will create a output subfolder for your newly created metric! For this test run, we will have replicated the outputs from `process_data.py` since we duplicated that task as our starting point (we'll want to go ahead and delete that). 
   
5. It is now up to you to build out the task logic for `merge_time_data.py` to reflect the outputs you want to generate. Happy coding!


## Processed data schema

*section coming soon ...*
