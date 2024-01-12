import unittest, os,requests,paramunittest,pymysql,time,json
from common import readExcel
from readConfig import readConfig
import urllib.request
#图片二维码识别
from PIL import Image
from pyzbar.pyzbar import decode
#获取本文件名，拼接出数据文件名称

#file_path = os.path.join(r'..\Data',os.path.basename(__file__).split('.')[0]+'.xlsx')
#通过数据文件名称获取到内部login页的数据
path = os.path.join(readConfig().readconfig('PATH','datapath'),os.path.basename(__file__).split('.')[0]+'.xlsx')
excel  = readExcel.readExcel().readexcel(path,sheet_name='Sheet1')
@paramunittest.parametrized(*excel)
class Test_App(unittest.TestCase):
    #参数化获取数据
    def setParameters(self, case_name, new_mobile, new_token,share_path,share_data,inviteCode_path):
        self.case_name = str(case_name)
        self.new_mobile = int(new_mobile)
        self.new_token = str(new_token)
        self.share_path = str(share_path)
        self.share_data = eval(share_data)
        self.inviteCode_path = str(inviteCode_path)
    #执行用例前定义url和headers信息
    @classmethod
    def setUpClass(cls) -> None:
        # 创建数据库连接
        cls.conn = pymysql.connect(
            host='127.0.0.1',  # 连接主机, 默认127.0.0.1
            user='root',  # 用户名
            passwd='132456',  # 密码
            port=3306,  # 端口，默认为3306
            db='mysql',  # 数据库名称
            charset='utf8'  # 字符编码
        )
        # 生成游标对象 cursor
        cls.cursor = cls.conn.cursor()
    @classmethod
    def tearDownClass(cls) -> None:
        del_sql = "DELETE develop.distribution from develop.tbl_users  left join develop.distribution  on distribution.user_id=tbl_users.user_id;"
        cls.cursor.execute(del_sql)
        cls.conn.commit()
        cls.cursor.close()  # 关闭游标
        cls.conn.close()  # 关闭连接
    def setUp(self) -> None:
        # 扫描二维码
        def scan_qrcode(filename="inviteCode.png"):
            # 读取二维码图片
            qrcode_image = Image.open(filename)
            result = decode(qrcode_image)
            # 输出扫描结果
            for code in result:
                return str(code.data.decode("utf-8")).split('/')[-1].split('.')[0]
        #获取邀请码
        inviteCode_sql = "SELECT code,token from develop.users where  mobile  ='13123123123'"
        self.sql_result = self.cursor.execute(inviteCode_sql)
        self.res = self.cursor.fetchone()
        self.inviteCode = self.res[0]
        self.old_token = self.res[1]

        url = readConfig().readconfig('ENV')
        share_path = url+self.share_path
        share_headers = {
                        "Content-Type": "application/json",
                        "token": self.old_token}
        result = requests.post(url=share_path, json=self.share_data, headers=share_headers).json()
        # 获取图片链接
        #判断分享接口是否成功响应
        if int(result["state"]) == 1 and "getHaibaoList" not in self.share_path:
            #self.image_url = img_result['data']['imgUrl']
            self.result_url = eval('result'+self.inviteCode_path)
            #获取的是png结尾的链接
            if self.result_url.split('.')[-1] == 'png':
                # 下载图片
                urllib.request.urlretrieve(self.result_url, "inviteCode.png")
                # 进行图片扫描,获取邀请码
                img_code = scan_qrcode("inviteCode.png")
                #如果解析结果长度不为邀请码的长度5，则是另一种方式的返回：邀请码_pro*.png
                if len(img_code) != 5:
                    self.inviteCode = self.result_url.split('/')[-1].split('_')[0]
                #如果长度为5则是邀请码
                else:
                    self.inviteCode = img_code
            # 如果获取的是shtml结尾的链接,直取码
            elif self.result_url.split('.')[-1] == 'shtml':
                self.inviteCode = self.result_url.split('/')[-1].split('.')[0]
        else:
            ...
    #用例方法，请求接口后提取响应内的state信息进行断言
    def test_dataSend(self):
        path = 'http://dataSend'
        #print(self.inviteCode)
        body = {
                  "Code": self.inviteCode,
                }
        headers = {
            "Content-Type": "application/json",
            "token": self.new_token,
        }
        result = requests.post(url=path, json=body, headers=headers).text
        #print(result)
        # 查询数据库
        check_sql = "select d.* from develop.users u left join develop.distribution d on d.user_id=u.user_id where u.mobile = %s"%self.new_mobile
        time.sleep(7)       #接口有5s的固定延迟处理
        self.cursor.execute(check_sql)  # 返回值是查询到的数据数量
        # 通过 fetchall方法获得数据
        data = self.cursor.fetchone()
        #print('data:'+str(data))
        self.assertEqual(data[6],1)

    def tearDown(self) -> None:
        #self.cursor.execute(del_gxx)
        print(self.case_name)
if __name__ == '__main__':
    #运行本用例
    unittest.main()
