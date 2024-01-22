# (c) 2023-2024 Piotr Wojciechowski <piotr@it-playground.pl>
# MIT License (see LICENSE)

import os
import sys
from argparse import ArgumentParser, Namespace

import yaml
from jinja2 import Environment, PackageLoader

from cml2tf.topology import CML2Topology

# TODO: Improve exceptions handling


def cml_to_terraform_convert(
    cml2topology: dict,
    project_name: str,
    flags: Namespace,
) -> None:
    """
    Convert a CML2 topology to Terraform configuration files.

    This function takes a CML2 topology and a project name, then generates
    Terraform configuration files for the given topology. It creates a new
    Terraform project directory, renders 'variables.tf' and 'main.tf' templates
    with the topology data, and saves them to the project directory.

    :param cml2topology: The CML2 topology data as a dictionary.
    :param project_name: The name of the Terraform project to be created.
    :param flags: provided command line flags
    """

    # Create topology object based on the topology YAML
    topology = CML2Topology(cml2topology)

    # Create directory for a new Terraform project
    create_directory(project_name, flags.force)

    # Render variables.tf from template
    environment = Environment(loader=PackageLoader("cml2tf"))

    # change into output directory
    os.chdir(project_name)

    # If force option is set then do not render variables.tf if file exists
    if flags.force and os.path.exists("variables.tf"):
        pass
    else:
        variables_template = environment.get_template("variables.tf.j2")
        variables_tf_content = variables_template.render()
        save_file_to_disk("variables.tf", variables_tf_content)

    # Render main.tf from template
    main_template = environment.get_template("main.tf.j2")
    main_tf_content = main_template.render(
        lab_title=topology.get_lab_info_title(),
        lab_description=topology.get_lab_info_description(),
        lab_notes=topology.get_lab_info_notes(),
        lab_nodes=topology.get_lab_nodes(),
        lab_links=topology.get_lab_links(),
        flags=flags,
    )
    save_file_to_disk("main.tf", main_tf_content)


def read_cml2_topology(yaml_file: str) -> dict:
    """
    Read and parse a CML2 topology from a YAML file.

    This function opens a YAML file containing a CML2 topology, reads its
    contents, and parses it into a Python dictionary.

    :param yaml_file: The path to the YAML file containing the CML2 topology.
    :return: A dictionary representing the parsed CML2 topology.
    """

    try:
        with open(yaml_file) as file:
            topology = yaml.safe_load(file)
            return topology
    except OSError as error:
        print(f"Error reading topology file: {error}")
        exit(1)


def save_file_to_disk(filename: str, content: str) -> None:
    """
    Save given content to a file on disk.

    This function writes the provided content to a file specified by
    'filename'. If the file cannot be written, it catches the IOError and
    returns an error message.

    :param filename: The name of the file to save the content to.
    :param content: The content to be saved in the file.
    :return: A success message if file is saved, otherwise an error message.
    """

    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"File '{filename}' saved successfully.")
    except OSError as error:
        print(f"Error: Unable to save file '{filename}'. {error}")
        exit(1)


def strip_extension(filename: str) -> str:
    """
    Remove the file extension from a filename.

    This function takes a filename and returns the filename without its
    extension. It is useful for processing file paths where the extension is
    not needed.

    :param filename: The filename from which to strip the extension.
    :return: The filename without its extension.
    """

    root, _ = os.path.splitext(filename)
    return root


def create_directory(directory_name: str, force=False) -> None:
    """
    Create a directory with the given name.

    This function attempts to create a directory with the specified
    'directory_name'. If the directory already exists, it prints an error
    message. It also handles and prints any OSError that might occur during the
    creation process.

    :param directory_name: The name of the directory to be created.
    :param force: If True then ignore that directory exists
    :return: None
    """

    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            print(
                f"Directory '{directory_name}' for Terraform project created successfully."
            )
        else:
            if force is False:
                print(
                    f"Error: Directory '{directory_name}' already exists. Please remove it first"
                )
                exit(1)
            else:
                print(
                    f"Directory '{directory_name}' already exists. Force flag set... Ignoring..."
                )
    except OSError as error:
        print(f"Error: {error}")
        exit(1)


def main():
    parser = ArgumentParser()
    parser.epilog = f"Usage example: {parser.prog} -i topology.yaml"

    args_input = parser.add_argument_group("Input options")
    args_output = parser.add_argument_group("Output options")

    args_input.add_argument(
        "-i",
        "--input",
        type=str,
        help="File with input lab topology in YAML exported from CML2",
    )

    args_output.add_argument(
        "-o",
        "--outdir",
        type=str,
        help="Output directory name where Terraform files will be created "
        + "(by default input topology filename)",
    )
    args_output.add_argument(
        "-c",
        "--configs",
        default=False,
        action="store_true",
        help="store configurations in separate files",
    )
    args_output.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        dest="force",
        help="Overwrite files if destination folder exists",
    )

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    p = parser.parse_args()
    if not p.input:
        parser.error("Missing input lab topology file")

    # Open and read the topology YAML file
    cml2_topology = read_cml2_topology(p.input)
    # TODO: Add support for reading configuration directly from CML

    # Convert YAML topology into Terraform
    outdir = strip_extension(p.input) if not p.outdir else p.outdir
    cml_to_terraform_convert(cml2_topology, outdir, p)

    print("Converted")


if __name__ == "__main__":
    main()
