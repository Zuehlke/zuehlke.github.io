import unittest

import github_response_parser


class TestGithubResponseParser(unittest.TestCase):

    def test__parse_response_item_single_key__should_select_all(self):
        schema = {
            "name": {}
        }
        response_item = {
            "name": "Jon Doe"
        }
        expected = {
            "name": "Jon Doe"
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__two_keys__should_ignore_second(self):
        schema = {
            "name": {}
        }
        response_item = {
            "name": "Jon Doe",
            "age": 42
        }
        expected = {
            "name": "Jon Doe"
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_one_level__should_implicitly_select_all(self):
        schema = {
            "id": {},
            "person": {}
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_one_level__empty_schema__should_implicitly_select_all(self):
        schema = {}
        response_item = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_one_level__should_explicitly_select_all(self):
        schema = {
            "id": {},
            "person": {
                "name": {},
                "age": {}
            }
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_one_level__should_ignore_person_age(self):
        schema = {
            "id": {},
            "person": {
                "name": {}
            }
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": "Jon Doe",
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": "Jon Doe"
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_two_levels__should_implicitly_empty_schema__should_select_all(self):
        schema = {}
        response_item = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_two_levels__should_explicitly_select_all(self):
        schema = {
            "id": {},
            "person": {
                "name": {
                    "first": {},
                    "last": {}
                },
                "age": {}
            }
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_two_levels__should_implicitly_select_full_name(self):
        schema = {
            "id": {},
            "person": {
                "name": {},
                "age": {}
            }
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_two_levels__should_implicitly_select_full_person(self):
        schema = {
            "id": {},
            "person": {}
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        expected = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__nested_two_levels__should_ignore_id_age_lastname(self):
        schema = {
            "person": {
                "name": {
                    "first": {}
                }
            }
        }
        response_item = {
            "id": "1234",
            "person": {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            }
        }
        expected = {
            "person": {
                "name": {
                    "first": "Jon"
                }
            }
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)
