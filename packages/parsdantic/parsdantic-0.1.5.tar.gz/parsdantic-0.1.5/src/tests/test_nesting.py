import pytest

from src.parsdantic.parser import parse


@pytest.mark.parametrize(
    "data, json_schema, expected",
    [
        (
            {"id": 1, "name": "name"},
            {"type": "object", "title" : "test", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
            True
        ),
        (
            {"id": 1, "name": "name", "obj": {"id": 2, "name": "name"}},
            {
                "type": "object",
                "title" : "test",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "obj": {
                        "title" : "test",
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"}
                        }
                    }
                }
            },
            True
        ),
        (
            {"id": 1, "name": "name", "obj": {"id": 2, "name": "name", "obj": {"id": 3, "name": "name"}}},
            {
                "type": "object",
                "title" : "test",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "obj": {
                        "title" : "test",
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "obj": {
                                "title" : "test",
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "name": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            True
        ),
    ]
)
def test_nested(data, json_schema, expected):
    try:
        pydantic_model = parse(json_schema)
        instance = pydantic_model(**data)
        pydantic_model.model_validate(instance)
        assert expected
    except Exception:
        assert not expected

