#xlrd=1.2.0
#根据输入的Excel和sheet名称返回数据，如未传入sheet名称则返回所有页数据，
#注：可修改返回所有或者返回首页数据
import xlrd,os
#datapath = readConfig().readconfig('PATH','datapath')
datapath = r'..\Data'
class readExcel:
    def readexcel(self,file_name,sheet_name=None):
        file = xlrd.open_workbook(os.path.join(datapath,file_name))
        '''
        #只可读取第一sheet页数据
        sheet = file.sheet_by_name(file.sheet_names()[0])
        print(sheet)
        data = []
        for i in range(sheet.nrows):
            if sheet.row_values(i)[0] != u'case_name':
                data.append(sheet.row_values(i))
        '''
        #如未传入sheet名称，则读取所有sheet页数据，但存至一个列表内
        data = []
        if not sheet_name:
            for i in range(len(file.sheet_names())):
                sheet = file.sheet_by_name(file.sheet_names()[i])
                for j in range(sheet.nrows):
                    if sheet.row_values(j)[0] != u'case_name':
                        data.append(sheet.row_values(j))
        #如传入sheet名称则返回对应页数据
        else:
            sheet = file.sheet_by_name(sheet_name)
            for i in range(sheet.nrows):
                if sheet.row_values(i)[0] != u'case_name':
                    data.append(sheet.row_values(i))
        return data
if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
    print('data：', readExcel().readexcel('test04case.xlsx','login'))