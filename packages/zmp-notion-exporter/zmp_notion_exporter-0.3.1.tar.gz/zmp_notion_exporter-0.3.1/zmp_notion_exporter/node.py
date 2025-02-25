from __future__ import annotations
from pathlib import Path
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Node:
    def __init__(
        self,
        *,
        object_id: str,
        name: str,
        is_directory: bool = False,
        parent: Node | None = None,
        children: list[Node] | None = None,
    ):
        self.object_id = object_id
        self.name = name
        self.is_directory = is_directory
        self.parent = parent
        self.children: list[Node] = (
            children if children else [] if is_directory else None
        )
        self.index = 1

    def add_child(self, child_node: Node):
        """Add a child node to the current node.

        Args:
            child_node (Node): The child node to add.

        Raises:
            ValueError: If the current node is not a directory.
        """
        if not self.is_directory:
            raise ValueError("Cannot add child to a file node")

        child_node.parent = self
        child_node.index = len(self.children) + 1

        if self.children is None:
            self.children = [child_node]
        else:
            self.children.append(child_node)

    def __repr__(self) -> str:
        """Return a string representation of the node.

        Returns:
            str: A string representation of the node.
        """
        result = (
            f"Node(object_id={self.object_id}, name={self.name}, is_directory={self.is_directory}, "
            f"parent={self.parent.name if self.parent else None})"
        )
        if self.is_directory and self.children:
            for child in self.children:
                child_repr = str(
                    child
                )  # This will recursively call __repr__ on children
                child_lines = child_repr.split("\n")
                result += "\n" + "\n".join("    " + line for line in child_lines)
        return result

    def find_by_object_id(self, object_id: str) -> Node | None:
        """Find a node by its object ID.

        Args:
            object_id (str): The object ID to find.

        Returns:
            Node | None: The node with the given object ID, or None if it is not found.
        """
        if self.object_id == object_id:
            return self
        if self.is_directory and self.children:
            for child in self.children:
                found = child.find_by_object_id(object_id)
                if found is not None:
                    return found

        return None

    def find_path_by_object_id(self, object_id: str) -> str | None:
        """Find the path to a node by its object ID.

        Args:
            object_id (str): The object ID to find.

        Returns:
            str | None: The path to the node with the given object ID, or None if it is not found.
        """
        if self.object_id == object_id:
            return self.name
        if self.is_directory and self.children:
            for child in self.children:
                found = child.find_path_by_object_id(object_id)
                if found is not None:
                    return f"{self.name}/{found}"
        return None

    def find_by_name(self, name: str) -> Node | None:
        """Find a node by its name.

        Args:
            name (str): The name to find.

        Returns:
            Node | None: The node with the given name, or None if it is not found.
        """
        if self.is_directory and self.children:
            for child in self.children:
                found = child.find_by_name(name)
                if found is not None:
                    return found
        return None

    def find_path_by_name(self, name: str) -> str | None:
        """Find the path to a node by its name.

        Args:
            name (str): The name to find.

        Returns:
            str | None: The path to the node with the given name, or None if it is not found.
        """
        if self.is_directory and self.children:
            for child in self.children:
                found = child.find_path_by_name(name)
                if found is not None:
                    return f"{self.name}/{found}"
        return None

    def print_pretty(self, *, indent: int = 0, include_leaf_node: bool = False):
        """Print the node in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        if include_leaf_node:
            indent_space = ""
            if self.parent:
                if indent > 1:
                    indent_space = "    " * (indent - 1)
                else:
                    indent_space = ""
            else:
                indent_space = ""
            prefix = "└── " if self.parent else ""
            display_name = Path(self.name).name

            print(
                indent_space
                + prefix
                + display_name
                + ("/" if self.is_directory else "")
            )

            if self.is_directory and self.children:
                for child in self.children:
                    child.print_pretty(
                        indent=indent + 1, include_leaf_node=include_leaf_node
                    )
        else:
            if self.is_directory:
                indent_space = ""
                if self.parent:
                    if indent > 1:
                        indent_space = "    " * (indent - 1)
                    else:
                        indent_space = ""
                else:
                    indent_space = ""
                prefix = "└── " if self.parent else ""
                display_name = Path(self.name).name

                print(
                    indent_space
                    + prefix
                    + display_name
                    + ("/" if self.is_directory else "")
                )

                if self.is_directory and self.children:
                    for child in self.children:
                        child.print_pretty(
                            indent=indent + 1, include_leaf_node=include_leaf_node
                        )

    def create_directory(self) -> None:
        """Create directories recursively from root node to leaf nodes.
        Only creates directories for nodes where is_directory=True.
        """
        if self.is_directory:
            # Build full path by traversing up to root
            path_parts = []
            current = self
            while current:
                path_parts.append(current.name)
                current = current.parent

            # Reverse to get correct order from root to current
            full_path = Path(*reversed(path_parts))
            full_path.mkdir(parents=True, exist_ok=True)

            # Recursively create directories for children
            if self.children:
                for child in self.children:
                    if child.is_directory:
                        child.create_directory()
