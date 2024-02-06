# CML2TF: CML to Terraform converter

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/WojciechowskiPiotr/cml-terraform-converter)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Coverage Status](https://coveralls.io/repos/github/WojciechowskiPiotr/cml-terraform-converter/badge.svg)](https://coveralls.io/github/WojciechowskiPiotr/cml-terraform-converter)
[![CI](https://github.com/WojciechowskiPiotr/cml-terraform-converter/actions/workflows/python-package.yml/badge.svg)](https://github.com/WojciechowskiPiotr/cml-terraform-converter/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/virl2-client.svg)](https://badge.fury.io/py/virl2-client)

Converts existing Cisco Modeling Labs lab into Terraform HCL .tf files from exported lab topology YAML file.

This is an early version of the script. This version is compatible with *terraform-provider-cml2* version 0.6.2/0.7.0. Not all features are implemented, yet. Please refer to [TODO.md](https://github.com/WojciechowskiPiotr/cml-terraform-converter/TODO.md) file for the list of unsupported features and current restrictions.

## Installation

To use this package install it via PyPI `pip install cml2tf`.  It's recommended to use either a virtual environment or use something like `pipx` to properly isolate the package.

## Development

If you want to develop the package then [PDM](https://pdm-project.org/latest/) is needed.  Follow their instructions on the web site to install PDM.  This requires Python3, it's been tested w/ 3.8, 3.9, 3.10 and 3.11.

Once installed, you can get a development environment using the follwing steps:

1. Clone the repo
    ```bash
    git clone https://github.com/WojciechowskiPiotr/cml-terraform-converter.git
    ```
2. Go to your project folder
    ```bash
    cd cml-terraform-converter
    ```
3. Set up a Python venv. First make sure that you have Python 3 installed on your machine. We will then be using PDM to create an isolated environment with only the necessary packages.
    ```bash
    pdm venv create
    pdm venv activate
    ```
    Copy / paste the resulting string into your shell or use something like [direnv](https://direnv.net) to automate this.

    > **Note:** Creation of the venv is only needed once, activation whenever you want to work with the venv!
4. Install dependencies
    ```bash
    pdm install --dev
    ```
5. Install the package as editable (optional, but eases development by installing the script / entry point). Don't commit it to the repo, though.
    ```bash
    pdm add --dev --editable .
    ```
    You can remove it again using
    ```bash
    pdm remove --dev .
    ```

Code should be formatted with _ruff_ which is installed as part of the dev dependencies.  Please ensure to format your code before submitting a PR, the GH action will fail otherwise.

## Usage

First, export the lab topology from Cisco Modeling Labs to the YAML file and store it in the project folder. Log into your Cisco Modeling Labs instance to export the lab, enter the lab you want to export from the top menu, select Lab → Download Lab, and save the file.

To convert a lab into Terraform files, use the following command: `cml2tf -i lab.yaml` where _lab.yaml_ is the name of the exported file.

As a result of running the script, a new folder _lab_ will be created. The folder name is always the same as the exported YAML filename. It contains two files: _variables.tf_ and _main.tf_. The first file contains variables like CML server URL, login, and password. Edit this file, providing the correct credentials. The _main.tf_ has the topology for Terraform.

If a destination folder exists you need to use the `-f` option to overwrite its content. This will let you update the converted _main.tf_ file. The _variables.tf_ file, if it exists, remains unchanged.

If you want to have the configurations of the lab nodes separated out into individual files which then you can provide the `-c / --configs` flag.  The _main.tf_ file will include the exported configurations via `file()`.

To read the full usage information issue `cml2tf -h` command.

```commandline
usage: cml2tf [-h] [-i INPUT] [-o OUTDIR] [-f]

options:
  -h, --help            show this help message and exit

Input options:
  -i INPUT, --input INPUT
                        File with input lab topology in YAML exported from CML2

Output options:
  -o OUTDIR, --outdir OUTDIR
                        Output directory name where terraform files will be created (by default input topology filename)
  -c, --configs         store configurations in separate files
  -f, --force           Overwrite files if destination folder exists

Usage example: cml2tf -i topology.yaml
```

## Known issues

Use [GitHub Issues](https://github.com/WojciechowskiPiotr/cml-terraform-converter/issues) to report any problems or share ideas about expanding the script.

## Getting involved

If you want to contribute to this project, feel free to fork it and then send your proposal using a [Pull Request](https://github.com/WojciechowskiPiotr/cml-terraform-converter/pulls).

