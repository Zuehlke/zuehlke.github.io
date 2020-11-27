import unittest

import json_reducer


class TestJsonReducer(unittest.TestCase):

    def test__reduce_single_key__should_select_all(self):
        schema = {
            "name": {}
        }
        json_node = {
            "name": "Jon Doe"
        }
        expected = {
            "name": "Jon Doe"
        }
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__two_keys__should_ignore_second(self):
        schema = {
            "name": {}
        }
        json_node = {
            "name": "Jon Doe",
            "age": 42
        }
        expected = {
            "name": "Jon Doe"
        }
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_one_level__should_implicitly_select_all(self):
        schema = {
            "id": {},
            "person": {}
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_one_level__empty_schema__should_implicitly_select_all(self):
        schema = {}
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_one_level__should_explicitly_select_all(self):
        schema = {
            "id": {},
            "person": {
                "name": {},
                "age": {}
            }
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_one_level__should_ignore_person_age(self):
        schema = {
            "id": {},
            "person": {
                "name": {}
            }
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_two_levels__should_implicitly_empty_schema__should_select_all(self):
        schema = {}
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_two_levels__should_explicitly_select_all(self):
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
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_two_levels__should_implicitly_select_full_name(self):
        schema = {
            "id": {},
            "person": {
                "name": {},
                "age": {}
            }
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_two_levels__should_implicitly_select_full_person(self):
        schema = {
            "id": {},
            "person": {}
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__nested_two_levels__should_ignore_id_age_lastname(self):
        schema = {
            "person": {
                "name": {
                    "first": {}
                }
            }
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__root_list__no_schema__should_select_all(self):
        schema = []
        json_node = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        expected = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__root_list__should_explicitly_select_all(self):
        schema = [{
            "name": {}
        }]
        json_node = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        expected = [
            {"name": "Jon Doe"},
            {"name": "Jane Doe"}
        ]
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__root_list__nested_elements__should_ignore_age_lastname(self):
        schema = [{
            "name": {
                "first": {}
            }
        }]
        json_node = [
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__child_list__nested_elements__should_ignore_list(self):
        schema = {
            "id": {},
            "title": {}
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__child_list__nested_elements__should_implicitly_select_full_items(self):
        schema = {
            "id": {},
            "title": {},
            "contributors": []
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__child_list__nested_elements__should_explicitly_select_full_items(self):
        schema = {
            "id": {},
            "title": {},
            "contributors": [{
                "id": {},
                "login": {}
            }]
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__child_list__nested_elements__should_ignore_title_login(self):
        schema = {
            "id": {},
            "contributors": [{
                "id": {}
            }]
        }
        json_node = {
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)

    def test__reduce__complex_nested_objects_and_lists(self):
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
        json_node = [
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
        actual = json_reducer.reduce(schema, json_node)
        self.assertEqual(expected, actual)
