from dav_tools import messages
from dav_tools.messages import TextFormat

import sys


def test_message_base():
    result = messages.message('MESSAGE', file=None)
    assert result == 'MESSAGE'

    result = messages.message('Another message', file=None)
    assert result == 'Another message'

    result = messages.message('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', file=None)
    assert result == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'


# def test_message_file_end():
#     # param `end` only works when `file` is set
#     # FIXME: need to capture stdout and stderr

#     result = messages.message('MESSAGE', file=sys.stdout)
#     assert result == 'MESSAGE\n'

#     result = messages.message('MESSAGE', file=sys.stderr, end='end')
#     assert result == 'MESSAGEend'


def test_message_text_object():
    class MyObject:
        def __str__(self):
            return 'MyObject'
        
    result = messages.message(MyObject(), file=None)
    assert result == 'MyObject'


def test_message_multiple_text():
    result = messages.message('MESSAGE', 'MESSAGE2', file=None)
    assert result == 'MESSAGE MESSAGE2'

    result = messages.message('MESSAGE', 'MESSAGE2', 'MESSAGE3', file=None)
    assert result == 'MESSAGE MESSAGE2 MESSAGE3'


def test_message_icon():
    result = messages.message('MESSAGE', file=None, icon='E')
    assert result == f'{TextFormat.Style.BOLD.decode()}[E]{TextFormat.RESET.decode()} MESSAGE'


def test_message_text_min_len():
    result = messages.message('MESSAGE', file=None, text_min_len=[10])
    assert result == 'MESSAGE   '
    
    result = messages.message('MESSAGE', 'MESSAGE 2', file=None, text_min_len=[10, 20])
    assert result == 'MESSAGE    MESSAGE 2           '

    result = messages.message('MESSAGE', 'MESSAGE 2', file=None, text_min_len=[10])
    assert result == 'MESSAGE    MESSAGE 2'


def test_message_formatting():
    result = messages.message('MESSAGE', file=None, default_text_options=[TextFormat.Style.BOLD])
    assert result == f'{TextFormat.Style.BOLD.decode()}MESSAGE{TextFormat.RESET.decode()}'

    result = messages.message('MESSAGE', file=None, default_text_options=[TextFormat.Style.ITALIC, TextFormat.Color.RED])
    assert result == f'{TextFormat.Style.ITALIC.decode()}{TextFormat.Color.RED.decode()}MESSAGE{TextFormat.RESET.decode()}'


def test_message_formatting_additional_options():
    result = messages.message('MESSAGE 1', 'MESSAGE 2', 'MESSAGE 3', file=None, additional_text_options=[[], [TextFormat.Color.GREEN]])
    assert result == f'MESSAGE 1 {TextFormat.Color.GREEN.decode()}MESSAGE 2{TextFormat.RESET.decode()} MESSAGE 3'
    
    result = messages.message('MESSAGE 1', 'MESSAGE 2', 'MESSAGE 3', file=None, default_text_options=[TextFormat.Color.BLUE], additional_text_options=[[], [TextFormat.Style.BOLD], [TextFormat.Background.YELLOW]])
    assert result == f'{TextFormat.Color.BLUE.decode()}MESSAGE 1{TextFormat.RESET.decode()} {TextFormat.Color.BLUE.decode()}{TextFormat.Style.BOLD.decode()}MESSAGE 2{TextFormat.RESET.decode()} {TextFormat.Color.BLUE.decode()}{TextFormat.Background.YELLOW.decode()}MESSAGE 3{TextFormat.RESET.decode()}'


def test_message_formatting_icon():
    result = messages.message('MESSAGE', file=None, icon='!', icon_options=[TextFormat.Color.PURPLE])
    assert result == f'{TextFormat.Color.PURPLE.decode()}{TextFormat.Style.BOLD.decode()}[!]{TextFormat.RESET.decode()} MESSAGE'

    result = messages.message('MESSAGE', file=None, icon='xyz', icon_options=[TextFormat.Color.GREEN, TextFormat.Style.ITALIC])
    assert result == f'{TextFormat.Color.GREEN.decode()}{TextFormat.Style.ITALIC.decode()}{TextFormat.Style.BOLD.decode()}[xyz]{TextFormat.RESET.decode()} MESSAGE'


def test_message_empty():
    result = messages.message('', file=None)
    assert result == ''
