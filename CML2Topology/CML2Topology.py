# (c) 2023-2024 Piotr Wojciechowski <piotr@it-playground.pl>
# MIT License (see LICENSE)
class CML2Topology:
    nodes = []
    links = []

    def __init__(self, cml2_topology):
        self.topology = cml2_topology

        self._read_lab_nodes()
        self._read_lab_links()

    def _read_lab_nodes(self) -> None:
        """
        Read and store node information from the topology data.

        This internal method extracts information about each node from the topology data, if available.
        It processes each node's details such as its name, ID, definition, position, interfaces, and other
        configurations, and stores them in a list.

        :return: None
        """

        # TODO: Add support for initial config
        # TODO: Add support for provider version 0.7.0 new features and fields

        if 'nodes' in self.topology:
            for node in self.topology['nodes']:
                new_node = {
                    "node_name": node.get('label'),
                    "node_id": node.get('id'),
                    "node_definition": node.get('node_definition'),
                    "node_x": node.get('x'),
                    "node_y": node.get('y'),
                    "node_interfaces": node.get('interfaces'),
                    "node_boot_disk_size": node.get('boot_disk_size'),
                    "node_image_definition": node.get('image_definition'),
                    "node_ram": node.get('ram'),
                    "node_cpus": node.get('cpus'),
                    "node_cpu_limit": node.get('cpu_limit'),
                    "node_data_volume": node.get('data_volume'),
                    "node_configuration": node.get('configuration'),
                    "node_tags": node.get('tags'),
                }
                self.nodes.append(new_node)

    def _read_lab_links(self) -> None:
        """
        Read and store link information from the topology data.

        This internal method extracts information about each link from the topology data, if available.
        It processes each link's details, including the connected nodes and their interfaces, and stores
        them in a list.

        :return: None
        """

        if 'links' in self.topology:
            for link in self.topology['links']:
                new_link = {
                    "link_name": link.get('id'),
                    "node_a": self.get_node_name_by_id(link.get('n1')),
                    "node_b": self.get_node_name_by_id(link.get('n2')),
                    # The "slot_a" and "slot_b" are optional for Terraform link resource, but when lab topology
                    # is exported from CML it is present in the YAML file so we keep it to preserve links
                    # being assigned to proper device interface
                    "slot_a": self.get_node_interface_slot_by_id(link.get('n1'), link.get('i1')),
                    "slot_b": self.get_node_interface_slot_by_id(link.get('n2'), link.get('i2')),
                }
                self.links.append(new_link)

    def get_lab_info(self) -> dict:
        """
        Retrieve general information about the lab.

        This method returns the general information about the lab, such as lab ID, if it is available
        in the topology data.

        :return: A dictionary containing the lab information, or None if not available.
        """

        return self.topology.get('lab')

    def get_lab_info_title(self) -> str:
        """
        Retrieve the title of the lab.

        This method returns the title of the lab from the topology data, if it is available.

        :return: The title of the lab as a string, or None if not available.
        """

        return self.topology.get('lab')['title'] or None

    def get_lab_info_description(self) -> str:
        """
        Retrieve the description of the lab.

        This method returns the description of the lab from the topology data, if it is available.

        :return: The description of the lab as a string, or None if not available.
        """

        return self.topology.get('lab')['description'] or None

    def get_lab_info_notes(self) -> str:
        """
        Retrieve the notes associated with the lab.

        This method returns any notes associated with the lab from the topology data, if available.

        :return: The notes of the lab as a string, or None if not available.
        """

        return self.topology.get('lab')['notes'] or None

    def get_lab_nodes(self) -> list:
        """
        Retrieve the list of nodes in the lab.

        This method returns a list of all nodes stored in the topology. Each node is represented as a
        dictionary containing its details.

        :return: A list of dictionaries, each representing a node in the lab.
        """

        return self.nodes

    def get_lab_links(self) -> list:
        """
        Retrieve the list of links in the lab.

        This method returns a list of all links stored in the topology. Each link is represented as a
        dictionary containing details about the connected nodes and their interfaces.

        :return: A list of dictionaries, each representing a link in the lab.
        """

        return self.links

    def get_node_name_by_id(self, node_id: str) -> str:
        """
        Returns the node_name for the given node_id.

        :param node_id: The node_id to search for.
        :return: The node_name corresponding to the node_id.
        :raises ValueError: If the node_id is not found in the list.
        """
        for node in self.nodes:
            if node.get('node_id') == node_id:
                return node.get('node_name')
        raise ValueError(f"Node with ID '{node_id}' not found.")

    def get_node_interface_slot_by_id(self, node_id: str, interface_id: str) -> str:
        """
        Returns the slot identifier for the given interface_id on node given by node_id.

        :param node_id: The node_id to query.
        :param interface_id: The interface_id to query.
        :return: The slot corresponding to the interface_id on node_id.
        :raises ValueError: If the node_id is not found in the list.
        """
        for node in self.nodes:
            if node.get('node_id') == node_id:
                for interface in node.get('node_interfaces'):
                    if interface.get('id') == interface_id:
                        return interface.get('slot')
        raise ValueError(f"Node with ID '{node_id}' not found.")

