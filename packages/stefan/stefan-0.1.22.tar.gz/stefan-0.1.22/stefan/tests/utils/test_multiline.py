from stefan.utils.multiline import multiline

def test_multiline_with_indentation():
    input_text = """
        Hello
        World
            With Indent
        Back
    """
    
    expected = """Hello
World
    With Indent
Back"""
    assert multiline(input_text) == expected

def test_multiline_no_newlines():
    input_text = """First
    Second
    Third"""
    
    expected = """First
Second
Third"""
    assert multiline(input_text) == expected

def test_multiline_empty_string():
    assert multiline("") == ""

def test_multiline_single_line():
    assert multiline("Hello") == "Hello" 