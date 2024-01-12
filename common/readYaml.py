import yaml,os
from readConfig import readConfig
datapath = readConfig().readconfig('PATH','datapath')  #获取项目路径
class readYaml:
    def readyaml(self,file_name):
        path = os.path.join(datapath,file_name)
        with open(path,'r',encoding='utf-8') as fp:
            data = yaml.safe_load(fp)['cases']
            #data = yaml.load(fp, Loader=yaml.FullLoader)['cases']
            result = []
            for i in range(len(data)):
                result.append(list(data[i].values()))
                #data[i] = list(data[i].values())
        return result
if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
    print('data：', readYaml().readyaml('test04case.yaml'))