import xmltodict

doc = xmltodict.parse("""<?xml version="1.0" encoding="UTF-8"?>
<key>
    <subkey1>thing1</subkey1>
    <subkey2>thing2</subkey2>
</key>"""
)

print(doc)