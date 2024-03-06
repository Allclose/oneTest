#自动将Fiddler导出的har文件，以接口为个体转换为自动化测试用例
import tkinter as tk
from tkinter import filedialog
import json,os


#用例存放的目标文件夹
file_path = ''
#选择目标har文件，获取路径
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[('HAR Files', '*.har')])
#转换
def loding_case(casefile_path):
    #读取har文件
    with open(str(file_path), 'rb') as fp:
        file = json.loads(fp.readline())

    #结果脚本是使用最简单的拼接进行的
    demo = b'import unittest,json,requests\r\nclass TestRequest(unittest.TestCase):\r\n    @classmethod\r\n    def setUpClass(cls) -> None:\r\n        print(\'start\')\r\n    @classmethod\r\n    def tearDownClass(cls) -> None:\r\n        print(\'end\')\r\n    '
    #多接口文件内的数据块
    datas = file['log']['entries']
    for data in datas:
        #依次将所需内容取出
        headers = {}
        for i in data['request']['headers']:
            key = i['name']
            value = i['value']
            headers.update({key:value})
        payload = str(data['request']['postData']['text']) if str(data['request']['postData']['text'])  else "''"
        url = str(data['request']['url'])
        method = data['request']['method']
        #使用接口最后的path信息作为用例名
        try:
            if '?' in url:
                case_name = url.split('?')[0].split('/')[-1].split('.')[0]
            else:
                case_name = url.split('/')[-1].split('.')[0]
        except:
            case_name=url.split('/')[-1]
        case_name = case_name.replace('-', '_')
        #创建用例文件
        if method == 'POST':
            case = "def test_{}(self):\r\n        url = \'{}\'\r\n        headers = {}\r\n        data = {}\r\n        res = requests.post(url, json=data, headers=headers).json()\r\n        self.assertStatusCode(200)\r\n    ".format(case_name,url,headers,payload)
        elif method == 'GET':
            case = "def test_{}(self):\r\n        url = \'{}\'\r\n        headers = {}\r\n        data = {}\r\n        res = requests.get(url, params=data, headers=headers).json()\r\n        self.assertStatusCode(200)\r\n    ".format(case_name,url,headers,payload)
        demo = demo+case.encode()
    #目标脚本信息
    file_name = 'test_'+str(file_path.split('/')[-1].split('.')[0])+'.py'
    case_path = os.path.join(casefile_path, file_name)
    with open(case_path,'wb') as f:
        f.write(demo)
    print('End')
    label = tk.Label(window, text="转换完成")
    label.grid(column=0,row=2)
#选择结果文件存放地址
def select_folder():
    folder_path = filedialog.askdirectory()
    loding_case(casefile_path=folder_path)

#前端
window = tk.Tk()
window.title("自动化用例生成器")
window.geometry("300x200")
choice_file = tk.Button(window, text="选择har文件", command=select_file)
choice_file.grid(column=0,row=0)
#选择目标文件夹并存放结果用例
conversion_button = tk.Button(window, text="转换", command=select_folder)
conversion_button.grid(column=0,row=1)
ruler = tk.Label(window, text="使用Fiddler抓包后选择目标接口导出为har文件，然后使用本工具选择该文件后即可转为自动化用例",wraplength=290, justify=tk.LEFT)
ruler.grid(column=0,row=3)
tishi = tk.Label(window, text="导出步骤：\n选中目标接口，File>Export Sessions>Selected Sessions>HTTPArchive v1.1保存即可",wraplength=300, justify=tk.LEFT)
tishi.grid(column=0,row=4)
window.mainloop()
