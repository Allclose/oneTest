
#可根据bug表格：BUG类型+解决者
#生成每个人下的Bug类型统计图
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# bug表格：BUG类型+解决者
data_file = r"C:\Users\a\Desktop\bug.xlsx"
# 结果保存路径
result_file = r"C:\Users\a\Desktop\Pic.xlsx"
def ExceltoPic(groupbyone,groupbytwo):
    # 读取 Excel 文件
    df = pd.read_excel(data_file)
    # 设置中文字体
    font = FontProperties(fname='C:\Windows\Fonts\simsun.ttc', size=14)  # 替换为您系统中支持的中文字体文件路径
    # 统计每个groupbyone的总行数
    total_bugs_per_resolver = df.groupby(groupbyone).size()
    # 生成不同groupbyone数据所属下各groupbytwo种类数量的饼图
    grouped_data = df.groupby([groupbyone, groupbytwo]).size().unstack(fill_value=0)
    # 创建新的 Excel 文件和 sheet 页
    wb = Workbook()
    ws = wb.active
    ws.title = 'Bug类型统计图'
    for resolver in grouped_data.index:
        resolver_data = grouped_data.loc[[resolver]]
        # 过滤掉数量为 0 的 Bug 类型
        resolver_data = resolver_data.loc[:, (resolver_data != 0).any()]
        if not resolver_data.empty:
            plt.figure()
            patches, texts, autotexts = plt.pie(resolver_data.values[0], labels=resolver_data.columns, autopct='%1.1f%%')
            for text in texts + autotexts:
                text.set_fontproperties(font)
            total_bug_count = total_bugs_per_resolver.get(resolver, 0)
            plt.title(f'{resolver}的Bug类型分布\n总Bug数量：{total_bug_count}', fontproperties=font)
            plt.axis('equal')  # 使饼图比例相等
            # 添加解决者下属的数据总量到标题后
            total_data_count = resolver_data.sum(axis=1).values[0]
            plt.suptitle(f'总数据量：{total_data_count}', x=0.5, y=0.05, ha='center', fontproperties=font)
            #plt.show()             #展示所有图片
            # 保存饼图为图片
            plt.savefig(f'{resolver}_pie_chart.png')
            plt.close()
            # 将图片插入到 Excel 中
            img = Image(f'{resolver}_pie_chart.png')
            ws.add_image(img, f'A{len(ws["A"]) + 2}')
    # 保存 Excel 文件
    wb.save(result_file)
#划分不同groupbyone下属的groupbytwo饼图数据
#输入目标表格内的列名
ExceltoPic('解决者','Bug类型')