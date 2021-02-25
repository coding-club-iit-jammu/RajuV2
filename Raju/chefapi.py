import requests
import json
import time
import os

class ChefAPI:
    CODECHEF_URL = "https://api.codechef.com"
    CHEF_CREDS = {}

    @staticmethod   
    def chefAuthorize():
        """
        Get Authorization Token
        """
        print("calling to get access token")
        #global CHEF_CREDS, CODECHEF_URL
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        body = {
            "grant_type" : "client_credentials",
            "scope" : "public",
            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET
        }
        URL = f"{ChefAPI.CODECHEF_URL}/oauth/token"
        res = requests.post(url = URL, json= body)
        #Response validation
        if(res.status_code != 200):
            return "some error occured in request"
        res_content = json.loads(res.content)
        if(res_content['status'] != 'OK'):
            return "Invalid creds"
        ChefAPI.CHEF_CREDS['time'] =  int(time.time())
        ChefAPI.CHEF_CREDS['accessToken'] = res_content['result']['data']['access_token']
        with open('chefCredentials.json', 'w', encoding='utf-8') as chefFile:
            json.dump(ChefAPI.CHEF_CREDS, chefFile, ensure_ascii=False, indent=4)
        return "OK"
    
    @staticmethod
    def getAccessToken():
        if(ChefAPI.CHEF_CREDS.get('accessToken',-1) != -1):
            if( (int(time.time()) - ChefAPI.CHEF_CREDS.get('time',0)) < 3300 ):
                return ChefAPI.CHEF_CREDS['accessToken']
            if( ChefAPI.chefAuthorize() == "OK"):
                return ChefAPI.CHEF_CREDS['accessToken']
        try:
            chefFile = open('chefCredentials.json','r')
            ChefAPI.CHEF_CREDS = json.loads(chefFile.read()) 
            chefFile.close()
            if( (int(time.time()) - ChefAPI.CHEF_CREDS.get('time',0)) < 3300):
                return ChefAPI.CHEF_CREDS['accessToken']
        except IOError:
            "File not exist"
        if(ChefAPI.chefAuthorize() == "OK"):
            return ChefAPI.CHEF_CREDS['accessToken']

    def chefReq(self, method:str, url:str, params:dict = None, headers:dict= {}):
        headers['Authorization'] = f'Bearer {ChefAPI.getAccessToken()}'
        res = requests.request(method=method, url=url, params=params, headers = headers)
        if(res.status_code != 200):
            return None
        res_dict = json.loads(res.content)
        return res_dict['result']

    def getContest(self, status:str = 'future', limit:int = 3):
        contest_url = f'{ChefAPI.CODECHEF_URL}/contests'
        params = {
            'status' : status,
            'limit' : limit,
            'sortOrder' : 'asc'
        }
        res = self.chefReq(method='get', url=contest_url, params=params)
        if(res is None):
            return None
        return res['data']['content']
