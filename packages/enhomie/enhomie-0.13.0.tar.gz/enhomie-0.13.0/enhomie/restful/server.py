"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from logging import getLogger
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TYPE_CHECKING

from encommon.types import DictStrAny

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import Security
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from starlette.responses import Response

from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from .persist import APIROUTER as PERSIST
from .static import APIROUTER as STATIC
from .. import VERSION

if TYPE_CHECKING:
    from .service import RestfulService
    from ..homie import Homie



_BASIC = HTTPBasic()



class RestfulApp(FastAPI):
    """
    FastAPI application for the Homie Automate RESTful API.

    :param restful: Primary class instance for the service.
    """

    homie: 'Homie'
    restful: 'RestfulService'


    def __init__(
        self,
        restful: 'RestfulService',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.homie = restful.homie
        self.restful = restful

        params = restful.params

        depends = (
            [Depends(_authenticate)]
            if params.authenticate
            else None)

        super().__init__(
            title='Homie Automate',
            version=VERSION,
            openapi_url='/api/openapi.json',
            docs_url='/api/docs',
            redoc_url='/api/redoc',
            dependencies=depends,
            exception_handlers={
                Exception: _exception})


        self.include_router(PERSIST)
        self.include_router(STATIC)


        middleware = (
            self.middleware('http'))

        middleware(_middlexcept)



class RestfulServer(UvicornServer):
    """
    Uvicorn server for Homie Automate RESTful API services.

    :param restful: Primary class instance for the service.
    :param config: Configuration for parent Uvicorn server.
    """

    __restful: 'RestfulService'


    def __init__(
        self,
        restful: 'RestfulService',
        config: UvicornConfig,
    ) -> None:
        """
        Initialize instance for class using provided parameters.

        .. note::
           Somewhat similar to same method in HomieAspiredItem.
        """

        self.__restful = restful

        super().__init__(config)


        for name in ['error', 'access']:

            logger = getLogger(
                f'uvicorn.{name}')

            setattr(
                logger, 'critical',
                self.__log_critical)

            setattr(
                logger, 'debug',
                self.__log_debug)

            setattr(
                logger, 'error',
                self.__log_error)

            setattr(
                logger, 'info',
                self.__log_info)

            setattr(
                logger, 'warn',
                self.__log_warning)

            setattr(
                logger, 'warning',
                self.__log_warning)


    def __log_process(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> DictStrAny:
        """
        Process the logging message and strip color characters.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        if isinstance(message, str):
            message = message % args

        if 'extra' in kwargs:
            del kwargs['extra']

        _kwargs = {
            'base': self,
            'message': message}

        return _kwargs | kwargs


    def __log_critical(
        # NOCVR
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided logging arguments into logger object.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        restful = self.__restful
        homie = restful.homie
        logger = homie.logger

        kwargs = self.__log_process(
            message, *args, **kwargs)

        logger.log_c(**kwargs)


    def __log_debug(
        # NOCVR
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided logging arguments into logger object.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        restful = self.__restful
        homie = restful.homie
        logger = homie.logger

        kwargs = self.__log_process(
            message, *args, **kwargs)

        logger.log_d(**kwargs)


    def __log_error(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided logging arguments into logger object.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        restful = self.__restful
        homie = restful.homie
        logger = homie.logger

        kwargs = self.__log_process(
            message, *args, **kwargs)

        logger.log_e(**kwargs)


    def __log_info(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided logging arguments into logger object.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        restful = self.__restful
        homie = restful.homie
        logger = homie.logger

        kwargs = self.__log_process(
            message, *args, **kwargs)

        logger.log_i(**kwargs)


    def __log_warning(
        # NOCVR
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided logging arguments into logger object.

        :param message: Message from the Uvicorn server routine.
        :param args: Positional arguments used with templating.
        :param kwargs: Keyword arguments for populating message.
        """

        restful = self.__restful
        homie = restful.homie
        logger = homie.logger

        kwargs = self.__log_process(
            message, *args, **kwargs)

        logger.log_w(**kwargs)



async def _exception(
    # NOCVR
    request: Request,
    reason: Any,  # noqa: ANN401
) -> Response:
    """
    Handle logging the exceptions encountered with FastAPI.
    """

    homie = request.app.homie

    homie.logger.log_e(
        base=request.app,
        status='exception',
        exc_info=reason)

    await asyncio.sleep(0)

    return Response(500)



async def _middlexcept(
    request: Request,
    next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """
    Handle logging the exceptions encountered with FastAPI.
    """

    homie = request.app.homie

    try:
        return await next(request)

    except Exception as reason:

        homie.logger.log_e(
            base=request.app,
            status='exception',
            exc_info=reason)

        await asyncio.sleep(0)

        return Response(500)



async def _authenticate(
    request: Request,
    submit: HTTPBasicCredentials = Security(_BASIC),
) -> None:
    """
    Authenticate the request using the configured tokens.
    """

    restful = request.app.restful
    params = restful.params
    users = params.authenticate

    assert users is not None

    username = submit.username
    password = submit.password

    headers = {
        'www-authenticate': 'basic'}

    await asyncio.sleep(0)

    if username not in users:
        raise HTTPException(
            401, headers=headers)

    _password = users[username]

    if password != _password:
        raise HTTPException(
            401, headers=headers)
