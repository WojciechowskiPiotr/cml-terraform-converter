import os

import pytest
from cml2tf.topology.nodeconfig import NodeConfig


def test_empty_config():
    config = NodeConfig("label", "")
    assert config.empty() is True


def test_empty_list_config():
    config = NodeConfig("label", [])
    assert config.empty()
    assert config.out() == ""


def test_oneline_config():
    config = NodeConfig("label", "one line")
    assert config.oneline() is True


def test_out():
    config = NodeConfig("label", "one line")
    assert config.out() == "one line"


def test_multi_line_out():
    config = NodeConfig("label", "line1\nline2")
    assert config.out() == "line1\nline2"


def test_fileout(tmp_path):
    os.chdir(tmp_path)
    config_str = "one line"
    config = NodeConfig("label", config_str)
    filename = config.fileout()
    with open(filename) as f:
        content = f.read()
    assert content == config_str


def test_unhandled_config_type():
    with pytest.raises(ValueError):
        NodeConfig("label", 123).fileout()  # pyright: ignore

    with pytest.raises(ValueError):
        NodeConfig("label", 123).out()  # pyright: ignore


def test_list_config():
    config = NodeConfig("label", [{"name": "Main", "content": "one line"}])
    assert config.out() == "one line"


def test_fileout_list_config(tmp_path):
    os.chdir(tmp_path)
    config_list = [{"name": "Main", "content": "one line"}]
    config = NodeConfig("label", config_list)
    filename = config.fileout()
    with open(filename) as f:
        content = f.read()
    assert content == config_list[0]["content"]
