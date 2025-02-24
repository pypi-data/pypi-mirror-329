"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from threading import Thread
from time import sleep as block_sleep
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from fastapi import FastAPI

from uvicorn import Config as UvicornConfig

from .server import RestfulApp
from .server import RestfulServer

if TYPE_CHECKING:
    from .params import RestfulServiceParams
    from ..homie import Homie



class RestfulService:
    """
    Application programming interface using Homie Automate.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __fastapi: RestfulApp
    __uvicorn: RestfulServer
    __thread: Thread

    __stopped: Event
    __started: bool


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.logger.log_d(
            base=self,
            status='initial')

        self.__homie = homie

        self.__build_objects()

        self.__started = False

        homie.logger.log_i(
            base=self,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params


        fastapp = RestfulApp(self)

        uvicorn = RestfulServer(
            self,
            UvicornConfig(
                app=fastapp,
                host=params.bind_addr,
                port=params.bind_port,
                reload=False,
                workers=25,
                log_level='debug'))


        thread = Thread(
            target=uvicorn.run)


        self.__fastapi = fastapp
        self.__uvicorn = uvicorn
        self.__thread = thread

        self.__stopped = Event()


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which the instance belongs.

        :returns: Homie instance to which the instance belongs.
        """

        return self.__homie


    @property
    def params(
        self,
    ) -> 'RestfulServiceParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        homie = self.__homie
        params = homie.params

        return params.restful


    @property
    def fastapi(
        self,
    ) -> Optional[FastAPI]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__fastapi


    @property
    def running(
        self,
    ) -> bool:
        """
        Return the list of threads which are determined running.

        :returns: List of threads which are determined running.
        """

        thread = self.__thread

        return thread.is_alive()


    def start(
        self,
    ) -> None:
        """
        Start the various threads within the Homie class object.
        """

        homie = self.__homie
        started = self.__started

        if started is True:
            return None

        self.__started = True

        homie.logger.log_i(
            base=self,
            status='starting')

        self.__thread.start()

        homie.logger.log_i(
            base=self,
            status='started')


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.__homie

        while self.running:
            block_sleep(0.05)

        homie.logger.log_i(
            base=self,
            status='vacated')


    def stop(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Stop the various threads within the Homie class object.

        :param kwargs: Keyword arguments ignored by the method.
        :param args: Positional arguments ignored by the method.
        """

        homie = self.__homie
        uvicorn = self.__uvicorn
        thread = self.__thread
        started = self.__started
        stopped = self.__stopped

        if started is False:
            return None

        if stopped.is_set():
            return None

        stopped.set()

        homie.logger.log_i(
            base=self,
            status='stopping')

        if uvicorn is not None:
            uvicorn.should_exit = True

        if thread is not None:
            thread.join()

        homie.logger.log_i(
            base=self,
            status='stopped')
