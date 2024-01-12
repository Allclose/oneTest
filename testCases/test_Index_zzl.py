from ddt import file_data,ddt,unpack
import requests,json,unittest,os
from readConfig import readConfig
base_name = os.path.basename(__file__).split('.')[0]+'.yaml'
@ddt
class Test_Index(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.env_url = readConfig().readconfig('ENV')
        cls.headers = {
            "Content-Type":"application/json",
            "token":readConfig().readconfig('HEADERS','token'),
            "clientName":"app_mall"
        }
    @classmethod
    def tearDownClass(cls) -> None:
        print('【首页】模块测试结束')

    @file_data(os.path.join(r'..\Data',base_name))
    def test_index(self,case_name,method,path,payload=None,check=1,assert_src=None):
        if method == 'GET':
            res = requests.get(url=self.env_url+path,headers=self.headers).json()
        else:
            res = requests.post(url=self.env_url + path,json=payload,headers=self.headers).json()
        exec(assert_src)

if __name__ == '__main__':
    #运行本用例
    unittest.main()
