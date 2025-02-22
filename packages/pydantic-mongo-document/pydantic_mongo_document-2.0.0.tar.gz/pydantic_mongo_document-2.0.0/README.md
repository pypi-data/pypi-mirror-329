# Pydantic Mongo Document

`pydantic_mongo_document` is a Python library that provides a base class for creating MongoDB documents using Pydantic models.

## Installation

Install the package using [pip](https://pip.pypa.io/en/stable/) or [poetry](https://python-poetry.org).

### Using pip
```bash
pip install pydantic_mongo_document
```

### Using poetry
```bash
poetry add pydantic_mongo_document
```

Usage
To use pydantic_mongo_document, you need to create a Pydantic model that represents your MongoDB document and inherit from the MongoDocument class provided by the library. Here's an example:

```python3
from pydantic_mongo_document import Document

class User(Document):
    __collection__ = "users"
    __database__ = "production"

    name: str
    email: str

```

In this example, we define a User Pydantic Document model with two fields (name and email) and  
specifies the MongoDB collection name (users) and database name (production) using the `__collection__` and `__database__` class attributes.

```python3
from pydantic_mongo_document import Document


# Set the MongoDB replica configuration
Document.set_replica_config({"localhost": "mongodb://localhost:27017"})


class User(Document):
    __replica__ = "localhost"
    __collection__ = "users"
    __database__ = "production"

    name: str
    email: str


async def create_user():
    user = User(name="John", email="john@example.com")

    await user.insert()

    user = await User.one(add_query={"name": "John"})
    print(user)  # User(id=ObjectId("64fc59cf6410868c9a40644b"), name="John", email="john@example")
```

In this example, we created new User in database. We then used the `User.one` method to retrieve the user from the database.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT
