def extract(schema_node, json_node):
    if (schema_node == {}) or (schema_node == []):
        # Base case - this JSON node does not need to be further destructured.
        return json_node
    if type(schema_node) is list:
        # Schema expects this JSON node to be a list - process children individually and collect results.
        assert len(schema_node) == 1, "List schema node can only contain 0 or 1 elements."
        assert type(json_node) is list, "Schema expected list, but JSON node was not list."
        schema_node = schema_node[0]
        return [extract(schema_node, item) for item in json_node]
    # Process this node as a dictionary.
    result = {}
    for key, schema_value in schema_node.items():
        result[key] = extract(schema_value, json_node[key])
    return result

