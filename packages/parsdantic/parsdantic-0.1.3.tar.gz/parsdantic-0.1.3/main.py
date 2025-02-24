from pprint import pp

from src.parsdantic.parser import parse

schema = {
    "$defs": {
        "Color": {
            "properties": {
                "id" : {"title": "ID", "type": "integer"},
                "r": {"title": "R", "type": "integer"},
                "g": {"title": "G", "type": "integer"},
                "b": {"title": "B", "type": "integer"},
            },
            "required": ["r", "g", "b"],
            "title": "Color",
            "type": "object",
        },
        "Hair": {
            "properties": {"id" : {"title": "ID", "type": "integer"}, "color": {"$ref": "#/$defs/Color"}},
            "required": ["color"],
            "title": "Hair",
            "type": "object",
        },
    },
    "properties": {
        "id" : {"title": "ID", "type": "integer"},
        "name": {"title": "Name", "type": "string"},
        "age": {"title": "Age", "type": "integer"},
        "hair": {"$ref": "#/$defs/Hair"},
    },
    "required": ["name", "age", "hair"],
    "title": "Person",
    "type": "object",
}

pydantic_model = parse(schema)

data = {
    "name": "John",
    "age": 30,
    "hair": {"color": {"r": 255, "g": 0, "b": 0}},
}

person = pydantic_model.model_validate(data)

pp(person.model_json_schema())