import pymongo
import requests
import tornado
from tornado import web
import tornado.ioloop
import os
import docker
import uuid
from subprocess import Popen, PIPE

##########
# FUNCTIONS
##########
def runPlaybook(self, callingUserName, pfilename, keypath, user):
    uid = str(uuid.uuid4())[:8]
    # build command to run an run it
    cmd = "ansible-playbook "+pfilename+" --key-file " + keypath + " --user " + user
    o = subprocess.Popen(cmd.split(" "), stdout = subprocess.PIPE).communicate()[0]
    return o

##########
# API
##########
class Handler_Main(tornado.web.RequestHandler):
    def get(self):
        self.render("/opt/wwwroot/static/index.html")

class Handler_API_HelloWorld(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Handler_API_Launch(tornado.web.RequestHandler):
    def get(self, username):
        self.write("Hello, "+ username)
        runPlaybook(username, )

##########
# MAIN
##########

settings = {}

app= tornado.web.Application([
    (r"/", Handler_Main),
    (r"/api/helloworld", Handler_API_HelloWorld),
    (r"/api/launch/(.*)", Handler_API_Launch),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/css" }),
    (r"/_framework/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/_framework" }),
], **settings)
app.listen(8000)
tornado.ioloop.IOLoop.current().start()