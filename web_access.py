#
#
# Proxy Server for Local Web Server
#
#
#
#
import urllib
import urllib2
import json

import requests
from requests.auth import HTTPDigestAuth

class Web_Client_Interface():
   def __init__( self ):
      pass

   def get_path( self, path="/", user="admin", password="password"):
      if path[0] != '/':
          path = "/"+path
      url = "http://192.168.1.82"+path
      #print "path",path,"url",url
      r = requests.get(url, auth=HTTPDigestAuth(user, password))   
      print "r",r.status_code    
      return { "success":(requests.codes.ok==r.status_code), "status":r.status_code   ,"results": r.text   }

   def post_path( self, path="/", user="admin", password="password",payload = ""):
       if path[0] != '/':
          path = "/"+path
       
       #print "post_path ---->",path,payload
       url = "http://192.168.1.82"+path
       headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
       r = requests.post(url, json=payload , auth=HTTPDigestAuth(user, password), headers=headers)
       return { "success":(requests.codes.ok==r.status_code), "status":r.status_code   ,"results": r.json()   }

if __name__ == "__main__":
   web_client = Web_Client_Interface( )
   print web_client.get_path(path="")
   
   json_object = {}
   json_object["hash_name"] = "CONTROL_VARIABLES"
   json_object["key_list"] = {}
   json_object["key_list"]["rain_day"]  = 0
   x =  json.dumps(json_object)
   print web_client.post_path(path="/ajax/set_redis_hkeys",payload=json.dumps(json_object))


