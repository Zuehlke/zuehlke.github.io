def reduce(schema_node, json_node):
    """
    Reduce a given JSON node (object or array) according to a given schema. Does not filter or transform
    the node. For more information on the expected schema, refer to the "JSON Reducer DSL" section in
    the README for the GitHub automation. For examples, refer to "test/test_json_reducer.py".
    :param schema_node: schema defining the expected reduction
    :param json_node: JSON node (object or array) to be reduced
    :return: JSON node reduced according to given schema
    """
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

