import xml.etree.ElementTree as et
from xmljson import parker as pa


def parseResponse(stringXml):
    return pa.data(et.fromstring(stringXml))
