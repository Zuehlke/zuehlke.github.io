def reduce(schema_node, json_node):
    if (schema_node == {}) or (schema_node == []):
        # Base case - this JSON node does not need to be further reduced.
        return json_node
    if type(schema_node) is list:
        # Schema expects this JSON node to be a list - reduce children individually and collect results.
        assert len(schema_node) == 1, "List schema node can only contain 0 or 1 elements."
        assert type(json_node) is list, "Schema expected list, but JSON node was not list."
        schema_node = schema_node[0]
        return [reduce(schema_node, item) for item in json_node]
    # Process this node as a dictionary.
    result = {}
    for key, schema_value in schema_node.items():
        result[key] = reduce(schema_value, json_node[key])
    return result

