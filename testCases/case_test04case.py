#单接口测试用例
import unittest, os,requests,paramunittest
from common import readExcel,readYaml
from readConfig import readConfig
#获取本文件名，拼接出数据文件名称
file_name = os.path.basename(__file__).split('.')[0]+'.xlsx'
#通过数据文件名称获取到内部login页的数据
excel  = readExcel.readExcel().readexcel(file_name)
#进行yaml参数化,yaml文件内payload必须为字符串''
yaml_name = os.path.basename(__file__).split('.')[0]+'.yaml'
yaml = readYaml.readYaml().readyaml(yaml_name)
token = readConfig().readconfig(section='HEADERS',option='token')

@paramunittest.parametrized(*yaml)     #参数化后可以单用例函数自行循环取用例进行执行
class Test_Login(unittest.TestCase):
    #执行用例前定义url和headers信息
    def setUp(self) -> None:
        self.url = readConfig().readconfig('ENV')
        self.headers = {
        "Content-Type": "application/json",
        "clientName": "app_mall",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    #参数化获取数据
    def setParameters(self, case_name, path, payload,check):
        self.case_name = str(case_name)
        self.path = str(path)
        self.payload = str(payload)
        self.check = int(check)
    #用例方法，请求接口后提取响应内的state信息进行断言
    def test_01(self):
        all_path = self.url+self.path
        result = requests.post(url=all_path,data=self.payload,headers=self.headers).json()
        self.assertEqual(result['state'],self.check,self.case_name+'————执行失败:'+str(result))

if __name__ == '__main__':
    #运行本用例
    unittest.main()
