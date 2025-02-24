'''External command execution on local machine.'''

import subprocess as _subprocess
from shlex import split as _split
from subprocess import CalledProcessError
from typing import Callable as _Callable
import sys as _sys
import platform as _platform

def execute(command: str, stdin = _sys.stdin, stdout = _sys.stdout, stderr = _sys.stderr) -> bool:
    '''
    Run a command.

    :param command: the command to execute

    :param stdin: input redirection
    :param stdout: output redirection
    :param stderr: error redirection

    :returns: `True` if the command exits with return code zero, `False` otherwise
    '''
    exit_status = _subprocess.check_call(_split(command), stdin=stdin, stdout=stdout, stderr=stderr)
    return exit_status == 0

def get_output(command: str, on_success: _Callable[[bytes], any] = lambda x: x, on_error: _Callable[[], any] = None,
               stdin = _sys.stdin, stderr = _sys.stderr):
    '''
    Run a command and return its output.
    
    :param command: the command to execute

    :param on_success: call the specified function on the output before returning the data. Useful for casting the output from its original `bytes` format
    :param on_error: call the specified function if the command raised an exception. If this value is `None`, raises the exception.

    :param stdin: input redirection
    :param stderr: error redirection
            '''
    try:
        return on_success(_subprocess.check_output(_split(command), stdin=stdin, stderr=stderr))
    except CalledProcessError as e:
        if on_error is None:
            raise e
        return on_success(on_error())

def is_installed(command: str) -> bool:
    '''
    Check if a command is installed on the system.

    :param command: the command to check

    :returns: `True` if the command is installed, `False` otherwise
    '''

    if _platform.system() == 'Windows':
        command = f'cmd /c where {command}'
    else:
        command = f'which {command}'
        
    return _subprocess.call(_split(command), stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL) == 0
