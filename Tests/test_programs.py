import random
import string
import tempfile
import os
from io import BytesIO
from unittest.mock import patch, MagicMock

from programs import get_last_strings_from_file, search_for_lines_by_words
    
def random_word(length):
    letters = string.ascii_letters + string.digits + ' '*10
    return ''.join(random.choice(letters) for i in range(length))

def write_to_file(temp_path, byte_string, mode='ab'):
    with open(temp_path, mode=mode) as f:
        f.write(byte_string)

#------------------tests for get_last_strings_from_file-------------------
def test_FileNotFoundError_get_last_strings_from_file():
    test_path = ''
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}') as test_file:
        test_path = test_file.name
    assert(get_last_strings_from_file(path_file=test_path, quantity_strings=10) == [(-1, b'log file disappeared: FileNotFoundError')])

def test_PermissionError_get_last_strings_from_file():
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}') as test_file:
        assert(get_last_strings_from_file(path_file=test_file.name, quantity_strings=10) == [(-1, b'Permission denied to log')])

def test_get_last_strings_from_file():
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=10) == [])
        write_to_file(test_file.name, b'\r\n', mode='ab')
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=5) == [(0, b'\r\n')])

def test_even_numbered_get_last_strings_from_file():
    test_text = b'line 1\r\nline 2\r\nline 3\r\n\r\n'
    string_number = 3
    expected_value = [(8, b'line 2\r\n'),(16, b'line 3\r\n'), (24, b'\r\n')]
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_odd_get_last_strings_from_file():
    string_number = 3
    test_text = b'line 1\r\nline 2\r\nline 33\r\n\r\n'
    expected_value = [(8, b'line 2\r\n'),(16, b'line 33\r\n'), (25, b'\r\n')]
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_random_get_last_strings_from_file():
    string_number = random.randint(1, 10)
    number_line = string_number + random.randint(1, 10)
    test_text = b''
    expected_value = []
    for i in range(number_line):
        test_cursor_position = len(test_text)
        test_line = random_word(random.randint(1, 30)).encode() + b'\r\n'
        test_text += test_line
        if (i >= number_line - string_number):
            expected_value.append((test_cursor_position, test_line))
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_zero_quantity_strings_get_last_strings_from_file():
    string_number = 0
    test_text = b'line 1\r\nline 2\r\nline 3'
    expected_value = []
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_one_empty_line_get_last_strings_from_file():
    string_number = 5
    test_text = b'\r\n'
    expected_value = [(0, b'\r\n')]
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_negativ_get_last_strings_from_file():
    string_number = -1
    test_text = b'line 1\r\nline 2\r\nline 3'
    expected_value = []
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

def test_more_max_get_last_strings_from_file():
    string_number = 10
    test_text = b'line 1\r\nline 2\r\nline 3'
    expected_value = [(0, b'line 1\r\n'), (8, b'line 2\r\n'), (16, b'line 3')]
    with tempfile.TemporaryFile(mode='w+b',
                                dir=f'{os.path.dirname(os.path.abspath(__file__))}',
                                delete_on_close=False) as test_file:
        test_file.write(test_text)
        test_file.close()
        assert(get_last_strings_from_file(f'{test_file.name}', quantity_strings=string_number) == expected_value)

#------------------tests for search_for_lines_by_words---------------------
def test_default_search_for_lines_by_words():
    input_list_line = [(8, b'line 2\r\n'),(16, b'line 33\r\n'), (25, b'\r\n')]
    kyewords = ('line')
    stopwords = ('33')
    start_position = 0
    expected_value = [16, ['line 2']]
    return_value = search_for_lines_by_words(position_last_find=start_position,
                                             byte_list_line=input_list_line,
                                             turple_keyword=kyewords,
                                             turple_stopword=stopwords)
    assert(expected_value == return_value)

def test_empty_search_for_lines_by_words():
    input_list_line = [(8, b'line 2\r\n'),(16, b'line 33\r\n'), (25, b'line test\r\n')]
    kyewords = ('line')
    stopwords = ('33')
    start_position = 25
    expected_value = [36, ['line test']]
    return_value = search_for_lines_by_words(position_last_find=start_position,
                                             byte_list_line=input_list_line,
                                             turple_keyword=kyewords,
                                             turple_stopword=stopwords)
    assert(expected_value == return_value)

