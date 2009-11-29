import time
import urllib
import urllib2
import hashlib
import hmac
import base64
from xml.dom.minidom import parseString as parseXML

class ECS:
    def __init__(self, access_key, secret_key, associate_tag):
        self.host = 'ecs.amazonaws.com'
        self.path = '/onca/xml'
        self.api_url = 'http://' + self.host + self.path
        self.api_version = '2009-10-01'
        self.service = 'AWSECommericeService'

        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag = associate_tag

    def request(self, attrs):
        attrs.update({'Service': self.service,
                      'Version': self.api_version,
                      'AWSAccessKeyId': self.access_key,
                      'AssociateTag': self.associate_tag,
                      'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                 time.gmtime())})
        
        query = []
        keys = sorted(attrs.keys())
        for k in keys:
            query.append('%s=%s' % (k, urllib.quote(attrs[k])))
        query = "&".join(query)

        query += '&Signature=%s' % self._makeSignature(query)
        url = '%s?%s' % (self.api_url, query)

        return parseXML(urllib2.urlopen(url).read())

    def _makeSignature(self, query):
        s = "GET\n%s\n%s\n%s" % (self.host, self.path, query)
        sig = hmac.new(self.secret_key, s, hashlib.sha256).digest()
        return urllib.quote(base64.b64encode(sig))

