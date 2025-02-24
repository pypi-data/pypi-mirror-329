# Parsdantic

Parsdantic is a powerful Python package that automatically generates Pydantic models from JSON schemas. It simplifies the process of data validation and serialization by bridging the gap between JSON Schema and Pydantic.
Features

## Features

- Convert JSON schemas to Pydantic models with a single function call
- Support for nested objects and complex data structures
- Automatic type inference and validation

## Installation

You can install Parsdantic using pip:

```bash
pip install parsdantic
```

## Quick Start
Here's a simple example of how to use Parsdantic:

```python
from parsdantic.parser import parse

schema = {
    "$defs": {
        "Person": {
            "properties": {
                "id": {"title": "Id", "type": "integer"},
                "name": {"title": "Name", "type": "string"},
                "directions": {
                    "items": {"type": "string"},
                    "title": "Directions",
                    "type": "array"
                }
            },
            "required": ["id", "name", "directions"],
            "title": "Person",
            "type": "object"
        }
    },
    "properties": {
        "people": {
            "items": {"$ref": "#/$defs/Person"},
            "title": "People",
            "type": "array"
        }
    },
    "required": ["people"],
    "title": "People",
    "type": "object"
}

People = parse(schema)

instance = People(
    people=[
        {"id": 1, "name": "John", "directions": ["Carrer de les Corts, 1", "Barcelona"]},
        {"id": 2, "name": "Jane", "directions": ["Carrer de les Corts, 2", "Barcelona"]},
    ]
)

print(instance) # People(people=[Person(id=1, name='John', directions=['Carrer de les Corts, 1', 'Barcelona']), Person(id=2, name='Jane', directions=['Carrer de les Corts, 2', 'Barcelona'])])
```
_Note: descriptions, default values, required fields, and Enum types are still not supported._
## Support
You can open an issue on the [GitHub issue tracker](https://github.com/SergiFuster/parsdantic/issues).


## LICENSE
This project is licensed under the MIT License. See the [LICENSE](https://github.com/SergiFuster/parsdantic/blob/main/LICENSE) file for details.