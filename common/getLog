import logging,os
from readConfig import readConfig
projectpath = readConfig().readconfig('PATH','projectpath')

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename=os.path.join(projectpath,'Output.log'),
                    filemode='a',
                    encoding='utf-8')

'''
logging.debug('debug级别，一般用来打印一些调试信息，级别最低')
logging.info('info级别，一般用来打印一些正常的操作信息')
logging.warning('waring级别，一般用来打印警告信息')
logging.error('error级别，一般用来打印一些错误信息')
logging.critical('critical级别，一般用来打印一些致命的错误信息，等级最高')
'''
