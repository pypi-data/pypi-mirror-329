import pytest

from stefan.ripgrep.rip_grep_parser import RipGrepParser

def test_parse_single_file():
    json_input = '''
{"type":"begin","data":{"path":{"text":"main.py"}}}
{"type":"match","data":{"path":{"text":"main.py"},"lines":{"text":"#!/usr/bin/env python"},"line_number":1}}
{"type":"context","data":{"path":{"text":"main.py"},"lines":{"text":"import argparse"},"line_number":2}}
'''
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines=json_input, directory="").files
    
    assert len(result) == 1
    assert result[0].file_path == "main.py"
    assert len(result[0].lines) == 2
    assert result[0].lines[0].text == "#!/usr/bin/env python"
    assert result[0].lines[0].line_number == 1
    assert result[0].lines[1].text == "import argparse"
    assert result[0].lines[1].line_number == 2

def test_parse_single_file_with_directory():
    json_input = '''
{"type":"begin","data":{"path":{"text":"main.py"}}}
{"type":"match","data":{"path":{"text":"main.py"},"lines":{"text":"#!/usr/bin/env python"},"line_number":1}}
{"type":"context","data":{"path":{"text":"main.py"},"lines":{"text":"import argparse"},"line_number":2}}
'''
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines=json_input, directory="/home/user/project").files
    
    assert len(result) == 1
    assert result[0].file_path == "/home/user/project/main.py"
    assert len(result[0].lines) == 2
    assert result[0].lines[0].text == "#!/usr/bin/env python"
    assert result[0].lines[0].line_number == 1
    assert result[0].lines[1].text == "import argparse"
    assert result[0].lines[1].line_number == 2

def test_parse_single_file_with_directory_with_trailing_slash():
    json_input = '''
{"type":"begin","data":{"path":{"text":"main.py"}}}
{"type":"match","data":{"path":{"text":"main.py"},"lines":{"text":"#!/usr/bin/env python"},"line_number":1}}
{"type":"context","data":{"path":{"text":"main.py"},"lines":{"text":"import argparse"},"line_number":2}}
'''
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines=json_input, directory="/home/user/project/").files
    
    assert len(result) == 1
    assert result[0].file_path == "/home/user/project/main.py"
    assert len(result[0].lines) == 2
    assert result[0].lines[0].text == "#!/usr/bin/env python"
    assert result[0].lines[0].line_number == 1
    assert result[0].lines[1].text == "import argparse"
    assert result[0].lines[1].line_number == 2

def test_parse_multiple_files():
    json_input = '''
{"type":"begin","data":{"path":{"text":"main.py"}}}
{"type":"match","data":{"path":{"text":"main.py"},"lines":{"text":"def main():"},"line_number":1}}
{"type":"begin","data":{"path":{"text":"test.py"}}}
{"type":"match","data":{"path":{"text":"test.py"},"lines":{"text":"def test():"},"line_number":1}}
'''
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines=json_input, directory="").files
    
    assert len(result) == 2
    assert result[0].file_path == "main.py"
    assert result[1].file_path == "test.py"
    assert result[0].lines[0].text == "def main():"
    assert result[1].lines[0].text == "def test():"

def test_empty_input():
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines="", directory="").files
    
    assert len(result) == 0

def test_invalid_json():
    parser = RipGrepParser()
    with pytest.raises(Exception):
        parser.parse_ripgrep_output("invalid json")

def test_parse_with_context_and_match():
    json_input = '''
{"type":"begin","data":{"path":{"text":"main.py"}}}
{"type":"context","data":{"path":{"text":"main.py"},"lines":{"text":"import os"},"line_number":1}}
{"type":"match","data":{"path":{"text":"main.py"},"lines":{"text":"def python_func():"},"line_number":2}}
{"type":"context","data":{"path":{"text":"main.py"},"lines":{"text":"    pass"},"line_number":3}}
'''
    parser = RipGrepParser()
    result = parser.parse_ripgrep_output(json_lines=json_input, directory="").files
    
    assert len(result) == 1
    assert len(result[0].lines) == 3
    assert result[0].lines[0].text == "import os"
    assert result[0].lines[1].text == "def python_func():"
    assert result[0].lines[2].text == "    pass"
