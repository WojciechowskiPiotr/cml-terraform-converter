# cml-terraform-coverter

Converts existing Cisco Modeling Labs lab into Terraform HCL .tf files from exported lab topology YAML file.

This is an early version of the script. This version is compatible with terraform-provider-cml2 version 0.6.2. Not all features are yet implemented. Please refer to [TODO.md](https://github.com/WojciechowskiPiotr/cml-terraform-converter/TODO.md) file for the list of unsupported features and current restrictions.

## Installation

Clone the repo
```bash
git clone https://github.com/WojciechowskiPiotr/cml-terraform-converter.git
```
Go to your project folder
```bash
cd cml-terraform-converter
```

Set up a Python venv
First make sure that you have Python 3 installed on your machine. We will then be using venv to create an isolated environment with only the necessary packages.

Install virtualenv via pip
```bash
pip install virtualenv
```

Create the venv
```bash
python3 -m venv venv
```

Activate your venv
```bash
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

First, export the lab topology from Cisco Modeling Labs to the YAML file and store it in the project folder. Log into your Cisco Modeling Labs instance to export the lab, enter the lab you want to export from the top menu, select Lab->Download Lab, and save the file.

To convert lab into Terraform files use the following command: `python3 cml-terraform-converter -i lab.yaml` where _lab.yaml_ is the name of the exported file. 

As a result of running the script, a new folder _lab_ will be created. The folder name is always the same as the exported YAML filename. It contains two files: _variables.tf_ and _main.tf_. The first file contains variables like CML server URL, login, and password. Edit this file, providing the correct credentials. The _main.tf_ has the topology for Terraform.

To read the full usage information issue `python3 cml-terraform-converter.py -h` command.

```commandline
usage: cml-terraform-converter.py [-h] [-i INPUT] [-o OUTDIR] [-f]

options:
  -h, --help            show this help message and exit

Input options:
  -i INPUT, --input INPUT
                        File with input lab topology in YAML exported from CML2

Output options:
  -o OUTDIR, --outdir OUTDIR
                        Output directory name where terraform files will be created (by default input topology filename
  -f, --force           Overwrite files if destination folder exists

Usage example: cml-terraform-converter.py -i file.yaml

```

## Known issues

Use the [GitHub Issues](https://github.com/WojciechowskiPiotr/cml-terraform-converter/issues) to report any problems or share ideas about expanding the script.

## Getting involved

If you want to contribute to this project. feel free to fork it and then send your proposal using the [Pull Request](https://github.com/WojciechowskiPiotr/cml-terraform-converter/pulls).

