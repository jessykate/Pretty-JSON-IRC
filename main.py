#!/usr/bin/python

# A template for a basic Tornado project. 
#
# To run:
# ./main.py
# and visit localhost:8888

import tornado.httpserver
import tornado.ioloop
import tornado.web
import urllib, urllib2, datetime, re
import os, datetime, urllib2
try:
    import json
except:
    import simplejson as json

JSON_LOG_URL='''http://api.talis.com/stores/lgridinoc-dev4/services/sparql?output=json&query=SELECT+%3Fdate+%3Fcreator+%3Fo+%0D%0AWHERE+{++%0D%0A%3Fs+%3Chttp://rdfs.org/sioc/ns%23content%3E+%3Fo+.+%0D%0A%3Fs+%3Chttp://purl.org/dc/elements/1.1/date%3E+%3Fdate+.+%0D%0A%3Fs+%3Chttp://purl.org/dc/elements/1.1/creator%3E+%3Fcreator+.+%0D%0A%3Fs+%3Chttp://purl.org/dc/elements/1.1/source%3E+%22%23p2pu-dev%22+.%0D%0A}++ORDER+BY+%3Fdate'''

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        fp = urllib2.urlopen(JSON_LOG_URL)
        js = json.loads(fp.read())
        # logs is now a list of dict objects for each statement made in the
        # chat room
        logs = js['results']['bindings']
        formatted = []
        for log in logs:
            line = {}
            line['date'] = datetime.datetime.strptime( log['date']['value'], "%Y-%m-%dT%H:%M:%S+0000").strftime("%b %d, %Y, %H:%M:%S")
            line['speaker'] =  log['creator']['value'] 
            string = log['o']['value']
            match = re.search('''https?://[\w._~:/?#\[\]@!$&'()*+=%;\-]+''', string)
            if match:
                match.start()
                match.end()
                string = string[:match.start()] + '<a href="' + match.group() + '">' + string[match.start():match.end()] + '</a>' + string[match.end():]
            line['string'] = string
            formatted.append(line)
        self.render('index.html', formatted=formatted)

application = tornado.web.Application([
        (r'/', IndexHandler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
