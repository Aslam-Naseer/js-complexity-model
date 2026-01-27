def flatten_functions(nodes, parent_name=""):
    """
    Recursively yields every function node from the tree.
    Also constructs the full name (e.g., 'foo.bar').
    """
    for node in nodes:
        current_name = f"{parent_name}.{node['name']}" if parent_name else node['name']

        node_with_context = {**node, "full_name": current_name}
        yield node_with_context

        if 'nestedFunctions' in node and node['nestedFunctions']:
            yield from flatten_functions(node['nestedFunctions'], current_name)
