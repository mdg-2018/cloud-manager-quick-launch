import pymongo
import requests
import tornado
from tornado import web
import tornado.ioloop
import os
import docker
import uuid

##########
# FUNCTIONS
##########
def startContainer(port,token="FROMBLAZOR",user="UNKNOWNUNKNOWNUNKNOWN"):
    # code here
    pass


##########
# API
##########
class Handler_Main(tornado.web.RequestHandler):
    def get(self):
        self.render("/opt/wwwroot/static/index.html")

class Handler_API_HelloWorld(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

##########
# MAIN
##########

settings = {}

app= tornado.web.Application([
    (r"/", Handler_Main),
    (r"/api/helloworld", Handler_API_HelloWorld),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/css" }),
    (r"/_framework/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/_framework" }),
], **settings)
app.listen(8000)
tornado.ioloop.IOLoop.current().start()