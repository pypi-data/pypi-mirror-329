import json
import sys
import nbformat
import subprocess
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from notebook.base.handlers import IPythonHandler
from maap.maap import MAAP
import functools
import os
import xml.etree.ElementTree as ET
import xmltodict
import logging
import requests
import yaml
import time
import urllib.parse
import re
import maap_jupyter_server_extension.constants as constants

logging.basicConfig(format='%(asctime)s %(message)s')

@functools.lru_cache(maxsize=128)
def get_maap_config(host):
    api_host = os.getenv("MAAP_API_HOST", constants.DEFAULT_API)
    maap_api_config_endpoint = os.getenv("MAAP_API_CONFIG_ENDPOINT", "api/environment/config")
    ade_host = host if host in constants.ADE_OPTIONS else os.getenv("MAAP_ADE_HOST", constants.DEFAULT_ADE)
    environments_endpoint = "https://" + api_host + "/" + maap_api_config_endpoint + "/"+urllib.parse.quote(urllib.parse.quote("https://", safe=""))+ade_host
    return requests.get(environments_endpoint).json()

def maap_api(host):
    return get_maap_config(host)['api_server']

def maap_ade_url(host):
	return 'https://{}'.format(get_maap_config(host)['ade_server'])

def maap_api_url(host):
	return 'https://{}'.format(get_maap_config(host)['api_server'])

def dps_bucket_name(host):
	return get_maap_config(host)['workspace_bucket']

def get_kibana_url(host):
	return get_maap_config(host)['kibana_url']


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyter-server-extension/get_example endpoint!!"
        }))


class KibanaConfigHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        url = get_kibana_url(maap_api(self.request.host))
        print(url)
        self.finish({"KIBANA_URL": url})


class MAAPConfigEnvironmentHandler(APIHandler):
    def get(self):  
        env = get_maap_config(self.request.host)
        self.finish(env)

class WorkspaceContainerHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        dockerimage_path_default = os.getenv('DOCKERIMAGE_PATH_DEFAULT')
        dockerimage_path_base_image = os.getenv("DOCKERIMAGE_PATH_BASE_IMAGE")
        self.finish({"DOCKERIMAGE_PATH_DEFAULT": dockerimage_path_default, "DOCKERIMAGE_PATH_BASE_IMAGE": dockerimage_path_base_image})


class RouteTest1Handler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyter-server-extension/maapsec_test endpoint!"
        }))


######################################
######################################
#
# DPS
#
######################################
######################################


class ListAlgorithmsHandler(IPythonHandler):
    @tornado.web.authenticated
    def get(self):
        print("In python list algos handler")

        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            print("Making query from backend.")
            r = maap.listAlgorithms()
            self.finish({"status_code": r.status_code, "response": r.json()})
        except:
            print("Failed list algorithms query.")
            self.finish({"status": r})


class DescribeAlgorithmsHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.describeAlgorithm(self.get_argument("algo_id"))
            o = xmltodict.parse(r.text)
            self.finish({"status_code": r.status_code, "response": json.dumps(o)})
        except:
            print("Failed describe algorithms query.")
            self.finish()


class GetQueuesHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()
        try:
            r = maap.getQueues()
            resp = json.loads(r.text)
            # result = [e[len('maap-worker-'):] for e in resp['queues'] if 'maap-worker' in e]
            result = resp['queues']
            self.finish({"status_code": r.status_code, "response": result})
        except:
            self.finish({"status_code": r.status_code, "response": r.text})


class GetCMRCollectionsHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.searchCollection()
            # Query returns a list -- not an object
            self.finish({"response": r})
        except Exception as e:
            print("Failed collections query: ")
            self.finish({"error": e})


class ListUserJobsHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.listJobs(page_size=200)
            self.finish({"status_code": r.status_code, "response": r.json()})
        except Exception as e:
            print("Failed list jobs query: {e}")
            self.finish()


class SubmitJobHandler(IPythonHandler):
    def args_to_dict(self):
        # convert args to dict
        params = self.request.arguments
        for k, v in params.items():
            params[k] = v[0].decode("utf-8")
        return params

    def get(self):
        print("JOB SUBMIT")

        kwargs = self.args_to_dict()
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()
        resp = maap.submitJob(**kwargs)
        #logger.debug(resp)
        
        # status_code = resp['http_status_code']
        status_code = resp.response_code
        job_id = resp.id
        if status_code == 200:
            result = 'JobID is {}'.format(job_id)
            self.finish({"status_code": status_code, "response": result})
        elif status_code == 400:
            self.finish({"status_code": status_code, "response": resp['result']})
        else:
            self.finish({"status_code": status_code, "response": resp['status']})



class CancelJobHandler(IPythonHandler):
    def get(self):
        maap = MAAP()
        response = ""
        exception_code = ""

        job_id = self.get_argument("job_id")

        if job_id is None:
            response = "Failed to cancel job: No job ID submitted."
            self.finish({"status_code": 400, "response": response})
        
        r = maap.cancelJob(job_id)
        root = ET.fromstring(r)
        rootTag = root.tag.split("}")[1]

        # Successful cancel will contain a 'StatusInfo' node. 
        if rootTag == "StatusInfo":
            response = "Job with ID {} was successfully cancelled.".format(job_id)

        # Unsuccessful cancel will contain an 'ExceptionReport' node.
        if rootTag == "ExceptionReport":
            exception_text = root.find('.//{http://www.opengis.net/ows/2.0}ExceptionText').text
            exception_code = root.find('.//{http://www.opengis.net/ows/2.0}Exception').attrib.get('exceptionCode')

            if exception_text:
                response = "Failed to cancel job with ID {}: ".format(job_id) + exception_text

        self.finish({"status_code": 200, "response": {"response": response, "exception_code": exception_code}})


class GetJobStatusHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.getJobStatus(self.get_argument("job_id"))
            o = xmltodict.parse(r.text)
            print("job status response:")
            print(r)
            self.finish({"status_code": r.status_code, "response": json.dumps(o)})
        except:
            print("Failed job status query.")
            self.finish()


class GetJobResultHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.getJobResult(self.get_argument("job_id"))
            o = xmltodict.parse(r.text)
            print("job result response:")
            print(r)
            self.finish({"status_code": r.status_code, "response": json.dumps(o)})
        except:
            print("Failed job result query.")
            self.finish()


class RegisterWithFileHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            config_file = self.get_argument("file")
            r = maap.register_algorithm_from_yaml_file(config_file)
            r.raise_for_status()
            print(r.text)
            self.finish({"status_code": r.status_code, "response": r.text})
        except:
            print("Failed to register.")
            self.finish()





class GetJobMetricsHandler(IPythonHandler):
    def get(self):
        #maap = MAAP(not_self_signed=False)
        maap = MAAP()

        try:
            r = maap.getJobMetrics(self.get_argument("job_id"))
            o = xmltodict.parse(r.text)
            print("job result response:")
            print(r)
            self.finish({"status_code": r.status_code, "response": json.dumps(o)})
        except:
            print("Failed job result query.")
            self.finish()


######################################
######################################
#
# EDSC
#
######################################
######################################

class GetGranulesHandler(IPythonHandler):
    def printUrls(self, granules):
        url_list = '[\n'
        for res in granules:
            if res.getDownloadUrl():
                url_list = url_list + '\'' + res.getDownloadUrl() + '\',\n'
        url_list = url_list + ']'
        return url_list

    def get(self):
        maap = MAAP()
        cmr_query = self.get_argument('cmr_query', '')
        limit = str(self.get_argument('limit', ''))
        print("cmr_query", cmr_query)

        query_string = maap.getCallFromCmrUri(cmr_query, limit=limit)
        granules = eval(query_string)
        query_result = self.printUrls(granules)
        try:
            print("Response is: ", query_result)
        except:
            print("Could not print results")
        self.finish({"granule_urls": query_result})


class GetQueryHandler(IPythonHandler):
    def get(self):
        maap = MAAP()
        cmr_query = self.get_argument('cmr_query', '')
        limit = str(self.get_argument('limit', ''))
        query_type = self.get_argument('query_type', 'granule')
        print("cmr_query", cmr_query)

        query_string = maap.getCallFromCmrUri(cmr_query, limit=limit, search=query_type)
        print("Response is: ", query_string)
        self.finish({"query_string": query_string})


class IFrameHandler(IPythonHandler):
    def initialize(self, welcome=None, sites=None):
        self.sites = sites
        self.welcome = welcome

    def get(self):
        self.finish(json.dumps({'welcome': self.welcome or '', 'sites': self.sites}))


class IFrameProxyHandler(IPythonHandler):
    def get(self):
        url = self.request.get_argument('url', '')
        if url:
            self.finish(requests.get(url, headers=self.request.headers).text)
        else:
            self.finish('')


######################################
######################################
#
# MAAPSEC
#
######################################
######################################

# class MaapEnvironmentHandler(IPythonHandler):
#     def get(self, **params):  
#         env = get_maap_config(self.request.host)
#         self.finish(env)

# class MaapLoginHandler(IPythonHandler):
#     def get(self, **params):
#         try:    
#             param_ticket = self.request.query_arguments['ticket'][0].decode('UTF-8')     
#             param_service = self.request.query_arguments['service'][0].decode('UTF-8') 
#             env = get_maap_config(self.request.host)
#             print("More testing")
#             print(env)
#             auth_server = 'https://{auth_host}/cas'.format(auth_host=env['auth_server'])

#             url = '{base_url}/p3/serviceValidate?ticket={ticket}&service={service}&pgtUrl={base_url}&state='.format(
#                 base_url=auth_server, ticket=param_ticket, service=param_service)

#             print('auth url: ' + url)

#             auth_response = requests.get(
#                 url, 
#                 verify=False
#             )

#             print('auth response:')
#             print(auth_response)

#             xmldump = auth_response.text.strip()
            
#             print('xmldump:')
#             print(xmldump)

#             is_valid = True if "cas:authenticationSuccess" in xmldump or \
#                             "cas:proxySuccess" in xmldump else False

#             if is_valid:
#                 tree = ElementTree(fromstring(xmldump))
#                 root = tree.getroot()

#                 result = {}
#                 for i in root.iter():
#                     if "PGTIOU" in i.tag:
#                         continue
#                     result[i.tag.replace("cas:", "").replace("{http://www.yale.edu/tp/cas}", "")] = i.text

#                 self.finish({"status_code": auth_response.status_code, "attributes": json.dumps(result)})
#             else:
#                 self.finish({"status_code": 403, "response": xmldump, "json_object": {}})
            
#         except ValueError:
#             self.finish({"status_code": 500, "result": auth_response.reason, "json_object": {}})

#     def _get_cas_attribute_value(self, attributes, attribute_key):

#         if attributes and "cas:" + attribute_key in attributes:
#             return attributes["cas:" + attribute_key]
#         else:
#             return ''


######################################
######################################
#
# User Workspace Management
#
######################################
######################################

class InjectKeyHandler(IPythonHandler):
    def get(self):
        public_key = self.get_argument('key', '')

        if public_key:
            print("=== Injecting SSH KEY ===")

            # Check if .ssh directory exists, if not create it
            os.chdir('/projects')
            if not os.path.exists(".ssh"):
                os.makedirs(".ssh")

            # Check if authorized_keys file exits, if not create it
            if not os.path.exists(".ssh/authorized_keys"):
                with open(".ssh/authorized_keys", 'w'):
                    pass

            # Check if key already in file
            with open('.ssh/authorized_keys', 'r') as f:
                linelist = f.readlines()

            found = False
            for line in linelist:
                if public_key in line:
                    print("Key already in authorized_keys")
                    found = True

            # If not in file, inject key into authorized keys
            if not found:
                cmd = "echo " + public_key + " >> .ssh/authorized_keys && chmod 700 /projects && chmod 700 .ssh/ && chmod 600 .ssh/authorized_keys"
                print(cmd)
                subprocess.check_output(cmd, shell=True)
                print("=== INJECTED KEY ===")
            else:
                print("=== KEY ALREADY PRESENT ===")

class InjectPGTHandler(IPythonHandler):
    def get(self):
        print("=== Checking for existence of MAAP_PGT ===")

        proxy_granting_ticket = self.get_argument('proxyGrantingTicket', '')

        if proxy_granting_ticket:
            print("=== MAAP_PGT found. Adding variable to environment ===")
            os.environ["MAAP_PGT"] = proxy_granting_ticket
        else:
            print("=== No MAAP_PGT found ===")


class GetSSHInfoHandler(IPythonHandler):
    """
    Get ssh information for user - IP and Port.
    Port comes from querying the kubernetes API
    """
    def get(self):

        try:
            svc_host = os.environ.get('KUBERNETES_SERVICE_HOST')
            svc_host_https_port = os.environ.get('KUBERNETES_SERVICE_PORT_HTTPS')
            namespace = os.environ.get('CHE_WORKSPACE_NAMESPACE') + '-che'
		
	    # Replicate Che's namespace converter policy
            # by substituting any non-alphanumeric characters with hyphens.
            namespace = re.sub(r"[^0-9a-zA-Z-]+", "-", namespace)
		
            che_workspace_id = os.environ.get('CHE_WORKSPACE_ID')
            sshport_name = 'sshport'

            ip = requests.get('https://api.ipify.org').text

            with open ("/var/run/secrets/kubernetes.io/serviceaccount/token", "r") as t:
                token=t.read()

            headers = {
                'Authorization': 'Bearer ' + token,
            }

            request_string = 'https://' + svc_host + ':' + svc_host_https_port + '/api/v1/namespaces/' + namespace +  '/services/'
            response = requests.get(request_string, headers=headers, verify=False)
            data = response.json()
            endpoints = data['items']

            # Ssh service is running on a seperate container from the user workspace. Query the kubernetes host service to find the container where the nodeport has been set.
            for endpoint in endpoints:
                if sshport_name in endpoint['metadata']['name']:
                    if che_workspace_id == endpoint['metadata']['labels']['che.workspace_id']:
                        port = endpoint['spec']['ports'][0]['nodePort']
                        self.finish({'ip': ip, 'port': port})

            self.finish({"status": 500, "message": "failed to get ip and port"})
        except:
            self.finish({"status": 500, "message": "failed to get ip and port"})


class Presigneds3UrlHandler(IPythonHandler):

    def get(self):
        # get arguments
        bucket = dps_bucket_name(self.request.host)
        key = self.get_argument('key', '')
        rt_path = os.path.expanduser(self.get_argument('home_path', ''))
        abs_path = os.path.join(rt_path, key)
        proxy_ticket = self.get_argument('proxy-ticket','')
        expiration = self.get_argument('duration','86400') # default 24 hrs
        che_ws_namespace = os.environ.get('CHE_WORKSPACE_NAMESPACE')

        print('bucket is '+bucket)     
        print('key is '+key)        
        print('full path is '+abs_path) 

        # -----------------------
        # Checking for bad input
        # -----------------------
        # if directory, return error - dirs not supported
        if os.path.isdir(abs_path):
            self.finish({"status_code": 412, "message": "error", "url": "Presigned S3 links do not support folders"})
            return

        # check if file in valid folder (under mounted folder path)
        resp = subprocess.check_output("df -h | grep s3fs | awk '{print $6}'", shell=True).decode('utf-8')
        mounted_dirs = resp.strip().split('\n')
        print(mounted_dirs)
        if len(mounted_dirs) == 0:
            self.finish({"status_code": 412, "message": "error",
                "url": "Presigned S3 links can only be created for files in a mounted org or user folder" +
                    "\nMounted folders include:\n{}".format(resp)
                })
            return

        if not any([mounted_dir in abs_path for mounted_dir in mounted_dirs]):
            self.finish({"status_code": 412, "message": "error",
                "url": "Presigned S3 links can only be created for files in a mounted org or user folder" +
                    "\nMounted folders include:\n{}".format(resp)
                })
            return

        # -----------------------
        # Generate S3 Link
        # -----------------------
        # if valid path, get presigned URL
        # expiration = '43200' # 12 hrs in seconds
        print('expiration is {} seconds', expiration)

        url = '{}/api/members/self/presignedUrlS3/{}/{}?exp={}&ws={}'.format(maap_api_url(self.request.host), bucket, key, expiration, che_ws_namespace)
        headers = {'Accept': 'application/json', 'proxy-ticket': proxy_ticket}
        r = requests.get(
            url,
            headers=headers,
            verify=False
        )
        print(r.text)

        resp = json.loads(r.text)   
        self.finish({"status_code":200, "message": "success", "url":resp['url']})


class CreateFileHandler(IPythonHandler):
    def get(self):

        file_name = self.get_argument("fileName")
        data = self.get_argument("data")
        path_name = self.get_argument("pathName", "")

        algo = json.loads(data)
        if path_name:
            try:
                if not os.path.exists(os.getcwd() + '/' + path_name):
                    print("Attempting to create folder")
                    os.makedirs(os.getcwd() + '/' + path_name)
                file_name = path_name + '/' + file_name
            except:
                # If failed to create folder, file_path will put the new file in the current directory
                print("Failed to create folder")

        try:
            print("Attempting to create file.")
            with open(file_name, 'w') as f:
                yaml.dump(algo, f)
                file_path = os.getcwd() + '/' + file_name
                print(file_path)
                while not os.path.exists(file_path):
                    time.sleep(1)
                self.finish({"file": file_path})
        except:
            print("Failed to create file.")
            self.finish()

class AccountInfoHandler(IPythonHandler):
    def get(self):
        proxy_granting_ticket = self.get_argument('proxyGrantingTicket', '')
        
        maap = MAAP()
        profile = maap.profile.account_info(proxy_ticket = proxy_granting_ticket)
        self.finish({"profile": profile})

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]


    # USER WORKSPACE MANAGEMENT
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "uwm", "injectPublicKey"), InjectKeyHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "uwm", "injectPGT"), InjectPGTHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "uwm", "getSSHInfo"), GetSSHInfoHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "uwm", "getSignedS3Url"), Presigneds3UrlHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "uwm", "getAccountInfo"), AccountInfoHandler)])


    # DPS
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "get_example"), RouteHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getKibanaUrl"), KibanaConfigHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getConfig"), MAAPConfigEnvironmentHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getWorkspaceContainer"), WorkspaceContainerHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "createFile"), CreateFileHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "listAlgorithms"), ListAlgorithmsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "describeAlgorithms"), DescribeAlgorithmsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getQueues"), GetQueuesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getCMRCollections"), GetCMRCollectionsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "listUserJobs"), ListUserJobsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "submitJob"), SubmitJobHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getJobStatus"), GetJobStatusHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getJobResult"), GetJobResultHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "getJobMetrics"), GetJobMetricsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "cancelJob"), CancelJobHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "registerUsingFile"), RegisterWithFileHandler)])


    # EDSC
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "edsc", "getGranules"), GetGranulesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "edsc", "getQuery"), GetQueryHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, "jupyter-server-extension", "edsc"), IFrameHandler, {'welcome': "Hello MAAP user"}), (url_path_join(base_url, 'jupyter-server-extension/edsc/proxy'), IFrameProxyHandler)])

    web_app.add_handlers(host_pattern, handlers)
    
