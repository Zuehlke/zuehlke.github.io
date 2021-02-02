# GitHub Automation
## Usage
- Run `pip install -r requirements.txt` (preferably in a `virtualenv` environment) from within this directory to
  install the required dependencies.
- Run `main.py` with Python 3, and with the required GitHub API token environment variable set.

### Example Usage
```
GITHUB_PAT=<PAT_PUBLIC> OUTPUT_DATA_DIR=<some_dir> EXTERNAL_CONTRIBUTIONS_FILE=<path_to_external_contributions.csv> python3 src/main.py
```

## JSON Reducer DSL
API responses usually contain much more information than we need for our data files. The `json_reducer` helps reduce
JSON payloads to only the fields we are interested in. A call to `json_reducer.reduce()` takes two arguments: a schema
node, and a JSON node (array or object) to be reduced. The schema follows a small DSL with the following rules:
- The schema is a nested Python dictionary which has the same structure as the JSON node to be reduced.
- If a JSON child node has no corresponding node in the schema, it is discarded in the output.
- The value `{}` defines a base case in the schema, and implies that the corresponding JSON value or child node should
  be fully included in the output without further reduction.
- Arrays in the schema can either be empty or contain exactly one object.
- The value `[]` defines another base case in the schema and implies that the contents of the corresponding JSON array
  should be fully included in the output without further reduction.
- An array containing an object in the schema implies that all elements of the corresponding JSON array should be
  reduced to the structure defined by that object.

For examples, refer to `github/test/test_json_reducer.py`.
