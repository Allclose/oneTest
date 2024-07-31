from readConfig import readConfig
import requests

#获取用户token
def getToken(mobile):
    host = readConfig().readconfig('ENV', 'app')
    body = {
      "mobile": mobile
    }
    headers ={
                "Content-Type": "application/json",
            }
    url = host+"/login"
    res = requests.post(url=url,headers=headers,json=body).json()
    return res['token']
if __name__ == '__main__':
    getToken()
