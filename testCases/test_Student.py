from ddt import file_data,ddt
import requests,unittest,os,ddt
from readConfig import readConfig
base_name = os.path.basename(__file__).split('.')[0]+'.yaml'
type = ['',1,2]
@ddt.ddt
class Test_Student(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.env_url = readConfig().readconfig('ENV','student')
        cls.headers = {
            "Content-Type":"application/json",
            "token":readConfig().readconfig('HEADERS','token')
        }
    @classmethod
    def tearDownClass(cls) -> None:
        print('测试完成')
    #约课课程列表
    def test_0_page(self):
        url = self.env_url+'/student'
        params = {
            "pageNum": 1,
            "pageSize": 5
        }
        res = requests.get(url,params=params).json()
        self.assertEqual(res['code'],1)
        self.assertTrue(res['data']['rows'])
        global class_id
        class_id = res['data']['rows'][0]['id']
        #print(res)
    #课程详情
    def test_1_detail(self):
        url = self.env_url + '/detail'
        params = {
            'id':class_id
        }
        res = requests.get(url,params=params).json()
        self.assertEqual(res['code'], 1)
        #print(res)
    #数量
    def test_2_courseStageDetail(self):
        url = self.env_url + '/StageDetail'
        params = {
            'id':class_id
        }
        res = requests.get(url,params=params).json()
        self.assertEqual(res['code'], 1)
        #print(res)
    #约课列表,type:空-全部/1-正式课/2-公开课
    @ddt.data(*type)
    def test_3_coursepage(self,type):
        url = self.env_url + '/page'
        params = {
            'type': type,
            'pageNum': 1,
            'pageSize': 5,
        }
        res = requests.get(url,params=params).json()
        self.assertEqual(res['code'], 1)

if __name__ == '__main__':
    #运行本用例
    unittest.main()
