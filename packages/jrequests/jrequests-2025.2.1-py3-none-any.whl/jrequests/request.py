from enum import Enum
import json
from typing import Any, Callable, Mapping, MutableMapping, Optional, Union, TypeVar
import requests
from requests import PreparedRequest
from requests.auth import AuthBase


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


Cookies = MutableMapping[str, str]
Proxies = MutableMapping[str, str]
Certs = Union[str, tuple[str, str]]
Timeout = Union[float, tuple[float, float], tuple[float, None]]
Auth = Union[tuple[str, str], AuthBase, Callable[[PreparedRequest], PreparedRequest]]
Headers = Mapping[str, Union[str, bytes]]
T = TypeVar("T")


class _F:
    def mth(self) -> None:
        pass


MthType = type(_F().mth)


def isMth(var: Any) -> bool:
    """
    Checks if the given argument is either a function or a method in a class.

    Args:
        var (Any): The argument to check

    Returns:
        bool: True if var is a function or method, False otherwise
    """
    varType = type(var)
    return varType is MthType


class RestResponse:
    def __init__(self, response: requests.Response) -> None:
        self.__response = response

    def raiseForStatus(self) -> None:
        """
        Raises an exception, if possible, for the response status
        """
        self.__response.raise_for_status()

    def getResponseCode(self) -> int:
        """
        Returns the response code for the response.

        Returns:
            int: The status code
        """
        return self.__response.status_code

    def getReason(self) -> str:
        """
        Returns the failure reason from the response. In case there was no failure, the reason will be empty.

        Returns:
            str: _description_
        """
        return self.__response.reason

    def __setVal(self, obj: Any, attr: str, value: Any) -> None:
        attrUpper = attr[0].upper() + attr[1:]
        variants = [attr, "set_" + attr, "set" + attrUpper]
        for variant in variants:
            if hasattr(obj, variant):
                variantFn = getattr(obj, variant)
                if isMth(variantFn):
                    variantFn(value)
                    return
        # Try to set the attribute directly
        try:
            setattr(obj, attr, value)
        except Exception as _:
            # Ignore setattr exceptions since we might have a __slots__ object
            # On this kind of object, we only set the values that we can set.
            pass

    def getObject(
        self, typ: type[T], throwExceptionOnFailure: bool = False
    ) -> Optional[T]:
        """
        Maps the response to an object of the given type.

        Args:
            typ (type[T]): The type of object to be returned
            throwExceptionOnFailure (bool, optional): Flag determining the behavior of the exception handling. Defaults to False.

        Raises:
            ValueError: A value error
            e: Caught exception while parsing the rest response

        Returns:
            Optional[T]: The constructed object, or None if the parsing fails
        """
        content = self.__response.content
        try:
            obj = json.loads(content)
            if not isinstance(obj, dict):
                raise ValueError("Response object cannot be mapped to %s" % typ)
            constructedObj = typ()
            for key, value in obj.items():
                self.__setVal(constructedObj, key, value)
            return constructedObj
        except Exception as e:
            if throwExceptionOnFailure:
                raise e
            return None

    def getList(
        self, typ: type[T], throwExceptionOnFailure: bool = False
    ) -> Optional[list[T]]:
        content = self.__response.content
        try:
            obj = json.loads(content)
            if not isinstance(obj, list):
                raise ValueError(
                    "Response object cannot be mapped to a list of %s" % typ
                )
            objectList: list[T] = []
            for listItem in obj:
                if not isinstance(listItem, dict):
                    raise ValueError(
                        "Response object cannot be mapped to a list of %s" % typ
                    )
                constructedObj = typ()
                for key, value in listItem.items():
                    self.__setVal(constructedObj, key, value)
                objectList.append(constructedObj)
            return objectList
        except Exception as e:
            if throwExceptionOnFailure:
                raise e
            return None


class RequestBuilder:
    def __init__(self, method: RequestMethod, url: str) -> None:
        self.__method = method
        self.__url = url
        self.__body: Any = None
        self.__retries: int = 0
        self.__headers: Optional[Headers] = None
        self.__cookies: Optional[Cookies] = None
        self.__allowRedirects: bool = False
        self.__proxies: Optional[Proxies] = None
        self.__cert: Optional[Certs] = None
        self.__verify: Union[bool, str, None] = None
        self.__timeout: Optional[Timeout] = None

        self.__auth: Optional[Auth] = None

    def __raiseIfNone(self, param: Any, message: str) -> None:
        if param is None:
            raise Exception(message)

    def withBody(self, body: Any) -> "RequestBuilder":
        self.__body = body
        return self

    def withRetries(self, retries: int) -> "RequestBuilder":
        self.__retries = retries
        return self

    def withHeaders(self, headers: Headers) -> "RequestBuilder":
        self.__headers = headers
        return self

    def withCookies(self, cookies: Cookies) -> "RequestBuilder":
        self.__cookies = cookies
        return self

    def withAllowRedirects(self, allowRedirects: bool) -> "RequestBuilder":
        self.__allowRedirects = allowRedirects
        return self

    def withProxies(self, proxies: Proxies) -> "RequestBuilder":
        self.__proxies = proxies
        return self

    def withCert(self, cert: Certs) -> "RequestBuilder":
        self.__cert = cert
        return self

    def withVerify(self, verify: Union[bool, str]) -> "RequestBuilder":
        self.__verify = verify
        return self

    def __validate(self) -> None:
        if self.__retries < 0:
            raise Exception(
                "Number of retries cannot be lower than 0. %s provided" % self.__retries
            )
        match self.__method:
            case RequestMethod.PUT:
                self.__raiseIfNone(
                    self.__body, "Request body cannot be None for PUT requests"
                )
                return
            case RequestMethod.POST:
                self.__raiseIfNone(
                    self.__body, "Request body cannot be None for POST requests"
                )
                return
            case RequestMethod.PATCH:
                self.__raiseIfNone(
                    self.__body, "Request body cannot be None for POST requests"
                )
                return

    def __callRetryable(self) -> requests.Response:
        if self.__retries == 0:
            return self.__callRequest()
        currentTry = 0
        lastException: Optional[Exception] = None
        while currentTry < self.__retries:
            try:
                return self.__callRequest()
            except Exception as ex:
                currentTry += 1
                lastException = ex
        if lastException is not None:
            raise lastException
        raise Exception("Unexpected exception ocurred while retrying call")

    def __callRequest(self) -> requests.Response:
        match self.__method:
            case RequestMethod.GET:
                return requests.get(
                    self.__url,
                    data=json.dumps(self.__body) if self.__body is not None else None,
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.POST:
                return requests.post(
                    self.__url,
                    data=json.dumps(self.__body),
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.DELETE:
                return requests.delete(
                    self.__url,
                    data=json.dumps(self.__body) if self.__body is not None else None,
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.PUT:
                return requests.put(
                    self.__url,
                    data=json.dumps(self.__body),
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.HEAD:
                return requests.head(
                    self.__url,
                    data=json.dumps(self.__body) if self.__body is not None else None,
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.OPTIONS:
                return requests.head(
                    self.__url,
                    data=json.dumps(self.__body) if self.__body is not None else None,
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )
            case RequestMethod.PATCH:
                return requests.head(
                    self.__url,
                    data=json.dumps(self.__body),
                    headers=self.__headers,
                    cookies=self.__cookies,
                    allow_redirects=self.__allowRedirects,
                    proxies=self.__proxies,
                    cert=self.__cert,
                    verify=self.__verify,
                    timeout=self.__timeout,
                    auth=self.__auth,
                )

    def execute(self) -> RestResponse:
        self.__validate()
        return RestResponse(self.__callRetryable())
