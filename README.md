# <h1><p style="text-align: center;">Effective Programming Practices: Final Project</p></h1>

<h2><p style="text-align: center;">Topic: Agriculture diversity, Structural Change, Long-run Development: Evidence from US</p></h2>

This project attempts to replicate the paper *Agriculture diversity, Structural Change,
Long-run Development: Evidence from US* by **Martin FiszBein**. The source paper uses
STATA to run the analysis whereas this project uses python to replicate the results. The
project was created with Cookiecutter.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/renuka-venkataramani/final_project/main.svg)](https://results.pre-commit.ci/latest/github/renuka-venkataramani/final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

1. To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate final_project
```

2. To build the project, type

```console
$ pytask
```

3. To execute pytest, type

```console
$ pytest
```

## Flowchart of the work: ALL the major files are stored in the SRC folder

### Data:
1. Inputs: Inputs are saved in SRC # build through config.py 
2. Outputs: Output dataframes, plots are stored in BLD

### Data_Management:

1. Initially the **data_raw.dta** file is imported
2. **data_to_construct_variables.dta** is also read. This file is used to create indicator
   dummies
3. The above step is done in variable_construction.py
4. **data_info.yaml** contains the name of the variables in the data_raw file and renaming
   dictionaries. It consists of lists and dictionaries.
5. This file is used to clean the data (rename columns, drop variables, etc)
6. **data_clean.py** is used to build three datasets, to rename the columns into meaningful
   string and to map the relevant variables constructed from
   **data_to_construct_variables.dta**



### Analysis:

1. **Model.py** contains the codes to run OLS with more than 2 controls

### Final:

1. plots and tables are stored in final directory. The relevant python files are located
   in the same directory

### Task: 

1. Task file is written for each and every steps

### Test: 

1. Test directory includes a duplicate datafile and a data_info.yaml file used to test
functions. The functions in clean_data under data_management directory are tested.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).

Fiszbein, M. (2022). Agricultural Diversity, Structural Change, and Long-Run
Development: Evidence from the United States. American Economic Journal: Macroeconomics,
14(2), 1-43.
