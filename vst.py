import requests
import requests.packages.urllib3
#from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
#class MyAuth():#requests.auth.AuthBase
#    def __call__(self, r):
#        return r
#values = {'username': '',
#          'password': ''}
#basicAuthCredentials = ('username', 'password')
try :
    url="https://facebook.com"#"https://icm.ad.msft.net/imp/v3/incidents/search/advanced"#"https://dev.azure.com/RD/_apis/wit/workitems?ids=15191737&api-version=5.0"           ##"https://icm.ad.msft.net"
    tfs=requests.get(url,verify=False)#HTTPBasicAuth('user', 'pass'))
    #tfs=response.json()
    if tfs.status_code == 401:                                #response 401 is for unauthorized
        print("authentication is required")
    #elif tfs.status_code == 200:                              #200 is for request successful
    #    print("request is succeeded")
    else:
        print (tfs)
except Exception as ex:
    print(ex)

      # Implement my authentication
