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
        node_agentVersion= ""
        node_key_name= ""
        node_instance_type= ""
        om_ansible_python_interpreter= ""
        om_key_name= ""
        ansible_ssh_private_key_file= ""
        ansible_python_interpreter=""
        node_rootURL= ""
        node_mmsGroupId= ""
        node_mmsApiKey= ""
        disk_size= ""


        if self.get_argument("password") != None:
            password = self.get_argument("password")
        if self.get_argument("count") != None:
            count = self.get_argument("count")
        if self.get_argument("node_agentVersion") != None:
            node_agentVersion = self.get_argument("node_agentVersion")
        if self.get_argument("node_key_name") != None:
            node_key_name = self.get_argument("node_key_name")
        if self.get_argument("node_instance_type") != None:
            node_instance_type = self.get_argument("node_instance_type")
        if self.get_argument("ansible_ssh_private_key_file") != None:
            ansible_ssh_private_key_file = self.get_argument("ansible_ssh_private_key_file")
        if self.get_argument("ansible_python_interpreter") != None:
            ansible_python_interpreter = self.get_argument("ansible_python_interpreter")
        if self.get_argument("node_rootURL") != None:
            node_rootURL = self.get_argument("node_rootURL")
        if self.get_argument("node_mmsGroupId") != None:
            node_mmsGroupId = self.get_argument("node_mmsGroupId")
        if self.get_argument("node_mmsApiKey") != None:
            node_mmsApiKey = self.get_argument("node_mmsApiKey")
        if self.get_argument("disk_size") != None:
            disk_size = self.get_argument("disk_size")
        if self.get_argument("expire") != None:
            expire = self.get_argument("expire")

        if((node_mmsGroupId == "") and (node_mmsApiKey == "")):
            with open('/opt/AnsibleContent/deployConfig.json', 'r') as myfile:
                deployConfigContents=myfile.read()
                deployConfig = json.loads(deployConfigContents)
                node_mmsGroupId = deployConfig["node_mmsGroupId"]
                node_mmsApiKey = deployConfig["node_mmsApiKey"]
            
        if(password == os.environ['APIPW']):
            pbPath = "/opt/AnsibleContent/playbook.yaml"
            uid = str(uuid.uuid4())[:8]
            # build command to run an run it
            # mad security
            cmd = "ansible-playbook {0} --extra-vars 'ownerUserName={1} node_replSetCount={2} node_expireon={3} node_agentVersion={4} node_key_name={5} node_instance_type={6} ansible_ssh_private_key_file={7} ansible_python_interpreter={8} node_rootURL={9} node_mmsGroupId={10} node_mmsApiKey={11} node_disk_size={12}' > /opt/wwwroot/static/output/{1}_cm.txt 2>&1".format(pbPath,username,count, expire, node_agentVersion,node_key_name,node_instance_type,ansible_ssh_private_key_file,ansible_python_interpreter,node_rootURL,node_mmsGroupId,node_mmsApiKey,disk_size)
            subprocess.Popen(cmd, shell=True, cwd="/opt/AnsibleContent",stdout = subprocess.PIPE)
            self.write("Running, "+ username)

class Handler_OM_API_Launch(tornado.web.RequestHandler):
    async def get(self, username):
        password = ""
        expire = "" 
        node_agentVersion= ""
        node_key_name= ""
        node_instance_type= ""
        om_ansible_python_interpreter= ""
        om_key_name= ""
        ansible_ssh_private_key_file= ""
        ansible_python_interpreter=""
        node_rootURL= ""
        node_mmsGroupId= ""
        node_mmsApiKey= ""
        disk_size= ""


        if self.get_argument("password") != None:
            password = self.get_argument("password")
        if self.get_argument("node_agentVersion") != None:
            node_agentVersion = self.get_argument("node_agentVersion")
        if self.get_argument("node_key_name") != None:
            node_key_name = self.get_argument("node_key_name")
        if self.get_argument("node_instance_type") != None:
            node_instance_type = self.get_argument("node_instance_type")
        if self.get_argument("ansible_ssh_private_key_file") != None:
            ansible_ssh_private_key_file = self.get_argument("ansible_ssh_private_key_file")
        if self.get_argument("ansible_python_interpreter") != None:
            ansible_python_interpreter = self.get_argument("ansible_python_interpreter")
        if self.get_argument("node_rootURL") != None:
            node_rootURL = self.get_argument("node_rootURL")
        if self.get_argument("node_mmsGroupId") != None:
            node_mmsGroupId = self.get_argument("node_mmsGroupId")
        if self.get_argument("node_mmsApiKey") != None:
            node_mmsApiKey = self.get_argument("node_mmsApiKey")
        if self.get_argument("disk_size") != None:
            disk_size = self.get_argument("disk_size")
        if self.get_argument("password") != None:
            password = self.get_argument("password")
        if self.get_argument("expire") != None:
            expire = self.get_argument("expire")
        if self.get_argument("om_key_name") != None:
            om_key_name = self.get_argument("om_key_name")
        if self.get_argument("om_ansible_python_interpreter") != None:
            om_ansible_python_interpreter = self.get_argument("om_ansible_python_interpreter")
            
        if(password == os.environ['APIPW']):
            pbPath = "/opt/AnsibleContent/omPlaybook.yaml"
            uid = str(uuid.uuid4())[:8]
            # build command to run an run it
            cmd = "ansible-playbook {0} --extra-vars 'ownerUserName={1} node_replSetCount={2} om_expireon={3} node_agentVersion={4} node_key_name={5} node_instance_type={6} ansible_ssh_private_key_file={7} ansible_python_interpreter={8} node_rootURL={9} node_mmsGroupId={10} node_mmsApiKey={11} om_disk_size={12} om_key_name={13} om_ansible_python_interpreter={14}' > /opt/wwwroot/static/output/{1}_om.txt 2>&1".format(pbPath,username,"", expire, node_agentVersion,node_key_name,node_instance_type,ansible_ssh_private_key_file,ansible_python_interpreter,node_rootURL,node_mmsGroupId,node_mmsApiKey,disk_size,om_key_name,om_ansible_python_interpreter)

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