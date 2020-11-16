def parse_response_item(schema, response_item):
    if schema == {}:
        # Base case - this response item does not need to be further destructured.
        return response_item
    result = {}
    for key, schema_value in schema.items():
        result[key] = parse_response_item(schema_value, response_item[key])
    return result


def parse_response_item_array(schema, response_array):
    result = {}
    for response_item in response_array:
        parsed_item = parse_response_item(schema, response_item)
        result[parsed_item["id"]] = parsed_item
    return result
