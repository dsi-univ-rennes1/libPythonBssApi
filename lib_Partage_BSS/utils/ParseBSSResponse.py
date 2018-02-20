import xml.etree.ElementTree as et
from xmljson import yahoo as pa


def parseResponse(stringXml):
    return pa.data(et.fromstring(stringXml))["Response"]
