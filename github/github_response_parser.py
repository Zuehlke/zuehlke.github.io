def parse_response_item(schema, response_item):
    if (schema == {}) or (schema == []):
        # Base case - this response item does not need to be further destructured.
        return response_item
    if type(schema) is list:
        # Schema expects this node to be a list - process children individually and collect results.
        assert len(schema) == 1, "List schema node can only contain 0 or 1 elements."
        assert type(response_item) is list, "Schema expected list, but response item was not list."
        schema = schema[0]
        return [parse_response_item(schema, item) for item in response_item]
    # Process this item as a dictionary.
    result = {}
    for key, schema_value in schema.items():
        result[key] = parse_response_item(schema_value, response_item[key])
    return result
