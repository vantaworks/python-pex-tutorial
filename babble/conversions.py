import json
import xmltodict
import dicttoxml

def xml_to_json(raw_xml):
    parsed_xml = xmltodict.parse(raw_xml, process_namespaces=True)
    return json.dumps(parsed_xml)

def json_to_xml(raw_json):
    parsed_json = json.loads(raw_json)
    return dicttoxml.dicttoxml(parsed_json)
