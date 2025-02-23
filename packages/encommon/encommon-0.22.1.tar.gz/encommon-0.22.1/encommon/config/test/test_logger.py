"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from _pytest.logging import LogCaptureFixture

from pytest import fixture

from ..logger import Logger
from ..logger import Message
from ..params import LoggerParams
from ...times import Time
from ...times.common import UNIXMPOCH
from ...times.common import UNIXSPOCH
from ...types import inrepr
from ...types import instr
from ...types import lattrs
from ...utils import strip_ansi



_CAPLOG = list[tuple[str, int, str]]



@fixture
def logger(
    tmp_path: Path,
) -> Logger:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    params = LoggerParams(
        stdo_level='debug',
        file_level='info',
        file_path=f'{tmp_path}/test.log')

    return Logger(params)



def test_Message() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    message = Message(
        time=UNIXMPOCH,
        level='info',
        string='foobar',
        none=None,
        list=['1', 2],
        tuple=('1', 2),
        set={'1', 2},
        dict={'1': 2},
        empty_list=[],
        empty_dict={},
        int=1,
        float=2.0,
        elapsed=3.69420)


    attrs = lattrs(message)

    assert attrs == [
        '_Message__level',
        '_Message__time',
        '_Message__fields']


    assert inrepr(
        'Message(level="info"',
        message)

    assert isinstance(
        hash(message), int)

    assert instr(
        'Message(level="info"',
        message)


    assert message.level == 'info'

    assert message.time == 0

    assert len(message.fields) == 8


    output = strip_ansi(
        message.stdo_output)

    assert output == (
        'level="info"'
        f' time="{UNIXSPOCH}"'
        ' string="foobar"'
        ' list="1,2"'
        ' tuple="1,2"'
        ' set="1,2"'
        ' dict="{\'1\': 2}"'
        ' int="1"'
        ' float="2.0"'
        ' elapsed="3.69"')


    output = message.file_output

    assert output == (
        '{"level": "info",'
        f' "time": "{UNIXMPOCH}",'
        ' "string": "foobar",'
        ' "list": "1,2",'
        ' "tuple": "1,2",'
        ' "set": "1,2",'
        ' "dict": "{\'1\': 2}",'
        ' "int": "1",'
        ' "float": "2.0",'
        ' "elapsed": "3.69"}')



def test_Logger(
    logger: Logger,
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param logger: Custom fixture for the logger instance.
    :param caplog: pytest object for capturing log message.
    """


    attrs = lattrs(logger)

    assert attrs == [
        '_Logger__params',
        '_Logger__stdo_level',
        '_Logger__file_level',
        '_Logger__file_path',
        '_Logger__started',
        '_Logger__logr_stdo',
        '_Logger__logr_file']


    assert inrepr(
        'logger.Logger object',
        logger)

    assert isinstance(
        hash(logger), int)

    assert instr(
        'logger.Logger object',
        logger)


    assert logger.params

    assert logger.stdo_level == 'debug'

    assert logger.file_level == 'info'

    assert logger.file_path

    assert not logger.started

    assert logger.logger_stdo

    assert logger.logger_file


    logger.log_d(msg='pytest')
    logger.log_c(msg='pytest')
    logger.log_e(msg='pytest')
    logger.log_i(msg='pytest')
    logger.log_w(msg='pytest')



def test_Logger_cover(
    logger: Logger,
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param logger: Custom fixture for the logger instance.
    :param caplog: pytest object for capturing log message.
    """

    time = Time('now')


    # Test preventing debug from
    # any needless instantiation
    setattr(
        logger,
        '_Logger__file_level',
        'info')

    # Test preventing debug from
    # any needless instantiation
    setattr(
        logger,
        '_Logger__stdo_level',
        'info')


    def _logger_logs() -> None:
        logger.log_d(msg='pytest')
        logger.log_c(msg='pytest')
        logger.log_e(msg='pytest')
        logger.log_i(msg='pytest')
        logger.log_w(msg='pytest')
        logger.log_i(elapsed=time)


    def _logger_stdo() -> _CAPLOG:

        output = caplog.record_tuples
        key = 'encommon.logger.stdo'

        return [
            x for x in output
            if x[0] == key]


    def _logger_file() -> _CAPLOG:

        output = caplog.record_tuples
        key = 'encommon.logger.file'

        return [
            x for x in output
            if x[0] == key]


    logger.start()

    _logger_logs()

    assert len(_logger_stdo()) == 5
    assert len(_logger_file()) == 5

    logger.stop()


    _logger_logs()

    assert len(_logger_stdo()) == 5
    assert len(_logger_file()) == 5


    logger.start()

    message = 'unknown exception'
    raises = Exception('pytest')

    logger.log_e(
        message=message,
        exc_info=raises)

    stdo = _logger_stdo()[-1][2]
    file = _logger_file()[-1][2]

    assert message in str(stdo)
    assert message in str(file)

    assert len(_logger_stdo()) == 6
    assert len(_logger_file()) == 6


    logger.stop()


    _logger_logs()

    assert len(_logger_stdo()) == 6
    assert len(_logger_file()) == 6
