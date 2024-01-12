import os,time,unittest,requests
from configparser import ConfigParser
from readConfig import readConfig
from XTestRunner import SMTP,HTMLTestRunner
import pymysql
#调度
# import pythoncom
# from apscheduler.schedulers.blocking import BlockingScheduler

class RunTest:
    def __init__(self):

        # 创建数据库连接
        conn = pymysql.connect(
            host='127.0.0.1',  # 连接主机, 默认127.0.0.1
            user='root',  # 用户名
            passwd='121516',  # 密码
            port=3306,  # 端口，默认为3306
            db='mysql',  # 数据库名称
            charset='utf8'  # 字符编码
        )
        # 生成游标对象 cursor
        cursor = conn.cursor()
        #查库取token
        token_sql = "SELECT token from develop.users where  mobile  ='13123123123';"
        cursor.execute(token_sql)
        token = cursor.fetchone()[0]
        # 获取前置配置信息
        config = ConfigParser()
        config.read('config.ini')
        projectPath = os.path.split(os.path.realpath(__file__))[0]
        config.set('PATH', 'projectpath', projectPath)
        config.set('PATH', 'datapath', os.path.join(projectPath,'Data\App'))
        config.set('HEADERS', 'token', str(token))
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        # 此时的配置保存在内存中，需要写入文件方可生效
        with open("config.ini", "w+") as f:
            config.write(f)
        self.email_open = readConfig().readconfig('EMAIL','open')
        self.casepath = os.path.join(projectPath, 'testCases')
        self.report = os.path.join(os.path.join(projectPath, 'Report'),"自动化测试报告_"+str(time.strftime('%Y_%m_%d_%H_%M_%S'))+".html")
        #print(self.report)
        #self.run()
    #推送报告到企业微信
    def push_wechat(self):
        # 获取WEBHOOK地址和access_token
        try:
            webhook_url = os.environ['webhook']
        except:
            webhook_url = readConfig().readconfig('HEADERS', 'webhook')
        #print(webhook_url)
        #如果webhook不为空则继续推送
        if webhook_url:
            #上传文件获取media_id
            key = webhook_url.split('=')[-1]
            file_upload_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key="+key+"&type=file"
            report_name = self.report.split('\\')[-1]
            headers = {"Content-Type": "multipart/form-data"}
            # 上传文件
            with open(self.report, "rb") as f:
                files = {"file": (report_name, f.read())}
                response = requests.post(file_upload_url, headers=headers, files=files).json()
            # 发送消息,获取上传文件后的media_id
            try:
                message = {
                "msgtype": "file",
                "file": {
                    "media_id": str(response["media_id"])
                 }
                }
                headers_up = {"Content-Type": "application/json"}
                # 直接调用webhook
                requests.post(webhook_url, json=message, headers=headers_up).json()
            except Exception as e:
                print("push_wechat发送消息报错：" + str(e))
    def run(self,option):
        suite = unittest.TestSuite()
        #依次加载所有用例
        '''self.case_list = readConfig().readconfig('CASES', option).split(',')
        for case in self.case_list:
            if not case.startswith('#'):
                discover = unittest.defaultTestLoader.discover(start_dir=self.casepath,pattern=case)
                suite.addTest(discover)'''
        print(readConfig().readconfig('CASES'))
        #获取环境变量内的option值，配合Jenkins内参数
        #option = os.environ['option']
        #通过输入来获取不同的用例捕捉规则pattern，据此执行不同批用例
        pattern = readConfig().readconfig('CASES', option)
        discover = unittest.defaultTestLoader.discover(start_dir=self.casepath, pattern=pattern)
        suite.addTests(discover)
        #如果用例集不为空则运行本次测试
        if suite:
            with open(self.report,'wb') as fp:
                runner = HTMLTestRunner(
                    tester='测试组',
                    stream=fp,
                    title=str(time.strftime('%Y_%m_%d_%H'))+'_接口测试报告',
                    description='接口自动化报告',
                    language='zh-CN')
                runner.run(testlist=suite)
        #邮件推送测试报告
        try:
            to = os.environ["email"]
            if to:
                user = readConfig().readconfig('EMAIL', 'user')
                password = readConfig().readconfig('EMAIL', 'password')
                host = readConfig().readconfig('EMAIL', 'host')
                # 发邮件功能
                # 使用ssl时应关闭tls
                smtp = SMTP(user=user, password=password, host=host,tls=False)
                smtp.sender(to=to, subject=str(time.strftime('%Y_%m_%d_%H_%M_%S'))+"_测试报告", attachments=self.report)
        except:
            if self.email_open == 'on':
                user = readConfig().readconfig('EMAIL', 'user')
                password = readConfig().readconfig('EMAIL', 'password')
                host = readConfig().readconfig('EMAIL', 'host')
                to = readConfig().readconfig('EMAIL', 'to')
                # 发邮件功能
                # 使用ssl时应关闭tls
                smtp = SMTP(user=user, password=password, host=host, tls=False)
                smtp.sender(to=to, subject="自动化测试报告_"+str(time.strftime('%Y_%m_%d_%H_%M_%S')), attachments=self.report)
        #将报告发送至企业微信群
        self.push_wechat()
        return self.report

if __name__ == '__main__':
    print('首次运行获取本地环境路径信息，请再次运行')
    try:
        #根据传入不同的pattern值执行不同批用例
        RunTest().run(os.environ['option'])
        # 调度运行
        '''pythoncom.CoInitialize()
        scheduler = BlockingScheduler()
        # 每周一到周五的14：50分执行RunTest().run
        scheduler.add_job(RunTest().run, 'cron', day_of_week='1-5', hour=9, minute=13)
        scheduler.start()'''
    except:
        RunTest().run('*')