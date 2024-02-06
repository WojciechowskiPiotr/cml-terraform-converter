import pytest
from cml2tf.topology import CML2Topology


# Define a fixture for common setup
@pytest.fixture
def topology_data():
    return {
        "lab": {
            "title": "Test Lab",
            "description": "This is a test lab",
            "notes": "Some notes",
        },
        "nodes": [
            {
                "label": "Node 1",
                "id": "n1",
                "node_definition": "Test Node",
                "x": 1,
                "y": 1,
                "interfaces": [{"id": "i1", "slot": "0"}],
                "boot_disk_size": "10GB",
                "image_definition": "Test Image",
                "ram": "2GB",
                "cpus": 1,
                "cpu_limit": 1,
                "data_volume": "5GB",
                "configuration": "Test Config",
                "tags": [],
            },
            {
                "label": "Node 2",
                "id": "n2",
                "node_definition": "Test Node",
                "x": 1,
                "y": 1,
                "interfaces": [{"id": "i1", "slot": "0"}],
                "boot_disk_size": "10GB",
                "image_definition": "Test Image",
                "ram": "2GB",
                "cpus": 1,
                "cpu_limit": 1,
                "data_volume": "5GB",
                "configuration": "Test Config",
                "tags": [],
            },
        ],
        "links": [{"id": "l1", "n1": "n1", "n2": "n2", "i1": "i1", "i2": "i1"}],
    }


def test_read_lab_nodes(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert len(cml2_topology.nodes) == 2
    assert cml2_topology.nodes[0]["node_name"] == "Node 1"


def test_read_lab_links(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert len(cml2_topology.links) == 1
    assert cml2_topology.links[0]["link_name"] == "l1"


def test_get_lab_info(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_lab_info() == topology_data["lab"]


def test_get_lab_info_title(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_lab_info_title() == topology_data["lab"]["title"]


def test_get_lab_info_description(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert (
        cml2_topology.get_lab_info_description() == topology_data["lab"]["description"]
    )


def test_get_lab_info_notes(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_lab_info_notes() == topology_data["lab"]["notes"]


def test_get_lab_nodes(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_lab_nodes() == cml2_topology.nodes


def test_get_lab_links(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_lab_links() == cml2_topology.links


def test_get_node_name_by_id(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_node_name_by_id("n1") == "Node 1"

    cml2_topology.nodes = []
    with pytest.raises(ValueError):
        cml2_topology.get_node_name_by_id("n1")


def test_get_node_interface_slot_by_id(topology_data):
    cml2_topology = CML2Topology(topology_data)
    assert cml2_topology.get_node_interface_slot_by_id("n1", "i1") == "0"

    node = cml2_topology.nodes[0]
    assert node["node_id"] == "n1"
    node["node_interfaces"] = []
    with pytest.raises(ValueError):
        cml2_topology.get_node_interface_slot_by_id("n1", "i1")
