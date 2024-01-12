#读取配置文件，如
from configparser import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser()
#file =  os.path.join(os.path.realpath(__file__)[0],'config.ini')          #
# 读取配置文件
config.read(os.path.join(BASE_DIR ,'config.ini'))
class readConfig:
    def readconfig(self,section=None,option=None):

        if not section:
            print('section不可为空')
            return 'section不可为空'
        #如果section为ENV   则获取环境对应的前缀URL
        elif 'ENV' in section:
            #CI执行，如果获取到了env的环境变量信息则使用此env
            try:
                env = os.environ('env')
                return config.get(env, option)
            #如果获取失败则默认返回test环境对应的URL
            except:
                return config.get('ENV_TEST',option=option)
        #如果有具体目标section和option，则返回
        elif option:
            try:
                return config.get(section,option)
            except Exception as e:
                print(e)
        else:
            return config.items(section)

if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
    print('Key值为：', readConfig().readconfig('ENV','app'))
    print('Key值为：', readConfig().readconfig('CASES'))