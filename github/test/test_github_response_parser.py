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

    def test__parse_response_item__root_list__no_schema__should_select_all(self):
        schema = []
        response_item = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        expected = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__root_list__should_explicitly_select_all(self):
        schema = [{
            "name": {}
        }]
        response_item = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        expected = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__root_list__nested_elements__should_ignore_age_lastname(self):
        schema = [{
            "name": {
                "first": {}
            }
        }]
        response_item = [
            {
                "name": {
                    "first": "Jon",
                    "last": "Doe"
                },
                "age": 42
            },
            {
                "name": {
                    "first": "Jane",
                    "last": "Doe"
                },
                "age": 85
            }
        ]
        expected = [
            {
                "name": {
                    "first": "Jon"
                },
            },
            {
                "name": {
                    "first": "Jane"
                }
            }
        ]
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__child_list__nested_elements__should_ignore_list(self):
        schema = {
            "id": {},
            "title": {}
        }
        response_item = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        expected = {
            "id": "1234",
            "title": "hello-world"
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__child_list__nested_elements__should_implicitly_select_full_items(self):
        schema = {
            "id": {},
            "title": {},
            "contributors": []
        }
        response_item = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        expected = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__child_list__nested_elements__should_explicitly_select_full_items(self):
        schema = {
            "id": {},
            "title": {},
            "contributors": [{
                "id": {},
                "login": {}
            }]
        }
        response_item = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        expected = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__child_list__nested_elements__should_ignore_title_login(self):
        schema = {
            "id": {},
            "contributors": [{
                "id": {}
            }]
        }
        response_item = {
            "id": "1234",
            "title": "hello-world",
            "contributors": [
                {
                    "id": "1111",
                    "login": "jondoe"
                },
                {
                    "id": "2222",
                    "login": "janedoe"
                }
            ]
        }
        expected = {
            "id": "1234",
            "contributors": [
                {
                    "id": "1111",
                },
                {
                    "id": "2222",
                }
            ]
        }
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)

    def test__parse_response_item__complex_nested_objects_and_lists(self):
        schema = [{
            "id": {},
            "title": {},
            "contributors": [
                {
                    "id": {},
                    "repos": [
                        {
                            "id": {}
                        }
                    ]
                }
            ]
        }]
        response_item = [
            {
                "id": "1234",
                "title": "hello-world",
                "contributors": [
                    {
                        "id": "1111",
                        "login": "jondoe",
                        "repos": [
                            {
                                "id": "1234",
                                "title": "hello-world"
                            },
                            {
                                "id": "5678",
                                "title": "hello-earth"
                            }
                        ]
                    },
                    {
                        "id": "2222",
                        "login": "janedoe",
                        "repos": [
                            {
                                "id": "1234",
                                "title": "hello-world"
                            }
                        ]
                    },
                ],
                "stargazers_count": 42
            },
            {
                "id": "9876",
                "title": "project1",
                "contributors": [
                    {
                        "id": "3333",
                        "login": "tommytest",
                        "repos": [
                            {
                                "id": "9876",
                                "title": "project1"
                            }
                        ]
                    },
                ],
                "stargazers_count": 2344
            }
        ]
        expected = [
            {
                "id": "1234",
                "title": "hello-world",
                "contributors": [
                    {
                        "id": "1111",
                        "repos": [
                            {
                                "id": "1234"
                            },
                            {
                                "id": "5678"
                            }
                        ]
                    },
                    {
                        "id": "2222",
                        "repos": [
                            {
                                "id": "1234"
                            }
                        ]
                    },
                ]
            },
            {
                "id": "9876",
                "title": "project1",
                "contributors": [
                    {
                        "id": "3333",
                        "repos": [
                            {
                                "id": "9876"
                            }
                        ]
                    },
                ]
            }
        ]
        actual = github_response_parser.parse_response_item(schema, response_item)
        self.assertEqual(expected, actual)
