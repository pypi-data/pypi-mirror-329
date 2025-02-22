from dataclasses import dataclass, field
from typing import Any, Optional
import unittest
from jrequests.request import RestResponse


class MockResponse:
    def __init__(self, response: Any) -> None:
        self.content = response


@dataclass
class MockObject:
    field1: str = field(init=False)
    field2: bool = field(init=False)
    field3: int = field(init=False)


class MockObjectPlain:
    def __init__(self) -> None:
        self.field1: Optional[str] = None
        self.field2: Optional[bool] = None
        self.field3: Optional[int] = None


class MockObjectSetters:
    def __init__(self) -> None:
        self.__field1: Optional[str] = None
        self.__field2: Optional[bool] = None
        self.__field3: Optional[int] = None
        self.__complexStringName: Optional[str] = None

    def setField1(self, value: str) -> None:
        self.__field1 = value

    def setField2(self, value: bool) -> None:
        self.__field2 = value

    def setField3(self, value: int) -> None:
        self.__field3 = value

    def setComplexStringName(self, value: str) -> None:
        self.__complexStringName = value

    def getField1(self) -> Optional[str]:
        return self.__field1

    def getField2(self) -> Optional[bool]:
        return self.__field2

    def getField3(self) -> Optional[int]:
        return self.__field3

    def getComplexStringName(self) -> Optional[str]:
        return self.__complexStringName


class MockObjectSettersUnder:
    def __init__(self) -> None:
        self.__field1: Optional[str] = None
        self.__field2: Optional[bool] = None
        self.__field3: Optional[int] = None

    def set_field1(self, value: str) -> None:
        self.__field1 = value

    def set_field2(self, value: bool) -> None:
        self.__field2 = value

    def set_field3(self, value: int) -> None:
        self.__field3 = value

    def get_field1(self) -> Optional[str]:
        return self.__field1

    def get_field2(self) -> Optional[bool]:
        return self.__field2

    def get_field3(self) -> Optional[int]:
        return self.__field3


class MockObjectProperty:
    def __init__(self) -> None:
        self.__field1: Optional[str] = None
        self.__field2: Optional[bool] = None
        self.__field3: Optional[int] = None

    @property
    def field1(self) -> Optional[str]:
        return self.__field1

    @field1.setter
    def field1(self, value: str) -> None:
        self.__field1 = value

    @property
    def field2(self) -> Optional[bool]:
        return self.__field2

    @field2.setter
    def field2(self, value: bool) -> None:
        self.__field2 = value

    @property
    def field3(self) -> Optional[int]:
        return self.__field3

    @field3.setter
    def field3(self, value: int) -> None:
        self.__field3 = value


class TestRestResponse(unittest.TestCase):
    def test_response_object_dataclass(self) -> None:
        response = MockResponse('{"field1": "value1", "field2": true, "field3": 1}')
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObject)
        self.assertTrue(
            isinstance(obj, MockObject), "Returned object should have correct type"
        )
        self.assertEqual(obj.field1, "value1", "Field should have correct value")
        self.assertEqual(obj.field2, True, "Field should have correct value")
        self.assertEqual(obj.field3, 1, "Field should have correct value")

    def test_response_object_plain(self) -> None:
        response = MockResponse('{"field1": "value1", "field2": true, "field3": 1}')
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObjectPlain)
        self.assertTrue(
            isinstance(obj, MockObjectPlain), "Returned object should have correct type"
        )
        self.assertEqual(obj.field1, "value1", "Field should have correct value")
        self.assertEqual(obj.field2, True, "Field should have correct value")
        self.assertEqual(obj.field3, 1, "Field should have correct value")

    def test_response_object_setters(self) -> None:
        response = MockResponse('{"field1": "value1", "field2": true, "field3": 1}')
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObjectSetters)
        self.assertTrue(
            isinstance(obj, MockObjectSetters),
            "Returned object should have correct type",
        )
        self.assertEqual(obj.getField1(), "value1", "Field should have correct value")
        self.assertEqual(obj.getField2(), True, "Field should have correct value")
        self.assertEqual(obj.getField3(), 1, "Field should have correct value")

    def test_response_object_setters_complex(self) -> None:
        response = MockResponse(
            '{"field1": "value1", "field2": true, "field3": 1, "complexStringName": "test"}'
        )
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObjectSetters)
        self.assertTrue(
            isinstance(obj, MockObjectSetters),
            "Returned object should have correct type",
        )
        self.assertEqual(obj.getField1(), "value1", "Field should have correct value")
        self.assertEqual(obj.getField2(), True, "Field should have correct value")
        self.assertEqual(obj.getField3(), 1, "Field should have correct value")
        self.assertEqual(
            obj.getComplexStringName(), "test", "Field should have correct value"
        )

    def test_response_object_setters_under(self) -> None:
        response = MockResponse('{"field1": "value1", "field2": true, "field3": 1}')
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObjectSettersUnder)
        self.assertTrue(
            isinstance(obj, MockObjectSettersUnder),
            "Returned object should have correct type",
        )
        self.assertEqual(obj.get_field1(), "value1", "Field should have correct value")
        self.assertEqual(obj.get_field2(), True, "Field should have correct value")
        self.assertEqual(obj.get_field3(), 1, "Field should have correct value")

    def test_response_object_property(self) -> None:
        response = MockResponse('{"field1": "value1", "field2": true, "field3": 1}')
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObjectProperty)
        self.assertTrue(
            isinstance(obj, MockObjectProperty),
            "Returned object should have correct type",
        )
        self.assertEqual(obj.field1, "value1", "Field should have correct value")
        self.assertEqual(obj.field2, True, "Field should have correct value")
        self.assertEqual(obj.field3, 1, "Field should have correct value")

    def test_response_object_with_more_fields_than_necessary(self) -> None:
        response = MockResponse(
            '{"field1": "value1", "field2": true, "field3": 1, "field4": {}}'
        )
        restResponse = RestResponse(response)
        obj = restResponse.getObject(MockObject)
        self.assertTrue(
            isinstance(obj, MockObject), "Returned object should have correct type"
        )
        self.assertEqual(obj.field1, "value1", "Field should have correct value")
        self.assertEqual(obj.field2, True, "Field should have correct value")
        self.assertEqual(obj.field3, 1, "Field should have correct value")
        self.assertEqual(obj.field4, {}, "Field should have correct value")

    def test_response_list(self) -> None:
        response = MockResponse('[{"field1": "value1", "field2": true, "field3": 1}]')
        restResponse = RestResponse(response)
        obj = restResponse.getList(MockObject)
        self.assertTrue(
            isinstance(obj, list),
            "Returned object should have correct type",
        )
        self.assertEqual(len(obj), 1, "List should contain 1 element")
        self.assertEqual(obj[0].field1, "value1", "Field should have correct value")
        self.assertEqual(obj[0].field2, True, "Field should have correct value")
        self.assertEqual(obj[0].field3, 1, "Field should have correct value")
