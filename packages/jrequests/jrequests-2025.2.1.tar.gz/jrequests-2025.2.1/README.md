# jrequests

jrequests is a fluent Python library aiming to replicate the following:
- Java's Jackson-like REST response to objects deserialization

The library is implemented with type safety in mind.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install jrequests.

```bash
pip install jrequests
```

## Usage
**jrequests** maps API call responses to objects or list of objects of the same type. It is based on the **requests** library and supports all parameters supported by the **requests** library. Currently, **jrequests** only supports the first level of objects, so stacked objects will instead be treated as dicts.

**jrequests** supports 3 types of data injection:
- direct attribute injection (works only with public attributes)
- dataclass fields injection (works with dataclasses with the restriction that all dataclass needs to have a no argument constructor)
- setter injection (works with classes that use methods such as 'setValue' or 'set_value' for the named fields parameters)

### Getting a single object from an API call
```python
from dataclasses import field, dataclass
from typing import Any, Optional
from jrequests import RequestBuilder, RequestMethod


@dataclass
class DeviceData:
    # Important to note that in order for the libary to instantiate, then set the values properly,
    # there needs to be a no argument constructor
    id: Optional[str] = field(init=False)
    name: Optional[str] = field(init=False)
    data: Optional[dict[Any, Any]] = field(init=False)


def main() -> None:
    response = (
        RequestBuilder(RequestMethod.GET, "https://api.restful-api.dev/objects/1")
        .withRetries(3)
        .withHeaders({"Content-Type": "application/json"})
        .execute()
        .getObject(DeviceData)
    )
    print(f"Device ID: {response.id}")
    print(f"Device Name: {response.name}")
    print(f"Device Data: {response.data}")


if __name__ == "__main__":
    main()
```

### Getting a list of objects from an API call
```python
from typing import Any, Optional
from jrequests import RequestBuilder, RequestMethod


class DeviceData:
    # Important to note that in order for the libary to instantiate, then set the values properly,
    # there needs to be a no argument constructor
    def __init__(self) -> None:
        self.__id: Optional[str] = None
        self.__name: Optional[str] = None
        self.__data: Optional[dict[Any, Any]] = None

    def setId(self, id: str) -> None:
        self.__id = id

    def getId(self) -> Optional[str]:
        return self.__id

    def setName(self, name: str) -> None:
        self.__name = name

    def getName(self) -> Optional[str]:
        return self.__name

    def setData(self, data: dict[Any, Any]) -> None:
        self.__data = data

    def getData(self) -> Optional[dict[Any, Any]]:
        return self.__data


def main() -> None:
    response = (
        RequestBuilder(RequestMethod.GET, "https://api.restful-api.dev/objects")
        .withRetries(3)
        .withHeaders({"Content-Type": "application/json"})
        .execute()
        .getList(DeviceData)
    )

    for elem in response:
        print(f"Device ID: {elem.getId()}")
        print(f"Device Name: {elem.getName()}")
        print(f"Device Data: {elem.getData()}")
        print("========")


if __name__ == "__main__":
    main()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)