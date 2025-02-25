import inspect
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


def symetric_dict(*args):
    caller_locals = inspect.currentframe().f_back.f_locals
    return {name: value for name, value in caller_locals.items() if value in args}


def xml_from_string(param: str) -> ET.XML:
    xml_start = param.index("<")
    xml_end = param.rfind(">")
    xml_string = param[xml_start:xml_end + 1]
    xml_string = fix_cdata_sections(xml_string)
    soup = BeautifulSoup(xml_string, "xml")
    xml = ET.fromstring(str(soup))
    return xml


def fix_cdata_sections(xml_string: str) -> str:
    def replace_cdata(match):
        content = match.group(1)
        if content.endswith(']]') or content.endswith(']>'):
            content = content[:-2]
        elif content.endswith(']'):
            content = content[:-1]
        return f'<![CDATA[{content}]]>'

    pattern = r'<!\[CDATA\[(.*?)(?:\]\]*>)'
    fixed_xml = re.sub(pattern, replace_cdata, xml_string, flags=re.DOTALL)
    return fixed_xml
