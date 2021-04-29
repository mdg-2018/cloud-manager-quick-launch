import pymongo
import requests
import tornado
from tornado import web
import tornado.ioloop
import os
import uuid
from subprocess import Popen, PIPE
import subprocess
from tornado import gen
import json

##########
# FUNCTIONS
##########

##########
# API
##########
class Handler_Main(tornado.web.RequestHandler):
    def get(self):
        self.render("/opt/wwwroot/static/index.html")

class Handler_API_HelloWorld(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Handler_CM_API_Launch(tornado.web.RequestHandler):
    async def get(self, username):
        password = ""
        count = "3"
        expire = "" 

        if self.get_argument("password") != None:
            password = self.get_argument("password")
        if self.get_argument("count") != None:
            count = self.get_argument("count")
        if self.get_argument("expire") != None:
            expire = self.get_argument("expire")
            
        if(password == os.environ['APIPW']):
            pbPath = "/opt/AnsibleContent/playbook.yaml"
            uid = str(uuid.uuid4())[:8]
            # build command to run an run it
            cmd = "ansible-playbook {0} --extra-vars 'ownerUserName={1} replSetCount={2} expireon={3}' > /opt/wwwroot/static/output/{1}_cm.txt 2>&1".format(pbPath,username,count, expire)
            subprocess.Popen(cmd, shell=True, cwd="/opt/AnsibleContent",stdout = subprocess.PIPE)
            self.write("Running, "+ username)

class Handler_OM_API_Launch(tornado.web.RequestHandler):
    async def get(self, username):
        password = ""
        expire = "" 
        if self.get_argument("password") != None:
            password = self.get_argument("password")
        if self.get_argument("expire") != None:
            expire = self.get_argument("expire")
            
        if(password == os.environ['APIPW']):
            pbPath = "/opt/AnsibleContent/omPlaybook.yaml"
            uid = str(uuid.uuid4())[:8]
            # build command to run an run it
            cmd = "ansible-playbook {0} --extra-vars 'ownerUserName={1} expireon={2}' > /opt/wwwroot/static/output/{1}_om.txt 2>&1".format(pbPath,username, expire)
            subprocess.Popen(cmd, shell=True, cwd="/opt/AnsibleContent",stdout = subprocess.PIPE)
            self.write("Running, "+ username)

class Handler_API_List(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
    def get(self):
        files = os.listdir("/opt/wwwroot/static/output")
        retDoc = {}
        retDoc["files"] = []
        for f in files:
            retDoc["files"].append(f.split(".txt")[0])
        self.write(json.dumps(retDoc))
        self.set_header("Content-Type", "application/json; charset=UTF-8")

##########
# MAIN
##########

settings = {'default_handler_class':Handler_Main}

app= tornado.web.Application([
    (r"/", Handler_Main),
    (r"/api/helloworld", Handler_API_HelloWorld),
    (r"/api/list", Handler_API_List),
    (r"/api/launchcm/(.*)", Handler_CM_API_Launch),
    (r"/api/launchom/(.*)", Handler_OM_API_Launch),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/css" }),
    (r"/js/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/js" }),
    (r"/output/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/output" }),
    (r"/resources/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/resources" }),
    (r"/_framework/(.*)", web.StaticFileHandler, {"path": "/opt/wwwroot/static/_framework" }),
], **settings)
app.listen(8000)
tornado.ioloop.IOLoop.current().start()