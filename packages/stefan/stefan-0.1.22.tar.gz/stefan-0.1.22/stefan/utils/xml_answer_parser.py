import traceback
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import re

class XMLAnswer(BaseModel):
    xml_text: str
    answer_dict: Dict[str, Any]

class XMLAnswerParser:
    # Add these as class constants
    CDATA_WRAP_ATTRIBUTES = {'old_text', 'new_text', 'content', 'values', 'value', 'detailed_description', 'response'}

    @staticmethod
    def parse_answer_xml(text: str, *, preserve_order: Optional[List[str]] = None) -> XMLAnswer:
        try:
            return XMLAnswerParser._parse_answer_xml(text, preserve_order=preserve_order)
        except ValueError as e:
            traceback.print_exc()
            raise ValueError(f"Answer XML parsing failed with error:\n\n{str(e)}\n\nfor value:\n\n{text}")
        
    @staticmethod
    def parse_xml_without_answer_tag(xml: str, *, preserve_order: Optional[List[str]] = None) -> XMLAnswer:
        try:
            return XMLAnswerParser._parse_answer_xml("<answer>" + xml + "</answer>", preserve_order=preserve_order)
        except ValueError as e:
            raise ValueError(f"Answer XML parsing failed with error:\n\n{str(e)}\n\nfor value:\n\n{xml}")

    @staticmethod
    def _parse_answer_xml(text: str, *, preserve_order: Optional[List[str]] = None) -> XMLAnswer:
        """
        Parse XML answer from LLM response, ensuring it's properly formatted and at the end of the message.
        
        Args:
            text: Full text response from LLM containing XML answer
            
        Returns:
            Dictionary containing parsed XML attributes
            
        Raises:
            ValueError: If answer tag is missing, multiple answers found, or answer is not at the end
        """
        # Find the last occurrence of <answer>
        answer_start = text.rfind("<answer>")
        if answer_start == -1:
            raise ValueError(f"No answer tag found in response: {text}")
            
        # Check there's only one answer tag
        if text.count("<answer>") > 1:
            raise ValueError(f"Multiple answer tags found in response: {text}")
            
        # Extract the XML part
        xml_text = text[answer_start:]
        
        # Check if there's any non-whitespace content after the closing tag
        end_tag = "</answer>"
        end_tag_pos = xml_text.rfind(end_tag)
        if end_tag_pos == -1 or xml_text[end_tag_pos + len(end_tag):].strip():
            raise ValueError(f"Answer must be at the end of the response: {text}")

        # Wrap specified attributes with CDATA before escaping
        xml_text = XMLAnswerParser._wrap_attributes_with_cdata(xml_text)
        
        # Preprocess the XML to escape special characters
        sanitized_xml = XMLAnswerParser._escape_xml_characters(xml_text)
        
        try:
            root = ET.fromstring(sanitized_xml)
            if root.tag != "answer":
                raise ValueError(f"Root element must be 'answer': {text}")
            
            preserve_order = preserve_order or []
            
            def parse_element(element: ET.Element, parent_tag: Optional[str] = None) -> Dict[str, Any]:
                result = {}
                child_counts = {}
                ordered_elements = []
                
                # First pass - count children
                for child in element:
                    child_counts[child.tag] = child_counts.get(child.tag, 0) + 1
                
                # Second pass - parse children
                for child in element:
                    # Unescape the text content
                    text_content = XMLAnswerParser._unescape_xml_characters(child.text.strip() if child.text else "")
                    
                    parsed_data = parse_element(child, child.tag) if len(child) > 0 else text_content
                    
                    # If element is in preserve_order list, collect all children as list items
                    if element.tag in preserve_order:
                        ordered_elements.append({
                            "type": child.tag,
                            "data": parsed_data
                        })
                    else:
                        # Regular grouping behavior
                        if child_counts[child.tag] > 1:
                            if child.tag not in result:
                                result[child.tag] = []
                            result[child.tag].append(parsed_data)
                        else:
                            result[child.tag] = parsed_data
                
                # If this element should preserve order, return the ordered list instead
                if element.tag in preserve_order:
                    return ordered_elements
                    
                return result
            
            return XMLAnswer(
                xml_text=sanitized_xml,
                answer_dict=parse_element(root)
            )
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {str(e)} for value: {text}")

    @staticmethod
    def _wrap_attributes_with_cdata(xml: str) -> str:
        """
        Wrap specified attributes content with CDATA sections.
        """
        for attr in XMLAnswerParser.CDATA_WRAP_ATTRIBUTES:
            pattern = f"<{attr}>(.*?)</{attr}>"
            
            def wrap_with_cdata(match):
                content = match.group(1)
                if not content.startswith('<![CDATA['):
                    return f"<{attr}><![CDATA[{content}]]></{attr}>"
                return match.group(0)
            
            xml = re.sub(pattern, wrap_with_cdata, xml, flags=re.DOTALL)
        
        return xml

    @staticmethod
    def _escape_xml_characters(xml: str) -> str:
        """
        Escape special XML characters within text nodes while preserving CDATA sections.
        """
        # First, temporarily replace CDATA sections with a placeholder
        cdata_sections = []
        
        def save_cdata(match):
            cdata_sections.append(match.group(1))
            return f"___CDATA_PLACEHOLDER_{len(cdata_sections)-1}___"
        
        xml = re.sub(r'<!\[CDATA\[(.*?)\]\]>', save_cdata, xml, flags=re.DOTALL)
        
        # Escape special characters
        escaped_text = (
            xml.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )
        
        # Restore XML tags
        pattern = re.compile(r"&lt;(\/?)([a-zA-Z][a-zA-Z0-9_\-\.]*)((?:\s+[a-zA-Z][a-zA-Z0-9_\-\.]*=\"[^\"]*\")*)\s*&gt;")
        escaped_text = pattern.sub(r"<\1\2\3>", escaped_text)
        
        # Restore CDATA sections
        for i, cdata in enumerate(cdata_sections):
            escaped_text = escaped_text.replace(
                f"___CDATA_PLACEHOLDER_{i}___",
                f"<![CDATA[{cdata}]]>"
            )
        
        return escaped_text
        
    @staticmethod
    def _unescape_xml_characters(text: str) -> str:
        """
        Unescape XML special characters in text.
        
        Args:
            text: The text containing escaped XML characters
            
        Returns:
            Text with XML special characters unescaped
        """
        return (
            text.replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&apos;", "'")
        )