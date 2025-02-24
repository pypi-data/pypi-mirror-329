import pytest

from ..parsdantic.parser import parse


@pytest.mark.parametrize(
    "data, json_schema, expected",
    [
        (
            {"id": 1, "names": ["name1", "name2"]},
            {"type": "object", "title" : "test", "properties": {"id": {"type": "integer"}, "names": {"type": "array", "items": {"type": "string"}}}},
            True
        ),
        (
            {"id": 1, "names": [["name1", "name2"], ["name3", "name4"]]},
            {"type": "object", "title" : "test", "properties": {"id": {"type": "integer"}, "names": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}}},
            True
        ),
    ]
)
def test_list(data, json_schema, expected):
    try:
        pydantic_model = parse(json_schema)
        instance = pydantic_model(**data)
        pydantic_model.model_validate(instance)
        assert expected
    except Exception:
        assert not expected

