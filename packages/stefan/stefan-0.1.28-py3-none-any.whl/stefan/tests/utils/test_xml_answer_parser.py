import pytest
from stefan.utils.xml_answer_parser import XMLAnswerParser

def test_parse_simple_answer():
    xml = """Some LLM thinking...
    <answer>
    <reasoning>Not very relevant function</reasoning>
    <score>0.3</score>
    <is_relevant>false</is_relevant>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "reasoning": "Not very relevant function",
        "score": "0.3",
        "is_relevant": "false"
    }
    assert result.xml_text.strip() == """<answer>
    <reasoning>Not very relevant function</reasoning>
    <score>0.3</score>
    <is_relevant>false</is_relevant>
    </answer>""".strip()

def test_parse_nested_answer():
    xml = """<answer>
    <metadata>
        <timestamp>2024-03-20</timestamp>
        <version>1.0</version>
    </metadata>
    <result>
        <score>0.8</score>
        <confidence>high</confidence>
    </result>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "metadata": {
            "timestamp": "2024-03-20",
            "version": "1.0"
        },
        "result": {
            "score": "0.8",
            "confidence": "high"
        }
    }

def test_answer_with_empty_values():
    xml = """<answer>
    <reasoning></reasoning>
    <score></score>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "reasoning": "",
        "score": ""
    }

def test_answer_must_be_at_end():
    xml = """<answer>
    <score>0.8</score>
    </answer>
    Some text after"""
    
    with pytest.raises(ValueError, match="Answer must be at the end of the response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_parse_repeated_elements():
    xml = """<answer>
    <file>file1.txt</file>
    <file>file2.txt</file>
    <other>single value</other>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "file": ["file1.txt", "file2.txt"],
        "other": "single value"
    }

def test_content_contains_invalid_xml_characters():
    xml = """
    <answer>
    <write_to_file>
    <file_path>calculator.py</file_path>
    <content>
    while i < len(tokens): & < > \" '
    </content>
    </write_to_file>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "write_to_file": {
            "file_path": "calculator.py",
            "content": "while i < len(tokens): & < > \" '",
        }
    }

def test_content_contains_xml_like_tags():
    xml = """
    <answer>
    <attempt_completion>
    <response>
    - Extends UseCase<LoginUseCase.Args, SignedInRedirect>
    </response>
    </attempt_completion>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "attempt_completion": {
            "response": "- Extends UseCase<LoginUseCase.Args, SignedInRedirect>"
        }
    }

def test_content_contains_xml_content():
    xml = """
    <answer>
    <create_file>
    <file_path>shared/resources/src/commonMain/moko-resources/base/strings.xml</file_path>
    <content><?xml version="1.0" encoding="utf-8"?>
    <resources>
        <!-- Previous content remains unchanged -->
        <!-- Profile -->
        <string name="profile_test_notification_button">Odeslat testovací notifikaci</string>
        <!-- Rest of the content remains unchanged -->
    </resources></content>
    </create_file>
    </answer>
    """

    expected_content = """<?xml version="1.0" encoding="utf-8"?>
    <resources>
        <!-- Previous content remains unchanged -->
        <!-- Profile -->
        <string name="profile_test_notification_button">Odeslat testovací notifikaci</string>
        <!-- Rest of the content remains unchanged -->
    </resources>"""

    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "create_file": {
            "file_path": "shared/resources/src/commonMain/moko-resources/base/strings.xml",
            "content": expected_content,
        }
    }

def test_content_contains_cdata():
    xml = """
    <answer>
    <content><![CDATA[Some text with & < > \" ' characters]]></content>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "content": "Some text with & < > \" ' characters",
    }

def test_multiple_answers_raises_error():
    xml = """<answer>first</answer>
    Some text
    <answer>second</answer>"""
    
    with pytest.raises(ValueError, match="Multiple answer tags found in response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_missing_answer_raises_error():
    xml = "Some text without answer tags"
    
    with pytest.raises(ValueError, match="No answer tag found in response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_invalid_xml_raises_error():
    xml = "<answer><invalid></answer>"
    
    with pytest.raises(ValueError, match="Invalid XML format"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_empty_content():
    xml = "<answer><content></content></answer>"
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "content": "",
    }

def test_parse_without_answer_tag():
    xml = """<reasoning>Not very relevant function</reasoning>
    <score>0.3</score>
    """
    
    result = XMLAnswerParser.parse_xml_without_answer_tag(xml)
    assert result.answer_dict == {
        "reasoning": "Not very relevant function",
        "score": "0.3",
    }
    
    # Compare XML content without caring about whitespace
    expected_xml = """<answer><reasoning>Not very relevant function</reasoning><score>0.3</score></answer>"""
    assert result.xml_text.replace(" ", "").replace("\n", "") == expected_xml.replace(" ", "").replace("\n", "")


def test_commands_preserve_order():
    xml = """
    <answer>
    <commands>
        <update_cell>
            <row>2</row>
            <column>B</column>
            <value>First Update</value>
        </update_cell>
        <get_all></get_all>
        <update_cell>
            <row>3</row>
            <column>B</column>
            <value>Second Update</value>
        </update_cell>
    </commands>
    </answer>
    """
    
    result = XMLAnswerParser.parse_answer_xml(xml, preserve_order=["commands"])
    assert result.answer_dict["commands"] == [
        {
            "type": "update_cell",
            "data": {"row": "2", "column": "B", "value": "First Update"}
        },
        {
            "type": "get_all",
            "data": ""
        },
        {
            "type": "update_cell",
            "data": {"row": "3", "column": "B", "value": "Second Update"}
        }
    ]

def test_default_grouping_behavior():
    xml = """
    <answer>
    <commands>
        <update_cell>
            <row>2</row>
            <column>B</column>
            <value>First Update</value>
        </update_cell>
        <get_all></get_all>
        <update_cell>
            <row>3</row>
            <column>B</column>
            <value>Second Update</value>
        </update_cell>
    </commands>
    </answer>
    """
    
    result = XMLAnswerParser.parse_answer_xml(xml)  # No preserve_order specified
    assert result.answer_dict == {
        "commands": {
            "update_cell": [
                {"row": "2", "column": "B", "value": "First Update"},
                {"row": "3", "column": "B", "value": "Second Update"}
            ],
            "get_all": ""
        }
    }

def test_nested_preserve_order():
    xml = """
    <answer>
    <outer_commands>
        <commands>
            <update_cell>
                <row>2</row>
                <column>B</column>
                <value>First Update</value>
            </update_cell>
            <get_all></get_all>
            <update_cell>
                <row>3</row>
                <column>B</column>
                <value>Second Update</value>
            </update_cell>
        </commands>
        <other_commands>
            <command>one</command>
            <command>two</command>
        </other_commands>
    </outer_commands>
    </answer>
    """
    
    result = XMLAnswerParser.parse_answer_xml(xml, preserve_order=["commands"])
    assert result.answer_dict == {
        "outer_commands": {
            "commands": [
                {
                    "type": "update_cell",
                    "data": {"row": "2", "column": "B", "value": "First Update"}
                },
                {
                    "type": "get_all",
                    "data": ""
                },
                {
                    "type": "update_cell",
                    "data": {"row": "3", "column": "B", "value": "Second Update"}
                }
            ],
            "other_commands": {
                "command": ["one", "two"]
            }
        }
    }

def test_multiple_preserve_order_tags():
    xml = """
    <answer>
    <outer_commands>
        <commands>
            <update_cell>
                <row>2</row>
                <column>B</column>
                <value>First</value>
            </update_cell>
            <get_all></get_all>
        </commands>
        <validations>
            <check>one</check>
            <check>two</check>
            <validate>final</validate>
        </validations>
    </outer_commands>
    </answer>
    """
    
    result = XMLAnswerParser.parse_answer_xml(xml, preserve_order=["commands", "validations"])
    assert result.answer_dict == {
        "outer_commands": {
            "commands": [
                {
                    "type": "update_cell",
                    "data": {"row": "2", "column": "B", "value": "First"}
                },
                {
                    "type": "get_all",
                    "data": ""
                }
            ],
            "validations": [
                {
                    "type": "check",
                    "data": "one"
                },
                {
                    "type": "check",
                    "data": "two"
                },
                {
                    "type": "validate",
                    "data": "final"
                }
            ]
        }
    }

def test_temp():
    text = """
<answer>
    <texts_updater_simple_agent>
        <task>Add a new section for jokes with the first joke:
<!-- Jokes -->
<string name="joke_stefan">Prečo si Telekom vybral ružovú farbu? Lebo je to jediná farba, ktorú vidno aj cez optické vlákno! 📱✨</string></task>
        <context>Adding a light-hearted joke related to Telekom's brand color (magenta/pink) that's appropriate for the young target audience (15-28 years). The joke maintains the app's casual and friendly tone while referencing both the telco industry (optical fiber) and the brand's distinctive color.</context>
    </texts_updater_simple_agent>
</answer>
"""

    result = XMLAnswerParser.parse_answer_xml(text)