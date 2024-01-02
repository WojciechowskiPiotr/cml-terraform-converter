# cml-terraform-coverter

Converts existing Cisco Modeling Labs lab into Terraform HCL .tf files from exported lab topology YAML file.

This is an early version of the script. This version is compatible with terraform-provider-cml2 version 0.6.2. Not all features are yet implemented.

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

First export the lab topology from Cisco Modeling Labs to YAML file and store it in project folder. To export the lab log into you Cisco Modeling Labs instance, enter lab you ant to export, from top menu select Lab->Download Lab and save the file.

To convert lab into Terraform files use the followin command: `python3 cml-terraform-converter -i lab.yaml` where _lab.yaml_ is name of the exported file. 

As a result of running the script new folder _lab_ will be created. Folder name is always the same as the exported YAML filename. It contains two files: _variables.tf_ and _main.tf_. The first files contains variables like CML server URL, login and password. Edit this file providing correct credentials. The _main.tf_ contains the topology for Terraform.

## Known issues

Use the [GitHub Issues](https://github.com/WojciechowskiPiotr/cml-terraform-converter/issues) to report any problems or share an ideas about how to expand the script.

## Getting involved

If you want to contribute to this project feel free to fork it and then send you proposal using the [Pull Request](https://github.com/WojciechowskiPiotr/cml-terraform-converter/pulls).

