import os
from argparse import Namespace
from pathlib import Path
from unittest.mock import mock_open, patch

import cml2tf.main
import pytest


def test_read_cml2_topology():
    mock_yaml_data = {
        "lab": {
            "title": "Test Lab",
            "description": "This is a test lab",
            "notes": "Some notes",
        },
    }
    with patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="lab: \n  title: Test Lab\n  description: This is a test lab\n  notes: Some notes",
    ) as mock_file:
        with patch("yaml.safe_load", return_value=mock_yaml_data):
            result = cml2tf.main.read_cml2_topology(mock_file)
            assert result == mock_yaml_data

    with pytest.raises(SystemExit, match="1"):
        cml2tf.main.read_cml2_topology("doesnotexist")


def test_save_file_to_disk():
    with patch("builtins.open", new_callable=mock_open()) as mock_file:
        cml2tf.main.save_file_to_disk("test.txt", "Hello, World!")
        mock_file.assert_called_once_with("test.txt", "w")
        file_handle = mock_file.return_value.__enter__.return_value
        file_handle.write.assert_called_once_with("Hello, World!")

    with patch("builtins.open", new_callable=mock_open()) as mock_file:
        mock_file.side_effect = OSError
        with pytest.raises(SystemExit, match="1"):
            cml2tf.main.save_file_to_disk("doesnotexist", "bla")


def test_create_directory():
    with patch("os.makedirs") as mock_makedirs, patch(
        "os.path.exists", return_value=False
    ):
        cml2tf.main.create_directory("test_dir")
        mock_makedirs.assert_called_once_with("test_dir")

    with patch("os.path.exists", return_value=True):
        with pytest.raises(SystemExit, match="1"):
            cml2tf.main.create_directory("test_dir")

    with patch("os.makedirs") as mock_makedirs:
        mock_makedirs.side_effect = OSError
        with pytest.raises(SystemExit, match="1"):
            cml2tf.main.create_directory("doesnotexist")


def test_strip_extension():
    filename = "test.txt"
    result = cml2tf.main.strip_extension(filename)
    assert result == "test"


def test_cml_to_terraform_convert():
    mock_cml2topology = {
        "lab": {
            "title": "Test Lab",
            "description": "This is a test lab",
            "notes": "Some notes",
        },
    }
    mock_project_name = "test_project"
    mock_flags = Namespace(force=True)

    saved_content = {}

    def mock_save(filename: str, content: str) -> None:
        _ = filename
        saved_content[filename] = content

    with patch("cml2tf.main.create_directory"), patch("os.chdir"), patch(
        "cml2tf.main.save_file_to_disk",
        side_effect=mock_save,
    ), patch("os.path.exists", return_value=False):
        cml2tf.main.cml_to_terraform_convert(
            mock_cml2topology, mock_project_name, mock_flags
        )
        assert len(saved_content.keys()) == 2


@pytest.mark.parametrize(
    "toponame,expected",
    [("topology.yaml", 8), ("mini.yaml", 4)],
)
def test_integration(request, tmp_path, toponame, expected):
    testdata = Path(request.path).parent / "testdata"

    test_dir = tmp_path / toponame
    os.mkdir(test_dir)
    os.chdir(test_dir)

    with patch(
        "sys.argv",
        ["prog", "-c", "-f", "-i", f"{testdata}/{toponame}", "-o", str(test_dir)],
    ):
        cml2tf.main.main()
    assert len(list(test_dir.iterdir())) == expected
