from flask import Flask, request
from .conversions import xml_to_json, json_to_xml

def xml_to_json_handler():
    xml_content_types = ["application/xhtml+xml", "text/xml",
                         "application/xml"]

    if request.headers['Content-Type'] in xml_content_types:
        return xml_to_json(request.data)
    return '{"error": "ambigious Content-Type"}'

def json_to_xml_handler():
    json_content_types = ["application/json", "application/x-javascript",
                          "text/javascript", "text/x-javascript",
                          "text/x-json"]
    if request.headers['Content-Type'] in json_content_types:
        return json_to_xml(request.data)
    return '{"error": "ambigious Content-Type"}'

def index():
    return "index"

app = Flask(__name__)

@app.before_request
def before_request():
    print("HEADERS", request.headers)
    print("REQ_path", request.path)
    print("ARGS", request.args)
    print("DATA", request.data)
    print("FORM", request.form)

app.add_url_rule('/', view_func=index)
app.add_url_rule('/xml_to_json', view_func=xml_to_json_handler, methods=['POST'])
app.add_url_rule('/json_to_xml', view_func=json_to_xml_handler, methods=['POST'])
