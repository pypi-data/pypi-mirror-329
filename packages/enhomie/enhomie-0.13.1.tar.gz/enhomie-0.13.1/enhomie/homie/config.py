"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from encommon.config import Config
from encommon.config import Params
from encommon.parse import Jinja2
from encommon.types import DictStrAny
from encommon.utils.common import PATHABLE

from .params import HomieParams



class HomieConfig(Config):
    """
    Contain the configurations from the arguments and files.

    :param sargs: Additional arguments on the command line.
    :param files: Complete or relative path to config files.
    :param cargs: Configuration arguments in dictionary form,
        which will override contents from the config files.
    """


    def __init__(  # noqa: CFQ001
        self,
        sargs: Optional[DictStrAny] = None,
        files: Optional[PATHABLE] = None,
        cargs: Optional[DictStrAny] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        sargs = dict(sargs or {})
        cargs = dict(cargs or {})


        _console = (
            sargs.get('console'))

        _debug = (
            sargs.get('debug'))

        key = 'enlogger/stdo_level'

        if _console is True:
            cargs[key] = 'info'

        if _debug is True:
            cargs[key] = 'debug'


        if 'config' in sargs:
            files = sargs['config']


        _dryrun = (
            sargs.get('dryrun'))

        _potent = (
            sargs.get('potent'))

        if _dryrun is not None:
            cargs['dryrun'] = _dryrun

        if _potent is not None:
            cargs['potent'] = _potent


        _faspires = (
            sargs.get('faspires'))

        _fdesires = (
            sargs.get('fdesires'))

        if _faspires is not None:
            key = 'filters/aspires'
            cargs[key] = _faspires

        if _fdesires is not None:
            key = 'filters/desires'
            cargs[key] = _fdesires


        _idesire = (
            sargs.get('idesire'))

        _iupdate = (
            sargs.get('iupdate'))

        _ihealth = (
            sargs.get('ihealth'))

        prefix = 'service/respite'

        if _idesire is not None:
            key = f'{prefix}/desire'
            cargs[key] = _idesire

        if _iupdate is not None:
            key = f'{prefix}/update'
            cargs[key] = _iupdate

        if _ihealth is not None:
            key = f'{prefix}/health'
            cargs[key] = _ihealth


        _dactions = (
            sargs.get('dactions'))

        _dupdates = (
            sargs.get('dupdates'))

        _dstreams = (
            sargs.get('dstreams'))

        _erestful = (
            sargs.get('erestful'))

        prefix = 'service/members'

        if _dactions is not None:
            key = f'{prefix}/actions'
            cargs[key] = not _dactions

        if _dupdates is not None:
            key = f'{prefix}/updates'
            cargs[key] = not _dupdates

        if _dstreams is not None:
            key = f'{prefix}/streams'
            cargs[key] = not _dstreams

        if _erestful is not None:
            key = f'{prefix}/restful'
            cargs[key] = _erestful


        _atimeout = (
            sargs.get('atimeout'))

        _utimeout = (
            sargs.get('utimeout'))

        _stimeout = (
            sargs.get('stimeout'))

        prefix = 'service/timeout'

        if _atimeout is not None:
            key = f'{prefix}/action'
            cargs[key] = _atimeout

        if _utimeout is not None:
            key = f'{prefix}/update'
            cargs[key] = _utimeout

        if _stimeout is not None:
            key = f'{prefix}/stream'
            cargs[key] = _stimeout


        _paction = (
            sargs.get('paction'))

        _pupdate = (
            sargs.get('pupdate'))

        _pstream = (
            sargs.get('pstream'))

        _pdesire = (
            sargs.get('pdesire'))

        _paspire = (
            sargs.get('paspire'))

        if _paction is not None:
            key = 'printer/action'
            cargs[key] = _paction

        if _pupdate is not None:
            key = 'printer/update'
            cargs[key] = _pupdate

        if _pstream is not None:
            key = 'printer/stream'
            cargs[key] = _pstream

        if _pdesire is not None:
            key = 'printer/desire'
            cargs[key] = _pdesire

        if _paspire is not None:
            key = 'printer/aspire'
            cargs[key] = _paspire


        super().__init__(
            files=files,
            cargs=cargs,
            sargs=sargs,
            model=HomieParams)

        self.merge_params()


    @property
    def params(
        self,
    ) -> HomieParams:
        """
        Return the Pydantic model containing the configuration.

        .. warning::
           This method completely overrides the parent but is
           based on that code, would be unfortunate if upstream
           changes meant this breaks or breaks something else.

        :returns: Pydantic model containing the configuration.
        """

        params = self.__params

        if params is not None:

            assert isinstance(
                params, HomieParams)

            return params


        basic = self.basic

        enconfig = (
            basic.get('enconfig'))

        enlogger = (
            basic.get('enlogger'))

        encrypts = (
            basic.get('encrypts'))

        basic = {
            'enconfig': enconfig,
            'enlogger': enlogger,
            'encrypts': encrypts}

        params = (
            self.model(**basic))

        assert isinstance(
            params, HomieParams)


        self.__params = params

        return self.__params


    def merge_params(
        self,
    ) -> None:
        """
        Update the Pydantic model containing the configuration.
        """

        merge = self.merge


        jinja2 = Jinja2({
            'source': merge,
            'config': self})

        parse = jinja2.parse

        params = self.model(
            parse, **merge)

        assert isinstance(
            params, HomieParams)


        self.__params = params


    @property
    def __params(
        self,
    ) -> Optional[Params]:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self._Config__params


    @__params.setter
    def __params(
        self,
        value: Params,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        self._Config__params = value
