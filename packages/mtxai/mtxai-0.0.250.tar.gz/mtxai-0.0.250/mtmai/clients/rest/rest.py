# coding: utf-8

"""
Mtmai API

The Mtmai API

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""  # noqa: E501

import io
import json
import re
import ssl
from typing import Optional, Union

import aiohttp
import aiohttp_retry
from mtmai.clients.rest.exceptions import ApiException, ApiValueError

RESTResponseType = aiohttp.ClientResponse

ALLOW_RETRY_METHODS = frozenset({"DELETE", "GET", "HEAD", "OPTIONS", "PUT", "TRACE"})


class RESTResponse(io.IOBase):
    def __init__(self, resp) -> None:
        self.response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = None

    async def read(self):
        if self.data is None:
            self.data = await self.response.read()
        return self.data

    def getheaders(self):
        """Returns a CIMultiDictProxy of the response headers."""
        return self.response.headers

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.response.headers.get(name, default)


class RESTClientObject:
    def __init__(self, configuration) -> None:
        # maxsize is number of requests to host that are allowed in parallel
        self.maxsize = configuration.connection_pool_maxsize

        self.ssl_context = ssl.create_default_context(cafile=configuration.ssl_ca_cert)
        if configuration.cert_file:
            self.ssl_context.load_cert_chain(
                configuration.cert_file, keyfile=configuration.key_file
            )

        if not configuration.verify_ssl:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

        self.proxy = configuration.proxy
        self.proxy_headers = configuration.proxy_headers

        self.retries = configuration.retries

        self.pool_manager: Optional[aiohttp.ClientSession] = None
        self.retry_client: Optional[aiohttp_retry.RetryClient] = None

    async def close(self) -> None:
        if self.pool_manager:
            await self.pool_manager.close()
        if self.retry_client is not None:
            await self.retry_client.close()

    async def request(
        self,
        method,
        url,
        headers=None,
        body=None,
        post_params=None,
        _request_timeout=None,
    ):
        """Execute request

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH", "OPTIONS"]

        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}
        # url already contains the URL query string
        timeout = _request_timeout or 5 * 60

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        args = {"method": method, "url": url, "timeout": timeout, "headers": headers}

        if self.proxy:
            args["proxy"] = self.proxy
        if self.proxy_headers:
            args["proxy_headers"] = self.proxy_headers

        # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
        if method in ["POST", "PUT", "PATCH", "OPTIONS", "DELETE"]:
            if re.search("json", headers["Content-Type"], re.IGNORECASE):
                if body is not None:
                    body = json.dumps(body)
                args["data"] = body
            elif headers["Content-Type"] == "application/x-www-form-urlencoded":
                args["data"] = aiohttp.FormData(post_params)
            elif headers["Content-Type"] == "multipart/form-data":
                # must del headers['Content-Type'], or the correct
                # Content-Type which generated by aiohttp
                del headers["Content-Type"]
                data = aiohttp.FormData()
                for param in post_params:
                    k, v = param
                    if isinstance(v, tuple) and len(v) == 3:
                        data.add_field(k, value=v[1], filename=v[0], content_type=v[2])
                    else:
                        # Ensures that dict objects are serialized
                        if isinstance(v, dict):
                            v = json.dumps(v)
                        elif isinstance(v, int):
                            v = str(v)
                        data.add_field(k, v)
                args["data"] = data

            # Pass a `bytes` or `str` parameter directly in the body to support
            # other content types than Json when `body` argument is provided
            # in serialized form
            elif isinstance(body, str) or isinstance(body, bytes):
                args["data"] = body
            else:
                # Cannot generate the request from given parameters
                msg = """Cannot prepare a request message for provided
                         arguments. Please check that your arguments match
                         declared content type."""
                raise ApiException(status=0, reason=msg)

        pool_manager: Union[aiohttp.ClientSession, aiohttp_retry.RetryClient]

        # https pool manager
        if self.pool_manager is None:
            self.pool_manager = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=self.maxsize, ssl=self.ssl_context
                ),
                trust_env=True,
            )
        pool_manager = self.pool_manager

        if self.retries is not None and method in ALLOW_RETRY_METHODS:
            if self.retry_client is None:
                self.retry_client = aiohttp_retry.RetryClient(
                    client_session=self.pool_manager,
                    retry_options=aiohttp_retry.ExponentialRetry(
                        attempts=self.retries,
                        factor=2.0,
                        start_timeout=0.1,
                        max_timeout=120.0,
                    ),
                )
            pool_manager = self.retry_client

        r = await pool_manager.request(**args)

        return RESTResponse(r)
