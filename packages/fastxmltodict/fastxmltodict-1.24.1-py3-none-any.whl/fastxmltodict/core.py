from xml.etree import ElementTree as ET


def xml_to_dict(element):
    """
    Recursively converts an XML element into a dictionary.
    :param element: XML element
    :return: dict
    """
    result = {}

    # Add attributes
    if element.attrib:
        result["@attributes"] = element.attrib

    # Add child elements
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_dict)
            else:
                result[child.tag] = [result[child.tag], child_dict]
        else:
            result[child.tag] = child_dict

    # Add text if present
    text = element.text.strip() if element.text else ""
    if text:
        result["#text"] = text

    return result or text


def parse(xml_string):
    """
    Converts an XML string into a Python dictionary.
    :param xml_string: XML string
    :return: dict
    """
    root = ET.fromstring(xml_string)
    return {root.tag: xml_to_dict(root)}


def version():
    return "1.24.0"