import os,time,unittest,requests,pymysql,time
from configparser import ConfigParser
from readConfig import readConfig
from XTestRunner import SMTP,HTMLTestRunner
from common.searchData import getToken

class RunTest:
    def __init__(self):
        self.setup_config()
        self.email_open = readConfig().readconfig('EMAIL', 'open')
        self.casepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testCases')
        self.report = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Report',
                                   f"自动化测试报告_{time.strftime('%Y_%m_%d_%H_%M_%S')}.html")
    #数据库连接和获取 token
    def setup_config(self):
        token = getToken(15263277047)
        config = ConfigParser()
        config.read('config.ini', encoding='utf-8')
        projectPath = os.path.dirname(os.path.realpath(__file__))
        config.set('PATH', 'projectpath', projectPath)
        config.set('PATH', 'datapath', os.path.join(projectPath, 'Data\App'))
        config.set('HEADERS', 'token', str(token))
        #统计运行次数
        try:
            env = os.environ['option']
        except:
            count = int(readConfig().readconfig('RUN_DATA', 'count')) + 1
            config.set('RUN_DATA', 'count', str(count))
        with open("config.ini", "w+") as f:
            config.write(f)
    #推送报告到企业微信
    def push_wechat(self):
        # 获取WEBHOOK地址和access_token
        try:
            webhook_url = os.environ['webhook']
        except:
            #webhook_url = readConfig().readconfig('HEADERS', 'webhook')
            webhook_url = ''
        #如果webhook不为空则继续推送
        if webhook_url:
            #上传文件获取media_id
            key = webhook_url.split('=')[-1]
            file_upload_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key="+str(key)+"&type=file"
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
        else:
            print('本次不推送报告')
    def run(self,option):
        suite = unittest.TestSuite()
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
        except Exception as e:
            print(f"邮件发送失败: {e}")

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
    try:
        #根据传入不同的pattern值执行不同批用例
        RunTest().run(os.environ['option'])
    except:
        RunTest().run('test')
